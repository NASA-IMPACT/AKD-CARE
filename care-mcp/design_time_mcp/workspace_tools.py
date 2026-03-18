"""Design-time MCP server for building CARE agent knowledge workspaces during SME interviews.

13 tools in 4 groups:
  A. Workspace Management: workspace_init, workspace_write, workspace_read, workspace_list
  B. Index Management: index_add_rule, index_generate
  C. Tool Specification: tool_spec_init, tool_spec_write, tool_spec_add_response
  D. Validation & Assembly: validate_workspace, validate_triggers, assemble_system_prompt, assemble_runtime_config
"""

import argparse
import json
import os
import re
from datetime import datetime, timezone

from loguru import logger
from mcp.server.fastmcp import FastMCP

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from storage import StorageBackend, create_storage

mcp = FastMCP(
    "care-workspace-builder",
    instructions="Design-time tools for building CARE agent knowledge workspaces during SME interviews",
)

storage: StorageBackend | None = None


def _tree(st: StorageBackend, path: str, prefix: str = "", max_depth: int = 4, depth: int = 0) -> str:
    if depth >= max_depth:
        return ""
    entries = st.list_dir_info(path)
    lines = []
    for i, entry in enumerate(entries):
        connector = "└── " if i == len(entries) - 1 else "├── "
        lines.append(f"{prefix}{connector}{entry['name']}")
        if entry["is_dir"]:
            extension = "    " if i == len(entries) - 1 else "│   "
            subtree = _tree(st, st.join(path, entry["name"]), prefix + extension, max_depth, depth + 1)
            if subtree:
                lines.append(subtree)
    return "\n".join(lines)


def _ensure_trigger_table(st: StorageBackend, path: str) -> None:
    """Ensure an _index.md file exists with a trigger table skeleton."""
    if st.exists(path):
        content = st.read_text(path)
        if "| If the situation involves..." in content:
            return
        content += "\n\n## Trigger Table\n\n| If the situation involves... | Retrieve from | Why |\n|------------------------------|---------------|-----|\n"
        st.write_text(path, content)
    else:
        content = (
            "# Index\n\n"
            "## Trigger Table\n\n"
            "| If the situation involves... | Retrieve from | Why |\n"
            "|------------------------------|---------------|-----|\n"
        )
        st.write_text(path, content)


def _append_trigger_row(st: StorageBackend, path: str, terms: list[str], target: str, description: str) -> None:
    """Append a trigger table row to an _index.md file, right after the table."""
    _ensure_trigger_table(st, path)
    row = f"| {', '.join(terms)} | {target} | {description} |"
    lines = st.read_text(path).splitlines()
    insert_idx = len(lines)
    in_table = False
    for i, line in enumerate(lines):
        if "| If the situation involves..." in line:
            in_table = True
            continue
        if in_table and line.startswith("|---"):
            continue
        if in_table and line.startswith("|"):
            continue
        if in_table and not line.startswith("|"):
            insert_idx = i
            break
    lines.insert(insert_idx, row)
    st.write_text(path, "\n".join(lines) + "\n")


def _parse_trigger_table(content: str) -> list[dict]:
    """Parse trigger table rows from _index.md content."""
    rows = []
    in_table = False
    for line in content.splitlines():
        if "| If the situation involves..." in line:
            in_table = True
            continue
        if in_table and line.startswith("|---"):
            continue
        if in_table and line.startswith("|"):
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) >= 3:
                rows.append({
                    "terms": [t.strip() for t in parts[0].split(",")],
                    "target": parts[1],
                    "description": parts[2],
                })
        elif in_table and not line.startswith("|"):
            in_table = False
    return rows


# ── Group A: Workspace Management ──────────────────────────────────────────


