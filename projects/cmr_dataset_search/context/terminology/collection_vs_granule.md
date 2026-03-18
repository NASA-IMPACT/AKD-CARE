# Collection vs. Granule

## The ambiguity
"Dataset" is used casually to mean many things. In CMR, there are two distinct levels: **collections** and **granules**. These are not interchangeable, and confusing them leads to searches that return nothing useful or far too much.

## The distinctions

| Term | CMR meaning | Example |
|---|---|---|
| **Collection** | A named product — the dataset as a whole | MOD11A1 (MODIS Land Surface Temperature, daily, 1 km) |
| **Granule** | A single file within a collection — one scene, one overpass, one time step | MOD11A1.A2023001.h10v05.061.*.hdf |

CMR collection search (`/search/collections`) returns collections.
CMR granule search (`/search/granules`) returns individual files within a collection.

## What to do
- **This agent works at the collection level.** Always use collection search.
- When a researcher asks "find me MODIS LST data," the answer is the collection `MOD11A1` (or `MYD11A1` for Aqua), not individual granule files.
- Never quote granule counts or file sizes as part of the recommendation — those are granule-level details outside this agent's scope.
- If a researcher asks how to download specific files, redirect them to Earthdata Search or the CMR granule API — that is outside this agent's task.
