Thought process:

Stage 8 Agent is an interviewer agent to support the benchmarking of the
Agent being Designed

Goal is to ask SME questions along these dimension

-   [Ask each SME to give 5 papers (DOIs) for the task to extract
    benchmark information - need full papers also]{.mark}

-   [give one or more science queries that can be addressed by
    information within the paper]{.mark}

-   What is their acceptance criteria

    -   Recall@k - how many results where returned in top 10

Benchmark Agent Pipeline - Agent specific

-   Extract datasets from the [right section]{.mark}

-   Extract datasets and relevant metadata

    -   \<prompt\> you are an scientific dataset information extraction
        agent specializing in extracting information from the provided
        paper. You are to extract the following:

Metadata:

-   Satellite data used

-   Sensor Name

-   Variable / Measurement

-   Phenomenon

-   Related Science topic

-   Resolution - spatial and temporal used in the paper

-   Acquisition dates

-   Coverage - location

-   Processing Level

Only extract from methodology section where the paper explicitly states
the usage of the dataset

-   Map it to the right concept ids

    -   \<prompt\>

        -   Use the metadata information to query CMR to extract Concept
            ids, Short Name

-   Create tiered queries based on the paper and SME query

    -   \<prompt\> You are a science data set query generation agent
        specializing in generating multiple queries with various levels
        of difficulty: Easy, Medium and Hard. The generated query should
        be such that the answer is the datasets/metadata provided being
        returned. Use the provided paper as the context. The query
        should be also such that there should be only one potential
        answer (which is the metadata provided).

    -   Will need to have some examples within the prompt

    -   Only one potential answer

-   Output into a structured spreadsheet

Where should SMEs provide feedback:

-Reasoning for data selection,keywords, variables, query construction,
scientific validity when there is ambiguity, end-to- end results

-Success criteria?

Notes:

-   Utility scores

    -   Metadata alignment coverage

        -   What are metadata fields for data agent ?

            -   

    -   Utility score (mrr, recall@k)

        -   recall@K for expected ConceptIDs

FINAL Prompt

**R --- Role / Persona\
** Stage 8 Interviewer Agent specializing in SME-led benchmark design
for RAG systems.

**G --- Goal\
** Elicit structured, benchmark-ready inputs from SMEs to evaluate the
Agent Being Designed.

**I --- Inputs**

-   Stage 1: Requirements Documents

-   Stage 2: Tool Requirements

-   SME expertise and domain knowledge

**C --- Constraints**

-   Any scientific/technical domain

-   Peer-reviewed or DOI-backed papers

-   End-to-end RAG focus

-   Both qualitative & quantitative acceptance criteria

-   No task execution; elicitation only

-   Output as tables

**O --- Output Format\
** Structured tables (Markdown-compatible)

**S --- Steps\
** Analyze requirements → Interview SME → Extract papers, queries,
criteria, metrics → Validate completeness → Output tables

extraction results

**{**

**\"datasets\": \[**

**{**

**\"Satellite data name\": \"Landsat-8 imagery (2 scenes; WRS-2 path/row
129/50 & 128/50)\",**

**\"Sensor Name\": \"OLI (and TIRS listed, but multispectral OLI bands
used)\",**

**\"Variable / Measurement\": \"Bottom-of-atmosphere (BoA) surface
reflectance for multispectral bands (Blue, Green, Red, NIR, SWIR-1,
SWIR-2) aggregated/resampled to 60 m; derived spectral indices and 60-m
intrapixel statistics used as AGB predictors\",**

**\"Phenomenon\": \"Forest aboveground biomass (AGB) spatial variation
and sensor saturation in tropical forest\",**

**\"Science topic\": \"Forest biomass / forest carbon mapping (tropical
forests)\",**

**\"Spatial Resolution\": \"Original 30 m; resampled/aggregated to 60 m
for modeling to match LiDAR-AGB reference map\",**

**\"Temporal Resolution\": \"Two acquisitions during dry season (used as
image mosaic)\",**

**\"Acquisition Date\": \"2018-11-05 and 2018-12-14\",**

**\"Location Coverage\": \"Khao Yai National Park (KYNP), central
Thailand (mosaicked to cover whole KYNP; \~2170 km² stated)\",**

**\"Processing Level\": \"Orthorectified and radiometrically calibrated
products; atmospheric correction and dehazing applied; BoA reflectance
computed (Overland software); mosaicked; then resampled to 60 m\",**

**\"How used\": \"Used as passive multispectral predictors (bands +
derived spectral/intrapixel indices) to train/validate Random Forest
models predicting LiDAR-derived AGB and to assess AGB prediction
accuracy and saturation limits.\"**

**},**

**{**

**\"Satellite data name\": \"Sentinel-2B imagery (2 tiles/mosaicked
scenes over MGRS tiles 47PQS, 47PQR, 47PRR)\",**

**\"Sensor Name\": \"MSI (Multispectral Instrument)\",**

**\"Variable / Measurement\": \"Bottom-of-atmosphere (BoA) surface
reflectance for multispectral bands including red-edge bands;
aggregated/resampled to 60 m; derived spectral indices (including
red-edge based indices) and 60-m intrapixel statistics used as AGB
predictors\",**

