
## 1. Workspace / Tool Organization

You chose grouping by **system**, with shared validation under `/tools/shared`, and the tool/server name **`CMR_MCP_Server`**. 

```text
/workspace
  /tools
    /cmr
      /CMR_MCP_Server
        tool.yaml
        handler.py
        contract.md
        /schemas
          cmr_search_request.schema.json
          cmr_search_response.schema.json
        /mappers
          collections_normalizer.py
          granules_normalizer.py
        /clients
          cmr_search_client.py
        /policies
          scope_policy.py
    /shared
      /validators
        required_search_fields.py
        page_bounds.py
        disallowed_download_ops.py
      /errors
        recoverable_error.py
        validation_error.py
      /types
        runtime_guidance.py
```

**Naming conventions**

* Server/container: `CMR_MCP_Server`
* Runtime tool name: `cmr_search`
* Schemas: `<tool>_<request|response>.schema.json`
* Shared validators live in `/tools/shared/validators`

**Grouping strategy**

* Group by **system** (`/cmr`), not by workflow, because this tool is a deterministic CMR execution unit rather than a reasoning or curation unit. That matches your boundary decision that query construction and metadata interpretation stay outside the tool. 

**Where logic lives**

* CMR request/response schema: `/tools/cmr/CMR_MCP_Server/schemas`
* Response normalization: `/tools/cmr/CMR_MCP_Server/mappers`
* Common validation and scope guards: `/tools/shared/validators`
* Download/scope blocking rules: `/tools/cmr/CMR_MCP_Server/policies`

## 2. Proposed Tool Inventory

### Tool inventory

Only **one tool** is approved:

* **`cmr_search`**

This tool handles:

* CMR query validation
* search execution
* one-page retrieval
* search-only scope enforcement
* normalized response shaping
* runtime guidance for continuation and recovery

This tool does **not** do:

* keyword expansion
* scientific variable inference
* metadata interpretation
* dataset ranking
* final dataset selection
* download orchestration

## 3. Tool-by-Tool Contract

### Tool name

`cmr_search`

### Purpose

Execute validated NASA CMR searches for collections and granules, return normalized results, and instruct the agent on whether and how to continue paging or refine the request. This fits the current workflow where researchers search CMR, inspect metadata, refine queries, and repeat.

### When it should be used

Use this tool only when:

* the agent has already clarified the search request
* vague keywords have already been cleaned before the tool call
* the agent has selected concrete CMR parameters
* the task is **search**, not download

Do not use this tool for:

* keyword expansion reference lookup
* variable discovery from literature
* scientific interpretation of returned metadata
* auto-selecting a final dataset shortlist without human confirmation

### Scope

* **Allowed:** collection search and granule search
* **Rejected:** download actions and download orchestration
* **No auth fields exposed:** search is open; Earthdata Login is needed for download, which is out of scope here. 

### Inputs / schema

```json
{
  "search_type": "collections | granules",
  "keyword": "string?",
  "short_name": "string?",
  "version": "string?",
  "provider": "string?",
  "platform": "string?",
  "instrument": "string?",
  "processing_level": "string?",
  "variable_name": "string?",
  "temporal": "string?",
  "bounding_box": "string?",
  "page_size": "integer?",
  "page_num": "integer?",
  "variable_name_hint": "string?"
}
```

### Input notes

* At least one meaningful search field is required, such as `keyword`, `short_name`, `variable_name`, or another substantive CMR filter. This aligns with your instruction that one or more true CMR search fields must be present. 
* `page_num` is 1-based in CMR. ([CMR Earthdata][1])
* `page_size` defaults to 10 in CMR and the documented max is 2000, though you want the tool policy to cap it at **50**. That means the tool should enforce a stricter product policy than the API itself. ([CMR Earthdata][1])
* `processing_level` is supported by CMR as an alias for `processing_level_id`. ([CMR Earthdata][1])
* `bounding_box` is `"west,south,east,north"`. ([CMR Earthdata][1])
* `keyword` is free text, case-insensitive, and behaves as an AND-style word search across indexed fields. Phrase syntax and wildcard limits are defined by CMR. ([CMR Earthdata][1])
* `variable_name_hint` is **not** a CMR parameter. It is an internal helper field used only to support your rule: auto-fill `variable_name` only when explicitly provided in a separate field. That preserves transparency and avoids hidden inference.

### Request mapping rules

For collection search, map fields directly to CMR query parameters:

* `keyword -> keyword`
* `short_name -> short_name`
* `version -> version`
* `provider -> provider`
* `platform -> platform`
* `instrument -> instrument`
* `processing_level -> processing_level`
* `variable_name -> variable_name`
* `temporal -> temporal`
* `bounding_box -> bounding_box`
* `page_size -> page_size`
* `page_num -> page_num`

