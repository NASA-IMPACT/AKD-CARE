# Agent Overview: CMR Dataset Search

## The Most Important Thing to Understand

NASA CMR is a **metadata catalog**, not a data delivery system. Every search returns **collections** (not granules) — a collection is a named dataset product that may contain thousands of individual files. The agent's job is to identify the right *collections*, not to retrieve actual data files.

CMR collections carry rich metadata (temporal coverage, spatial extent, processing level, instrument, platform, variables, DOI, data format, access links) that is the authoritative source for dataset evaluation. **CMR collection metadata should always be consulted before drawing conclusions about a dataset's suitability** — do not rely on instrument tables or external references alone.

## How the Agent Operates

1. **Translate the science question** into required variables and GCMD-controlled keyword terms
2. **Search CMR** using those keywords (and optional temporal/spatial filters)
3. **Evaluate metadata** of returned collections for completeness, processing level, and relevance
4. **Refine via literature** if results are insufficient — use Semantic Scholar to find papers on similar problems, extract the variables and datasets they used, and re-search
5. **Return a curated list** of 5–6 collections that collectively address all aspects of the question

## Primary Users

Experienced Earth science researchers (Master's level and above) who are familiar with NASA data, CMR, and Earthdata Search. The agent does not need to explain basic remote sensing concepts, but it must make the *reasoning behind dataset selection* explicit and traceable.

## What Stays Human

- Interpreting spatial and temporal requirements
- Selecting preferred instruments when multiple are valid
- Final scientific judgment on dataset appropriateness

## Definition of Done

A curated list of 5–6 CMR collections, each with: short name, entry title, processing level, temporal coverage, spatial resolution, and a brief rationale for inclusion tied to the science question.
