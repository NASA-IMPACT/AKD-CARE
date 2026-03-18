Queries the Semantic Scholar Graph API to find peer-reviewed papers related to the researcher's science question. Triggered ONLY as a fallback when the initial CMR search returns insufficient results. The agent uses returned abstracts and keywords to infer additional variables, resolution requirements, and processing levels — then feeds these into a refined CMR search.

Trigger condition: invoke only when initial CMR search returns 0 results or results are clearly not relevant to the science question.

Two endpoints used:
1. Paper search:  GET https://api.semanticscholar.org/graph/v1/paper/search
2. Paper detail: GET https://api.semanticscholar.org/graph/v1/paper/{paperId}

Authentication: None required (public).
Rate limit: 1 request per second — must be respected.

Fields to extract from results:
- title, abstract, year, doi
- topics / keywords
- citationCount (proxy for paper quality/relevance)
- Dataset short names (inferred from abstract via CMR short_name lookup — see cmr_collection_search)

Notes:
- Dataset mentions must be inferred from abstract text; there is no structured "datasets used" field
- To resolve inferred dataset names to CMR short_names, use cmr_collection_search with the inferred name as keyword
- Limit queries to 5–10 results per search
- Prefer recent papers (last 5–10 years) unless the science question is historical
