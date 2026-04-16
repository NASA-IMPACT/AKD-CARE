# **Reasoning Strategy Specification**

---

## **1. Task Decomposition Strategy**

### **1.1 Execution Backbone**

The agent must follow a **strict, ordered pipeline**:

1. `discover_variables_and_expand`
2. optional `extract_literature_signals`
3. `search_cmr_collections`
4. `evaluate_dataset_candidates`
5. `construct_dataset_bundle` 

No steps may be skipped. Iteration occurs only via tool-guided recovery.

---

### **1.2 Step Progression Rules**

**Variable Discovery**

* Proceed with a **usable variable set**, not necessarily complete
* Missing dimensions must be **explicitly tracked for downstream recovery**

**Literature Usage**

* **Hybrid trigger**

  * Proactive: multi-domain, novel coupling, poorly constrained variables
  * Reactive: low variable confidence or weak search results

**Search**

* Require **diverse candidate set**, not just strong matches
* Automatically retry once with expanded inputs
* Proceed unless:

  * empty results
  * or low informational diversity

**Evaluation**

* Allow **moderate candidates**
* Require only **some signal of relevance across variables**

**Bundle Construction**

* Proceed when **collective coverage is achievable**
* Do not require per-dataset completeness

---

### **1.3 Early Stop Conditions**

Stop before bundling if:

* no strong candidates **and** weak core variable coverage
* critical variables unresolved after retry + literature
* evaluation confidence is uniformly low

---

## **2. Clarification vs Autonomy Rules**

### **2.1 General Behavior**

* Collaborative assistant
* Default: **proceed without interruption**
* Ask only when ambiguity blocks meaningful reasoning

---

### **2.2 Clarification Triggers**

| Scenario              | Behavior                                      |
| --------------------- | --------------------------------------------- |
| Broad question        | Proceed broadly; suggest narrowing later      |
| Missing temporal      | Ask if fully missing; else proceed non-strict |
| Missing spatial       | Ask early (higher priority)                   |
| Instrument preference | Do not ask; remain agnostic                   |
| Processing level      | Do not ask; resolve later                     |
| Proxy usage           | Include with caveats; no pre-approval         |

---

### **2.3 Non-Assumable Elements**

The agent must never assume:

* spatial interpretation
* temporal interpretation
* preferred instrument/platform
* proxy acceptability 

---

### **2.4 Default Assumptions**

Allowed:

* exploratory broad search
* soft spatial/temporal constraints
* multi-instrument aggregation
* mixed processing levels during discovery
* proxies as supporting evidence

---

## **3. Context Retrieval Strategy**

### **3.1 Retrieval Trigger Behavior**

* **Always retrieve immediately** when a context trigger fires 

---

### **3.2 Retrieval Scope**

* **Moderate (block-level) retrieval**
* Never load full documents unnecessarily

---

### **3.3 Usage of Context**

Primary:

* shape tool inputs (keywords, variables, filters)

Secondary:

* validate weak outputs

Never:

* expose raw context to the user 

---

### **3.4 Iteration Limit**

* Max **1 additional retrieval loop**
* Only if signal remains weak after refinement

---

### **3.5 Context vs Tool Conflict**

* Minor → follow tool silently
* Major (affects validity/interpretation) → escalate to user

---

## **4. Tool Selection & Tool-Following Strategy**

### **4.1 `next_action` Policy**

* **Guided execution**
* Follow by default
* Override only with **explicit scientific justification**

---

### **4.2 `hint` Usage**

* Parameter refinement only
* No workflow branching

---

### **4.3 `alternative_actions`**

* Consider only after **measurable underperformance**
* No early branching

---

### **4.4 Recovery Priority Order**

1. Retry with refinement
2. Use literature
3. Continue pipeline
4. Ask user (if blocked)
5. Stop early

---

### **4.5 Tool Selection Priority**

1. `next_action`
2. Highest information gain
3. Lowest-cost recovery
4. Sequence position

---

### **4.6 Override Rule**

Allowed only when:

* scientific precision would degrade
* signal-to-noise would collapse

Preferred behavior:

* **override with rationale**, not blind execution

---

## **5. Comparison / Synthesis / Conflict Handling**

### **5.1 Literature vs Metadata**

* Metadata → existence truth
* Literature → relevance truth
* Never force agreement

---

### **5.2 Weak Dataset Inclusion**

* Include **only if gap-closing**
* Otherwise exclude

---

### **5.3 Duplicate Handling**

* Prefer strongest dataset
* Keep multiple only for:

  * distinct roles
  * robustness

---

### **5.4 Signal Priority Hierarchy**

1. Variable coverage
2. Metadata completeness
3. Instrument relevance
4. Temporal/spatial fit
5. Processing level
6. Literature consistency

---

### **5.5 Conflict Reporting**

* Surface all material conflicts
* Suppress minor ones
* Escalate only when interpretation diverges

---

## **6. Uncertainty & Incomplete Information Handling**

### **6.1 Global Confidence Definition**

Low confidence = **multi-signal failure convergence**

Full failure only when:

* ≥2 core axes fail:

  * variable mapping
  * retrieval
  * evaluation
  * bundling

Otherwise:

* downgrade to `partial`

---

### **6.2 Uncertainty Behavior**

* Use **moderate quantification**
* Emphasize clarity over density
* Increase narrative explanation when:

  * confidence is low
  * uncertainty affects interpretation

---

### **6.3 Gap Handling**

* Explicitly track:

  * missing variables
  * weak coverage
  * conflicting signals

---

## **7. Escalation / Abstention Rules**

### **7.1 Escalation Triggers**

Escalate when:

* multiple valid bundles exist
* proxy dependence drives conclusions
* tradeoffs require scientific judgment

---

### **7.2 Hard Stop Conditions**

Stop completely when:

* no datasets exist
* no variable-to-dataset mapping possible
* global inconsistency prevents coherent reasoning

---

### **7.3 Recovery Policy**

* Exhaust:

  * 1 retry
  * 1 context loop
  * optional literature
* Then stop if no improvement

No over-iteration in degrading signal regimes

---

## **8. Canonical Example Flows**

### **Flow A — Standard Success**

1. Variables → usable set
2. Search → diverse candidates
3. Evaluate → moderate+ signals
4. Bundle → coverage achieved
5. Output → success

---

### **Flow B — Weak Search Recovery**

1. Variables → low confidence
2. Literature → enrich variables
3. Search → retry
4. Evaluate → moderate signals
5. Bundle → partial coverage
6. Output → partial + gaps

---

### **Flow C — Early Stop**

1. Variables → weak
2. Search → weak + retry fails
3. Literature → insufficient improvement
4. Evaluate → low across all
5. Stop → failure with recovery suggestions

---

### **Flow D — Scientific Conflict**

1. Good candidates found
2. Multiple valid bundles emerge
3. Tradeoffs affect interpretation
4. Escalate to user for decision

---

## **9. Open Questions / TBDs**

* CMR pagination limits and behavior
* Rate limiting strategy
* Reliability of `variable_name` across DAACs
* NASA SDE API availability
* Metadata consistency (temporal/spatial fields)
* Definition of “deprecated” datasets
* Scoring thresholds calibration
* Proxy dataset policy refinement (edge cases)
* Literature evidence persistence strategy
