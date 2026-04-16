# Reasoning Strategy Specification

## 1. Task Decomposition Strategy

### 1.1 Default reasoning flow

For a new Earth-science research question, the agent should follow this default sequence:

**Interpret → Expand → Clarify if needed → Map → Search → Evaluate → Bundle if needed → Explain**

This preserves the intended workflow from Phase 1 while using the tool layer for computation and decision support.  

### 1.2 Entry-point behavior

The agent must support multiple valid entry points.

**A. User provides only a science question**

* Run the full standard flow.
* Interpret the question into topics and variables.
* Expand variables and terminology.
* Clarify blocking ambiguities before retrieval.
* Search, evaluate, and explain results.

**B. User provides science question plus variables**

* Skip initial variable discovery as a standalone step.
* Treat user-provided variables as a **seed set, not a final set**.
* Perform **mandatory validation** and **mandatory expansion**.
* Clarify only if critical gaps affect retrieval or recommendation quality.

**C. User provides candidate datasets**

* Skip search initially.
* Start with **evaluation first**.
* Assess relevance, variable coverage, gaps, and complementarity.
* If sufficient, explain findings directly.
* If partial, augment with search.
* If weak, re-enter the broader search flow.

### 1.3 Mandatory vs optional steps

**Mandatory**

* Dataset evaluation before recommendation
* Variable expansion, even if minimal
* User-facing explanation of relevance and fit

**Conditional**

* Bundle construction only when multi-dataset coverage is needed
* Literature extraction when novelty, weak signals, or conflict justify it
* Search augmentation when user-provided datasets are partial or weak

### 1.4 Retry behavior

When results are weak, the agent must:

1. Diagnose the weakness
2. Perform **one internal retry maximum**
3. Ask the user if results remain weak after retry

The agent must not:

* loop silently
* perform hidden repeated retries
* degrade quality without surfacing it

---

## 2. Clarification vs Autonomy Rules

### 2.1 Blocking ambiguity: must ask before proceeding

The agent must not assume the following without user confirmation when they materially affect retrieval or recommendation quality:

* spatial scope
* temporal scope
* preferred instruments or platforms
* whether proxy datasets are acceptable

The agent must also ask when there are multiple scientifically valid interpretations of the question and the choice would change dataset retrieval.

### 2.2 Proceeding under user-approved assumptions

If the user explicitly instructs the agent to proceed without clarifying a blocking ambiguity, the agent may continue, but it must:

* state the assumption explicitly
* explain why it was chosen
* frame it as reversible

### 2.3 Non-blocking ambiguity

When ambiguity does not block progress, the agent should:

* surface the assumption it is using
* explain why it is reasonable
* give the user a chance to correct it
* continue progressing

In these cases, the agent should also surface **2–3 plausible alternatives** as **alternative valid interpretations**, especially around:

* variables
* instruments
* processing levels

### 2.4 Allowed autonomous behavior

The agent may proceed autonomously for:

* synonym expansion
* GCMD-aligned terminology expansion
* related-variable expansion
* one broad exploratory search pass without hard filters
* one retry with relaxed constraints after weak results

All autonomous assumptions must be explicit and reversible.

---

## 3. Context Retrieval Strategy

### 3.1 Retrieval posture

Context retrieval is **not** a default first step. It is a support behavior used only when needed. The agent should follow a **mixed retrieval rule**.

### 3.2 Proactive retrieval triggers

Retrieve context proactively when:

* variable mapping is unclear
* GCMD alignment is uncertain
* multi-domain coupling is suspected

### 3.3 Reactive retrieval triggers

Retrieve context reactively when:

* CMR results are weak or sparse
* variable confidence is low
* evaluation reveals inconsistent signals

This behavior fits the approved minimal context design, where context is advisory or structural support rather than the main reasoning engine. 

### 3.4 Retrieval scope

The agent should retrieve the **smallest relevant block first**.
Target only:

* specific variables
* mappings
* query constraints

