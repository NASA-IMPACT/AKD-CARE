# **Existing Systems & Data Inventory (Final)**

---

## **1\. Tool / API Inventory**

### **1.1 NASA CMR API (Collections Search)**

* **Owner:** NASA Earthdata  
* **Purpose:**  
  Primary programmatic interface for dataset discovery via metadata search  
* **Access Method:**  
  REST API  
  Example:  
  `GET /search/collections.umm_json?umm_json=true`

---

### **Inputs (Query Parameters)**

**Required:**

* `keyword` — free-text search

**Optional:**

* `variable_name` — used when known (typically from literature)  
* `short_name` — dataset identifier  
* `instrument` — instrument filter  
* `temporal[]` — `[start, end]` (ISO timestamps)  
* `spatial[]` — bounding box (optional; default \= global)

---

### **Outputs**

* **Format:** UMM-JSON  
* **Fields Actively Used:**  
  * `ShortName`  
  * `EntryTitle`  
  * `Abstract`  
  * `Platforms[]`  
  * `Instruments[]`  
  * `ProcessingLevelId`  
  * `ScienceKeywords[]`  
  * `DataCenters[]`  
  * `RelatedUrls[]`  
  * `TemporalExtents`  
  * `SpatialExtent`

---

### **Usage Patterns**

* Primary: **Collection-level search**  
* Secondary: **Granule search (only for download workflows; out of scope)**  
* Query strategy:  
  * Keyword-based (default)  
  * Variable-based (when known from literature)

---

### **Auth Model**

* No authentication required for search

---

### **Limits / Constraints**

* Pagination: **not handled (ignored in practice)**  
* Result limits: **TBD**  
* Rate limits: **TBD**

---

### **Known Failure Patterns**

* Incomplete retrieval due to ignored pagination  
* Missed datasets due to weak keyword queries  
* Dependence on prior knowledge (variables)

---

### **Notes / Unknowns**

* Exact pagination behavior and caps (**TBD**)  
* Reliability of `variable_name` filtering across datasets (**TBD**)

---

---

### **1.2 Earthdata Search UI**

* **Owner:** NASA  
* **Purpose:** Primary manual dataset discovery interface

---

### **Usage**

* Default tool for researchers  
* Used for:  
  * Keyword search  
  * Metadata inspection

---

### **Constraints**

* Does not expose full dataset universe  
* Limited precision for variable-based filtering

---

### **Failure Modes**

* Missing datasets  
* Time-intensive manual filtering and inspection

---

---

### **1.3 Google Scholar**

* **Owner:** Google  
* **Purpose:** Literature discovery for:  
  * Variable identification  
  * Method replication

---

### **Access**

* Web UI only (no structured API)

---

### **Failure Modes**

* Manual extraction required  
* Unstructured results

---

---

### **1.4 NASA Science Discovery Engine (SDE)**

* **Owner:** NASA SMD  
* **Purpose:** Cross-domain discovery across:  
  * Publications  
  * Datasets  
  * Code  
  * Models  
  * Tools

---

### **Capabilities**

* Filter by:  
  * Missions  
  * Instruments  
  * Science domains  
* Returns:  
  * Datasets  
  * Documentation  
  * Software  
  * Media

---

### **Role**

* Supplement to Google Scholar  
* Provides more structured discovery signals

---

### **Unknowns**

* API availability (**TBD**)  
* Structured export capabilities (**TBD**)

---

---

### **1.5 Data Analysis Tools (Out of Scope)**

* QGIS  
* Python  
* R  
* GIS toolsets

---

### **Role**

* Post-discovery analysis only

---

---

### **1.6 Authentication System**

* **Name:** Earthdata Login  
* **Purpose:** Required for dataset download  
* **Not required for:** Search

---

---

## **2\. Dataset / Knowledge Source Inventory**

---

### **2.1 CMR-Indexed Dataset Universe (Canonical Source)**

* Includes:  
  * NASA datasets  
  * Non-NASA datasets (if indexed in CMR)

---

### **Characteristics**

* Centralized discovery layer  
* Metadata-driven access  
* Distributed ownership across DAACs

---

---

### **2.2 Scientific Literature**

#### **Sources:**

* Google Scholar  
* NASA Science Discovery Engine

---

### **Purpose**

* Identify:  
  * Variables  
  * Methods  
  * Dataset selection patterns

---

### **Structure**

* Unstructured → manual interpretation required

---

---

### **2.3 Researcher-Maintained Dataset Knowledge**

* **Form:** Personal dataset lists  
* **Purpose:**  
  * Reproducibility  
  * Method documentation in papers

---

### **Access**

* Not system-accessible  
* Only shared indirectly via publications

---

### **Constraints**

* Not standardized  
* Not reusable across researchers

---

---

### **2.4 Data Formats**

* User-dependent  
* Likely includes:  
  * NetCDF  
  * HDF5  
  * GeoTIFF

---

---

## **3\. Schemas, Access Patterns, and Documentation**

---

### **Search Behavior**

* Primary: Keyword-based search  
* Secondary: Variable-based (when known from literature)

---

### **Metadata Inspection**

**Fields prioritized by researchers:**

* Variables  
* Spatial resolution  
* Instruments  
* Processing level

---

### **Execution Modes**

* Manual (Earthdata UI)  
* Programmatic (CMR API)

---

### **Workflow Pattern**

1. Keyword search  
2. Metadata inspection  
3. Literature consultation  
4. Query refinement  
5. Repeat

---

---

## **4\. Permissions, Limits, and Operational Constraints**

---

### **Permissions**

* Search: Open  
* Download: Requires Earthdata Login

---

### **Operational Constraints**

* No system integration or orchestration  
* No shared dataset knowledge base  
* No standardized query methodology  
* Pagination not handled → risk of incomplete results

---

---

## **5\. Known Error Patterns / Failure Modes**

---

### **Discovery Failures**

* Missing datasets due to:  
  * Weak keyword queries  
  * Lack of variable knowledge  
  * Ignored pagination

---

### **Metadata Issues**

* Some metadata incomplete  
* Core required fields generally present

---

### **Dataset Issues**

* Deprecated datasets may still appear  
* Duplicate or inconsistent entries possible (rare)

---

### **Structural Gaps**

* No reusable mapping:  
  * Question → variables → datasets  
* Literature interpretation is manual  
* No shared institutional memory

---

---

## **6\. Open Questions / Unknowns**

---

### **CMR API**

* Pagination limits and behavior  
* Result size caps  
* Rate limiting  
* Cross-DAAC consistency of `variable_name`

---

### **Metadata**

* Consistency of variable representation across datasets  
* Reliability of spatial/temporal metadata fields

---

### **NASA SDE**

* API availability  
* Structured output access  
* Dataset linkage reliability

---

### **Data Layer**

* Granule-level metadata usage (currently out of scope but undefined)

---