@mcp.tool()
def workspace_init(project_name: str, domain_description: str) -> str:
    """Initialize a new CARE workspace for a project. Creates the directory structure
    with context/, tools/, and scope.md. Call this at the end of Step 1 after the SME
    confirms the scope summary."""
    st = storage
    if st.exists(project_name):
        return f"Error: Project '{project_name}' already exists"

    logger.info(f"Initializing workspace for project: {project_name}")

    for d in ["context/terminology", "context/heuristics", "context/common_mistakes", "tools"]:
        st.mkdir(st.join(project_name, d))

    st.write_text(st.join(project_name, "context/_index.md"),
        f"# {project_name} — Domain Knowledge Index\n\n"
        f"{domain_description}\n\n"
        "## Trigger Table\n\n"
        "| If the situation involves... | Retrieve from | Why |\n"
        "|------------------------------|---------------|-----|\n"
        "\n"
        "## General rules (always active)\n\n"
    )

    st.write_text(st.join(project_name, "tools/_index.md"),
        "# Tool Specifications\n\n"
        "| Tool | Purpose |\n"
        "|------|---------|\n"
    )

    st.write_text(st.join(project_name, "scope.md"),
        f"# {project_name} — Scope\n\n*(To be filled during Step 1)*\n"
    )

    tree = _tree(st, project_name)
    logger.info(f"Workspace created:\n{tree}")
    return f"Workspace created for '{project_name}':\n{tree}"


@mcp.tool()
def workspace_write(
    project_name: str,
    path: str,
    content: str,
    trigger_terms: list[str] | None = None,
    trigger_description: str | None = None,
) -> str:
    """Write a knowledge file to the workspace and optionally register trigger terms.
    Use trigger_terms to specify keywords that should cause this file to be retrieved
    at runtime. trigger_description explains WHY retrieval is needed."""
    st = storage
    if not st.exists(project_name):
        return f"Error: Project '{project_name}' does not exist. Call workspace_init first."

    file_path = st.join(project_name, path)
    st.write_text(file_path, content)
    logger.info(f"Wrote {path} ({len(content)} chars)")

    if trigger_terms:
        description = trigger_description or ""
        filename = st.name(file_path)

        # Register in parent directory's _index.md
        parent_index = st.join(st.parent(file_path), "_index.md")
        _append_trigger_row(st, parent_index, trigger_terms, filename, description)

        # Register in root context/_index.md with relative path from context/
        context_prefix = st.join(project_name, "context")
        try:
            relative_to_context = st.relative_to(file_path, context_prefix)
            root_index = st.join(context_prefix, "_index.md")
            _append_trigger_row(st, root_index, trigger_terms, relative_to_context, description)
            logger.info(f"Registered triggers for {path}: {trigger_terms}")
        except ValueError:
            logger.warning(f"File {path} is not under context/, skipping root index registration")

    return f"Written: {path}" + (f" (triggers: {trigger_terms})" if trigger_terms else "")


@mcp.tool()
def workspace_read(project_name: str, path: str) -> str:
    """Read and return the content of a file in the workspace."""
    st = storage
    file_path = st.join(project_name, path)
    if not st.exists(file_path):
        return f"Error: File not found: {path}"
    content = st.read_text(file_path)
    logger.info(f"Read {path} ({len(content)} chars)")
    return content


@mcp.tool()
def workspace_list(project_name: str, path: str = "") -> str:
    """List the workspace directory structure. Use this to show the SME what has been
    captured so far."""
    st = storage
    target = st.join(project_name, path) if path else project_name
    if not st.exists(target):
        return f"Error: Path not found: {path or project_name}"
    tree = _tree(st, target, max_depth=4)
    return f"{st.name(target)}/\n{tree}"


# ── Group B: Index Management ──────────────────────────────────────────────


