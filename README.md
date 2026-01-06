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
