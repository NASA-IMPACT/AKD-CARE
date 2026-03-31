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

**Output:**
Descriptive inventory of available systems (no reasoning or design decisions)

---

### **2.2: Context Workspace Design (Core Layer)**

Defines the agent’s **knowledge environment**:

* Context files (domain, workflows, policy, examples)
* Hierarchy (global vs task-specific)
* Retrieval triggers
* Authority and precedence rules

**Output:**

* Context structure
* Trigger → Context mappings

**Note:**
Defines *what context exists and when it is used*, not how the agent reasons with it.

---

### **2.3: MCP Tool Design**

Defines tools as **execution + instruction systems**:

* What tools exist
* What they compute/validate
* What they return (data + guidance)

**Output:**

* Tool contracts
* Instructional outputs (e.g., next actions, recovery steps)

**Dependency:**
Tool design depends on context workspace (2.2).

---

### **2.4: Output Format Design**

Defines how the agent communicates results:

* Output structure
* Intermediate steps (if needed)
* Failure and recovery signals

---

## Key Shift from CARE V1

| Area               | CARE V1                  | CARE V2                               |
| ------------------ | ------------------------ | ------------------------------------- |
| Context            | Static knowledge         | Structured, retrievable workspace     |
| Tools              | Data access              | Execution + instruction systems       |
| Design Order       | Tools + context together | Context → Tools (dependency enforced) |
| Knowledge Handling | Embedded in prompts      | Externalized into context system      |

---

## Role of Helper Agents

Helper agents:

* Elicit structured inputs from SMEs and developers
* Draft context workspace, tool contracts, and outputs
* Convert domain knowledge into **reviewable artifacts**

Humans validate all outputs through review gates.

---

## Outcome of Phase 2

A validated set of artifacts defining:

* Available systems and constraints
* Structured context workspace
* Tool execution contracts
* Output expectations

These form the **environment layer** that reasoning and prompts operate on in later phases.
