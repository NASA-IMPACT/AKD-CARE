# **Context Workspace**

## 1. Context Bucket Registry

### **1. Global Structural Context**

* **Type:** structural
* **Purpose:** Define invariant foundations of the system
* **Source Artifacts:** Phase 1 Scope, system design decisions
* **Scope:** global
* **Triggers:** always loaded at startup
* **Authority Level:** highest (non-overridable except by physical validity constraints)
* **Inheritance / Override:**

  * Cannot be overridden by lower layers
  * Constrains all other context
* **Canonical Path:**
  `context/_overview.md`
* **Owner:** SME + Developer
* **Update Frequency:** rare
* **Notes:**
  Includes:

  * agent purpose
  * role of CMR as metadata system
  * human-in-the-loop boundaries
  * core scientific non-assumptions

---

### **2. Core Scientific Principles & Validity Constraints**

* **Type:** policy / domain
* **Purpose:** Ensure scientific correctness and prevent invalid reasoning
* **Source Artifacts:** SME-defined principles
* **Scope:** global
* **Triggers:** always loaded
* **Authority Level:** absolute (cannot be overridden)
* **Inheritance / Override:**

  * Overrides all except user constraints within valid bounds
* **Canonical Path:**
  `context/scientific_principles/core_validity.md`
* **Owner:** SME
* **Update Frequency:** rare
* **Notes:**
  Includes:

  * physical validity rules
  * non-equivalence of variables with same name
  * limits of derived/model products

---

### **3. High-Level Dataset Evaluation Heuristics**

* **Type:** procedural
* **Purpose:** Guide elimination of invalid datasets
* **Source Artifacts:** SME heuristics
* **Scope:** global
* **Triggers:** always loaded (lightweight version only)
* **Authority Level:** high (below scientific principles)
* **Inheritance / Override:**

  * Can be refined by conditional context
* **Canonical Path:**
  `context/dataset_evaluation/core_heuristics.md`
* **Owner:** SME (mixed with developer structuring)
* **Update Frequency:** occasional
* **Notes:**
  High-level only (no detailed rules here)

---

### **4. Detailed Dataset Evaluation & Comparison Guidance**

* **Type:** procedural / domain
* **Purpose:** Enable structured comparison of datasets
* **Source Artifacts:** SME-defined evaluation dimensions
* **Scope:** conditional
* **Triggers:**

  * when multiple datasets are identified
  * when user asks for comparison
* **Authority Level:** high
* **Inheritance / Override:**

  * Extends core heuristics
* **Canonical Path:**
  `context/dataset_evaluation/comparison_guidance.md`
* **Owner:** SME
* **Update Frequency:** occasional
* **Notes:**
  Includes:

  * variable definition comparison
  * resolution tradeoffs
  * processing level implications
  * coverage gaps

---

### **5. Topic → Variable Pattern Knowledge**

* **Type:** domain
* **Purpose:** Reusable mapping of science problems to variables
* **Source Artifacts:** validated patterns across tasks
* **Scope:** conditional
* **Triggers:**

  * when decomposing a science question
* **Authority Level:** medium
* **Inheritance / Override:**

  * overridden by:

    * literature (task-local)
    * scientific validity constraints
* **Canonical Path:**
  `context/variables/topic_variable_patterns.md`
* **Owner:** SME (mixed ownership)
* **Update Frequency:** periodic
* **Notes:**
  Only includes:

  * repeated, validated patterns
  * not one-off cases

---

### **6. Variable Representation Layer (Raw + Normalized)**

* **Type:** structural / domain
* **Purpose:** Maintain mapping between raw and normalized variables
* **Source Artifacts:** metadata + literature + SME normalization
* **Scope:** conditional
* **Triggers:**

  * when variables are extracted or compared
* **Authority Level:** medium
* **Inheritance / Override:**

  * normalization does not override raw meaning
* **Canonical Path:**
  `context/variables/variable_representation.md`
* **Owner:** Developer + SME
* **Update Frequency:** periodic
* **Notes:**
  Supports:

  * raw variable preservation
  * internal consistency

---

### **7. Proxy Variable Knowledge**

* **Type:** domain
* **Purpose:** Define when proxies are valid or invalid
* **Source Artifacts:** literature + SME synthesis
* **Scope:** conditional
* **Triggers:**

  * when direct variables are missing
  * when proxy variables appear
* **Authority Level:** high
* **Inheritance / Override:**

  * overrides topic-variable patterns
* **Canonical Path:**
  `context/variables/proxy_rules.md`
* **Owner:** SME
* **Update Frequency:** occasional
* **Notes:**
  Includes:

  * validity conditions
  * failure modes
  * regional/scale constraints

---

### **8. Scientific Caveats & Failure Modes**

* **Type:** policy / domain
* **Purpose:** Prevent incorrect interpretation of datasets
* **Source Artifacts:** SME + literature synthesis
* **Scope:** conditional
* **Triggers:**

  * when evaluating datasets
  * when proxies or derived products are used
* **Authority Level:** very high
* **Inheritance / Override:**

  * overrides:

    * literature
    * patterns
* **Canonical Path:**
  `context/scientific_principles/caveats.md`
* **Owner:** SME
* **Update Frequency:** occasional
* **Notes:**
  High-risk knowledge:

  * semantic mismatch
  * aggregation issues
  * sensor limitations

---

