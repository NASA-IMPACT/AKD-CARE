Queries the NASA CMR Collections Search API to find Earth science datasets relevant to a research question. Returns UMM-JSON metadata for each matching collection. Used as the primary discovery mechanism — the agent searches by keyword and/or variable name, then reads collection metadata to evaluate relevance, coverage, and completeness.

Base endpoint: GET https://cmr.earthdata.nasa.gov/search/collections.umm_json?umm_json=true

Authentication: None (public).
Rate limits: None specified.

Query design principle: queries must be targeted enough that the most relevant collection appears at the top. Use page_size=1 — a well-formed query should surface the best match as the first result. Do not paginate.

Fields the agent must read from each result:
- ShortName, EntryTitle, Abstract
- Platforms[], Instruments[]
- ProcessingLevelId
- ScienceKeywords[]
- DataCenters[]
- RelatedUrls[]
- TemporalExtents
- SpatialExtent (if present)