For granule search, the same request model can be used, but unsupported parameters should be omitted or flagged with guidance depending on the granule endpoint’s supported parameters. The official docs distinguish collection and granule search parameter sets. ([CMR Earthdata][1])

### Outputs / schema

```json
{
  "status": "success | recoverable_failure | validation_failure",
  "search_type": "collections | granules",
  "applied_query": {
    "keyword": "string?",
    "short_name": "string?",
    "version": "string?",
    "provider": "string?",
    "platform": "string?",
    "instrument": "string?",
    "processing_level": "string?",
    "variable_name": "string?",
    "temporal": "string?",
    "bounding_box": "string?",
    "page_size": "integer",
    "page_num": "integer"
  },
  "results": [
    {
      "id": "string?",
      "short_name": "string?",
      "entry_title": "string?",
      "abstract": "string?",
      "platforms": ["string"],
      "instruments": ["string"],
      "processing_level_id": "string?",
      "science_keywords": ["string"],
      "data_centers": ["string"],
      "related_urls": ["string"],
      "temporal_extents": "object?",
      "spatial_extent": "object?"
    }
  ],
  "result_count_page": "integer",
  "message": "string",
  "next_action": "string?",
  "next_action_params": "object?",
  "warnings": ["string"],
  "query_quality": "strong | adequate | weak | invalid",
  "coverage_note": "string"
}
```

### Output design choices

You asked for:

* no raw CMR response shown to the user
* normalized collection list
* output aligned to the agent’s style rather than API format

So the tool should return **normalized results only** at the runtime contract layer. Internally it may preserve raw payloads for logging, but they should not be surfaced to the agent as the primary payload. The normalized fields above come from the fields your inventory says are actively used. 

For collection results, normalize at least:

* `ShortName`
* `EntryTitle`
* `Abstract`
* `Platforms`
* `Instruments`
* `ProcessingLevelId`
* `ScienceKeywords`
* `DataCenters`
* `RelatedUrls`
* `TemporalExtents`
* `SpatialExtent` 

## 4. Validation & Business Rule Placement

### In-tool validation

Place these inside the tool or shared validators:

**Required search content**

* Reject requests with no meaningful search fields.
* The tool should not accept a call that only contains paging controls with no substantive search criteria.

**Variable enforcement**

* If `variable_name` is absent and `variable_name_hint` is present, auto-fill `variable_name` from the hint and add a warning that the field was auto-filled from an explicit upstream value.
* The tool must never infer `variable_name` on its own.
* If neither `variable_name` nor `variable_name_hint` is provided, the tool does not fail purely for that reason, because the agent may still be making a keyword or short-name search. But if the agent knows a variable upstream, it must pass it explicitly.

**Page bounds**

* Enforce `page_num >= 1`.
* Enforce product cap `page_size <= 50`, even though CMR documents a higher max. ([CMR Earthdata][1])

**Temporal / spatial format**

* Validate basic syntactic shape only.
* Do not interpret scientific suitability.
* If absent, do not auto-default silently. Your instruction is that the agent should clarify temporal and bounding box choices before relying on defaults.

**Search-only scope**

* Reject download requests.
* Reject any attempt to request data access/download URLs as an operational step.
* Allow granule search, since granule search is in scope; only download is excluded. The official API has separate collection and granule search sections. ([CMR Earthdata][1])

### What stays outside the tool

* keyword expansion remains in context
* query clarification stays with the agent
* scientific interpretation of metadata stays with the agent
* choosing best datasets remains human-controlled and agent-assisted, but not tool-decided

## 5. Response-as-Instruction Design

You approved these runtime guidance fields:

* `message`
* `next_action`
* `next_action_params`
* `warnings`
* `query_quality`
* `coverage_note`

### Expected runtime guidance behavior

**message**

* concise execution summary
* example: “Returned 50 collection results for page 1 using keyword, platform, and variable filters.”

**next_action**
Use a compact verb set such as:

* `continue_search_page`
* `refine_query`
* `broaden_query`
* `narrow_query`
* `switch_to_granule_search`
* `stop`

**next_action_params**
Prefill likely continuation values, for example:

```json
{
  "page_num": 2,
  "page_size": 50,
  "search_type": "collections"
}
```

**warnings**
Examples:

* `variable_name auto-filled from explicit variable_name_hint`
* `page_size reduced to policy max 50`
* `keyword-only search may have low precision`
* `temporal omitted; coverage may be broad`

**query_quality**
Suggested scoring rubric:

* `strong`: includes precise identifiers like `short_name`, `variable_name`, provider, or bounded temporal/spatial filters
* `adequate`: valid search with moderate specificity
* `weak`: broad keyword-only or minimally constrained search
* `invalid`: failed validation

