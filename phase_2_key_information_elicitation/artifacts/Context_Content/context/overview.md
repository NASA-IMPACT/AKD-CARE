# Context Workspace Overview

## Purpose
This workspace defines the knowledge environment for an Earth-science dataset discovery agent.

The agent supports:
- Mapping science questions → variables → datasets
- Discovering datasets via NASA CMR
- Assisting dataset evaluation and comparison

## Key Principles
- Human remains in control of final scientific judgment
- Agent assists discovery, not decision authority
- Context is minimal and trigger-based (not preloaded)

## System Role of CMR
- CMR is the canonical dataset discovery layer
- Provides metadata, not scientific validation
- Ranking is not sufficient for scientific suitability

## Context Design Philosophy
- Minimal default context
- On-demand loading via triggers
- Clear precedence rules
- Separation of:
  - scientific validity
  - reusable knowledge
  - local evidence
  - user preferences
