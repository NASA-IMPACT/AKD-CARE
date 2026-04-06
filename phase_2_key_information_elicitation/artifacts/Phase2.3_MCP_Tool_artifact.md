# MCP Tool Specification

## 1. Proposed Tool Inventory

### 1. `discover_variables_and_expand`

Turns a science question, topic set, seed variables, and optional literature evidence into a structured variable package for downstream dataset search.

### 2. `search_cmr_collections`

Executes smart CMR collection search with internal query tactics, pagination handling, deduplication, ranking, and instructional failure behavior.

### 3. `evaluate_dataset_candidates`

Assesses candidate datasets individually and in context, including complementarity and suitability signals.

### 4. `construct_dataset_bundle`

Builds the final optimized 5–6 dataset bundle with coverage reasoning, gaps, swaps, and caveats.

### 5. `extract_literature_signals`

Extracts variables, datasets, instruments, method hints, and traceable evidence from literature, with summarized results by default and raw evidence on demand.

---

## 2. Tool-by-Tool Contract

## Tool 1: `discover_variables_and_expand`

**Purpose**
Convert research intent into a search-ready variable and terminology package.

**When it should be used**

* At the start of a new research question
* When the agent lacks enough variables for search
* After weak CMR retrieval
* After literature evidence introduces new concepts

**Inputs**

```json id="zv8tvt5n"
{
  "science_question": "string",
  "topics": ["string"],
  "seed_variables": ["string"],
  "literature_snippets": ["string"],
  "include_keyword_expansion": true
}
```

**Outputs**

```json id="jlwmjlwm"
{
  "variables": [
    {
      "name": "string",
      "role": "core|supporting|derived|proxy",
      "confidence": "high|medium|low",
      "evidence": ["question|topic|literature"]
    }
  ],
  "expanded_keywords": {
    "variable_name": ["keyword1", "keyword2"]
  },
  "missing_dimensions": [
    {
      "dimension": "string",
      "reason": "string",
      "suggested_variables": ["string"]
    }
  ],
  "confidence_signals": {
    "overall": "high|medium|low",
    "notes": ["string"]
  },
  "search_hints": {
    "recommended_query_terms": ["string"],
    "recommended_filters": ["variable_name", "keyword", "instrument"],
    "notes": ["string"]
  },
  "message": "string",
  "hint": "string",
  "next_action": "search_cmr_collections",
  "next_action_params": {
    "keywords": ["string"],
    "variables": ["string"]
  },
  "alternative_actions": [
    {
      "action": "extract_literature_signals",
      "reason": "string"
    }
  ]
}
```

**Validation layers**

* Validate input structure
* Normalize duplicate or synonymous seed variables
* Flag missing scientific dimensions without enforcing completeness
* Reject empty input only if there is no science question, no topics, and no seed variables

**Internal logic / computation**

* Parse question into candidate variables
* Merge topic-derived and seed variables
* Expand terms using context-backed keyword reference internally
* Detect likely missing dimensions
* Produce search hints and next-action guidance

**Security / permission model**

* No special permissions assumed
* No sensitive credentials required

**Expected failure modes**

* Input too vague to derive variables
* Literature snippets too noisy or contradictory
* Confidence too low across all extracted variables

**Runtime guidance fields**

* `message`: what happened
* `hint`: how to improve input
* `next_action`: likely next tool
* `next_action_params`: prefilled terms for the next tool
* `alternative_actions`: broaden path when extraction is weak

**What stays in context instead**

* GCMD-style keyword reference stays human-maintained in context rather than becoming hardcoded tool logic. 

---

## Tool 2: `search_cmr_collections`

**Purpose**
Search CMR collections with internal search strategy control and return a ranked, deduplicated candidate set.

**When it should be used**

* After variable discovery
* When refining searches
* When rerunning with broader or narrower constraints
* When recovering from weak candidate quality

**Inputs**

