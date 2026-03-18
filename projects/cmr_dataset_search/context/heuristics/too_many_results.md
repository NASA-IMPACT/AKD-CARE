# Too Many Results: Narrowing a Broad CMR Search

## The heuristic
If a CMR search returns more than ~20 collections, the search is too broad to be useful. Apply filters in this order until the result set is manageable (5–15 collections):

1. **Add processing level filter** — default to L3; exclude L1 products
2. **Add temporal range** — if the researcher's study period is known, apply it
3. **Narrow the GCMD keyword** — move one level deeper in the hierarchy (e.g., from "OCEAN TEMPERATURE" to "SEA SURFACE TEMPERATURE")
4. **Add instrument or platform filter** — if a preferred sensor is implied or stated
5. **Add spatial bounding box** — if the study region is defined

## When it applies
Any time a CMR search returns an unmanageably large number of collections (>20 results with no clear differentiation).

## Exceptions
- Do not apply all filters simultaneously on the first narrowing attempt — add one at a time and re-evaluate
- Do not apply spatial bounding box as a first filter — it can exclude globally valid collections that happen not to declare a bounding box in their metadata

## What to do
When narrowing, tell the researcher which filter was applied and why. Do not silently discard results — the researcher may want to know that the broader search existed.
