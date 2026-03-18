# GCMD Science Keywords vs. Free-Text Search

## The ambiguity
CMR supports both free-text keyword search and GCMD controlled vocabulary search. These return different results and have different precision. Researchers and the agent may default to natural language terms that don't match GCMD vocabulary, causing missed collections.

## The distinctions

| Search type | How it works | Risk |
|---|---|---|
| **Free text** | Matches against collection titles, abstracts, short names | May miss collections that use different wording |
| **GCMD keyword** | Matches the controlled vocabulary field exactly | High precision, but requires the exact GCMD term |

GCMD science keywords follow a hierarchical structure:
`Topic > Term > Variable Level 1 > Variable Level 2 > Variable Level 3 > Detailed Variable`

Example:
`ATMOSPHERE > ATMOSPHERIC RADIATION > SOLAR IRRADIANCE > PHOTOSYNTHETICALLY ACTIVE RADIATION`

## What to do

1. **Always use `gcmd_keyword_lookup` before searching CMR** when the search involves a science variable. This normalizes the researcher's term to the correct GCMD hierarchy level.
2. Use the GCMD keyword result as the primary `keyword` parameter in `cmr_collection_search`.
3. If `gcmd_keyword_lookup` returns no match, fall back to free-text search — but flag to the researcher that results may be less precise.
4. Do not use overly specific GCMD terms (Variable Level 3 or Detailed Variable) as the primary search — these may return zero results. Start at Variable Level 1 or 2, then narrow if results are too broad.
5. Do not use overly broad GCMD terms (Topic level only, e.g., "ATMOSPHERE") — these will return thousands of collections with no discrimination.

## Good starting level
Variable Level 1 or Variable Level 2 is almost always the right entry point. Example:
- Too broad: `ATMOSPHERE`
- Too specific: `ATMOSPHERE > ATMOSPHERIC RADIATION > SOLAR IRRADIANCE > PHOTOSYNTHETICALLY ACTIVE RADIATION > PAR AT 490NM`
- Right level: `ATMOSPHERE > ATMOSPHERIC RADIATION > PHOTOSYNTHETICALLY ACTIVE RADIATION`
