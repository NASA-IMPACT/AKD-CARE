"""Runtime MCP server for serving CARE agent knowledge workspaces.

Indexes all knowledge files at startup using BM25 + trigger matching,
then serves them via get_context and list_knowledge tools.
"""

import argparse
import math
import os
import re
from pathlib import Path

from loguru import logger
from mcp.server.fastmcp import FastMCP

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from storage import StorageBackend, create_storage

mcp = FastMCP(
    "care-knowledge",
    instructions="Runtime knowledge server for CARE agents — serves domain knowledge via BM25 search and trigger matching",
)

storage: StorageBackend | None = None
CONTEXT_PREFIX: str = ""  # e.g. "context" — set at init


class BM25:
    """Zero-dependency BM25 ranking implementation."""

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: list[dict] = []
        self.df: dict[str, int] = {}
        self.avg_dl: float = 0.0

    def _tokenize(self, text: str) -> list[str]:
        return re.findall(r"\w+", text.lower())

    def index_document(self, path: str, content: str) -> None:
        tokens = self._tokenize(content)
        self.documents.append({
            "path": path,
            "content": content,
            "tokens": tokens,
            "length": len(tokens),
        })
        seen = set()
        for token in tokens:
            if token not in seen:
                self.df[token] = self.df.get(token, 0) + 1
                seen.add(token)
        total_length = sum(d["length"] for d in self.documents)
        self.avg_dl = total_length / len(self.documents) if self.documents else 0

    def search(self, query: str, top_k: int = 3, scope: str | None = None) -> list[dict]:
        query_tokens = self._tokenize(query)
        if not query_tokens or not self.documents:
            return []

        n = len(self.documents)
        scores = []

        for doc in self.documents:
            if scope and not doc["path"].startswith(scope):
                continue

            score = 0.0
            tf_map: dict[str, int] = {}
            for token in doc["tokens"]:
                tf_map[token] = tf_map.get(token, 0) + 1

            for term in query_tokens:
                if term not in self.df:
                    continue
                df = self.df[term]
                idf = math.log((n - df + 0.5) / (df + 0.5) + 1)
                tf = tf_map.get(term, 0)
                dl = doc["length"]
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * dl / self.avg_dl)
                score += idf * (numerator / denominator)

            if score > 0:
                scores.append({
                    "path": doc["path"],
                    "content": doc["content"],
                    "score": score,
                })

        scores.sort(key=lambda x: x["score"], reverse=True)
        return scores[:top_k]


class TriggerIndex:
    """Parses _index.md trigger tables and matches queries against trigger terms."""

    def __init__(self):
        self.entries: list[dict] = []

    def load_from_index(self, st: StorageBackend, index_path: str, base_dir: str) -> None:
        """Load trigger entries from an _index.md file."""
        if not st.exists(index_path):
            return
        content = st.read_text(index_path)
        in_table = False
        for line in content.splitlines():
            if "| If the situation involves..." in line:
                in_table = True
                continue
            if in_table and line.startswith("|---"):
                continue
            if in_table and line.startswith("|"):
                parts = [p.strip() for p in line.split("|")[1:-1]]
                if len(parts) >= 2:
                    terms = [t.strip().lower() for t in parts[0].split(",")]
                    target = parts[1]
                    # path relative to context dir
                    full_path = st.join(base_dir, target)
                    if st.exists(full_path):
                        self.entries.append({
                            "terms": terms,
                            "path": full_path,
                        })
            elif in_table and not line.startswith("|"):
                in_table = False

    def find_matches(self, query: str) -> list[str]:
        query_lower = query.lower()
        matched_paths = []
        seen = set()
        for entry in self.entries:
            for term in entry["terms"]:
                if term in query_lower and entry["path"] not in seen:
                    matched_paths.append(entry["path"])
                    seen.add(entry["path"])
                    break
        return matched_paths


# ── Global state ───────────────────────────────────────────────────────────

bm25_index = BM25()
trigger_index = TriggerIndex()


def _init_index(st: StorageBackend, context_dir: str) -> None:
    """Index all knowledge files in the workspace at startup."""
    if not st.exists(context_dir):
        logger.warning(f"No context/ directory in workspace")
        return

    knowledge_count = 0

    for md_path in sorted(st.rglob(context_dir, "*.md")):
        fname = st.name(md_path)
        if fname == "_index.md":
            parent_dir = st.parent(md_path)
            trigger_index.load_from_index(st, md_path, parent_dir)
            continue
        if fname.startswith("_"):
            continue
        content = st.read_text(md_path)
        # Store path relative to context dir for display, but full storage path for lookups
        bm25_index.index_document(md_path, content)
        knowledge_count += 1
        rel = st.relative_to(md_path, context_dir)
        logger.debug(f"Indexed: {rel}")

    logger.info(f"Indexed {knowledge_count} knowledge files, {len(trigger_index.entries)} trigger entries")