```json id="mef5xsvl"
{
  "keywords": ["string"],
  "variables": ["string"],
  "instrument": ["string"],
  "processing_level_preferences": ["string"],
  "temporal": {
    "start": "ISO-8601",
    "end": "ISO-8601",
    "strict": false
  },
  "spatial": {
    "bbox": [0, 0, 0, 0],
    "strict": false
  },
  "max_results": 25,
  "search_mode": "balanced|broad|targeted",
  "literature_signals": {
    "datasets": ["string"],
    "instruments": ["string"],
    "terms": ["string"]
  }
}
```

**Outputs**

```json id="5xau0oo8"
{
  "status": "success|weak_matches|no_strong_matches|partial_results|retryable_error",
  "search_strategies_used": [
    {
      "strategy": "variable_first|keyword_first|blended|fallback_broadened",
      "query_summary": "string",
      "result_count": 0
    }
  ],
  "ranked_collections": [
    {
      "collection_id": "string",
      "short_name": "string",
      "entry_title": "string",
      "score": 0.0,
      "match_rationale": {
        "variable_match": ["string"],
        "instrument_match": ["string"],
        "processing_level_match": "string",
        "metadata_completeness": "high|medium|low",
        "temporal_signal": "strong|moderate|weak|unknown",
        "spatial_signal": "strong|moderate|weak|unknown",
        "active_status": "active|unclear|deprecated_likely",
        "literature_alignment": "strong|moderate|weak|none",
        "keyword_match_notes": ["string"]
      },
      "warnings": ["string"],
      "raw_ref": "string"
    }
  ],
  "excluded_results_summary": {
    "weak_matches_removed": 0,
    "duplicates_removed": 0,
    "deprecated_or_unclear_flagged": 0
  },
  "message": "string",
  "hint": "string",
  "tell_user": "string",
  "next_action": "evaluate_dataset_candidates|discover_variables_and_expand",
  "next_action_params": {},
  "alternative_actions": [
    {
      "action": "search_cmr_collections",
      "reason": "string",
      "params": {}
    }
  ]
}
```

**Validation layers**

* Validate query inputs and normalize filters
* Enforce pagination internally
* Validate search mode and result count bounds
* Detect contradictory constraints
* Detect empty result sets vs low-quality result sets

**Internal logic / computation**

* Run multiple search tactics in one call
* Blend keyword and variable-based search
* Deduplicate overlapping results
* Filter weak/low-information matches
* Detect likely deprecated collections
* Rank candidates using your chosen priority order:

  1. variable match
  2. instrument match when relevant
  3. processing level suitability
  4. metadata completeness
  5. temporal suitability signal
  6. spatial suitability signal
  7. recency / active status
  8. literature alignment
  9. keyword match
  10. popularity as weak optional signal

**Security / permission model**

* Search is open; no Earthdata Login required for this step, consistent with the system inventory. 

**Expected failure modes**

* No strong matches
* Query too narrow
* CMR partial retrieval / transient API failure
* Too many weak keyword-led matches
* Pagination / API limit uncertainty

**Runtime guidance fields**

* Strong fail-forward outputs that can tell the agent to:

  * broaden search
  * remove constraints
  * adjust variables
  * retry with alternate strategy

**What stays in context instead**

* CMR parameter reference stays in context for maintainability and quick lookup, while actual tactic execution lives in the tool. 

---

## Tool 3: `evaluate_dataset_candidates`

**Purpose**
Evaluate candidate datasets one by one and in relation to the research need, including complementarity.

**When it should be used**

* After CMR returns a candidate set
* Before final bundle construction
* When users want rationale for strengths and weaknesses

**Inputs**

```json id="02a401oj"
{
  "science_question": "string",
  "topics": ["string"],
  "required_variables": ["string"],
  "candidate_collections": [
    {
      "collection_id": "string",
      "short_name": "string",
      "raw_ref": "string"
    }
  ],
  "instrument_preferences": ["string"],
  "processing_level_preferences": ["string"],
  "temporal_context": {
    "start": "ISO-8601",
    "end": "ISO-8601",
    "strict": false
  },
  "spatial_context": {
    "bbox": [0, 0, 0, 0],
    "strict": false
  },
  "literature_signals": {
    "datasets": ["string"],
    "instruments": ["string"],
    "variables": ["string"],
    "methods": ["string"]
  }
}
```

