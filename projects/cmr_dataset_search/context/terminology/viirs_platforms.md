# VIIRS — Multiple Platforms, Same Instrument

## The ambiguity
VIIRS now flies on three platforms: Suomi NPP, NOAA-20, and NOAA-21. CMR treats these as separate collections. Researchers often say "VIIRS data" without specifying which platform, and may not know that the collections have different short name prefixes and slightly different orbital characteristics.

## The distinctions

| Platform | Short name prefix | Equator crossing | Archive start |
|---|---|---|---|
| Suomi NPP | `VNP` | ~1:30 PM | Jan 2012 |
| NOAA-20 (JPSS-1) | `VJ1` | ~12:20 PM | Dec 2017 |
| NOAA-21 (JPSS-2) | `VJ2` | ~1:30 PM | Mar 2023 |

For most science variables, the products are scientifically interchangeable — the instrument calibration and algorithms are designed for consistency across platforms.

## What to do

- When a researcher asks for "VIIRS [variable]," **recommend the Suomi NPP collection (VNP) as the primary** — it has the longest archive (2012–present).
- For studies requiring **continuity or multi-platform time series**, mention that NOAA-20 (VJ1) provides overlap and extends coverage with a slightly different overpass time.
- NOAA-21 (VJ2) products are still maturing in CMR — only recommend if the researcher specifically needs the most current data or NOAA-21 coverage.
- Do not treat the three as identical in metadata — check the `platform` field in CMR collection results to confirm which platform a collection belongs to.
