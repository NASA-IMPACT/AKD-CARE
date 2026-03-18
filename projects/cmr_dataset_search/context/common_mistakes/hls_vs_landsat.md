# Mistake: Recommending HLS When Researcher Asks for "Landsat"

## The mistake
A researcher asks for "Landsat surface reflectance" and the agent returns only classic Landsat collections (e.g., `LC08_L2SP`), missing **HLS (Harmonized Landsat Sentinel-2)** — which is often the better choice for research requiring more frequent 30 m coverage.

## Why it happens
HLS is not branded as "Landsat" in its name — it is a harmonized product that combines Landsat 8/9 and Sentinel-2. Researchers who are not familiar with HLS will not ask for it by name, and a keyword search for "Landsat" may not surface it prominently.

## How to avoid it
- When a researcher asks for "Landsat" for **land surface research at 30 m resolution**, proactively check for HLS collections as well
- HLS short names: `HLSL30` (Landsat-derived), `HLSS30` (Sentinel-2-derived)
- HLS provides ~2–3 day revisit at 30 m vs. ~16-day for Landsat alone — a significant advantage for time-sensitive studies
- HLS is available from 2013–present, matching Landsat 8 archive depth

## How to detect it
- Researcher asks for "high resolution land surface" data with frequent revisit
- Researcher asks for Landsat for vegetation monitoring, agriculture, or urban studies (where revisit frequency matters)

## What to do
When Landsat is requested for time-series or frequent-observation studies, recommend **HLS alongside standard Landsat collections** and explain the revisit frequency benefit. Let the researcher decide — do not silently substitute HLS for Landsat.
