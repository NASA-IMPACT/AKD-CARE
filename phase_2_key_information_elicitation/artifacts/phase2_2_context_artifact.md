
# Phase 2.2: Context- NASA Worldview Data Pathfinder

*Condensed reference to satellite imagery layers available through NASA Worldview and GIBS*  
*Reflects layer availability as of December 2024*

---

## 1. About This Document

This pathfinder provides a concise reference to **1,200+ satellite imagery layers** available via **NASA Worldview** and the **Global Imagery Browse Services (GIBS)**.

It maps Earth-science measurements to:
- Source instruments
- Spatial resolution
- Temporal characteristics

### Intended Uses
- Identify available measurements by Earth-science domain
- Select appropriate satellite/instrument combinations
- Understand spatial vs. temporal resolution trade-offs
- Support hazard monitoring and rapid response
- Cross-reference measurements across disciplines

Source: NASA Worldview configuration, GIBS documentation, and NASA Earthdata resources.

---

## 2. Science Disciplines and Measurements

### 2.1 Atmosphere

| Measurement | Description | Instruments | Resolution |
|------------|-------------|-------------|------------|
| Aerosol Optical Depth (AOD) | Column aerosol concentration | MODIS, VIIRS, MISR, OMI | 1–10 km |
| Aerosol Index | UV-absorbing aerosol detection | OMI, OMPS | 25 km |
| Angstrom Exponent | Particle size indicator | VIIRS, MODIS, AERONET | 1–6 km |
| Aerosol Type | Dust, smoke, mixed | VIIRS Deep Blue | 6 km |
| Carbon Monoxide (CO) | Tropospheric concentration | MOPITT, AIRS | 22–50 km |
| Nitrogen Dioxide (NO₂) | Tropospheric column | OMI, TROPOMI | 13–25 km |
| Ozone (O₃) | Total & tropospheric column | OMI, OMPS | 25 km |
| Sulfur Dioxide (SO₂) | Volcanic/industrial emissions | OMI, OMPS | 25 km |
| Cloud Fraction | Cloud cover percentage | MODIS, VIIRS, OMI | 1–25 km |
| Cloud Optical Thickness | Cloud opacity | MODIS | 1 km |
| Cloud Pressure | Cloud-top pressure | OMI | 25 km |
| Water Vapor | Column precipitable water | MODIS, AIRS, AMSR2 | 1–25 km |
| Brightness Temperature | Thermal emission | MODIS, VIIRS | 1 km |

---

### 2.2 Biosphere

| Measurement | Description | Instruments | Resolution |
|------------|-------------|-------------|------------|
| NDVI | Vegetation greenness | MODIS, VIIRS | 250 m–1 km |
| EVI | Enhanced vegetation index | MODIS, VIIRS | 250 m–1 km |
| Chlorophyll-a | Phytoplankton concentration | MODIS, VIIRS, PACE, Sentinel-3 | 1–4 km |
| Land Cover Type | IGBP classification | MODIS | 500 m |
| LAI | Leaf Area Index | MODIS | 500 m |
| FPAR | PAR fraction absorbed | MODIS | 500 m |
| Net Primary Production | Ecosystem carbon uptake | MODIS | 1 km |
| PAR (Ocean) | Ocean light availability | MODIS, VIIRS | 4 km |
| Burned Area | Fire-affected extent | MODIS | 500 m |

---

### 2.3 Cryosphere

| Measurement | Description | Instruments | Resolution |
|------------|-------------|-------------|------------|
| Sea Ice Concentration | Fractional ice cover | AMSR2 | 12.5–25 km |
| Sea Ice Extent | Ice edge detection | MODIS, VIIRS | 1 km |
| Snow Cover | Binary snow presence | MODIS, VIIRS | 500 m–1 km |
| Snow Water Equivalent | Snowpack water content | AMSR2 | 25 km |
| Ice Surface Temperature | Polar ice thermal state | MODIS | 1 km |
| NDSI | Snow detection index | MODIS | 500 m |

---

### 2.4 Ocean