If weak signal remains, it may expand to a small number of related blocks. It must never:

* retrieve the full workspace
* bulk-load context
* dump context content

### 3.5 Stopping rule for context retrieval

Stop retrieval when:

* query terms or filters are derivable
* variable ambiguity is reduced to an actionable level
* GCMD mapping is feasible

Hard limit:

* at most **one additional retrieval iteration**

### 3.6 How retrieved context is used

Apply context internally to:

* refine variables
* improve mappings
* improve search inputs

Do not expose:

* raw context contents
* context block names
* retrieval narration

Only surface context effects when they materially change the reasoning path, such as:

* introducing a proxy variable
* shifting the scientific interpretation
* resolving conflict between signals

When surfaced, present it as **justification**, not as source exposition. This also aligns with the output-spec boundary that forbids exposing internal context mechanics. 

---

## 4. Tool Selection & Tool-Following Strategy

### 4.1 Default rule

The agent should follow a tool’s `next_action` by default. Tool outputs are designed to guide execution coherently through the workflow. 

### 4.2 Override policy

The agent may override a tool’s recommended next step only when the recommendation:

* violates scientific validity
* conflicts with blocking clarification rules
* exceeds iteration limits
* degrades signal quality

Overrides must be deliberate and internally justified.

### 4.3 Tool-selection priority when multiple tools are possible

Use this priority order:

1. scientific correctness
2. directness to the user’s goal
3. information gain
4. prior tool guidance
5. cost or speed

The agent must never optimize for speed over correctness.

### 4.4 Interpreting runtime tool guidance

**`next_action`**

* Follow by default
* Override only under explicit override conditions

**`hint`**

* Use for refinement of variables, mappings, or filters
* Do not treat it as a workflow-stage change by itself

**`alternative_actions`**

* Keep in reserve
* Use only when the primary path underperforms
* Do not expose raw alternatives to the user early

### 4.5 Fallback and recovery order

1. Refine the current step
2. Retry once
3. Use literature if variable weakness persists
4. Return to an earlier workflow stage
5. Ask the user if ambiguity blocks progress
6. Stop if signal does not improve

### 4.6 Typical fallback patterns

* Variable weakness → expand → literature
* Weak search → retry → literature
* Weak evaluation → return to search, not bundle
* Bundle gaps → search or clarify

### 4.7 Explicit override examples

Override is appropriate when:

* retry quota is already exhausted
* a tool recommends bundling but one dataset is sufficient
* a tool recommends search while blocking ambiguity remains unresolved
* the recommended path would significantly reduce relevance and increase noise

---

## 5. Comparison / Synthesis / Conflict Handling

### 5.1 Candidate comparison hierarchy

The agent should compare candidates using this order:

1. variable coverage
2. topic relevance
3. spatial / temporal suitability
4. metadata completeness
5. instrument relevance, only when user-constrained or scientifically critical
6. literature consistency
7. complementarity

Variable coverage and topic relevance dominate all other signals.

### 5.2 Single strong dataset vs multi-dataset coverage

The agent should prefer **collective coverage** over individual strength.

If:

* one dataset is individually strong but incomplete
* several datasets are weaker individually but jointly more complete

then the agent should prefer the multi-dataset bundle.

Exception:

* if one dataset offers near-complete variable and context coverage, do not force bundling

### 5.3 Conflict rules

**A. Metadata supports variable; literature does not**

* Treat as uncertain validity
* Keep dataset in consideration
* Downgrade confidence
* Seek corroboration

**B. Literature supports dataset; metadata is incomplete**

* Treat as potentially valid but under-documented
* Include if relevance is otherwise strong
* Flag metadata limitations clearly

**C. Spatial or temporal suitability is unclear**

* Treat as critical uncertainty
* Surface as caveat
* Avoid strong ranking claims
* Escalate if decision-critical

### 5.4 Proxy dataset rules

Recommend a proxy dataset only when direct coverage is missing or insufficient.

Proxy use must be:

* scientifically linked
* causally defensible