### **9. GCMD Keyword & Ontology Support**

* **Type:** reference
* **Purpose:** Assist query expansion and alignment with CMR
* **Source Artifacts:** GCMD keyword system 
* **Scope:** conditional
* **Triggers:**

  * when search coverage is insufficient
  * when aligning to CMR fields (instrument/platform/keywords)
* **Authority Level:** low
* **Inheritance / Override:**

  * never overrides scientific meaning
* **Canonical Path:**
  `context/references/gcmd_keywords.md`
* **Owner:** Curator
* **Update Frequency:** periodic
* **Notes:**
  Lookup-only, not authoritative

---

### **10. Literature-Derived Local Context**

* **Type:** local / domain
* **Purpose:** Provide task-specific scientific evidence
* **Source Artifacts:** uploaded papers, references
* **Scope:** task-local
* **Triggers:**

  * when user provides or references literature
* **Authority Level:** medium-high
* **Inheritance / Override:**

  * overrides reusable patterns within task
  * constrained by scientific validity
* **Canonical Path:**
  `context/local/{task_id}/literature.md`
* **Owner:** dynamic (user-provided)
* **Update Frequency:** per task
* **Notes:**
  Extract:

  * why decisions were made
  * assumptions and limitations

---

### **11. Processing Patterns (Reusable)**

* **Type:** procedural
* **Purpose:** Capture repeated transformations (e.g., anomalies, aggregation)
* **Source Artifacts:** literature patterns
* **Scope:** conditional
* **Triggers:**

  * when variables require transformation
* **Authority Level:** medium
* **Inheritance / Override:**

  * overridden by task-specific constraints
* **Canonical Path:**
  `context/processing/patterns.md`
* **Owner:** SME + Curator
* **Update Frequency:** periodic
* **Notes:**
  Only repeated patterns included

---

### **12. Human Preference Context**

* **Type:** preference
* **Purpose:** Capture user-specific priorities
* **Source Artifacts:** user input / profile
* **Scope:** conditional
* **Triggers:**

  * explicit user input
  * session continuity
  * stored profile
* **Authority Level:** highest within valid options
* **Inheritance / Override:**

  * overrides all except scientific validity
* **Canonical Path:**
  `context/preferences/user_profile.md`
* **Owner:** user / system
* **Update Frequency:** dynamic
* **Notes:**
  Never assumed if user is unsure

---

## 2. Workspace Structure / Hierarchy

```
context/
  _overview.md
  _index.md

  scientific_principles/
    core_validity.md
    caveats.md

  dataset_evaluation/
    core_heuristics.md
    comparison_guidance.md

  variables/
    topic_variable_patterns.md
    variable_representation.md
    proxy_rules.md

  processing/
    patterns.md

  references/
    gcmd_keywords.md

  preferences/
    user_profile.md

  local/
    {task_id}/
      literature.md
```

---

## 3. Trigger → Context Mapping

| Trigger                     | Context Loaded                           |
| --------------------------- | ---------------------------------------- |
| Startup                     | overview, core_validity, core_heuristics |
| Question decomposition      | topic_variable_patterns                  |
| Variable ambiguity          | variable_representation                  |
| Missing direct variables    | proxy_rules                              |
| Dataset evaluation          | caveats + comparison_guidance            |
| Multiple datasets           | comparison_guidance                      |
| Weak search results         | GCMD keywords                            |
| Literature provided         | local literature context                 |
| Repeated processing pattern | processing patterns                      |
| User states preferences     | preference context                       |

---

## 4. Authority, Precedence, Inheritance

**Precedence Order (as defined):**

1. User preferences (within valid bounds)
2. Scientific validity principles
3. Task-local literature
4. Proxy & caveat knowledge
5. Literature (generalized)
6. Topic → variable patterns
7. CMR metadata

**Key Rules:**

* Scientific validity is **non-overridable**
* Preferences only operate within valid options
* Metadata is **lowest authority**
* Local context can override reusable context **within task scope only**

---

## 5. Policy & Guardrail Placement

* **Core validity rules:**
  `scientific_principles/core_validity.md`

* **High-risk caveats:**
  `scientific_principles/caveats.md`

* These act as:

  * guardrails against invalid inference
  * constraints on all other context layers

---

## 6. Canonical Paths Summary

* `context/_overview.md`
* `context/scientific_principles/core_validity.md`
* `context/scientific_principles/caveats.md`
* `context/dataset_evaluation/core_heuristics.md`
* `context/dataset_evaluation/comparison_guidance.md`
* `context/variables/topic_variable_patterns.md`
* `context/variables/variable_representation.md`
* `context/variables/proxy_rules.md`
* `context/processing/patterns.md`
* `context/references/gcmd_keywords.md`
* `context/preferences/user_profile.md`
* `context/local/{task_id}/literature.md`

---

## 7. Ownership, Freshness, Maintenance

| Context Type        | Owner           | Update Frequency |
| ------------------- | --------------- | ---------------- |
| Core principles     | SME             | rare             |
| Caveats / proxies   | SME             | occasional       |
| Heuristics          | SME + Developer | occasional       |
| Variable patterns   | SME (mixed)     | periodic         |
| Processing patterns | SME + Curator   | periodic         |
| References (GCMD)   | Curator         | periodic         |
| Preferences         | User            | dynamic          |
| Local literature    | Task-specific   | per task         |

