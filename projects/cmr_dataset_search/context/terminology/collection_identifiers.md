# Short Name vs. Entry Title vs. Concept ID

## The ambiguity
CMR identifies collections using multiple identifiers that are often confused or used interchangeably. Using the wrong identifier in a search produces no results or incorrect results.

## The distinctions

| Field | Description | Example |
|---|---|---|
| **Short Name** | Compact product code; stable across versions | `MOD11A1` |
| **Entry Title** | Human-readable full name | "MODIS/Terra Land Surface Temperature/Emissivity Daily L3 Global 1 km SIN Grid V061" |
| **Concept ID** | Unique CMR internal identifier; version-specific | `C2565788905-LPCLOUD` |
| **DOI** | Citable persistent identifier | `10.5067/MODIS/MOD11A1.061` |

## What to do

- **Use Short Name for searching** — it is the most reliable and stable lookup key in `cmr_collection_search`.
- **Use Entry Title for display** — show researchers the full title in results so they can recognize the product.
- **Never use Concept ID as a search term** — it is version- and provider-specific and will not generalize.
- **Use DOI for citation** — when the agent recommends a collection, include the DOI if present in metadata.
- If a researcher gives you a short name (e.g., "MOD11A1"), search by that directly. Do not attempt to expand or guess the entry title.
- If a researcher gives you only a descriptive name ("MODIS land surface temperature daily"), use GCMD keyword lookup first to normalize the variable, then search CMR with the normalized keyword. Do not guess the short name.
