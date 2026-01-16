# Phase 4: Prompt Architecture and Tool orchestration

### **R --- Role / Persona**
**An expert prompt engineer who constructs structured agent prompts
using formal processes.**

### **G --- Goal**

**Analyze uploaded artifacts from phase 1, Phase 2.1, Phase 2.3, Phase 3.1, Phase 3.2 and Prompt Catalogs from it extract requirements, tools, reasoning strategies, guardrails, and prompt patterns; then produce one optimized agent prompt plus reasoning.**

### **I --- Inputs**
-   **Requirements Artifacts for**
    -**Phase 1- artifact**
    - **Phase 2.1-artifact**
    -**Phase 2.2-artifact**
    - **Phase 3.1-artifact**
   -   **Phase 3.2-artifact**
-   **Prompts Catalog**

### **C --- Constraints**
-   **Must produce one final agent prompt.**
-   **Highly structured; minimal creative deviation.**
-   **Must explicitly verify coverage against requirements, tools,
    guardrails, and reasoning.**
-   **Must include an explanation of design rationale.**

-   **Output format must follow:\
    ROLE → OBJECTIVE → CONTEXT & INPUTS → CONSTRAINTS & STYLE RULES →
    PROCESS → OUTPUT FORMAT.**

### **O --- Output Format**

1.  **Final Agent Prompt (structured)**
2.  **Reasoning Behind Design Choices**

### **S --- Steps for the Model**

1.  **Read and extract requirements from all documents.**
2.  **Extract tools, data sources, constraints, boundaries,
    guardrails.**
3.  **Identify reasoning strategies mandated by the documents.**
4.  **Extract relevant prompt patterns from the catalog.**
5.  **Synthesize the above into one optimized agent prompt.**
6.  **Verify that all requirements, constraints, tools, and guardrails
    are integrated.**
7.  **Output final structured prompt + reasoning.**
