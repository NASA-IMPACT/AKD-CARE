
# Phase-2.1: Tools Requirements Specification
**For the planned NASA Earth-Science Dataset Discovery Agent**  
Based on Stage-1 requirements and SME responses


## 1. Overview
This document defines the tools, APIs, datasets, schemas, constraints, and known quirks required for the future agent that helps experienced Earth-science researchers identify NASA datasets via **CMR**, **GCMD**, and **literature-informed variable discovery**.
This document focuses only on **tools and data** — not prompts, reasoning, or workflow design.

## 2. Tools / APIs
### 2.1 NASA CMR Collections Search API
**Owner**  
NASA ESDIS (Earth Science Data and Information System)
**Purpose**  
The agent uses CMR Collections Search to:
- Search for datasets relevant to:
  - Variables (`variable_name`)
  - Temporal range
  - Spatial constraints
  - Keywords derived from the science question
- Retrieve **UMM-JSON** metadata for dataset evaluation
**Authentication**  
None (public, unauthenticated)
**Rate Limits**  
None specified
**Base Endpoint**
```
GET https://cmr.earthdata.nasa.gov/search/collections.umm_json?umm_json=true
```

#### Parameters
**Required**
| Parameter | Type | Description |
|---------|------|-------------|
| keyword | string | Free-text search term(s) |

**Optional**
| Parameter | Type | Notes |
|---------|------|-------|
| variable_name | string | Variable name(s) inferred from question or literature |
| short_name | string | Dataset short name |
| instrument | string | Instrument filter |
| temporal[] | array | `temporal[]=start,end` (ISO timestamps) |
| spatial[] | array | If omitted → global search (bbox supported) |

**Response Format**  
Always request **UMM-JSON**.

**Fields the Agent Must Read**
- `ShortName`
- `EntryTitle`
- `Abstract`
- `Platforms[]`
- `Instruments[]`
- `ProcessingLevelId`
- `ScienceKeywords[]`
- `DataCenters[]`
- `RelatedUrls[]`
- `TemporalExtents`
- `SpatialExtent` (if present)

**Known Quirks**
- Metadata quality varies; fields may be missing
- Data quality flags may be incomplete
- Keyword search can be noisy

**Documentation**
- https://cmr.earthdata.nasa.gov/search/site/docs/search/api.html
- https://wiki.earthdata.nasa.gov/spaces/CMR/pages/50037330

### 2.2 NASA GCMD Keyword Service (KMS)
**Purpose**
- Controlled vocabulary lookups for:
  - Science Keywords
  - Instruments
  - Platforms
- Normalize free text and expand search terms

**Query Method**
- Static local vocabulary (JSON), or
- Direct KMS API calls

**Preferred Format**
- JSON (XML/CSV also available)

**Required Fields**

**Science Keywords**
- Category
- Topic
- Term
- Variable_Level_1
- Variable_Level_2
- Variable_Level_3
- Detailed_Variable (if present)

**Instruments & Platforms**
- Short_Name
- Long_Name
- Associated identifiers / URIs

**Known Issues**
- May lag behind newest missions
- Inconsistent hierarchy depth

**Endpoints**
- Science Keywords:  
  https://cmr.earthdata.nasa.gov/kms/concepts/concept_scheme/sciencekeywords/
- Instruments:  
  https://cmr.earthdata.nasa.gov/kms/concepts/concept_scheme/instruments/
- Platforms:  
  https://cmr.earthdata.nasa.gov/kms/concepts/concept_scheme/platforms/

---

### 2.3 Semantic Scholar API

**Purpose**
Identify literature that:
- Uses relevant datasets
- Addresses similar science questions
- Helps refine variables, spatial/temporal scales, and processing levels

**Rate Limit**
- 1 request per second

**Authentication**
- None

#### Endpoints

**Paper Search**
```
GET /graph/v1/paper/search
```

**Important Fields**
- `query`
- `limit` (5–10 recommended)
- `fields`

**Paper Details**
```
GET /graph/v1/paper/{paperId}
```
**Fields to Extract**
- Title
- Abstract
- Topics / Keywords
- Authors
- Year
- DOI
- Methods info (if present)
- Citation counts
- Dataset mentions (inferred)

**Documentation**
- https://api.semanticscholar.org/api-docs/

---

## 3. Data Sources

### 3.1 Live External Sources
- CMR Collections Search
- GCMD/KMS vocabularies
- Semantic Scholar

### 3.2 Cached / Static Sources
- GCMD vocabularies (JSON dumps recommended)
  - Science Keywords
  - Instruments
  - Platforms

### 3.3 Internal Structures (Future)
No internal datasets specified yet. If added later, document:
- Name
- Storage location
- Access method
- Schema
- Permissions

---

## 4. Input / Output Schemas

### 4.1 CMR Collection Search — Example Request
```
GET https://cmr.earthdata.nasa.gov/search/collections.umm_json?umm_json=true
&keyword=soil+moisture
&variable_name=soil_moisture
&temporal[]=2010-01-01T00:00:00Z,2020-12-31T23:59:59Z
&spatial[]=-180,-90,180,90
```

### 4.2 CMR Collection Search — Example Response
```json
{
  "hits": 124,
  "items": [
    {
      "meta": { "concept-id": "C12345-EXAMPLE" },
      "umm": {
        "ShortName": "SMAP_L3_SM_P",
        "EntryTitle": "SMAP L3 Passive Soil Moisture",
        "Abstract": "Daily global soil moisture...",
        "Platforms": [{ "ShortName": "SMAP" }],
        "Instruments": [{ "ShortName": "SMAP_RAD" }],
        "ProcessingLevelId": "3",
        "ScienceKeywords": [
          { "Category": "Hydrology", "Topic": "Soil Moisture", "Term": "Surface" }
        ],
        "DataCenters": [{ "ShortName": "NSIDC" }],
        "RelatedUrls": [{ "URL": "https://nsidc.org/data/smap" }]
      }
    }
  ]
}
```

### 4.3 Semantic Scholar — Example Search Request
```
GET /graph/v1/paper/search?query=soil+moisture+trend+analysis&limit=5
```

### 4.4 Semantic Scholar — Example Paper Response
```json
{
  "paperId": "abcdef12345",
  "title": "Assessing Global Soil Moisture Trends",
  "abstract": "...",
  "year": 2021,
  "doi": "10.1234/example.doi"
}
```

---

## 5. Permissions & Constraints

- All tools are **public and read-only**
- No state-changing operations
- Semantic Scholar rate limit must be respected

---

## 6. Known Issues & TBD

**Known Issues**
- Incomplete CMR metadata
- GCMD lag for new missions
- Dataset detection in literature must be inferred

**TBD**
- Caching strategies
- Internal indexes
- Error handling conventions
- Storage location for vocabularies
