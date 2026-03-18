# Mistake: Confusing Ocean vs. Terrestrial Chlorophyll Products

## The mistake
Searching for "chlorophyll" returns both **ocean color chlorophyll-a** (phytoplankton concentration in water) and **terrestrial vegetation chlorophyll** products (e.g., FPAR, canopy chlorophyll). These have completely different physical meanings, algorithms, and valid use cases. Recommending the wrong one is a significant scientific error.

## Why it happens
Both are called "chlorophyll" in natural language. GCMD and CMR metadata use different keyword paths for each, but a free-text search for "chlorophyll" returns both. The instrument and spatial resolution are the key differentiators, but a naive agent may not check these.

## How to avoid it
- Confirm the research domain before searching: **ocean/marine biology** → ocean color chlorophyll-a; **terrestrial ecology/vegetation** → canopy chlorophyll or FPAR/LAI
- Ocean color chlorophyll-a is produced by MODIS, VIIRS, PACE, and SeaWiFS; typical short names include `MODISA_L3m_CHL`, `PACE_OCI_L3m`
- Terrestrial chlorophyll proxies are LAI/FPAR from MODIS (`MOD15A2H`) or vegetation indices (NDVI/EVI from `MOD13`)
- GCMD keyword paths diverge early: `OCEANS > OCEAN CHEMISTRY > CHLOROPHYLL` vs. `BIOSPHERE > VEGETATION > LEAF CHARACTERISTICS`

## How to detect it
- If a collection's instrument is MODIS/VIIRS **and** the platform is oceanography-focused (e.g., provider is OB.DAAC), it is ocean color
- If the collection's spatial resolution is 500 m or finer, it is almost certainly terrestrial
- If the collection's temporal resolution is 8-day or monthly composite, it may be either — check the abstract

## What to do
When "chlorophyll" appears in a science question, **always ask or infer the domain** (ocean vs. land) before searching. Use domain-specific GCMD keywords from the start.
