# MODIS Terra vs. Aqua — Same Instrument, Different Platforms

## The ambiguity
Researchers say "MODIS" without specifying Terra or Aqua. These are two separate satellite platforms carrying near-identical MODIS instruments, producing separate collections with different short name prefixes and different equator crossing times. CMR treats them as distinct collections.

## The distinctions

| Attribute | Terra-MODIS | Aqua-MODIS |
|---|---|---|
| Short name prefix | `MOD` (e.g., MOD11A1) | `MYD` (e.g., MYD11A1) |
| Equator crossing (descending) | ~10:30 AM local | ~1:30 PM local |
| Archive start | Feb 2000 | Jul 2002 |
| Status | Operational (aging) | Operational (aging) |

Combined/merged products exist and use the prefix `MCD` (e.g., `MCD43A3` for albedo, `MCD12Q1` for land cover) — these draw from both platforms.

## What to do

- When a researcher says "MODIS [variable]" without specifying a platform, **recommend both MOD and MYD collections** and note the overpass time difference.
- If the research question involves **diurnal variation** (e.g., morning vs. afternoon LST, urban heat island), explicitly flag the 10:30 AM vs. 1:30 PM distinction as scientifically meaningful.
- If the researcher needs the **longest possible archive**, prefer Terra (MOD) — it starts Feb 2000 vs. Aqua's Jul 2002.
- For variables where a **combined product exists** (MCD prefix), recommend the combined product first as it provides better temporal sampling.
- Do not assume "MODIS" means Terra only.