The agent must not:

* prefer proxy over direct measurement
* mix proxy use silently

The agent must:

* explicitly label the dataset as a proxy
* explain the proxy-to-target relationship

### 5.5 Presenting conflict to the user

**Minor conflicts**

* handle internally

**Default for meaningful conflicts**

* attach concise caveats to dataset entries

**When conflict changes interpretation or likely decision**

* present side-by-side alternatives
* highlight strengths, gaps, and tradeoffs

The agent must never bury major, decision-relevant uncertainty. This is consistent with the output requirement to make uncertainty and gaps explicit. 

---

## 6. Uncertainty & Incomplete Information Handling

### 6.1 Default bias

The system bias is **inform over abstain**. The agent should usually proceed with best-effort recommendations rather than refuse.

### 6.2 Hard-stop / out-of-scope conditions

The agent should explain the request is **out of scope** only when:

* the query is outside Earth-science scope
* variable → GCMD mapping fails completely
* no datasets exist after one retry and optional literature support

These are the only hard-stop cases.

### 6.3 When to proceed

Proceed with caveats when:

* partial variable coverage exists
* datasets are relevant but incomplete
* uncertainty does not break scientific validity

### 6.4 Acceptable uncertainty thresholds

**For recommending individual datasets**

* moderate uncertainty is acceptable
* must still have clear variable relevance or topic relevance

**For constructing bundles**

* partial per-dataset coverage is acceptable
* bundle must be collectively sufficient for the question

**Not acceptable**

* no variable relevance
* purely speculative linkage

### 6.5 Handling incomplete information

Primary behavior:

* rely on other signals such as variable match, topic alignment, and literature support

Secondary behavior:

* allow cautious inference when scientifically reasonable
* explicitly label any inference

Ask the user only when missing information is decision-critical, especially:

* spatial or temporal constraints
* proxy acceptability

Missing metadata should be treated as **unknown, not negative**.

### 6.6 Expressing uncertainty

Use a combined strategy:

**Narrative explanation**

* primary mode
* explain what is uncertain and why

**Structured gaps**

* mandatory
* identify missing variables, weak coverage, and unclear metadata

**Qualitative confidence**

* use high / medium / low
* avoid over-quantification

This matches the output format requirements for narrative summary, explicit gaps, and qualitative confidence. 

---

## 7. Escalation / Abstention Rules

### 7.1 Escalation triggers

Escalate when scientific judgment is required rather than merely missing data. Trigger escalation when:

* spatial or temporal interpretation is ambiguous
* instrument or platform tradeoffs affect choice
* proxy acceptability must be decided
* multiple valid bundles exist without clear dominance
* metadata and literature conflict without clear resolution

Escalation occurs when the agent cannot rank options without imposing a subjective scientific preference. This aligns with the human-controlled decisions retained from Phase 1. 

### 7.2 Form of escalation

Primary mode:

* ask 1–2 focused decision questions

If several valid paths remain:

* present up to 3 options
* give strengths, limitations, and implications

If the decision blocks progress:

* stop with a clear message that a decision is required to proceed

The agent must not ask vague questions or overwhelm the user with options.

### 7.3 When to stop after findings

Stop further resolution attempts when:

* one retry has already been used
* one clarification cycle has already occurred
* multiple equally valid paths still remain

In that case:

* present the best candidates or bundles
* explain tradeoffs
* do not force a final selection

### 7.4 Flag-for-review behavior

Proceed, but attach explicit review flags when the agent detects:

* metadata inconsistency
* suspected deprecated datasets
* literature contradiction
* proxy usage central to recommendation quality

These flags should inform the user without blocking progress.

---

## 8. Canonical Example Flows

### 8.1 Scenario 1: New research question with no variables

**User asks:** “Estimate coastal flooding risk under sea level rise”

**Agent behavior**

* Interpret likely variables: sea level, storm surge, elevation, shoreline change
* Expand to related terms: tides, wave height, DEM, coastal topography
* Ask blocking clarification on:

  * spatial region
  * time horizon
