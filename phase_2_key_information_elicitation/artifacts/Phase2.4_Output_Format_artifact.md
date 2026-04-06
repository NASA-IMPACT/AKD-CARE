# **Output Format Specification**

## **1\. Design Principles**

The output must:

1. Be **human-readable first**.  
2. Present a **narrative decision-support summary** before structured recommendations.  
3. Make **dataset-level provenance and recommendation rationale explicit**.  
4. Represent **uncertainty, missing information, and weak evidence clearly**.  
5. Translate internal tool guidance into **clean user-facing next steps**.  
6. Avoid exposing raw tool outputs, internal context block names, or system mechanics. This is especially important because Phase 2.2 treats context as internal reference support, and Phase 2.3 places operational decision support inside tools.

---

## **2\. Default Exploratory Mode Schema**

### **2.1 Top-Level Output Shape**

output:

  timestamp: string

  status: success | partial | failure

  summary:

    research\_need: string

    recommendation\_summary: string

    selection\_factors:

      \- string

    overall\_confidence: high | medium | low

  recommended\_datasets:

    \- rank: integer

      dataset\_name: string

      collection\_id: string

      source: string

      instrument: string | \[string\]

      match\_strength: strong | moderate | weak

      confidence: high | medium | low

      primary\_role: core | supporting | proxy | gap\_filler | TBD

      why\_included:

        \- string

      variables\_covered:

        \- string

      topics\_supported:

        \- string

      relevant\_characteristics:

        processing\_level: string | null

        temporal\_signal: string | null

        spatial\_signal: string | null

        metadata\_completeness: high | medium | low | null

      provenance:

        variable\_origin:

          \- variable: string

            source\_type: heuristic | literature | user\_question | topic\_decomposition | unknown

            source\_detail: string | null

        literature\_support:

          used: boolean

          evidence\_snippets:

            \- source\_label: string

              snippet: string

              evidence\_id: string | null

      caveats:

        \- string

  coverage\_and\_gaps:

    variables\_well\_covered:

      \- string

    variables\_partially\_covered:

      \- string

    missing\_or\_weakly\_covered\_variables:

      \- string

    conflicting\_signals:

      \- string

  suggested\_next\_steps:

    \- string

  possible\_improvements:

    \- string

  error\_or\_recovery:

    issue\_summary: string | null

    recovery\_suggestions:

      \- string

---

## **3\. Field Definitions**

### **`timestamp`**

Required. ISO-8601 timestamp indicating when the output was generated.

### **`status`**

Required. One of:

* `success`: recommendations are usable with no major unresolved blockers  
* `partial`: recommendations are usable but gaps, weak matches, or unresolved conflicts remain  
* `failure`: recommendations could not be produced with acceptable quality

### **`summary`**

Required.

#### **`research_need`**

Short restatement of the science question or task.

#### **`recommendation_summary`**

Narrative explanation of what was selected and why.

#### **`selection_factors`**

Required list of high-level factors only, such as:

* variable coverage  
* topic coverage  
* instrument relevance  
* processing suitability  
* temporal or spatial suitability  
* metadata completeness  
* literature consistency

This section must not expose raw internal context names or tool internals. That boundary is consistent with the context and tool separation defined in Phase 2.2 and Phase 2.3.

#### **`overall_confidence`**

Required. `high | medium | low`

---

## **4\. Dataset Recommendation Object**

Each item in `recommended_datasets` is required to contain:

### **Mandatory fields**

* `rank`  
* `dataset_name`  
* `collection_id`  
* `source`  
* `instrument`  
* `match_strength`  
* `confidence`  
* `why_included`  
* `variables_covered`  
* `provenance`  
* `caveats` (may be empty)

### **Recommended fields**

* `topics_supported`  
* `primary_role`  
* `relevant_characteristics`

### **Rules**

* Every dataset recommendation must include a **clear justification**.  
* Every dataset recommendation must identify **what it helps cover**.  
* Provenance must at minimum support traceability back to the dataset source and core supporting evidence.  
* If literature was not used, `literature_support.used` must be `false`.

---

## **5\. Provenance Rules**

### **Required provenance**

For every recommended dataset:

* `collection_id`  
* `source`  
* `instrument`

These are mandatory because discovery is collection-centered and CMR metadata exposes these fields directly.

### **Preferred provenance**

When available:

* variable origin by source type  
* literature evidence snippets  
* source detail for how a variable entered consideration

### **Provenance display rules**

* Tool names and raw tool traces should not appear in the user-facing output.  
* Internal context artifact names or file paths should not appear.  
* Provenance should be understandable to a researcher without needing system knowledge.

---

## **6\. Uncertainty and Missing Information Rules**

Uncertainty must appear in two places:

1. Inline within each dataset entry  
2. In the global `coverage_and_gaps` section

### **Standardized enums**

* `confidence`: `high | medium | low`  
* `match_strength`: `strong | moderate | weak`

### **Required uncertainty content**

* weak dataset matches  
* missing variable coverage  
* conflicting literature/metadata signals  
* important caveats about metadata completeness or suitability

### **Narrative requirement**

