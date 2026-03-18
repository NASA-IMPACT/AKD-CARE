# Phase 1 Artifact: Scope and Decompose

## Agent Purpose
Search NASA's Common Metadata Repository (CMR) to identify the most relevant Earth science datasets for complex research questions, automating variable discovery, dataset search, metadata evaluation, and literature-informed refinement.

## Primary Users
Experienced Earth science researchers (Master's level and above)

## User Expertise
Advanced Earth-science research experience  
Familiar with NASA data, CMR, and Earthdata Search

## Expected Tasks the Agent Must Support
- Identify relevant NASA datasets from CMR to answer Earth-science research questions  
- Map science questions → topics → required variables  
- Search datasets based on variables, keywords, and scientific context  
- Incorporate insights from existing literature to expand variables and processing requirements  
- Evaluate dataset metadata completeness and relevance  

## Current Workflow
1. Formulate a science question  
2. Identify all scientific topics involved  
3. Determine underlying variables required  
4. Search Earthdata Search for datasets matching variables  
5. If insufficient, review papers with similar studies to refine variables, resolution, and processing levels  
6. Re-search Earthdata Search using refined variables and keywords  
7. Review metadata to confirm completeness and applicability  

## Main Pain Points / Bottlenecks
- Difficult to identify all variables, especially for new research problems  
- Hard to choose the best dataset among many options  
- Time-consuming metadata inspection to ensure dataset suitability  

## Decisions That Must Remain Human-Controlled
- Interpreting spatial and temporal requirements  
- Selecting preferred instruments  
- Final scientific judgment on dataset appropriateness  

## Definition of Success
The agent returns a curated list of 5–6 datasets that collectively address all aspects of the science question—directly or indirectly—supported by existing research literature.

## Knowledge Volume Assessment
SME/research-scholar level domain knowledge required. Knowledge is deep and varies substantially by Earth science subdomain (e.g., ocean color, land surface temperature, atmospheric chemistry). A handbook-scale knowledge workspace will be needed in Phase 2.

## Summary
This agent supports experienced Earth science researchers in efficiently identifying the most relevant NASA datasets from CMR for complex research questions. It automates variable discovery, dataset search, metadata evaluation, and literature-informed refinement, while preserving human control over scientific interpretation and instrument selection.