@mcp.tool()
def index_add_rule(project_name: str, rule: str, rationale: str = "") -> str:
    """Add a persistent rule to the root context index under 'General rules (always active)'.
    These rules are ALWAYS included in the deployed agent's system prompt. Use this for
    hard constraints the SME identifies — rules that must never be violated."""
    st = storage
    root_index = st.join(project_name, "context/_index.md")
    if not st.exists(root_index):
        return f"Error: Root index not found. Call workspace_init first."

    content = st.read_text(root_index)
    entry = f"- **{rule}**"
    if rationale:
        entry += f" — {rationale}"
    entry += "\n"

    marker = "## General rules (always active)"
    if marker not in content:
        content += f"\n{marker}\n\n{entry}"
    else:
        idx = content.index(marker) + len(marker)
        rest = content[idx:]
        content = content[:idx] + rest + entry

    st.write_text(root_index, content)
    logger.info(f"Added rule: {rule}")
    return f"Rule added: {rule}"


@mcp.tool()
def index_generate(project_name: str, directory_path: str) -> str:
    """Auto-generate a sub-index _index.md for a directory by scanning its .md files.
    Extracts the first heading and first paragraph from each file. If an existing _index.md
    has a trigger table, preserves it and returns the listing for review."""
    st = storage
    target_dir = st.join(project_name, directory_path)
    if not st.is_dir(target_dir):
        return f"Error: Directory not found: {directory_path}"

    index_path = st.join(target_dir, "_index.md")
    has_trigger_table = False

    if st.exists(index_path):
        existing_content = st.read_text(index_path)
        if "| If the situation involves..." in existing_content:
            has_trigger_table = True

    dir_name = st.name(target_dir)
    listing_lines = [f"# Index: {dir_name}\n"]
    md_files = sorted(
        p for p in st.glob(target_dir, "*.md")
        if st.name(p) != "_index.md"
    )

    for md_path in md_files:
        content = st.read_text(md_path)
        lines = content.strip().splitlines()
        heading = ""
        paragraph = ""
        for line in lines:
            if line.startswith("#") and not heading:
                heading = line.lstrip("#").strip()
            elif heading and line.strip() and not paragraph:
                paragraph = line.strip()
                break

        fname = st.name(md_path)
        listing_lines.append(f"- **{fname}**: {heading}")
        if paragraph:
            listing_lines.append(f"  {paragraph}")
        listing_lines.append("")

    generated = "\n".join(listing_lines)

    if has_trigger_table:
        logger.info(f"Existing trigger table found in {directory_path}/_index.md, preserving it")
        return (
            f"Existing _index.md has a trigger table — not overwriting.\n\n"
            f"Generated listing for review:\n\n{generated}"
        )

    st.write_text(index_path, generated)
    logger.info(f"Generated index for {directory_path}")
    return f"Index generated for {directory_path}:\n\n{generated}"


# ── Group C: Tool Specification ────────────────────────────────────────────


@mcp.tool()
def tool_spec_init(project_name: str, tool_name: str, purpose: str) -> str:
    """Create a tool specification directory with skeleton files. Call this when the SME
    starts demonstrating a new tool in Step 3."""
    st = storage
    tool_dir = st.join(project_name, "tools", tool_name)
    if st.exists(tool_dir):
        return f"Error: Tool spec '{tool_name}' already exists."

    st.mkdir(st.join(tool_dir, "responses"))

    st.write_text(st.join(tool_dir, "description.md"),
        f"# {tool_name}\n\n{purpose}\n\n## What it does\n\n*(To be filled)*\n\n"
        "## When to use it\n\n*(To be filled)*\n"
    )
    st.write_text(st.join(tool_dir, "parameters.md"),
        f"# {tool_name} — Parameters\n\n"
        "| Parameter | Type | Required | Description |\n"
        "|-----------|------|----------|-------------|\n"
    )
    st.write_text(st.join(tool_dir, "responses/_index.md"),
        f"# {tool_name} — Response Patterns\n\n"
        "| Scenario | Condition | File |\n"
        "|----------|-----------|------|\n"
    )

    tools_index = st.join(project_name, "tools/_index.md")
    if st.exists(tools_index):
        content = st.read_text(tools_index)
        content += f"| {tool_name} | {purpose} |\n"
        st.write_text(tools_index, content)

    logger.info(f"Tool spec initialized: {tool_name}")
    return f"Tool spec created: tools/{tool_name}/"