**\"Phenomenon\": \"Forest aboveground biomass (AGB) spatial variation
and sensor saturation in tropical forest\",**

**\"Science topic\": \"Forest biomass / forest carbon mapping (tropical
forests)\",**

**\"Spatial Resolution\": \"Original 10 m (as used in paper);
resampled/aggregated to 60 m for modeling to match LiDAR-AGB reference
map\",**

**\"Temporal Resolution\": \"Two acquisitions during dry season (used as
image mosaic)\",**

**\"Acquisition Date\": \"2018-11-03 and 2019-03-23\",**

**\"Location Coverage\": \"Khao Yai National Park (KYNP), central
Thailand (mosaicked to cover whole KYNP; \~2170 km² stated)\",**

**\"Processing Level\": \"Orthorectified and radiometrically calibrated
products; atmospheric correction and dehazing applied; BoA reflectance
computed (Overland software); mosaicked; then resampled to 60 m\",**

**\"How used\": \"Used as passive multispectral predictors (including
red-edge information) to train/validate Random Forest models predicting
LiDAR-derived AGB, compare performance vs Landsat-8 and WorldView-3, and
quantify AGB signal saturation point.\"**

**},**

**{**

**\"Satellite data name\": \"WorldView-3 imagery (single scene;
purchased; covering LiDAR area)\",**

**\"Sensor Name\": \"WorldView-3 (multispectral + panchromatic used for
textures)\",**

**\"Variable / Measurement\": \"BoA reflectance derived from calibrated
digital numbers for multispectral bands; panchromatic band used to
derive texture metrics (FOTO and lacunarity) in 60-m windows; all
predictors resampled/aggregated to 60 m\",**

**\"Phenomenon\": \"Forest aboveground biomass (AGB) spatial variation
and sensor saturation in tropical forest\",**

**\"Science topic\": \"Forest biomass / forest carbon mapping (tropical
forests)\",**

**\"Spatial Resolution\": \"Original MSS 1.2 m; Panchromatic 0.3 m (used
for texture); resampled/aggregated to 60 m for modeling to match
LiDAR-AGB reference map\",**

**\"Temporal Resolution\": \"Single acquisition\",**

**\"Acquisition Date\": \"2018-06-23\",**

**\"Location Coverage\": \"LiDAR-covered area in northern KYNP, Thailand
(WV3 coverage stated as 113 km²; used only cloud- and shadow-free pixels
over LiDAR area)\",**

**\"Processing Level\": \"Ortho-ready product; orthorectified using
rational polynomial coefficients plus LiDAR DSM and ground control
points; cloud masking; calibrated and converted to BoA reflectance; then
resampled to 60 m\",**

**\"How used\": \"Used as very high-resolution passive predictors
(spectral + texture + intrapixel metrics) to train/validate Random
Forest models predicting LiDAR-derived AGB and to compare AGB prediction
accuracy and saturation limits against Sentinel-2B and Landsat-8.\"**

**},**

**{**

**\"Satellite data name\": \"Shuttle Radar Topography Mission (SRTM)
elevation (DEM)\",**

**\"Sensor Name\": \"SRTM\",**

**\"Variable / Measurement\": \"Elevation (DEM) used as an auxiliary
predictor variable\",**

**\"Phenomenon\": \"Topographic control on forest AGB variability (via
effects on water/nutrient availability)\",**

**\"Science topic\": \"Forest biomass / forest carbon mapping;
topographic effects on vegetation structure\",**

**\"Spatial Resolution\": \"30 m (as stated)\",**

**\"Temporal Resolution\": \"Single-date DEM product (static)\",**

**\"Acquisition Date\": \"2014-09-23 (date stated in Table 2)\",**

**\"Location Coverage\": \"Khao Yai National Park (KYNP), Thailand (used
over study area)\",**

**\"Processing Level\": \"DEM product (SRTM; processing level not
further specified in the paper)\",**

**\"How used\": \"Included as an additional predictor in Random Forest
models to improve prediction of LiDAR-derived AGB by accounting for
topography-related AGB variation.\"**

**}**

**\]**

**}**

query generation results

{

\"easy\": \[

{

\"query\": \"I need a global digital elevation model at about 30 m grid
spacing that can be used as a terrain covariate (elevation) when
modeling forest aboveground biomass patterns in mountainous tropical
landscapes in Southeast Asia.\",

\"target_metadata_fields\": \[

\"variables: elevation (DEM)\",

\"spatial_resolution: \~30 m\",

\"spatial_coverage: near-global land\",

\"processing_level/product_type: DEM/topography product\"

\]

},

{

\"query\": \"Which freely available optical satellite
surface-reflectance imagery provides 30 m multispectral bands (visible,
NIR, and SWIR) suitable for computing common vegetation indices (e.g.,
NDVI, NDWI, NBR) for mapping tropical forest aboveground biomass over a
national-park--sized region?\",

\"target_metadata_fields\": \[

\"measurement: optical surface reflectance (visible/NIR/SWIR)\",

\"spatial_resolution: 30 m\",

\"product_type: orthorectified, radiometrically calibrated; surface/BOA
reflectance\",

\"use_case: vegetation indices for forest biomass mapping\"

\]

}