**Outputs**

```json id="g8avf05h"
{
  "status": "success|partial|insufficient_evidence",
  "evaluations": [
    {
      "collection_id": "string",
      "short_name": "string",
      "overall_assessment": "strong|moderate|weak|exclude",
      "scores": {
        "variable_coverage": 0.0,
        "topic_coverage": 0.0,
        "metadata_completeness": 0.0,
        "instrument_relevance": 0.0,
        "processing_level_suitability": 0.0,
        "temporal_signal": 0.0,
        "spatial_signal": 0.0,
        "access_usability": 0.0,
        "literature_consistency": 0.0,
        "complementarity_value": 0.0
      },
      "coverage": {
        "variables_covered": ["string"],
        "topics_supported": ["string"],
        "missing_needed_variables": ["string"]
      },
      "fit_notes": ["string"],
      "complementarity_notes": {
        "works_well_with": ["collection_id"],
        "weak_alone_but_useful_in_bundle": true,
        "reason": "string"
      },
      "warnings": ["string"],
      "exclusion_reason": "string"
    }
  ],
  "message": "string",
  "hint": "string",
  "next_action": "construct_dataset_bundle|search_cmr_collections|discover_variables_and_expand",
  "next_action_params": {},
  "alternative_actions": []
}
```

**Validation layers**

* Check candidate integrity
* Detect obviously invalid variable/resolution mismatch
* Mark severely incomplete metadata
* Flag deprecated datasets for exclusion unless uniquely necessary

**Internal logic / computation**

* Score A–J factors you approved
* Assess standalone strength vs bundle value
* Separate hard exclusions from soft warnings
* Identify complementarity opportunities across candidates

**Security / permission model**

* No additional auth expected
* Uses metadata and prior tool outputs only

**Expected failure modes**

* Insufficient metadata to score confidently
* Too many near-duplicate candidates
* Inputs do not cover the required variable set

**What stays in context instead**

* General human guidance on interpreting metadata remains contextual; deterministic scoring and complementarity logic move into the tool.

---

## Tool 4: `construct_dataset_bundle`

**Purpose**
Build the optimized final dataset set for the research question.

**When it should be used**

* After candidate evaluation
* When the agent must present the curated 5–6 datasets
* When coverage optimization matters more than per-dataset rank

**Inputs**

```json id="5qwonsyo"
{
  "science_question": "string",
  "topics": ["string"],
  "required_variables": ["string"],
  "evaluated_candidates": [
    {
      "collection_id": "string",
      "short_name": "string",
      "overall_assessment": "string",
      "coverage": {},
      "scores": {},
      "warnings": ["string"]
    }
  ],
  "target_bundle_size": 6,
  "instrument_preferences": ["string"],
  "must_cover_variables": ["string"],
  "allow_proxy_datasets": true
}
```

**Outputs**

```json id="bccl4imp"
{
  "status": "success|bundle_with_gaps|insufficient_candidates",
  "final_bundle": [
    {
      "collection_id": "string",
      "short_name": "string",
      "why_included": ["string"],
      "primary_role": "core|supporting|proxy|gap_filler"
    }
  ],
  "coverage_matrix": {
    "variables": {
      "variable_name": ["collection_id"]
    },
    "topics": {
      "topic_name": ["collection_id"]
    }
  },
  "unresolved_gaps": [
    {
      "gap": "string",
      "severity": "high|medium|low",
      "suggested_search_direction": "string"
    }
  ],
  "alternate_swaps": [
    {
      "replace": "collection_id",
      "with": "collection_id",
      "reason": "string"
    }
  ],
  "user_caveats": ["string"],
  "message": "string",
  "tell_user": "string",
  "hint": "string",
  "next_action": "present_bundle|search_cmr_collections|discover_variables_and_expand",
  "next_action_params": {},
  "alternative_actions": []
}
```

**Validation layers**