@mcp.tool()
def tool_spec_write(project_name: str, tool_name: str, section: str, content: str) -> str:
    """Write or overwrite a section of a tool spec. Section must be one of:
    'description', 'parameters', 'audience'."""
    st = storage
    tool_dir = st.join(project_name, "tools", tool_name)
    if not st.exists(tool_dir):
        return f"Error: Tool spec '{tool_name}' not found. Call tool_spec_init first."

    valid_sections = ("description", "parameters", "audience")
    if section not in valid_sections:
        return f"Error: Section must be one of {valid_sections}"

    st.write_text(st.join(tool_dir, f"{section}.md"), content)
    logger.info(f"Wrote tool spec section: {tool_name}/{section}.md")
    return f"Written: tools/{tool_name}/{section}.md"


@mcp.tool()
def tool_spec_add_response(
    project_name: str,
    tool_name: str,
    scenario: str,
    when: str,
    agent_hint: str,
    user_message: str,
    next_action: str = "",
) -> str:
    """Add a response pattern for a tool. This captures how the agent should handle
    a specific tool outcome — both what the agent needs to know (agent_hint) and what
    the user should see (user_message)."""
    st = storage
    responses_dir = st.join(project_name, "tools", tool_name, "responses")
    if not st.exists(responses_dir):
        return f"Error: Tool spec '{tool_name}' not found. Call tool_spec_init first."

    safe_name = re.sub(r"[^a-z0-9_]", "_", scenario.lower())

    content_parts = [
        f"# {scenario}\n",
        f"## When this happens\n\n{when}\n",
        f"## Agent hint\n\n{agent_hint}\n",
        f"## User message\n\n{user_message}\n",
    ]
    if next_action:
        content_parts.append(f"## Suggested next action\n\n{next_action}\n")

    st.write_text(st.join(responses_dir, f"{safe_name}.md"), "\n".join(content_parts))

    index_path = st.join(responses_dir, "_index.md")
    if st.exists(index_path):
        idx_content = st.read_text(index_path)
        idx_content += f"| {scenario} | {when[:60]}{'...' if len(when) > 60 else ''} | {safe_name}.md |\n"
        st.write_text(index_path, idx_content)

    logger.info(f"Added response pattern: {tool_name}/responses/{safe_name}.md")
    return f"Response pattern added: {tool_name}/responses/{safe_name}.md"


# ── Group D: Validation & Assembly ─────────────────────────────────────────