# ── Tools ──────────────────────────────────────────────────────────────────


@mcp.tool()
def get_context(query: str, scope: str | None = None) -> str:
    """Retrieve domain-specific knowledge. Pass a natural language query describing
    what you need to know. Results are ranked by relevance — trigger matches (high
    confidence, SME-defined) appear first, followed by BM25 search matches.

    Use `scope` to restrict results to a knowledge category:
      - "terminology" — term disambiguation and definitions
      - "heuristics" — expert rules of thumb and decision shortcuts
      - "common_mistakes" — known pitfalls and how to avoid them
    Omit scope to search across all categories."""
    st = storage
    if not st:
        return "Error: No workspace configured."

    scope_prefix = st.join(CONTEXT_PREFIX, scope) if scope else None
    results: list[dict] = []
    seen_paths: set[str] = set()

    # Step 1: Trigger matches (filtered by scope)
    trigger_matches = trigger_index.find_matches(query)
    for path in trigger_matches:
        if scope_prefix and not path.startswith(scope_prefix):
            continue
        if path not in seen_paths:
            try:
                content = st.read_text(path)
                rel = st.relative_to(path, CONTEXT_PREFIX)
                results.append({"path": rel, "content": content, "match_type": "trigger match"})
                seen_paths.add(path)
            except (OSError, ValueError):
                logger.warning(f"Could not read trigger match: {path}")

    # Step 2: BM25 search (filtered by scope)
    bm25_results = bm25_index.search(query, top_k=3, scope=scope_prefix)
    for result in bm25_results:
        if result["path"] not in seen_paths:
            try:
                rel = st.relative_to(result["path"], CONTEXT_PREFIX)
                results.append({"path": rel, "content": result["content"], "match_type": "search match"})
                seen_paths.add(result["path"])
            except ValueError:
                pass

    # Step 3: Return top 3
    results = results[:3]

    if not results:
        return (
            "No matching knowledge found for this query. "
            "Proceed with caution — the knowledge base may not cover this topic. "
            "Consider asking the user for clarification or checking broader terms."
        )

    output_parts = []
    for r in results:
        output_parts.append(f"--- {r['path']} ({r['match_type']}) ---\n\n{r['content']}")

    return "\n\n".join(output_parts)


@mcp.tool()
def list_knowledge(path: str = "") -> str:
    """List available knowledge categories. If the directory has an _index.md, returns
    its content. Otherwise lists directory entries."""
    st = storage
    if not st:
        return "Error: No workspace configured."

    target = st.join(CONTEXT_PREFIX, path) if path else CONTEXT_PREFIX

    if not st.exists(target):
        return f"Error: Path not found: {path or 'context/'}"

    if st.is_dir(target):
        index_path = st.join(target, "_index.md")
        if st.exists(index_path):
            return st.read_text(index_path)

        entries = st.list_dir_info(target)
        lines = [f"# {st.name(target)}/\n"]
        for entry in entries:
            if entry["name"].startswith("."):
                continue
            prefix = "📁 " if entry["is_dir"] else "📄 "
            lines.append(f"- {prefix}{entry['name']}")
        return "\n".join(lines)

    if st.is_file(target):
        return st.read_text(target)

    return f"Error: {path} is not a file or directory."


# ── Entry Point ────────────────────────────────────────────────────────────


def main():
    global storage, CONTEXT_PREFIX
    parser = argparse.ArgumentParser(description="CARE Knowledge Server MCP")
    parser.add_argument("--workspace", required=True, help="Path to the completed CARE workspace (or project name for gdrive)")
    parser.add_argument("--storage-type", choices=["local", "gdrive"], default="local")
    parser.add_argument("--gdrive-folder-id", help="Google Drive folder ID (for gdrive storage)")
    parser.add_argument("--gdrive-credentials", help="Path to Google service account credentials JSON")
    args = parser.parse_args()

    if args.storage_type == "gdrive":
        if not args.gdrive_folder_id:
            parser.error("--gdrive-folder-id is required when using gdrive storage")
        storage = create_storage("gdrive", folder_id=args.gdrive_folder_id, credentials=args.gdrive_credentials)
        CONTEXT_PREFIX = st.join(args.workspace, "context") if args.workspace else "context"
    else:
        storage = create_storage("local", root=args.workspace)
        CONTEXT_PREFIX = "context"

    if not storage.exists(CONTEXT_PREFIX):
        logger.error(f"Context directory not found: {CONTEXT_PREFIX}")
        raise SystemExit(1)

    _init_index(storage, CONTEXT_PREFIX)
    mcp.run()


if __name__ == "__main__":
    main()