**coverage_note**
This should teach the agent what the current page means, for example:

* “This tool returns one page only. More results may exist; call again with page_num=2 to continue.”
* “Current page is full, so additional pages are likely.”
* “Zero results returned; refine or broaden the query.”

## 6. Failure / Retry / Recovery Patterns

### Validation failure

Return:

```json
{
  "status": "validation_failure",
  "message": "No substantive CMR search fields provided.",
  "next_action": "refine_query",
  "next_action_params": {},
  "warnings": ["Provide at least one search parameter such as keyword, short_name, or variable_name."],
  "query_quality": "invalid",
  "coverage_note": "Search was not executed."
}
```

### Zero results

Treat as **recoverable failure** or success-with-guidance depending on implementation preference, but the contract should guide the agent to refine rather than stop. Since your workflow is iterative, the agent should be told to adjust and retry. 

Recommended behavior:

* `status = recoverable_failure`
* `next_action = broaden_query` or `refine_query`

### API/network failure

You asked me to take behavior from the API docs where relevant, but the docs mainly define request mechanics, not client retry policy. A reasonable contract is:

* retry once for transient transport failure
* then return `recoverable_failure`
* include an actionable message rather than silently swallowing errors

This is an implementation recommendation rather than a documented NASA rule.

### Pagination / continuation

You specified: **retrieve one page and tell the agent to continue**.

Recommended policy:

* Always return one page only.
* If returned result count equals page size, set:

  * `next_action = continue_search_page`
  * `next_action_params.page_num = current_page + 1`
* If result count is less than page size, set:

  * `next_action = stop`
  * `coverage_note = "Returned final partial page; additional pages are unlikely."`

This aligns with the documented paging model where `page_size` and `page_num` control page retrieval. The docs also note that `page_num` is deprecated in favor of newer strategies for very large result sets, but it remains documented and functional. ([CMR Earthdata][1])

## 7. Tool vs Context Boundary Decisions

### Remains in context

* GCMD/keyword expansion reference
* parameter lookup references
* descriptive knowledge meant for human-maintained recall and search support 

### Remains in agent reasoning

* clarifying vague keywords with the user
* deciding whether temporal or bounding box constraints are needed before search
* mapping science questions to candidate variables
* interpreting returned metadata for scientific relevance
* comparing returned datasets and preserving user control for final selection 

### Moves into the tool

* deterministic request validation
* explicit variable autofill from `variable_name_hint`
* paging mechanics
* scope blocking for download requests
* normalized result formatting
* runtime continuation guidance

## 8. Security / Identity / Permission Notes

* This tool is **search-only**.
* It should expose **no auth fields**.
* Earthdata Login is required for dataset download, but search does not require authentication. 
* Granule search is allowed.
* Download workflows are rejected as out of scope.
* The tool should not accept or process token/authentication parameters unless the future scope expands beyond search.

## 9. Open Questions / TBDs

These remain open or should be finalized during implementation:

1. **Whether `variable_name` should be included in the formally documented agent-facing request schema**

   * Your earlier answers required variable enforcement.
   * Your parameter list omitted it.
   * The CMR docs do support `variable_name` for collection search. ([CMR Earthdata][1])
     My recommendation is to keep it in the tool contract because it directly supports your “force use of variables when available” rule.

2. **Granule result normalization schema**

   * You confirmed granule search is in scope.
   * The normalized output fields you approved are collection-centric.
   * Granule output fields should be defined separately.

3. **Tool policy cap vs API max for `page_size`**

   * You specified max 50.
   * CMR documents max 2000. ([CMR Earthdata][1])
     This is fine, but should be explicitly documented as a product policy.

4. **Whether to expose deprecated paging or adopt Search After later**

   * You currently want `page_num`.
   * CMR docs note deep paging deprecation in favor of Search After for large result sets. ([CMR Earthdata][1])
     This does not block the current tool, but it is an architectural consideration.

5. **Whether query-quality scoring should be rule-based or heuristic**

   * I recommend a simple rule-based rubric for determinism.

## Recommended final contract summary

### Canonical tool

* **Server:** `CMR_MCP_Server`
* **Tool:** `cmr_search`

### Core behavior

* accepts clarified CMR search parameters
* validates search-only scope
* auto-fills `variable_name` only from explicit upstream field
* runs collection or granule search
* returns one normalized page
* tells the agent exactly what to do next

### Minimal response pattern

```json
{
  "status": "success",
  "results": [...],
  "message": "Returned 50 collection results for page 1.",
  "next_action": "continue_search_page",
  "next_action_params": {
    "page_num": 2,
    "page_size": 50,
    "search_type": "collections"
  },
  "warnings": [],
  "query_quality": "adequate",
  "coverage_note": "This tool returns one page only. More results may exist."
}
```
