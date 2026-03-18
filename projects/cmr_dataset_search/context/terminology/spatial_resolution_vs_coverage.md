# Spatial Resolution vs. Spatial Coverage

## The ambiguity
"Resolution" and "coverage" are often used interchangeably but mean opposite things. A high-resolution dataset may have limited spatial coverage; a coarse-resolution dataset may be globally complete. Confusing these leads to recommending datasets that are either too coarse for the research question or have coverage gaps in the study region.

## The distinctions

| Concept | Meaning | Example |
|---|---|---|
| **Spatial resolution** | Size of the smallest resolvable unit (pixel/footprint) | 500 m, 1 km, 25 km |
| **Spatial coverage** | Geographic extent of the collection | Global, regional, CONUS-only, polar |
| **Spatial completeness** | Whether coverage is continuous or gap-filled | Daily gaps due to swath width; composites fill gaps |

A 30 m Landsat product has high resolution but a 16-day revisit cycle with swath gaps. A 25 km SMAP product is coarse but globally complete every 2–3 days.

## What to do

- When a researcher specifies a study region, check CMR metadata for `spatial_extent` or `bounding_box` to confirm the collection covers that region.
- When resolution matters (e.g., urban-scale, field-scale studies), prioritize resolution. When global or regional completeness matters more, prioritize coverage.
- **Default tiebreaker**: if two collections otherwise seem equivalent, prefer the one with better spatial completeness (fewer gaps) over the one with marginally higher resolution.
- Flag to the researcher if a high-resolution dataset has significant temporal gaps in their study region — they may need to use composites or a coarser alternative.
- Do not confuse spatial resolution with pixel size in degrees — always convert to meters/km when comparing products.
