# Mistake: Recommending Deprecated or Ended Missions Without a Successor

## The mistake
Recommending a collection from a mission that has ended (e.g., SeaWiFS, MERIS, Aquarius, CZCS) as a primary dataset, without noting the discontinuation or pointing to the current successor.

## Why it happens
CMR still hosts and returns historical collections from ended missions. These are scientifically valid for historical studies but are not usable for current or ongoing research. An agent that doesn't check the end date may recommend them as if they are operational.

## Common ended missions and their successors

| Ended mission | End date | Variable | Current successor |
|---|---|---|---|
| SeaWiFS | Dec 2010 | Ocean color, chlorophyll | MODIS Aqua, VIIRS, PACE |
| CZCS | Jun 1986 | Ocean color | SeaWiFS → MODIS → PACE |
| MERIS | Apr 2012 | Ocean color | OLCI (Sentinel-3), PACE |
| Aquarius | Jun 2015 | Sea surface salinity | SMAP |
| TRMM | Apr 2015 | Precipitation | GPM |
| Aura/MLS | Still operational as of 2024 | Stratospheric composition | — |

## How to avoid it
- Check `temporal_extent.end_date` in CMR metadata for any collection being considered
- If end date is more than 2 years ago, flag the collection as historical and identify the active successor
- Do not use "it's still in CMR" as evidence that a mission is operational

## What to do
If the researcher's study period overlaps with a historical mission's archive, recommend it for that period and explicitly name the successor for the remaining period. Example: "For 1998–2010, use SeaWiFS (SEAWIFS_L3m_CHL). For 2002–present, use MODIS Aqua ocean color (MODISA_L3m_CHL). PACE OCI (Feb 2024–present) is now the highest-quality successor."