Where uncertainty materially affects recommendations, include a plain-language explanation in either:

* `recommendation_summary`  
* dataset `caveats`  
* `issue_summary`

This is important because Phase 2.1 and Phase 2.3 already identify incomplete metadata, weak matches, and unresolved search gaps as normal operating conditions.

---

## **7\. Context Usage Disclosure Rules**

Allowed:

* “Selection was influenced by variable coverage, instrument fit, metadata completeness, and literature consistency.”

Not allowed:

* internal context block names  
* workspace file references  
* hidden system mechanics  
* raw tool routing logic

This partial-visibility design matches the SME decision and the context model in Phase 2.2.

---

## **8\. Next-Step Guidance Rules**

The final output must include user-friendly recovery or follow-on guidance, but not raw fields like `next_action` or `next_action_params`.

### **User-facing sections**

* `suggested_next_steps`  
* `possible_improvements`

### **Examples**

* “Review whether proxy datasets are scientifically acceptable for the missing salinity variable.”  
* “Broaden the search to include alternate instrument terminology.”  
* “Use literature-supported terms to refine processing-level preferences.”

These sections are transformations of the runtime guidance pattern already built into the tool contracts.

---

## **9\. Error / Recovery Structure**

### **On `success`**

`error_or_recovery.issue_summary` may be null, but `suggested_next_steps` can still be present.

### **On `partial`**

Must include:

* `issue_summary`  
* at least one `recovery_suggestions` item  
* explicit gap or weakness description

### **On `failure`**

Must include:

* `issue_summary`  
* `recovery_suggestions`  
* no misleading recommendation list presented as final-quality output

Recommended failure categories for narrative use:

* insufficient variable coverage  
* no strong dataset matches  
* conflicting evidence  
* insufficient metadata

---

## **10\. Default Human-Readable Rendering Order**

The rendered response should appear in this order:

1. **Status \+ brief headline**  
2. **Narrative summary**  
3. **Recommended datasets**  
4. **Coverage and gaps**  
5. **Suggested next steps**  
6. **Possible improvements**  
7. **Error/recovery block**, if applicable

---

## **11\. Optional Structured JSON Mode**

When the user explicitly requests JSON, return a machine-readable object using the same semantic sections.

### **JSON mode requirements**

* No narrative-only omissions  
* Same enum values as default mode  
* Same top-level sections where feasible  
* No raw tool fields exposed  
* Human-readable strings may remain in fields like `recommendation_summary`, `why_included`, and `caveats`

### **JSON mode example skeleton**

{

  "timestamp": "2026-04-05T12:00:00Z",

  "status": "partial",

  "summary": {

    "research\_need": "string",

    "recommendation\_summary": "string",

    "selection\_factors": \["string"\],

    "overall\_confidence": "medium"

  },

  "recommended\_datasets": \[

    {

      "rank": 1,

      "dataset\_name": "string",

      "collection\_id": "string",

      "source": "NASA CMR",

      "instrument": \["string"\],

      "match\_strength": "strong",

      "confidence": "high",

      "primary\_role": "core",

      "why\_included": \["string"\],

      "variables\_covered": \["string"\],

      "topics\_supported": \["string"\],

      "relevant\_characteristics": {

        "processing\_level": "string",

        "temporal\_signal": "strong",

        "spatial\_signal": "moderate",

        "metadata\_completeness": "medium"

      },

      "provenance": {

        "variable\_origin": \[

          {

            "variable": "string",

            "source\_type": "literature",

            "source\_detail": "string"

          }

        \],

        "literature\_support": {

          "used": true,

          "evidence\_snippets": \[

            {

              "source\_label": "string",

              "snippet": "string",

              "evidence\_id": "string"

            }

          \]

        }

      },

      "caveats": \["string"\]

    }

  \],

  "coverage\_and\_gaps": {

    "variables\_well\_covered": \["string"\],

    "variables\_partially\_covered": \["string"\],

    "missing\_or\_weakly\_covered\_variables": \["string"\],

    "conflicting\_signals": \["string"\]

  },

  "suggested\_next\_steps": \["string"\],

  "possible\_improvements": \["string"\],

  "error\_or\_recovery": {

    "issue\_summary": "string",

    "recovery\_suggestions": \["string"\]

  }

}

---

## **12\. Output Mode Definitions**

### **Default mode: `exploratory`**

Use:

* narrative summary  
* structured recommendation list  
* explicit caveats and gaps  
* user-friendly next steps

### **Optional mode: `structured_json`**

Use:

* the JSON schema above  
* no audit trace  
* no hidden system fields surfaced

### **Not included yet**

* full audit mode  
* raw tool trace mode  
* schema-versioned contract mode

Status: **TBD for future phases**

---

## **13\. Final Recommendation on Implementation Boundary**

For consistency with the artifacts:

* **User output layer** should own narrative summary, recommendation presentation, caveat framing, and suggested next steps.  
* **Tool layer** should continue owning computation, ranking, validation, and recovery generation internally.  
* **Context layer** should remain hidden except for high-level influence summaries.

That separation best matches the current architecture decisions across Phase 1, Phase 2.2, and Phase 2.3.

