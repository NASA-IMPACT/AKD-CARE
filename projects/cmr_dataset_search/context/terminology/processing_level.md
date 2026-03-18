# Processing Level

## The ambiguity
Researchers say "I need MODIS data" without specifying processing level. CMR will return collections at every level — raw counts (L1), geophysical retrievals (L2), gridded composites (L3), and model-assimilated products (L4). These are not interchangeable and serve different research purposes.

## The distinctions

| Level | Description | Typical use |
|---|---|---|
| **L1B** | Calibrated, geolocated radiances or counts | Input to retrieval algorithms; not used directly |
| **L2** | Geophysical retrievals at native swath resolution | Custom processing, high spatial detail, gap-filled by user |
| **L3** | Gridded, composited (daily, 8-day, monthly) | Most research analyses; ready to use |
| **L4** | Model output, data assimilation, gap-filled | When spatial/temporal completeness is required |

## What to do

**Default recommendation: L3**, unless the researcher has a specific reason to need L2 or L4.

Recommend **L2** when:
- The researcher needs the highest native spatial resolution
- They are building their own compositing or retrieval pipeline
- They need data at the exact time of overpass (not composited)

Recommend **L4** when:
- The researcher needs spatially complete, gap-free coverage
- The variable is derived from model assimilation (e.g., GEOS-FP, MERRA-2)
- They are doing climate-scale or global analysis where data gaps are unacceptable

**Never recommend L1B** as the primary dataset for a research question — it requires instrument-specific expertise to use and is not a geophysical product.

## CMR search behavior
CMR collections include processing level in their metadata (`processing_level_id`). Always check this field when evaluating a returned collection. If processing level is ambiguous or missing from the collection metadata, flag it as a completeness concern.
