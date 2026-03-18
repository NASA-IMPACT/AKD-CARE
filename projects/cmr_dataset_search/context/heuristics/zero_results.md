# Zero Results: Recovering from an Empty CMR Search

## The heuristic
If a CMR search returns zero results, the keyword or filter is too specific or incorrectly formed. Recover in this order:

1. **Check GCMD keyword spelling** — re-run `gcmd_keyword_lookup` with a simpler term; GCMD terms are case-sensitive in some implementations
2. **Move up one level in the GCMD hierarchy** — if searching at Variable Level 2, try Variable Level 1
3. **Try free-text search** — use the researcher's original plain-language description as the keyword
4. **Remove temporal/spatial filters** — confirm the collection exists at all before re-applying constraints
5. **Search Semantic Scholar** — find papers on the same topic and extract the exact dataset names/short names they used, then search CMR directly by short name

## When it applies
Any time a CMR search returns zero collections.

## Exceptions
- If zero results persist after all steps above, the variable may not be available as a NASA CMR collection — flag this explicitly to the researcher rather than continuing to search
- Do not cycle through synonyms indefinitely; if 3 keyword variants return zero results, escalate to literature search

## What to do
Report the zero-result state transparently. Tell the researcher what was searched and what will be tried next. Do not silently skip a failed search.
