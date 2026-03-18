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

---

## Dynamic CARE Augmentation

> When the `care-workspace-builder` MCP server is connected, perform these additional steps after the core prompt synthesis above. This validates the workspace and assembles the deployable artifacts. If no MCP server is connected, skip this section entirely.

### Part A: Draft Reasoning Strategy

Using everything captured in Phases 1-3, draft a reasoning policy:
1. Review the scope (from `scope.md`)
2. Review the knowledge structure (from `context/_index.md`)
3. Review the tool specifications (from `tools/`)
4. Write a reasoning policy describing HOW the agent should think

Present the draft to the SME for review and refinement.

### Part B: Validate the Workspace

Run validation to catch structural issues:

1. `validate_workspace(project_name)` — check for missing indexes, orphan files, incomplete tool specs
2. `validate_triggers(project_name)` — check trigger coverage percentage

Fix any issues found:
- Missing indexes → `index_generate(project_name, directory_path)`
- Orphan files → add trigger terms via `workspace_write`
- Missing tool spec files → `tool_spec_write`
- Broken references → fix the target paths

### Part C: Assemble Outputs

Generate the deployable artifacts:

1. `assemble_system_prompt(project_name, reasoning_policy=<the drafted reasoning strategy>)`
2. `assemble_runtime_config(project_name)`

Review with:
- **SME**: Is the assembled prompt accurate? Does it capture your expertise correctly?
- **Developer**: Is the runtime config correct? Can you connect the MCP servers?

### Transition

Tell the SME:

> "We've assembled the agent's knowledge base and system prompt. Next, we'll design test cases to verify the agent works correctly."
