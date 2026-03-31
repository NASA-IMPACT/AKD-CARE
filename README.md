# AKD-CARE (CARE V2)
AKD-CARE is a structured repository for designing AI agents for science using the **CARE V2 (Collaborative Agent Reasoning Engineering Version 2)** methodology.

CARE V2 reframes agent development as a **layered systems architecture**, where **context, tools, reasoning, and safety are explicitly separated** and composed through structured artifacts.

The methodology enforces:
> **Environment first → Behavior next → Implementation last**
This repository serves as the **single source of truth** for all CARE artifacts, including workspace design, tool contracts, reasoning policies, and evaluation.

---

## What is CARE V2?
CARE V2 is an evolution of CARE that treats:
* **Context as a structured, retrievable system (not a prompt blob)**
* **Tools as execution + instruction layers (not just APIs)**
* **Reasoning as orchestration across context and tools**
* **Prompts as lightweight wiring (not logic containers)**

It introduces **clear separation of concerns**:
* Knowledge → Context Workspace
* Execution → Tools
* Decision-making → Reasoning Policy
* Safety → Guardrails

---

## Key Differences: CARE V1 vs CARE V2

| Area               | CARE V1                     | CARE V2                                         |
| ------------------ | --------------------------- | ----------------------------------------------- |
| Context            | Static, embedded in prompts | Structured, hierarchical, retrieved dynamically |
| Tools              | Data access APIs            | Execution + validation + instruction providers  |
| Prompts            | Contain logic and reasoning | Thin orchestration layer                        |
| Design Flow        | Prompt-first                | Environment-first                               |
| Knowledge Handling | Mixed into prompts          | Explicit context workspace                      |
| Reasoning          | Implicit                    | Explicit orchestration policy                   |
| Safety             | Mixed with reasoning        | Separated into dedicated guardrails             |

---

## Repository Purpose
* Organize artifacts by design phase
* Capture structured specifications (not just prompts)
* Enable collaboration between SMEs, developers, and helper agents
* Track evolution of agent design and evaluation

Focus: **design artifacts, not runtime code**

---

## CARE V2 Phases
### Phase 1: Scope *(Unchanged)*
Defines:
* Problem
* Users
* Workflows
* Constraints
* Success criteria

---

### Phase 2: Key Information Elicitation *(Major Redesign)*

#### Phase 2.1: Existing Systems & Data Inventory
* Tools, APIs, datasets
* Schemas, permissions, constraints
* Error patterns

**Output:** Descriptive system inventory

---

#### Phase 2.2: Context Workspace Design *(Core Shift)*
Defines the agent’s **knowledge environment**:
* Context files (domain, workflows, policy, examples)
* Hierarchy (global vs task-specific)
* Retrieval triggers
* Authority rules

**Output:**
* Context structure
* Trigger → Context mappings

---

#### Phase 2.3: MCP Tool Design *(New)*
Designs tools as:

* Execution + validation systems
* Instruction providers (next_action, hints, recovery)

**Key principle:**

> Tools compute and guide — not just return data

---

#### Phase 2.4: Output Format Design *(Mostly Unchanged)*

Defines:
* Output structure
* Intermediate steps
* Failure handling
* Tool vs context transparency

---

### Phase 3: Reasoning Policy & Guardrails
#### Phase 3.1: Reasoning Strategy *(Major Update)*

Defines:

* How context is retrieved and used
* How tools are invoked
* Error handling and retries
* Conflict resolution

**Key addition:**
Context retrieval is now part of reasoning.

---

#### Phase 3.2: Policy & Guardrails *(Refined)*

Defines:

* Safety rules
* Prohibitions
* Escalation conditions
* Risk boundaries

**Separation introduced:**

* Phase 2 → where policy lives
* Phase 3 → what policy is

---

### Phase 4: Prompt Architecture *(Same Role, Better Inputs)*

* Converts artifacts into implementation
* Prompts become **execution wiring only**

---

### Phase 5: Benchmarking & Verification *(Unchanged)*

* Evaluation datasets
* Scoring criteria
* Pass/fail validation

---

## Repository Structure

```text
AKD-CARE/
├── phase_1_scope/
├── phase_2_key_information_elicitation/
│   ├── 2_1_system_inventory/
│   ├── 2_2_context_workspace/
│   ├── 2_3_tool_design/
│   └── 2_4_output_format/
├── phase_3_reasoning_and_guardrails/
│   ├── 3_1_reasoning_strategy/
│   └── 3_2_policy_guardrails/
├── phase_4_prompt_architecture/
├── phase_5_benchmarking/
├── examples/
├── docs/
└── changelog.md
```

---

## Core Principles (CARE V2)

* **Separate knowledge from execution**
* **Retrieve context just-in-time**
* **Push computation and validation into tools**
* **Make reasoning explicit and reviewable**
* **Keep prompts minimal and maintainable**

