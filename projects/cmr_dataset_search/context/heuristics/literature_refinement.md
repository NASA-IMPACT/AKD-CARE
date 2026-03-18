# Using Literature to Refine a CMR Search

## The heuristic
When the initial variable list is incomplete or the CMR results are insufficient, search Semantic Scholar for papers addressing a similar science question. Extract three types of signals:

1. **Dataset signals** — exact collection names, short names, or DOIs cited in the Methods section
2. **Variable signals** — variables the authors measured or derived that weren't in the original list
3. **Resolution/scale signals** — the spatial resolution and temporal period the authors used, which reveals what's scientifically appropriate for the problem

## When it applies
- After an initial CMR search returns fewer than 5 useful collections
- When the researcher's variable list seems incomplete for the science question
- When the agent is unsure which processing level or resolution is standard for this type of study

## Exceptions
- Do not search literature before attempting at least one CMR search — literature search is a refinement step, not a starting point
- Do not treat cited datasets as automatically correct — some papers use legacy or suboptimal datasets; evaluate the cited collections against current CMR offerings

## What to do
1. Call `semantic_scholar_search` with the core science topic (2–4 keywords)
2. Scan the returned papers for Methods sections mentioning datasets, instruments, or variables
3. Add any new variables to the search list
4. If a paper cites a specific collection by short name, search CMR directly for that short name to confirm it still exists and is active
5. Summarize which papers informed which additions — this makes the final recommendation traceable

## Search query construction for Semantic Scholar
Keep queries to 3–5 words focused on the phenomenon, not the data: e.g., "sea surface temperature coral bleaching" not "MODIS SST dataset ocean color." The literature search is about the science problem, not the data product.
