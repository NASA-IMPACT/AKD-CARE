# AKD-CARE

**Collaborative Agent Reasoning Engineering** (CARE) is a disciplined, stage-gated methodology for systematically engineering AI agents in scientific and technical workflows. Influenced by the vision of Accelerated Knowledge Discovery (AKD), CARE moves away from ad hoc prompt tinkering toward a structured engineering process built around reusable design artifacts and human-in-the-loop oversight.

---

## Why CARE?

Building reliable LLM agents for domain-sensitive workflows requires more than iterative prompting. CARE treats agent development as an engineering discipline — one that demands explicit specifications, staged design reviews, and grounded evaluation against realistic benchmarks. The goal is agent behavior that is **repeatable, reviewable, and maintainable** over time.

---

## The Triadic Collaboration Model

CARE is defined by a three-party workflow that balances scientific integrity with technical feasibility:

<p align="center">
  <img width="1024" height="559" src="https://github.com/NASA-IMPACT/akd-care/blob/ada34b52b420aaf6e2e95fa5b2496a9b62608966/3-Party.png?raw=true" />
</p>
  
| Role | Responsibility |
|---|---|
| **Subject Matter Experts (SMEs)** | Provide domain authority, surface nuanced constraints, and validate scientific correctness |
| **Developers** | Act as implementation authority, ensuring tool realism and feasibility |
| **Helper LLM Agents** | Serve as facilitation infrastructure — asking phase-aligned questions, drafting Markdown specifications, and proposing revisions for human approval |

Each phase requires joint approval at a stage gate before work proceeds. No phase is skipped.

---

## Five Phases of Development

CARE is organized into five distinct phases, each producing concrete artifacts that feed into the next:

### Phase 1 — Scope & Decompose
Define the target workflow, intended users, system boundaries, and constraints. This phase answers: *What is this agent for, and what is it explicitly not for?*

### Phase 2 — Key Information Elicitation
Capture everything the agent needs to know: the systems it interacts with, authoritative domain context, available tools, and expected output formats. This phase is subdivided into:

- `2_1_system_inventory` — catalogue of relevant systems and data sources
- `2_2_context_workspace` — domain knowledge, references, and grounding material
- `2_3_tool_design` — tool specifications, inputs/outputs, and error behavior
- `2_4_output_format` — structured definitions of expected agent outputs

### Phase 3 — Reasoning Policy & Guardrails
Codify how the agent should think. This phase translates expert reasoning patterns into explicit policies and defines safety boundaries for uncertainty, ambiguity, and tool failures. Subdivided into:

- `3_1_reasoning_strategy` — task decomposition logic, uncertainty handling, and decision heuristics
- `3_2_policy_guardrails` — failure modes, escalation behavior, and out-of-scope boundaries

### Phase 4 — Prompt Architecture
Translate approved design artifacts into structured prompts and tool-routing logic using established design patterns. This is where specifications become an engineered agent.

### Phase 5 — Benchmarking & Verification
Define realistic query sets and scoring rubrics. Establish baselines and track regressions over time. Evaluation is grounded in user-centric success criteria on complex, representative tasks — not curated demos.

---

## Four Key Design Targets

CARE deconstructs agent quality into four interacting targets, designed to surface "silent failures" where outputs appear plausible but violate domain constraints or provenance expectations:

| Target | Description |
|---|---|
| **Interaction Policy** | How the agent decomposes tasks and manages uncertainty |
| **Domain Grounding** | Defines authoritative knowledge boundaries to reduce plausible-but-wrong outputs |
| **Tool Orchestration** | Specifies which tools to use, in what order, and how to handle errors or retries |
| **Evaluation & Verification** | Defines user-centric success criteria on realistic, complex tasks |

---

## Repository Structure

This repository is the single source of truth for CARE artifacts, prompts, and evaluation materials across all design phases.

```
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

The focus of this repository is **documentation and design artifacts**, not runtime code.

---

## Changelog

### v2.0.0
Restructured the repository to better reflect the internal complexity of Phases 2 and 3. Both phases are now subdivided into dedicated sub-directories, making artifact ownership clearer and enabling more granular review at each stage gate.

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

## Core Principles (CARE V2)
* **Separate knowledge from execution**
* **Retrieve context just-in-time**
* **Push computation and validation into tools**
* **Make reasoning explicit and reviewable**
* **Keep prompts minimal and maintainable**

## Citation

If you use CARE or this repository in your work, please cite:

> Ramachandran, R., Jha, N., & Ramasubramanian, M. (2026). *Collaborative Agent Reasoning Engineering (CARE): A Structured Three-Party Design Methodology for Systematically Engineering AI Agents with SMEs, Developers, and Helper Agents* (Technical Memorandum). National Aeronautics and Space Administration. <https://doi.org/10.64631/TAXQ7736>

### BibTeX

```bibtex
@techreport{ramachandran2026care,
  title       = {Collaborative Agent Reasoning Engineering (CARE): A Structured Three-Party Design Methodology for Systematically Engineering AI Agents with SMEs, Developers, and Helper Agents},
  author      = {Ramachandran, Rahul and Jha, Nidhi and Ramasubramanian, Muthukumaran},
  institution = {National Aeronautics and Space Administration},
  type        = {Technical Memorandum},
  year        = {2026},
  doi         = {10.64631/TAXQ7736},
  url         = {https://doi.org/10.64631/TAXQ7736}
}
```

---

## License

This project is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for the full text, or <http://www.apache.org/licenses/LICENSE-2.0>.

```text
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
```

---

## Disclaimer

This material is based upon work supported by the National Aeronautics and Space Administration under Contract No. `80MSFC22M0004`. Any opinions, findings, conclusions, or recommendations expressed in this repository are those of the authors and do not necessarily reflect the views of NASA or the United States Government.

The software and associated artifacts in this repository are provided "AS IS", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability arising from the use of this material.

Use of this repository does not imply endorsement by NASA, the U.S. Government, the University of Alabama in Huntsville, or any other affiliated institution.
