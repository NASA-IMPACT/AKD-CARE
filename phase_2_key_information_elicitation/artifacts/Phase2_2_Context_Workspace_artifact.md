# Approved Context Spec Blocks

---

# Context: Keyword Expansion Reference (GCMD Science Keywords)

## Purpose

Support expansion of variables or concepts into alternative keyword forms to improve dataset search recall.

---

## Type

Domain

---

## Scope

Conditional

---

## Triggers

* When forming or refining search queries
* When variables are identified but terminology is unclear
* When search results are weak or incomplete
* When additional keyword variations are needed

---

## Authority

Advisory
(Not a source of truth for variable correctness, dataset selection, or scientific meaning)

---

## Canonical Path

context/domain/keyword_expansion_reference.md

---

## Maintenance

* Keep only keyword names and minimal hierarchy references
* Avoid maintaining full taxonomy structure
* Update only if keyword schema meaningfully changes
* Ensure usability remains focused on search recall

---

# Context: CMR Query Parameters Reference

## Purpose

Provide a reference of available CMR search parameters and fields to support correct query formulation and refinement.

---

## Type

Structural

---

## Scope

Conditional

---

## Triggers

* When constructing or refining a CMR query
* When selecting or recalling available filters
* When search results are weak, unexpected, or failing
* When unsure which parameters exist or how they are structured

---

## Authority

Source of truth (technical only)
(Valid for syntax and parameter availability, not for scientific relevance)

---

## Canonical Path

context/structural/cmr_query_parameters_reference.md

---

## Maintenance

* Keep parameter lists and examples up to date with CMR API
* Remove non-practical or verbose sections if not used
* Ensure quick lookup usability (filters, fields, examples)
* Reflect actual behavior where documentation diverges

---

# ✅ 3. Final Workspace Structure

```id="h0o0n7"
context/
  ├── _overview.md
  ├── domain/
  │     └── keyword_expansion_reference.md
  ├── structural/
  │     └── cmr_query_parameters_reference.md
```
If you want to continue to **Phase 3 (Reasoning Strategy)**, I can guide that next.