@mcp.tool()
def validate_workspace(project_name: str) -> str:
    """Check structural completeness of the workspace. Reports issues (must fix)
    and warnings (review). Call this at the end of Step 2 and in Step 4."""
    st = storage
    if not st.exists(project_name):
        return f"Error: Project '{project_name}' not found."

    issues = []
    warnings = []
    stats = {"files": 0, "indexes": 0, "tool_specs": 0, "rules": 0, "triggers": 0}

    # Check directories with .md files have _index.md (skip tool subdirs)
    tools_prefix = st.join(project_name, "tools")
    for dirpath in st.rglob(project_name, "*"):
        if not st.is_dir(dirpath):
            continue
        # Skip tool spec directories
        if dirpath.startswith(tools_prefix + "/") and dirpath != tools_prefix:
            continue
        md_files = st.glob(dirpath, "*.md")
        if md_files:
            non_index = [f for f in md_files if st.name(f) != "_index.md"]
            stats["files"] += len(non_index)
            if any(st.name(f) == "_index.md" for f in md_files):
                stats["indexes"] += 1
            elif dirpath != project_name:
                stats_path = st.relative_to(dirpath, project_name)
                issues.append(f"Missing _index.md in {stats_path}")

    # Check root index has rules
    root_index = st.join(project_name, "context/_index.md")
    if st.exists(root_index):
        content = st.read_text(root_index)
        rule_section = content.split("## General rules (always active)")
        if len(rule_section) > 1:
            rules_text = rule_section[1]
            rule_count = len(re.findall(r"^- \*\*", rules_text, re.MULTILINE))
            stats["rules"] = rule_count
            if rule_count == 0:
                warnings.append("No persistent rules defined in root index")
        triggers = _parse_trigger_table(content)
        stats["triggers"] = len(triggers)

    # Check knowledge files are referenced in trigger tables
    context_dir = st.join(project_name, "context")
    if st.exists(context_dir):
        all_triggered_files = set()
        for idx_path in st.rglob(context_dir, "_index.md"):
            idx_content = st.read_text(idx_path)
            rows = _parse_trigger_table(idx_content)
            idx_parent = st.parent(idx_path)
            for row in rows:
                target = row["target"]
                if idx_parent == context_dir:
                    all_triggered_files.add(target)
                else:
                    rel_dir = st.relative_to(idx_parent, context_dir)
                    all_triggered_files.add(st.join(rel_dir, target))

        for md_path in st.rglob(context_dir, "*.md"):
            fname = st.name(md_path)
            if fname == "_index.md" or fname.startswith("_"):
                continue
            rel = st.relative_to(md_path, context_dir)
            if rel not in all_triggered_files:
                warnings.append(f"Orphan knowledge file (no triggers): {rel}")

    # Check tool specs
    if st.exists(tools_prefix):
        for entry in st.list_dir_info(tools_prefix):
            if not entry["is_dir"] or entry["name"].startswith("_"):
                continue
            tool_name = entry["name"]
            tool_dir = st.join(tools_prefix, tool_name)
            stats["tool_specs"] += 1
            if not st.exists(st.join(tool_dir, "description.md")):
                issues.append(f"Tool '{tool_name}' missing description.md")
            if not st.exists(st.join(tool_dir, "parameters.md")):
                issues.append(f"Tool '{tool_name}' missing parameters.md")
            resp_dir = st.join(tool_dir, "responses")
            if st.exists(resp_dir):
                resp_files = [f for f in st.glob(resp_dir, "*.md") if st.name(f) != "_index.md"]
                if not resp_files:
                    issues.append(f"Tool '{tool_name}' has no response patterns")
            else:
                issues.append(f"Tool '{tool_name}' missing responses/ directory")

    report = f"# Workspace Validation: {project_name}\n\n"
    report += f"## Stats\n- Files: {stats['files']}\n- Indexes: {stats['indexes']}\n"
    report += f"- Tool specs: {stats['tool_specs']}\n- Rules: {stats['rules']}\n"
    report += f"- Triggers: {stats['triggers']}\n\n"

    if issues:
        report += f"## Issues ({len(issues)})\n"
        for issue in issues:
            report += f"- {issue}\n"
        report += "\n"

    if warnings:
        report += f"## Warnings ({len(warnings)})\n"
        for warning in warnings:
            report += f"- {warning}\n"
        report += "\n"

    if not issues and not warnings:
        report += "No issues or warnings found.\n"

    logger.info(f"Validation complete: {len(issues)} issues, {len(warnings)} warnings")
    return report


