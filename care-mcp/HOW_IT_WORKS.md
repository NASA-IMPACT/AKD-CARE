# How Dynamic CARE Works

## The Problem

A CARE interview captures expert knowledge as text artifacts. But the deployed agent has no structured way to *use* that knowledge at runtime. It either gets everything crammed into the system prompt (too long, dilutes attention) or gets nothing (loses the expertise).

## The Solution: Two-Phase Knowledge Routing

Dynamic CARE splits captured knowledge into two categories during the interview, without asking the SME to classify anything:

**Persistent knowledge** — always in the system prompt. Small, critical, must-never-forget rules.

**On-demand knowledge** — retrieved only when relevant. Detailed terminology, heuristics, mistake warnings.

The split happens naturally based on *what the SME is doing*:

| SME activity | Interview phase | Where it goes | How agent accesses it |
|---|---|---|---|
| "This rule must always be followed" | Phase 3.2 (Guardrails) | System prompt | Always visible |
| "This term is confusing" | Phase 2.2 (Context) | Knowledge file + trigger | Retrieved via `get_context` |
| "Here's a shortcut I use" | Phase 2.2 (Context) | Knowledge file + trigger | Retrieved via `get_context` |
| "People always make this mistake" | Phase 2.2 (Context) | Knowledge file + trigger | Retrieved via `get_context` |
| "Here's how I use this tool" | Phase 2.1 (Tools) | Tool spec + response patterns | Shapes tool behavior |

## The Bridge: `context/_index.md`

One file connects design-time and runtime. It contains:

```markdown
## Trigger Table

| If the situation involves... | Retrieve from | Why |
|------------------------------|---------------|-----|
| precipitation, rainfall, rain | terminology/precipitation.md | Disambiguation |
| too many results, narrow, filter | heuristics/narrowing_results.md | Search strategy |
| raw data, unprocessed | common_mistakes/wrong_processing_level.md | Level warning |

## General rules (always active)

- **Always include dataset DOI when citing data products** — Reproducibility
- **Never present results without showing query parameters** — Transparency
```

This file is embedded in the deployed agent's system prompt. The agent can *see* the trigger table and knows when to call `get_context`.

## How the Agent Uses Knowledge at Runtime

```
User: "I need precipitation data for Brazil"
         │
         ▼
┌─────────────────────────────────────────────┐
│ Agent reads its system prompt, sees:        │
│                                             │
│   Trigger table row:                        │
│   "precipitation, rainfall, rain"           │
│   → retrieve terminology/precipitation.md   │
│                                             │
│ The user said "precipitation" — trigger hit  │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│ Agent calls: get_context("precipitation")   │
│                                             │
│ Runtime MCP server:                         │
│  1. Trigger match: "precipitation" →        │
│     terminology/precipitation.md            │
│  2. BM25 search for backup matches          │
│  3. Returns full file content               │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│ Agent now knows:                            │
│                                             │
│  "Precipitation" is ambiguous — it could    │
│  mean rainfall rate, accumulated, snowfall, │
│  or total water equivalent.                 │
│                                             │
│  Action: Ask the user which type before     │
│  searching.                                 │
└──────────────┬──────────────────────────────┘
               │
               ▼
Agent: "Precipitation can mean several things —
        rainfall rate, accumulated precipitation,
        or snow water equivalent. Which type do
        you need for your Brazil study?"
```

Without the knowledge file, the agent would blindly search "precipitation Brazil" and return a confusing mix of datasets.

## How the Interviewer Tools Build This

During the interview, the interviewer LLM calls workspace tools as the SME talks:

**1. SME says a term is confusing → interviewer calls `workspace_write`**

```
workspace_write(
    project_name="earth_obs",
    path="context/terminology/precipitation.md",
    content="# Precipitation\n\n## The ambiguity\n...\n## What to do\n...",
    trigger_terms=["precipitation", "rainfall", "rain"],
    trigger_description="Disambiguation of precipitation types"
)
```

This does two things atomically:
- Writes the knowledge file to disk
- Adds a row to the trigger table in `context/_index.md`

**2. SME states a hard rule → interviewer calls `index_add_rule`**

```
index_add_rule(
    project_name="earth_obs",
    rule="Always include dataset DOI when citing data products",
    rationale="Reproducibility requirement"
)
```

This appends to the "General rules (always active)" section of `context/_index.md`. These rules go directly into the system prompt — no retrieval needed.

**3. SME demonstrates a tool → interviewer calls `tool_spec_*`**

```
tool_spec_add_response(
    project_name="earth_obs",
    tool_name="cmr_search",
    scenario="No Results",
    when="Query returns zero matches",
    agent_hint="Try removing the most restrictive filter first",
    user_message="No datasets found. Let me suggest adjustments.",
    next_action="Suggest broadening one constraint"
)
```

Response patterns teach the agent what to do when a tool succeeds, fails, or returns edge cases. The `agent_hint` is for the agent's reasoning (not shown to user). The `user_message` is what the human sees.

**4. At the end → interviewer calls `assemble_system_prompt`**

This combines scope + reasoning strategy + trigger table + rules + tool descriptions into one deployable system prompt. The trigger table is embedded so the agent always knows what knowledge exists and when to retrieve it.

## What the Runtime Server Does

The runtime MCP server (`care-knowledge`) starts up, reads the workspace, and provides two tools:

**`get_context(query)`** — Three-step retrieval:
1. Check trigger terms for exact keyword matches (high confidence)
2. Run BM25 text search over all knowledge files (broader matches)
3. Merge results, triggers first, return top 3 as full file content

**`list_knowledge(path)`** — Browse the knowledge structure. Returns the index file if one exists, or lists directory entries.

The server uses zero-dependency BM25 (no vector store, no embeddings). This is sufficient because CARE workspaces are small (10-50 files) and triggers handle the high-confidence cases.

## Summary

```
INTERVIEW TIME                          RUNTIME
═══════════════                         ═══════

SME teaches terminology ──────┐
SME shares heuristics ────────┤
SME warns about mistakes ─────┤
                              ▼
                    workspace_write()
                    + trigger registration
                              │
SME states hard rules ────────┤
                              ▼
                    index_add_rule()
                              │
SME demonstrates tools ───────┤
                              ▼
                    tool_spec_*()
                              │
                              ▼
                    assemble_system_prompt()
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
    System prompt contains:         Knowledge files on disk,
    - Scope                         indexed by BM25 + triggers,
    - Reasoning strategy            served via get_context()
    - Trigger table
    - Persistent rules
    - Tool descriptions
```

The agent sees the trigger table in its system prompt. When a user query matches a trigger, the agent calls `get_context`. The runtime server returns the relevant knowledge file. The agent uses that knowledge to respond correctly.

No knowledge is lost. No system prompt is bloated. The SME's expertise is structured, retrievable, and auditable as plain Markdown files.