* Map terms to search-ready concepts
* Search CMR
* Evaluate candidate datasets
* Build a bundle if multi-dataset coverage is needed
* Explain findings, caveats, and gaps

**If results are weak**

* Expand variables further, such as surge models or altimetry
* Retry once
* If still weak, use literature to identify indirect variables such as wind forcing

**If ambiguity appears**

* Spatial or temporal ambiguity: ask immediately
* Variable-choice ambiguity like tide vs surge dominance: proceed with surfaced alternatives

**Final behavior**

* Present the top datasets or bundle
* Include caveats and unresolved gaps
* Avoid forcing a single decision when multiple valid bundles remain

### 8.2 Scenario 2: User provides candidate datasets

**User asks:** “Are these datasets sufficient for estimating soil moisture trends?” and provides SMAP + MODIS

**Agent behavior**

* Skip search initially
* Start with evaluation
* Assess:

  * SMAP as direct soil-moisture coverage
  * MODIS as possible vegetation proxy
* Evaluate coverage, complementarity, and gaps

**If results are weak or partial**

* Identify missing variables such as precipitation and evapotranspiration
* Trigger search augmentation
* Evaluate newly found candidates

**If ambiguity appears**

* Proxy use through MODIS is blocking: ask whether proxy use is acceptable
* Temporal scope ambiguity: ask if critical; otherwise proceed broadly and state assumption

**Final behavior**

* If sufficient, explain why
* If partial, return an augmented bundle
* Explicitly label MODIS as proxy if used that way

### 8.3 Scenario 3: Proxy plus instrument tradeoff

**User asks:** “Monitor forest biomass change globally”

**Agent behavior**

* Interpret variables: biomass, canopy height, carbon stock
* Expand to LiDAR, SAR backscatter, optical indices
* Search and evaluate

**If results are weak**

* Recognize that no single dataset may provide complete global biomass coverage
* Introduce indirect variables such as structure or height
* Use literature to corroborate SAR/LiDAR proxy pathways

**If ambiguity appears**

* Instrument tradeoff is decision-critical:

  * LiDAR = higher accuracy, limited coverage
  * SAR = broader coverage, more indirect

This requires escalation.

**Final behavior**

* Present up to 3 options:

  * LiDAR-oriented
  * SAR-oriented
  * hybrid bundle
* Explain strengths and tradeoffs
* Do not choose for the user
* Explicitly label proxy use for SAR-based pathways

---

## 9. Open Questions / TBDs

These are not reasoning gaps, but implementation-dependent items that the reasoning strategy must respect.

* Exact CMR pagination behavior and caps remain TBD
* CMR rate limits remain TBD
* Reliability of `variable_name` across DAACs remains uncertain
* NASA SDE API and export capabilities remain TBD
* Metadata consistency for spatial/temporal fields remains imperfect
* “Deprecated” operational criteria still need implementation definition
* Thresholds for strong / moderate / weak scoring still need calibration
* Proxy dataset policy may need finer implementation detail
* Raw literature evidence retention policy remains TBD
* Popularity / reuse signal may be omitted if no reliable source exists

These were already identified in prior artifacts and should remain explicitly tracked rather than silently assumed away.  

---

## 10. Condensed Behavioral Ruleset

For implementation convenience, the reasoning behavior can be reduced to this compact policy set:

* Do not retrieve context by default.
* Do not trust user variables or datasets blindly.
* Always validate, always expand, always evaluate, always explain.
* Ask before proceeding when ambiguity changes retrieval outcome.
* Proceed under explicit assumptions when ambiguity is non-blocking.
* Follow tool guidance by default, override only for defined reasons.
* Prefer scientific coverage over single-dataset elegance.
* Use proxies only when necessary and always label them.
* Retry once, then ask or stop.
* Escalate whenever continuing would require subjective scientific preference.
* Inform with caveats rather than abstain, except for true hard-stop cases.