@mcp.tool()
def validate_triggers(project_name: str) -> str:
    """Check trigger coverage — identifies orphan files and broken references.
    Call this in Step 4 to ensure all knowledge is reachable."""
    st = storage
    context_dir = st.join(project_name, "context")
    if not st.exists(context_dir):
        return f"Error: No context directory found for '{project_name}'."

    knowledge_files = set()
    for md_path in st.rglob(context_dir, "*.md"):
        fname = st.name(md_path)
        if fname == "_index.md" or fname.startswith("_"):
            continue
        knowledge_files.add(st.relative_to(md_path, context_dir))

    triggered_refs = set()
    broken_refs = []

    for idx_path in st.rglob(context_dir, "_index.md"):
        idx_content = st.read_text(idx_path)
        rows = _parse_trigger_table(idx_content)
        idx_parent = st.parent(idx_path)
        for row in rows:
            target = row["target"]
            if idx_parent == context_dir:
                normalized = target
            else:
                rel_dir = st.relative_to(idx_parent, context_dir)
                normalized = st.join(rel_dir, target)

            triggered_refs.add(normalized)
            if not st.exists(st.join(context_dir, normalized)):
                broken_refs.append(normalized)

    orphan_files = knowledge_files - triggered_refs
    total = len(knowledge_files)
    covered = total - len(orphan_files)
    coverage = (covered / total * 100) if total > 0 else 0

    report = f"# Trigger Coverage: {project_name}\n\n"
    report += f"- Knowledge files: {total}\n"
    report += f"- Covered by triggers: {covered}\n"
    report += f"- Coverage: {coverage:.0f}%\n\n"

    if orphan_files:
        report += f"## Orphan files ({len(orphan_files)})\n"
        for f in sorted(orphan_files):
            report += f"- {f}\n"
        report += "\n"

    if broken_refs:
        report += f"## Broken references ({len(broken_refs)})\n"
        for ref in sorted(set(broken_refs)):
            report += f"- {ref}\n"
        report += "\n"

    if not orphan_files and not broken_refs:
        report += "All files covered. No broken references.\n"

    logger.info(f"Trigger validation: {coverage:.0f}% coverage, {len(orphan_files)} orphans, {len(broken_refs)} broken")
    return report


@mcp.tool()
def assemble_system_prompt(project_name: str, reasoning_policy: str) -> str:
    """Generate the deployed agent's system prompt by combining scope, reasoning policy,
    domain knowledge index, and tool descriptions. Call this in Step 4 after validation."""
    st = storage
    if not st.exists(project_name):
        return f"Error: Project '{project_name}' not found."

    scope_path = st.join(project_name, "scope.md")
    scope_content = st.read_text(scope_path) if st.exists(scope_path) else "*(No scope defined)*"

    root_index_path = st.join(project_name, "context/_index.md")
    index_content = st.read_text(root_index_path) if st.exists(root_index_path) else "*(No index)*"

    # Build knowledge categories section
    context_dir = st.join(project_name, "context")
    categories_section = ""
    category_descriptions = {
        "terminology": "Term disambiguation and definitions — use when the user's query contains ambiguous or domain-specific terms",
        "heuristics": "Expert rules of thumb and decision shortcuts — use when you need a strategy for a situation",
        "common_mistakes": "Known pitfalls and how to avoid them — use when the user's approach seems likely to fail",
    }
    if st.exists(context_dir):
        categories = []
        for entry in st.list_dir_info(context_dir):
            if not entry["is_dir"] or entry["name"].startswith("_"):
                continue
            subdir = st.join(context_dir, entry["name"])
            file_count = len([
                f for f in st.rglob(subdir, "*.md")
                if st.name(f) != "_index.md"
            ])
            if file_count == 0:
                continue
            desc = category_descriptions.get(entry["name"], "Domain knowledge")
            categories.append(f"- **`{entry['name']}`** ({file_count} files) — {desc}")
        if categories:
            categories_section = (
                "### Knowledge categories (use as `scope` parameter)\n\n"
                + "\n".join(categories)
                + "\n\nPass `scope` to `get_context` to restrict results to one category. "
                "Omit it to search across all categories.\n"
            )

    # Read tool descriptions
    tools_section = ""
    tools_dir = st.join(project_name, "tools")
    if st.exists(tools_dir):
        for entry in st.list_dir_info(tools_dir):
            if not entry["is_dir"] or entry["name"].startswith("_"):
                continue
            desc_path = st.join(tools_dir, entry["name"], "description.md")
            if st.exists(desc_path):
                tools_section += f"### {entry['name']}\n\n{st.read_text(desc_path)}\n\n"

    prompt = (
        f"## Identity and Purpose\n\n{scope_content}\n\n"
        f"## Reasoning Strategy\n\n{reasoning_policy}\n\n"
        f"## Domain Knowledge Index\n\n"
        f"You have access to a domain knowledge base via the `get_context` tool.\n"
        f"When a situation matches the triggers below, call `get_context` with a relevant query.\n\n"
        f"{index_content}\n\n"
        f"{categories_section}\n\n"
        f"## Available Tools\n\n"
        f"### get_context\n\n"
        f"Retrieve domain-specific knowledge from the knowledge base. Pass a natural language query "
        f"describing what you need to know. Optionally pass `scope` to restrict to a knowledge category. "
        f"Results are ranked by relevance — trigger matches (SME-defined, high confidence) appear first, "
        f"followed by BM25 search matches.\n\n"
        f"{tools_section}"
        f"## Output Behavior\n\n"
        f"Follow the guidelines established in the scope and reasoning strategy above. "
        f"Always retrieve relevant domain knowledge before making domain-specific claims. "
        f"When uncertain, use `get_context` to check for applicable heuristics or common mistakes.\n"
    )

    st.write_text(st.join(project_name, "assembled_system_prompt.md"), prompt)
    logger.info(f"System prompt assembled: {len(prompt)} chars")
    return prompt


