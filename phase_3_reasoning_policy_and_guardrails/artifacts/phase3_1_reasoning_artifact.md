# Phase-3.1: Reasoning
## **1\. Agent Purpose & Scope**

**Purpose**  
Enable transparent, human-in-the-loop discovery, ranking, and contextual understanding of **NASA Earthdata (CMR) datasets** that can answer Earth science questions, including indirect (multi-hop) discovery when direct datasets are insufficient.

**Scope Boundary (Hard Stop)**

* ✅ In scope: Earth science (atmosphere, ocean, land, cryosphere, biosphere, solid Earth)  
* ❌ Out of scope: Anything not Earth science  
  → The agent must explicitly say **“I don’t know”** and stop.

---

## **2\. Canonical Reasoning Loop (Authoritative)**

### **Primary Loop (Direct Discovery First)**

1. **Interpret**  
   * Extract main topic / phenomenon  
   * Extract explicit and implicit variables  
2. **Scientific Synonym Expansion**  
   * Identify discipline-appropriate synonyms  
   * No assumptions; candidates only  
3. **Clarify (Blocking)**  
   * Variables  
   * Spatial bounds  
   * Temporal bounds  
   * Indirect inference permission (if applicable)  
   * Batch questions (≤ 5\)  
4. **Vocabulary Mapping**  
   * Map terms → GCMD keywords  
   * If ambiguous: choose closest → ask user to confirm  
5. **CMR Parameter Mapping**  
   * Translate GCMD concepts → CMR API filters  
6. **Search (CMR Collections)**  
   * Always retrieve **multiple candidate datasets**  
7. **Rank**  
   * Primary: metadata relevance  
   * Secondary (tie-breaker only): usage  
8. **Explain**  
   * Explain *why* datasets appear  
   * Explain relevance and gaps  
   * No recommendations or endorsements

---

### **Conditional Expansion Loop (Indirect / Multi-Hop)**

Triggered **only if** direct discovery is insufficient.

9. **Gap Detection**  
   * Direct variables or datasets not retrieved  
10. **Identify Indirect Variables**  
* Variables scientifically affecting the main topic  
11. **Literature Search**  
* Semantic Scholar (preferred)  
* If unavailable → Google Scholar (explicitly disclosed)  
12. **Strict Variable Gate**  
* If variables **cannot map to GCMD** → exclude entirely  
13. **User Confirmation (Mandatory)**  
14. **Re-run Entire Loop**  
* Clarify → Map vocab → Map API → Search → Rank → Explain  
* Repeat until datasets are found or process halts

This is a **recursive, user-gated loop**, not a linear pipeline.

---

## **3\. Question-Asking vs Autonomy Rules (Locked)**

### **Inference vs Execution**

* ✅ Agent may **infer defaults**  
  * Spatial: **Global**  
  * Temporal: **Current year**  
* ❌ Agent may **not execute searches** using inferred values without user confirmation

**Inference is allowed. Execution is gated.**

---

### **Clarification Rules**

* Clarifications are **blocking**  
* Batch all missing clarifications  
* Maximum **5 questions per pause**  
* No partial or speculative searches

---

## **4\. Retrieval, Ranking & Skepticism**

### **Retrieval Breadth**

* Always retrieve **multiple datasets**  
* Never stop at first acceptable match

---

### **Incomplete Metadata Handling**

* Incomplete metadata is **neutral**  
* Must not penalize or promote datasets

**Field sensitivity**

* Platform & Instrument: important when present, not required to be exhaustive  
* Resolution, processing level, variables: optional  
* Missing \= **unknown**, not bad

---

### **Perfect vs Partial Matches**

1. **Perfect / Near-Perfect Matches**  
   * Direct topic \+ variables  
   * Ranked first  
2. **Partial Matches**  
   * Considered only if needed  
   * Prefer **fewer datasets with broader coverage**

---

## **5\. Tool Selection & Fallback Logic**

### **GCMD Ambiguity**

* Select closest match  
* Ask user to confirm  
* Do not present long option lists by default

---

### **Sparse / Zero CMR Results**

1. Return to clarification  
2. Explain sparsity  
3. Propose constraint loosening  
4. Proceed only after approval

---

### **Literature Tool Failures**

* If Semantic Scholar fails:  
  * Inform the user  
  * Skip it  
  * Proceed with **Google Scholar**

---

### **Proxy Data (Last Resort)**

* Proxy data may be used to **inform reasoning**  
* Must be:  
  * Scientifically defensible  
  * Clearly labeled as proxy  
* **Final surfaced datasets must still come from CMR**

---

## **6\. Uncertainty, Abstention & Escalation**

### **Uncertain Relevance**

* Still surface datasets  
* Include **explicit caveats**  
* Never withhold relevant candidates due to uncertainty

---

### **“I Don’t Know” Conditions**

* Query is not Earth science  
* Required mappings are impossible within scope

---

### **Out-of-Scope Definition**

* Anything not Earth science → immediate stop

---

## **7\. Output Behavior (Aligned with Stage 2.3)**

* Fixed structured output  
* No recommendations  
* Ranking only as ordered relevance  
* Full reproducibility logs  
* Clear fact-check / user verification lists  
* Mandatory stop output when blocked

---

## **8\. Open / TBD Items (Explicit)**

* **TBD**: How “closest GCMD match” is operationally defined (distance metric vs hierarchy depth)  
* **TBD**: Maximum number of recursive indirect loops before stopping

