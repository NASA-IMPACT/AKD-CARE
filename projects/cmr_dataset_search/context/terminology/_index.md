# Index

## Trigger Table

| If the situation involves... | Retrieve from | Why |
|------------------------------|---------------|-----|
| granule, granules, collection, collections, files, scenes, tiles, overpasses, dataset files, download files | collection_vs_granule.md | Retrieve when the user or agent conflates collections with granules, asks about specific files or scenes, or when the distinction between collection-level and granule-level search is relevant to the task. |
| processing level, L1, L2, L3, L4, L1B, L2 product, L3 product, composite, swath, gridded, gap-filled, assimilation, MERRA, GEOS | processing_level.md | Retrieve when processing level is relevant to choosing between collections, when a researcher does not specify a processing level, or when the agent needs to explain the difference between L1/L2/L3/L4 products. |
| short name, entry title, concept ID, DOI, product name, dataset name, collection name, MOD, MYD, VNP, SPL, OMPS, identifier | collection_identifiers.md | Retrieve when the agent or user references a collection by name, short name, or title, or when constructing CMR search parameters that require a specific identifier type. |
| MODIS, Terra, Aqua, MOD, MYD, MCD, MODIS Terra, MODIS Aqua, overpass time, diurnal | modis_terra_vs_aqua.md | Retrieve when the user mentions MODIS without specifying Terra or Aqua, or when choosing between MOD, MYD, and MCD product families. |
| VIIRS, Suomi NPP, NOAA-20, NOAA-21, JPSS, VNP, VJ1, VJ2, NPP, Joint Polar Satellite | viirs_platforms.md | Retrieve when the user mentions VIIRS without specifying a platform, or when choosing between Suomi NPP, NOAA-20, and NOAA-21 VIIRS collections. |
| GCMD, science keywords, controlled vocabulary, keyword search, free text, keyword hierarchy, Variable Level, GCMD term, keyword lookup | gcmd_keyword_hierarchy.md | Retrieve when deciding whether to use GCMD keywords or free-text search, when constructing keyword parameters for CMR search, or when gcmd_keyword_lookup returns no match. |
| spatial resolution, resolution, spatial coverage, coverage, pixel size, footprint, swath, global coverage, regional, gap, completeness, 30 m, 1 km, 25 km, 500 m | spatial_resolution_vs_coverage.md | Retrieve when resolution vs. coverage is a factor in choosing between collections, when a researcher specifies a study region or minimum resolution requirement, or when comparing datasets with different spatial characteristics. |