@mcp.tool()
def assemble_runtime_config(project_name: str) -> str:
    """Generate the runtime MCP server configuration JSON. Call this in Step 4 after
    assembling the system prompt."""
    st = storage
    if not st.exists(project_name):
        return f"Error: Project '{project_name}' not found."

    context_dir = st.join(project_name, "context")
    knowledge_count = 0
    if st.exists(context_dir):
        knowledge_count = len([
            f for f in st.rglob(context_dir, "*.md")
            if st.name(f) != "_index.md" and not st.name(f).startswith("_")
        ])

    tool_specs = []
    tools_dir = st.join(project_name, "tools")
    if st.exists(tools_dir):
        tool_specs = [
            e["name"] for e in st.list_dir_info(tools_dir)
            if e["is_dir"] and not e["name"].startswith("_")
        ]

    config = {
        "project_name": project_name,
        "workspace_path": st.resolve(project_name),
        "context_path": st.resolve(context_dir),
        "search": {
            "method": "bm25",
            "return_mode": "parent_document",
            "max_results": 3,
        },
        "knowledge_files": knowledge_count,
        "tool_specs": tool_specs,
        "generated": datetime.now(timezone.utc).isoformat(),
    }

    st.write_text(st.join(project_name, "runtime_config.json"), json.dumps(config, indent=2))
    logger.info(f"Runtime config generated: {knowledge_count} knowledge files, {len(tool_specs)} tools")
    return json.dumps(config, indent=2)


# ── Entry Point ────────────────────────────────────────────────────────────


def main():
    global storage
    parser = argparse.ArgumentParser(description="CARE Workspace Builder MCP Server")
    parser.add_argument("--workspace-root", default=os.environ.get("CARE_WORKSPACE_ROOT", "./projects"))
    parser.add_argument("--storage-type", choices=["local", "gdrive"], default="local")
    parser.add_argument("--gdrive-folder-id", help="Google Drive folder ID (for gdrive storage)")
    parser.add_argument("--gdrive-credentials", help="Path to Google service account credentials JSON")
    args = parser.parse_args()

    if args.storage_type == "gdrive":
        if not args.gdrive_folder_id:
            parser.error("--gdrive-folder-id is required when using gdrive storage")
        storage = create_storage("gdrive", folder_id=args.gdrive_folder_id, credentials=args.gdrive_credentials)
    else:
        os.makedirs(args.workspace_root, exist_ok=True)
        storage = create_storage("local", root=args.workspace_root)

    logger.info(f"Starting care-workspace-builder with {args.storage_type} storage")
    mcp.run()


if __name__ == "__main__":
    main()