* Ensure bundle size target is valid
* Check coverage against must-cover variables
* Prevent redundant selections unless redundancy is justified
* Apply hard exclusions before optimization

**Internal logic / computation**

* Optimize for set coverage, not just top-ranked items
* Include lower-ranked datasets when they close critical gaps
* Explicitly model proxy and supporting roles
* Generate alternates/swaps rather than a single brittle answer

**Security / permission model**

* No special credentials expected

**Expected failure modes**

* Not enough viable candidates
* Gaps remain after bundle construction
* Coverage goals conflict with exclusion rules

**What stays in context instead**

* User-specific scientific judgment about whether a proxy dataset is acceptable remains outside the tool, consistent with the human-control constraints in Phase 1. 

---

## Tool 5: `extract_literature_signals`

**Purpose**
Extract dataset-relevant structured signals from papers and similar studies.

**When it should be used**

* Before variable discovery when the question is novel
* After weak search results
* When method replication patterns matter
* When the user requests literature-supported selection

**Inputs**

```json id="k75iuqir"
{
  "science_question": "string",
  "topics": ["string"],
  "seed_terms": ["string"],
  "sources": ["string"],
  "return_raw_results": false,
  "max_evidence_items": 10
}
```

**Outputs**

```json id="elt8owvd"
{
  "status": "success|partial|insufficient_evidence|source_unavailable",
  "variables_mentioned": [
    {
      "name": "string",
      "confidence": "high|medium|low",
      "evidence_ids": ["string"]
    }
  ],
  "datasets_used": [
    {
      "name": "string",
      "confidence": "high|medium|low",
      "evidence_ids": ["string"]
    }
  ],
  "instruments_used": ["string"],
  "processing_and_method_hints": ["string"],
  "search_terms_from_papers": ["string"],
  "evidence_snippets": [
    {
      "evidence_id": "string",
      "source_label": "string",
      "snippet": "string"
    }
  ],
  "confidence_summary": {
    "overall": "high|medium|low",
    "notes": ["string"]
  },
  "message": "string",
  "hint": "string",
  "next_action": "discover_variables_and_expand|search_cmr_collections",
  "next_action_params": {},
  "alternative_actions": [],
  "raw_results": []
}
```

**Validation layers**

* Normalize extracted names
* Deduplicate dataset and variable mentions
* Limit raw output unless explicitly requested
* Mark extraction confidence

**Internal logic / computation**

* Summarize by default
* Return raw only on demand
* Keep source integration abstract for now
* Support future adapters for Google Scholar, NASA SDE, or other sources

**Security / permission model**

* Source-specific auth is TBD
* Search permissions and usage terms depend on eventual source adapter, which is still unresolved in the current inventory. 

**Expected failure modes**

* Source unavailable
* Raw source too noisy
* Weak extraction confidence
* Conflicting literature signals

**What stays in context instead**

* Context should not hold literature extraction logic; only light references or source notes if needed.

---

## 3. Validation & Business Rule Placement

These rules should live in the tool layer, not in the agent:

### Inside tools

* Query normalization
* Pagination handling
* Multi-strategy search retries
* Deduplication
* Ranking
* Weak-match filtering
* Deprecated dataset detection
* Metadata completeness checks
* Bundle optimization
* Complementarity scoring
* Gap detection
* Instructional failure returns
* Prefilled next-action parameters

### Stay outside tools / remain human-controlled

* Final scientific acceptance of dataset appropriateness
* Interpretation of spatial and temporal requirements when ambiguous
* Preference among scientifically valid instruments
* Acceptance of proxies or tradeoffs in borderline cases

That boundary directly reflects the Phase 1 human-control constraints. 

---

## 4. Response-as-Instruction Design

Every tool should return not just data, but guidance.

### Required runtime guidance fields

* `message`
* `hint`
* `tell_user` where relevant
* `next_action`
* `next_action_params`
* `alternative_actions`

### Design principle

A tool response should reduce the agent’s need to infer:

* what happened
* whether results are good enough
* what to do next
* how to parameterize the next step

### Example patterns

A weak search result should not just say “0 results.” It should say:

