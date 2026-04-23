# Tool Specification

## 1. Workspace / Tool Organization

Canonical workspace:

```text
CMR_Data_Search/
  tools/
    cmr/
      CMR_MCP_Server/
```

Naming conventions:

* Tool folders: `CMR_Data_Search` for standalone server-style tools
* Domain folder: lowercase by source or capability, here `cmr`
* One approved tool only in this phase: `CMR_MCP_Server`

Notes:

* Keep GCMD keyword expansion and CMR parameter references in **context**, not in tool logic, unless later evidence shows they must become executable validation assets.
* This tool is limited to **CMR collection search and query refinement**, not scientific judgment, literature reasoning, or dataset choice finalization.   

## 2. Proposed Tool Inventory

### `CMR_MCP_Server`

Purpose:

* Execute CMR collection search with allowed filters
* Validate search inputs
* Detect over-constrained searches
* Perform one bounded refinement retry
* Return structured search results plus match explanations

Not included:

* Deciding scientific relevance
* Choosing preferred instrument
* Interpreting ambiguous spatial / temporal intent
* Literature extraction
* Final cross-dataset curation judgment 

## 3. Tool Spec (Minimal Contract)

### Tool Name

`CMR_MCP_Server`

### Purpose

Run validated CMR collection searches and perform one constrained refinement pass when the original query is too restrictive.

### Trigger Condition

Call this tool when the agent needs to:

* search CMR collections
* apply collection filters
* retrieve top dataset candidates
* explain why returned collections matched
* recover from weak or zero-result searches without changing user-fixed constraints

### Inputs

At least one of the following must be present:

* `keyword`
* `short_name`
* `version`
* `provider`
* `platform`
* `instrument`
* `processing_level`
* `temporal`
* `bounding_box`

Additional paging inputs:

* `page_size` — max 50
* `page_num` — 1-based

Input field meanings:

* `keyword`: text search across collection metadata using AND behavior
* `short_name`: collection short name, for example `MOD09A1`
* `version`: collection version, for example `6.1`
* `provider`: data provider, for example `LPDAAC_ECS`
* `platform`: platform or satellite name, for example `Terra`
* `instrument`: instrument name, for example `MODIS`
* `processing_level`: one of `L0`, `L1A`, `L1B`, `L2`, `L3`, `L4`
* `temporal`: `YYYY-MM-DDTHH:mm:ssZ,YYYY-MM-DDTHH:mm:ssZ`
* `bounding_box`: `"west,south,east,north"`
* `page_size`: results per page, max 50
* `page_num`: page number starting at 1

### Output

Return **only structured data**.

Minimum output contract:

* `normalized_query_used`
* `results`
* `top_results` limited to top 6
* `total_results_found`
* `applied_filters`
* `relaxed_filters` if retry occurred
* `retry_performed` boolean
* `overconstrained_filter_hint` if applicable
* `errors` if validation or API failure occurs

For each top result, include:

* `ShortName`
* `EntryTitle`
* `Platform`
* `Instrument`
* `ProcessingLevel`
* `TemporalExtent`
* `SpatialExtent`
* `match_reason`

Recommended structured shape:

```json
{
  "normalized_query_used": {},
  "applied_filters": {},
  "retry_performed": false,
  "relaxed_filters": [],
  "overconstrained_filter_hint": null,
  "total_results_found": 0,
  "top_results": [
    {
      "ShortName": "",
      "EntryTitle": "",
      "Platform": [],
      "Instrument": [],
      "ProcessingLevel": "",
      "TemporalExtent": {},
      "SpatialExtent": {},
      "match_reason": ""
    }
  ],
  "errors": []
}
```

### Key Validation

Inside the tool:

* reject invalid temporal range
* reject malformed bounding box
* ignore empty filters
* require at least one search input
* normalize repeated filters
* enforce `page_size <= 50`

Validation boundaries:

* syntax and parameter validity belong in the tool
* scientific meaning of filters does not belong in the tool

### Failure / Retry / Recovery Patterns

#### Validation failure

Return structured error with:

* failing field
* reason
* no retry

#### API/search failure

Return structured error with:

* source: `CMR`
* failure type
* original normalized query
* no speculative user-facing text

#### Weak or zero-result search

The tool may perform **1 retry only**.

Retry rules:

* identify which filter likely over-constrained the query
* relax only constraints **not explicitly fixed by the user**
* a constraint is treated as fixed if it was mentioned in the user science query or established in a clarification answer
* do not relax explicit user-provided constraints
* retry with assumed parameters only when the relaxed field was not user-fixed

Recovery guidance returned as structured data:

* `overconstrained_filter_hint`
* `relaxed_filters`
* updated `normalized_query_used`

### Hard Boundary on Constraint Relaxation

Never relax fields that came directly from:

* the user science query
* a clarification response from the user

This rule applies regardless of field type, including `instrument`, `provider`, `short_name`, `temporal`, `bounding_box`, or others if user-specified.

## 4. Logic Placement Boundary

Belongs in tool:

* parameter validation
* query normalization
* CMR request execution
* paging support
* bounded retry logic
* structured match explanation for returned datasets

Belongs in context:

* CMR query parameter reference
* keyword expansion reference
* advisory lookup knowledge for better search recall

Belongs to human / agent outside tool:

* scientific relevance judgment
* preferred instrument choice
* ambiguous temporal or spatial interpretation
* final dataset appropriateness decision   
