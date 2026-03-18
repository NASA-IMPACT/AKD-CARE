# NASA Worldview / GIBS Data Pathfinder
*Reference: Satellite imagery layers available via NASA Worldview and GIBS. Reflects layer availability as of December 2024.*

## Purpose
Maps Earth-science measurements to source instruments, spatial resolution, and temporal characteristics across 1,200+ satellite imagery layers.

Use this reference to:
- Identify which instruments measure a given variable
- Select appropriate satellite/instrument combinations
- Understand spatial vs. temporal resolution trade-offs
- Identify near-real-time (NRT) options for hazard monitoring
- Cross-reference measurements across disciplines

---

## Atmosphere

| Measurement | Instruments | Resolution |
|---|---|---|
| Aerosol Optical Depth (AOD) | MODIS, VIIRS, MISR, OMI | 1–10 km |
| Aerosol Index | OMI, OMPS | 25 km |
| Angstrom Exponent | VIIRS, MODIS, AERONET | 1–6 km |
| Aerosol Type | VIIRS Deep Blue | 6 km |
| Carbon Monoxide (CO) | MOPITT, AIRS | 22–50 km |
| Nitrogen Dioxide (NO₂) | OMI, TROPOMI | 13–25 km |
| Ozone (O₃) | OMI, OMPS | 25 km |
| Sulfur Dioxide (SO₂) | OMI, OMPS | 25 km |
| Cloud Fraction | MODIS, VIIRS, OMI | 1–25 km |
| Cloud Optical Thickness | MODIS | 1 km |
| Cloud Pressure | OMI | 25 km |
| Water Vapor | MODIS, AIRS, AMSR2 | 1–25 km |
| Brightness Temperature | MODIS, VIIRS | 1 km |

---

## Biosphere

| Measurement | Instruments | Resolution |
|---|---|---|
| NDVI | MODIS, VIIRS | 250 m–1 km |
| EVI | MODIS, VIIRS | 250 m–1 km |
| Chlorophyll-a | MODIS, VIIRS, PACE, Sentinel-3 | 1–4 km |
| Land Cover Type | MODIS | 500 m |
| LAI (Leaf Area Index) | MODIS | 500 m |
| FPAR | MODIS | 500 m |
| Net Primary Production | MODIS | 1 km |
| PAR (Ocean) | MODIS, VIIRS | 4 km |
| Burned Area | MODIS | 500 m |

---

## Cryosphere

| Measurement | Instruments | Resolution |
|---|---|---|
| Sea Ice Concentration | AMSR2 | 12.5–25 km |
| Sea Ice Extent | MODIS, VIIRS | 1 km |
| Snow Cover | MODIS, VIIRS | 500 m–1 km |
| Snow Water Equivalent | AMSR2 | 25 km |
| Ice Surface Temperature | MODIS | 1 km |
| NDSI | MODIS | 500 m |

---

## Ocean

| Measurement | Instruments | Resolution |
|---|---|---|
| Sea Surface Temperature (SST) | MODIS, VIIRS, GHRSST | 1–4 km |
| Sea Surface Salinity (SSS) | SMAP, Aquarius | 25–40 km |
| Ocean Color | MODIS, VIIRS, PACE | 1–4 km |
| Chlorophyll-a | MODIS, VIIRS, PACE | 1–4 km |
| Particulate Organic Carbon | MODIS | 4 km |
| Diffuse Attenuation (Kd490) | MODIS, VIIRS | 4 km |

---

## Land Surface

| Measurement | Instruments | Resolution |
|---|---|---|
| Land Surface Temperature (LST) | MODIS, VIIRS | 1 km |
| Surface Reflectance | MODIS, VIIRS, Landsat, HLS | 250 m–30 m |
| Albedo | MODIS MCD43 | 500 m |
| Digital Elevation | ASTER GDEM, SRTM | 30–90 m |
| Soil Moisture | SMAP, AMSR2, CYGNSS | 9–25 km |
| Flood Extent | MODIS MCDWD | 250 m |
| Fire / Thermal Anomalies | MODIS, VIIRS | 375 m–1 km |

---

## Human Dimensions

| Measurement | Instruments | Resolution |
|---|---|---|
| Night Lights (Black Marble) | VIIRS DNB | 500 m |

---

## Satellite Platforms

### Polar-Orbiting
| Platform | Instrument | Equator Crossing | Start | Focus |
|---|---|---|---|---|
| Terra | MODIS | 10:30 AM | Feb 2000 | Land, ocean, atmosphere |
| Aqua | MODIS | 1:30 PM | Jul 2002 | Land, ocean, atmosphere |
| Aura | OMI | 1:45 PM | Oct 2004 | Ozone, trace gases |
| Suomi NPP | VIIRS | 1:30 PM | Jan 2012 | Imagery, fires |
| NOAA-20 | VIIRS | 12:20 PM | Dec 2017 | Continuity |
| NOAA-21 | VIIRS | 1:30 PM | Mar 2023 | Next-gen |
| PACE | OCI | Sun-sync | Feb 2024 | Ocean color |
| Landsat 8/9 | OLI/TIRS | 10:00 AM | 2013/2021 | Land surface |

### Geostationary
| Platform | Instrument | Coverage | Update Frequency |
|---|---|---|---|
| GOES-East | ABI | Americas | 10 min |
| GOES-West | ABI | Americas | 10 min |
| Himawari-8/9 | AHI | Asia-Pacific | 10 min |

---

## Hazard Monitoring (NRT Layers)

| Event Type | Key Variables | Update Cadence |
|---|---|---|
| Wildfires | Fire thermal anomalies | Daily / NRT |
| Dust & Haze | AOD, Aerosol Index | Daily |
| Tropical Storms | Reflectance, IR brightness temp | 10 min |
| Volcanoes | SO₂, Ash RGB | Daily |
| Floods | MODIS MCDWD flood extent | Daily |
| Snow Events | Snow cover | Daily |
| Sea Ice | Concentration, extent | Daily |

---

## Temporal Archive Windows

| Sensor/Platform | Archive Start |
|---|---|
| MODIS Terra | Feb 2000 |
| MODIS Aqua | Jul 2002 |
| VIIRS (Suomi NPP) | Jan 2012 |
| PACE | Feb 2024 |
| Landsat 8/9 | 2013 / 2021 |
| Geostationary (GOES, Himawari) | Rolling ~90 days |

### Temporal Resolution Options
- Sub-daily (10 min to 3 hr) — geostationary only
- Daily — most polar-orbiting instruments
- 8-day composites
- 16-day composites
- Monthly / annual / static climatologies

---

## Imagery Types Available in Worldview

### Corrected Reflectance
- **True Color (RGB)**: Natural appearance
- **False Color (7-2-1)**: Fire detection
- **False Color (M11-I2-I1)**: Vegetation and water bodies

### Science Parameters
- Raster (gridded fields)
- Vector (point data: active fires, AERONET stations)

### Reference Overlays
- Coastlines, political borders, roads, labels, graticules
