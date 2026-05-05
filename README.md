# AKD-CARE
AKD-CARE is a structured repository for documenting and applying the **CARE (Collaborative Agent Reasoning Engineering)** methodology for designing reliable, domain-grounded LLM agents.

CARE treats agent development as an **engineering discipline**, emphasizing explicit artifacts, staged design, and joint review by subject-matter experts (SMEs), developers, and LLM-based helper agents.

This repository serves as a **single source of truth** for CARE artifacts, prompts, and evaluation materials across all design stages.

## What is CARE?
CARE (Collaborative Agent Reasoning Engineering) is a staged, artifact-driven methodology for engineering LLM agents that are:
- Explicitly specified rather than prompt-tuned by trial and error
- Grounded in authoritative domain context
- Designed with clear reasoning policies and guardrails
- Evaluated using realistic benchmarks instead of demos
The methodology emphasizes **repeatability, reviewability, and maintainability** of agent behavior over time.

---

## Repository Purpose

This repository is intended to:

- Organize CARE artifacts by design phase
- Capture prompts, specifications, and outputs in a reviewable format
- Support collaboration between SMEs, developers, and helper agents
- Track design evolution and evaluation results over time

The focus is on **documentation and design artifacts**, not on runtime code.

---

## CARE Phases

The repository is organized into **five CARE phases**, each corresponding to a distinct stage of agent design:

### **Phase 1: Scope and Decompose**
Define the agent’s purpose, intended users, workflow boundaries, and constraints.

### **Phase 2: Key Information Elicitation**
Document tools, authoritative domain context, and expected output formats.

### **Phase 3: Reasoning Policy and Guardrails**
Specify reasoning strategies, verification behavior, failure modes, and guardrails.

### **Phase 4: Prompt Architecture and Tool Orchestration**
Translate design artifacts into structured prompts and tool-routing logic.

### **Phase 5: Benchmarking**
Define evaluation queries, scoring rubrics, and verification results.

---

## Repository Structure

```text
AKD-CARE/
├── phase_1_scope_and_decompose/
├── phase_2_key_information_elicitation/
├── phase_3_reasoning_policy_and_guardrails/
├── phase_4_prompt_architecture_and_tool_orchestration/
├── phase_5_benchmarking/
├── examples/
├── docs/
└── changelog.md
```

---

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