\],

\"medium\": \[

{

\"query\": \"What optical surface-reflectance dataset offers \~10 m
multispectral imagery with multiple red-edge bands, enabling red-edge
vegetation indices to improve aboveground biomass mapping in dense
tropical forests compared with traditional red--NIR indices?\",

\"target_metadata_fields\": \[

\"measurement: optical surface reflectance\",

\"spatial_resolution: \~10 m\",

\"spectral_characteristics: includes multiple red-edge bands\",

\"use_case: red-edge indices for tropical forest AGB mapping\"

\]

},

{

\"query\": \"I need very high spatial resolution commercial optical
imagery that includes a red-edge band and a sub-meter panchromatic band
so I can derive canopy texture metrics (e.g., Fourier-based texture
ordination or gap/heterogeneity measures) to model tropical forest
aboveground biomass, then aggregate predictors to \~60 m for comparison
with a biomass reference map.\",

\"target_metadata_fields\": \[

\"measurement: optical multispectral reflectance + panchromatic
imagery\",

\"spectral_characteristics: includes red-edge band\",

\"spatial_resolution: multispectral \~1--2 m; panchromatic sub-meter\",

\"use_case: texture metrics from pan band; biomass mapping after
aggregation\"

\]

}

\],

\"hard\": \[

{

\"query\": \"Which medium-resolution optical surface-reflectance product
provides visible--NIR--SWIR bands at 30 m that can be mosaicked from
multiple adjacent scenes acquired in the dry season over central
Thailand, and then resampled to 60 m to match a reference biomass grid
for random-forest modeling and saturation analysis above \~200 Mg/ha?\",

\"target_metadata_fields\": \[

\"measurement: BOA/surface reflectance optical bands
(visible/NIR/SWIR)\",

\"spatial_resolution: 30 m (native)\",

\"processing/workflow: multi-scene mosaic; dry-season acquisitions;
resampled/aggregated to 60 m\",

\"use_case: RF biomass modeling; signal saturation analysis\"

\]

},

{

\"query\": \"Which red-edge--capable 10 m optical surface-reflectance
dataset can be assembled from two acquisitions several months apart
(dry-season timing) to cover a large protected area in central Thailand,
and then aggregated to a 60 m grid for aboveground biomass prediction
using red-edge predictors and standard vegetation/water indices?\",

\"target_metadata_fields\": \[

\"measurement: BOA/surface reflectance\",

\"spatial_resolution: 10 m (native) with red-edge bands\",

\"temporal_characteristics: two acquisitions in dry-season window;
mosaicked coverage\",

\"processing: aggregated/resampled to 60 m\",

\"use_case: biomass prediction using red-edge + indices\"

\]

},

{

\"query\": \"Which commercial optical dataset provides \~1.2 m
multispectral reflectance (including coastal/visible/NIR plus a
dedicated red-edge band) together with \~0.3 m panchromatic imagery,
suitable for orthorectification with RPCs and deriving canopy texture
features in 60 m windows for tropical forest aboveground biomass
modeling over a \~100 km² calibration area?\",

\"target_metadata_fields\": \[

\"measurement: multispectral reflectance + panchromatic imagery\",

\"spectral_characteristics: includes dedicated red-edge band and
multiple NIR bands\",

\"spatial_resolution: \~1.2 m multispectral and \~0.3 m panchromatic\",

\"processing: RPC-based orthorectification; texture derivation using 60
m windows\",

\"spatial_coverage: scene-scale (\~100 km²)\"

\]

}

\]

}

Earth Science-Stage 6

# **Cognitive Verifier --- Prompt Logic Decomposition**

### **R --- Role / Persona**

An impartial, rigorous **Scientific Benchmark Interviewer Agent**
coordinating structured SME interviews for extract high-quality
benchmark paper and science query to build high-quality benchmark for
the Agent specified in 1

### **G --- Goal**

Extract high-quality benchmark paper, Science queries pointing to
dataset in those papers, and relevance judgments for evaluating
retrieval + reasoning performance.

### **I --- Inputs**

-   Stage-1 Scope document

-   Stage-2.1 Tools & Data Requirements

-   Stage-2.3 Output Formatting

-   Stage-3 Reasoning Strategy

-   Stage-4 Safety & Guardrails

-   Stage-5 Prompt Specifications

-   Live SME responses

### **C --- Constraints**

-   Peer-reviewed preferred; arXiv allowed at SME discretion

-   Open-access **full text required\
    **Exactly **5 papers per SME**

-   DOI **must be validated**

-   Recall metric fixed at **Recall@10**

-   No hallucinated citations

-   Output must be **script-parsable\
    **

### **O --- Output Format**

Table, CSV and structured JSON (for downstream evaluation pipelines)

### **S --- Process**

Progressive interview → validation → normalization → final dataset
packaging