* no strong matches found
* broaden terminology
* remove instrument constraint
* try literature extraction
* retry with prefilled alternate parameters

A bundle tool should not just output 6 datasets. It should say:

* why each is included
* what remains uncovered
* what to swap if the user prioritizes a different instrument or processing level

---

## 5. Failure / Retry / Recovery Patterns

### Tool 1: variable discovery

**Failure pattern**

* question too vague
* insufficient variable confidence

**Recovery**

* request literature extraction
* broaden topics
* accept low-confidence exploratory variables

### Tool 2: CMR search

**Failure pattern**

* no strong matches
* too many weak keyword-led matches
* partial CMR retrieval

**Recovery**

* broaden variable terminology
* remove constraints
* switch search mode
* retry with literature-supported terms

### Tool 3: candidate evaluation

**Failure pattern**

* insufficient metadata
* too few candidates with strong coverage

**Recovery**

* return to CMR search with missing variable focus
* flag where additional literature is needed

### Tool 4: bundle construction

**Failure pattern**

* cannot cover all variables within 5–6 datasets
* coverage conflicts with exclusion rules

**Recovery**

* produce `bundle_with_gaps`
* suggest targeted search directions
* provide alternates and explicit caveats

### Tool 5: literature extraction

**Failure pattern**

* source unavailable
* weak evidence
* contradictory extracted signals

**Recovery**

* fallback to question/topic-driven variable extraction
* downgrade literature to secondary signal
* preserve traceability snippets

---

## 6. Tool vs Context Boundary Decisions

Your context workspace should remain narrow and stable, as designed in 2.2. 

### Keep in context

* GCMD keyword expansion reference
* CMR query parameter reference
* minimal workspace overview
* human-maintained guidance that changes often

### Put in tools

* runtime keyword expansion execution
* variable extraction
* search orchestration
* ranking logic
* metadata evaluation
* complementarity analysis
* bundle optimization
* literature summarization
* fail-forward instructions

### Why

Context is best for lightweight reference.
Tools are best for validation, computation, summarization, and deterministic next actions.

---

## 7. Security / Identity / Permission Notes

### Confirmed from current inventory

* CMR search does not require authentication
* Download workflows are out of scope
* Earthdata Login is only relevant for download, not search. 

### Recommended tool-layer posture

* Keep all current tools search/evaluation-oriented
* Do not build download or account-bound actions into this phase
* Keep auth concerns isolated to future tool additions

### TBD security items

* NASA SDE auth / API availability
* Any source-specific restrictions for literature adapters
* Rate-limit handling and throttling policies for CMR
* Logging / audit policy for user queries and literature traces

---

## 8. Open Questions / TBDs

These remain unresolved from the inventory and should be explicitly tracked:

1. **CMR pagination behavior and caps** are still unknown in detail. The tool should abstract this, but implementation must confirm exact behavior. 
2. **CMR rate limits** are TBD. Tool design should include retry and throttling hooks. 
3. **`variable_name` reliability across DAACs** is uncertain. Search tactics should not depend on it exclusively. 
4. **NASA SDE API availability and structured export** remain TBD. Literature tool should use an adapter model. 
5. **Metadata consistency for spatial/temporal fields** is uncertain enough that those should remain scoring signals, not default hard filters. 
6. **Definition of “deprecated”** should be operationalized in implementation, not left implicit.
7. **Scoring thresholds** for strong/moderate/weak/exclude still need calibration.
8. **Proxy dataset policy** likely needs clearer implementation rules, especially when no direct variable match exists.
9. **Raw literature evidence retention** needs a storage/traceability decision if this becomes productionized.
10. **Popularity / reuse signal** is intentionally weak and may be omitted entirely if no reliable source exists.

---

# Recommended execution sequence at runtime

1. `discover_variables_and_expand`
2. optional `extract_literature_signals` if novelty or weak variable confidence
3. `search_cmr_collections`
4. `evaluate_dataset_candidates`
5. `construct_dataset_bundle`

That sequence fits the workflow described in Phase 1 while moving the expensive repeatable logic into tools.
