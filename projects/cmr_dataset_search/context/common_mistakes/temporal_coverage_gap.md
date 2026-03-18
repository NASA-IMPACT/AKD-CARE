# Mistake: Ignoring Temporal Coverage Gaps

## The mistake
Recommending a collection without verifying that it covers the researcher's study period, leading to a dataset recommendation that is useless for the actual analysis.

## Why it happens
CMR returns collections that match keyword criteria regardless of whether they overlap the researcher's time window. A collection may have ended years ago (e.g., SeaWiFS ended in 2010, Aquarius ended in 2015) but still appear in search results. The agent may see a relevant-sounding collection and recommend it without checking dates.

## How to avoid it
- Always check `temporal_extent` in the CMR collection metadata before recommending
- If the researcher's study period is known, pass it as a filter parameter in `cmr_collection_search` (temporal range filter)
- For any collection older than ~5 years: explicitly verify its end date — do not assume it is ongoing

## How to detect it
- Collection end date is before the researcher's study period start → disqualify immediately
- Collection start date is after the researcher's study period end → disqualify immediately
- Collection has a gap in the middle of the study period → flag as a known limitation

## What to do
If a recommended collection has a temporal gap or does not fully cover the study period:
1. Flag it explicitly in the recommendation
2. Suggest a successor mission if one exists (e.g., SeaWiFS → MODIS ocean color → VIIRS ocean color → PACE)
3. Do not recommend a collection that has zero overlap with the study period under any circumstance
