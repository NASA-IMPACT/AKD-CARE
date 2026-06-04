# guardrails_risk_taxonomy_reference.md

## Purpose
This artifact provides a reference to the RiskAgent taxonomy used for automated guardrail detection.

The full taxonomy is defined in:

`<repo_path>/risk_taxonomy.yaml`

The taxonomy is intentionally not included in this artifact to avoid exceeding LLM context limits.

## Taxonomy Structure
Each risk entry contains:

- id
- description
- concern

Example structure:

```yaml
risks:
- id: ...
  description: ...
  concern: ...
```

## Risk IDs:

- compliance
- privacy
- maliciousness
- profanity
- toxicity
- out-of-distribution-checks
- jailbreak-prevention
- fairness
- consistency
- uncertainty-identification
- verification
- ip-and-copyright
- societal-impact
- hallucination-identification
- attribution
- static-knowledge
- outdated-confidence
- overgeneralization
- multidisciplinary-failure
- lack-of-adaptive-reasoning
- positivity-bias

## RiskAgent Behavior
RiskAgent evaluates generated content using a selected list of risk IDs.

Signature:

RiskAgent(generated_content: str, risk_ids: List[str]) → assessments

## Phase 3.2 Responsibilities
During the Phase 3.2 interview:

- SMEs must select which risk IDs from the taxonomy should be actively monitored.
- The interviewer must not invent new risk IDs.
- The interviewer must not reproduce the full taxonomy.

Only SME-approved risk IDs should appear in the Phase 3.2 Guardrail Enforcement Matrix.

## Guardrail Composition (Current)
input_guardrail = GraniteGuardianTool() >> RiskAgent()
output_guardrail = RiskAgent()
