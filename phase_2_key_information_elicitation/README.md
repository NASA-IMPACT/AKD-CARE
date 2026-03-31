# Phase 2: Key Information Elicitation (CARE V2)

Phase 2 defines the agent’s **operational environment** by separating:
* what exists
* what knowledge is needed
* what should be handled by tools

This phase shifts from collecting inputs to **designing structured systems** for context and execution.

---

## Phase Structure

### **2.1: Existing Systems & Data Inventory**
Captures what already exists:
* Tools, APIs, datasets
* Schemas, permissions, constraints
* Known error patterns

### **2.2: Context Workspace Design (Core Layer)**

Defines the agent’s **knowledge environment**:
* Context files (domain, workflows, policy, examples)
* Hierarchy (global vs task-specific)
* Retrieval triggers
* Authority and precedence rules

### **2.3: MCP Tool Design**

Defines tools as **execution + instruction systems**:
* What tools exist
* What they compute/validate
* What they return (data + guidance)

### **2.4: Output Format Design**

Defines how the agent communicates results:
* Output structure
* Intermediate steps (if needed)
* Failure and recovery signals

## Outcome of Phase 2

A validated set of artifacts defining:

* Available systems and constraints
* Structured context workspace
* Tool execution contracts
* Output expectations

These form the **environment layer** that reasoning and prompts operate on in later phases.