| Measurement | Description | Instruments | Resolution |
|------------|-------------|-------------|------------|
| Sea Surface Temperature | Ocean skin temperature | MODIS, VIIRS, GHRSST | 1–4 km |
| Sea Surface Salinity | Ocean salt concentration | SMAP, Aquarius | 25–40 km |
| Ocean Color | Water-leaving radiance | MODIS, VIIRS, PACE | 1–4 km |
| Chlorophyll-a | Phytoplankton biomass | MODIS, VIIRS, PACE | 1–4 km |
| Particulate Organic Carbon | Ocean carbon content | MODIS | 4 km |
| Diffuse Attenuation (Kd490) | Water clarity | MODIS, VIIRS | 4 km |

---

### 2.5 Land Surface

| Measurement | Description | Instruments | Resolution |
|------------|-------------|-------------|------------|
| Land Surface Temperature | Ground thermal emission | MODIS, VIIRS | 1 km |
| Surface Reflectance | Atmospherically corrected | MODIS, VIIRS, Landsat, HLS | 250 m–30 m |
| Albedo | Surface reflectivity | MODIS MCD43 | 500 m |
| Digital Elevation | Topographic height | ASTER GDEM, SRTM | 30–90 m |
| Soil Moisture | Surface water content | SMAP, AMSR2, CYGNSS | 9–25 km |
| Flood Extent | Inundation mapping | MODIS MCDWD | 250 m |
| Fire/Thermal Anomalies | Active fire detection | MODIS, VIIRS | 375 m–1 km |

---

### 2.6 Human Dimensions

| Measurement | Description | Instruments | Resolution |
|------------|-------------|-------------|------------|
| Night Lights (Black Marble) | Anthropogenic light | VIIRS DNB | 500 m |
| Earth at Night | City lights composite | VIIRS | 500 m |

---

## 3. Satellite Platforms and Instruments

### 3.1 Polar-Orbiting

| Platform | Instrument | Equator Time | Start | Focus |
|--------|------------|--------------|-------|-------|
| Terra | MODIS | 10:30 AM | Feb 2000 | Land, ocean, atmosphere |
| Aqua | MODIS | 1:30 PM | Jul 2002 | Land, ocean, atmosphere |
| Aura | OMI | 1:45 PM | Oct 2004 | Ozone, trace gases |
| Suomi NPP | VIIRS | 1:30 PM | Jan 2012 | Imagery, fires |
| NOAA-20 | VIIRS | 12:20 PM | Dec 2017 | Continuity |
| NOAA-21 | VIIRS | 1:30 PM | Mar 2023 | Next-gen |
| PACE | OCI | Sun-sync | Feb 2024 | Ocean color |
| Landsat 8/9 | OLI/TIRS | 10:00 AM | 2013/2021 | Land surface |

---

### 3.2 Geostationary

| Platform | Instrument | Coverage | Update |
|---------|------------|----------|--------|
| GOES-East | ABI | Americas | 10 min |
| GOES-West | ABI | Americas | 10 min |
| Himawari-8/9 | AHI | Asia-Pacific | 10 min |

---

## 4. Hazards and Disasters

| Event | Key Layers | Update |
|------|-----------|--------|
| Wildfires | Fire anomalies | Daily / NRT |
| Dust & Haze | AOD, Aerosol Index | Daily |
| Tropical Storms | Reflectance, IR | 10 min |
| Volcanoes | SO₂, Ash RGB | Daily |
| Floods | MODIS MCDWD | Daily |
| Snow Events | Snow cover | Daily |
| Sea Ice | Concentration, extent | Daily |

---

## 5. Imagery Types

### Corrected Reflectance
- True Color (RGB)
- False Color (7-2-1): fires
- False Color (M11-I2-I1): vegetation & water

### Science Parameters
- Raster (gridded)
- Vector (points: fires, AERONET)

### Reference Layers
- Coastlines, borders, roads
- Labels and graticules

---

## 6. Temporal Coverage

### Archive Availability
- MODIS Terra: Feb 2000
- MODIS Aqua: Jul 2002
- VIIRS: 2012–present
- Geostationary: rolling 90 days
- PACE: Feb 2024
- Landsat: 2013–present

### Temporal Resolution
- Sub-daily (10 min–3 hr)
- Daily
- 8-day composites
- 16-day composites
- Monthly, annual, static
