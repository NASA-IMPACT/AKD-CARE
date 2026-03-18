# Composite vs. Daily Data: When to Recommend Each

## The heuristic
**Default to composites (L3 8-day or monthly)** for most research use cases. Recommend daily data only when the science question requires it.

| Product type | When to recommend |
|---|---|
| **Daily L3** | Phenology, rapid-onset events, day-to-day variability, anomaly detection |
| **8-day composite** | Vegetation studies, land cover change, most optical variable time series |
| **16-day composite** | Landsat-based studies, albedo, moderate-frequency land monitoring |
| **Monthly composite** | Climatology, trend analysis, ocean color averages, long-term means |
| **Annual/static** | Land cover classification, DEM, slow-changing reference datasets |

## When it applies
Any time the agent is choosing between composite and daily versions of the same product (e.g., MOD11A1 daily vs. MOD11A2 8-day for LST).

## Exceptions
- For **fire/thermal anomaly** studies: always use daily or sub-daily data — compositing destroys fire detection signals
- For **ocean color**: monthly composites are standard for productivity/phenology studies; daily is rarely used except for bloom detection
- For **precipitation and atmospheric gases**: daily is the norm; compositing is rarely done at the collection level

## What to do
When recommending a composite product, note the temporal resolution explicitly (e.g., "MOD13A2 provides 16-day NDVI composites — sufficient for seasonal vegetation monitoring"). If the researcher's question implies high temporal frequency (e.g., "daily changes," "rapid response"), recommend daily data and explain the trade-off with gap coverage.
