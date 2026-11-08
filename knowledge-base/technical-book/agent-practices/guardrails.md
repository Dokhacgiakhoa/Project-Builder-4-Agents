---
title: "Guardrails & Anti-Hallucination"
description: "Defence-in-depth, verbatim citations, conservative bias — cohorts 1 & 2"
weight: 3
---

# Guardrails & Anti-Hallucination

## Cohort Lessons

Relying solely on prompt-based safeguards is risky — LLMs can be manipulated through prompt injections or jailbreaks. Team 005 (NestAI) enforced guardrails at **both the prompt AND deterministic code layers**, establishing robust defense-in-depth. Team 012 (ARAS) instituted a "verbatim is sacred" rule to prevent statistical hallucinations in academic metrics.

## Pattern 1: Defence-in-Depth (Team 005 NestAI)

Two independent protective layers:

**Layer 1 — Prompt Safeguard** (`prompts/safeguards.md`):
```text
<safeguards>
EMERGENCY: Immediate danger indicators → trigger red alert, decline general advice.
</safeguards>
```

**Layer 2 — Code Gate** (`nodes/safety_node.py`): Evaluate `DANGER_KEYWORDS` BEFORE invoking the LLM:
```python
DANGER_KEYWORDS = ("bleeding", "dyspnea", "self-harm", "overdose", ...)
if any(kw in query.lower() for kw in DANGER_KEYWORDS):
    return {"bypass": True, "response": DANGER_RESPONSE}
```

If a prompt injection bypasses the prompt layer, the deterministic code layer still intercepts the request. This pattern is essential for high-stakes healthcare, legal, or financial applications.

## Pattern 2: Verbatim is Sacred (Team 012 ARAS)

When an agent cites retrieved data or statistics:
```text
- NEVER round numeric figures.
- NEVER paraphrase domain equations or legal citations.
- NEVER convert units arbitrarily.
- Excerpt verbatim from canonical source chunks.
```
Rounding academic or financial figures constitutes synthetic fabrication and triggers compliance violations.

## Pattern 3: Conservative Bias (Team 012)

When evidence is ambiguous or incomplete, default to `verdict: "uncertain"` rather than asserting `verdict: "supported"`:
```text
Declaring insufficient evidence is always preferred over speculative synthesis.
```

Schema enforcement (`models/schemas.py`):
```python
class AgentAnswer(BaseModel):
    verdict: Literal["supported", "partially_supported", "unsupported", "uncertain"]
    confidence: float = Field(ge=0.0, le=1.0)
    citation_ids: list[str]

    def is_safe(self) -> bool:
        if self.verdict != "uncertain" and not self.citation_ids:
            return False  # Asserting an answer without citation is rejected as unsafe
        return True
```

## Pattern 4: Strict Output Schema Locking (Teams 009, 012)

Do not rely solely on prompting for JSON output. Validate outputs in code using Pydantic schemas. Enforce double validation: prompt contract + runtime schema parsing.

## Pattern 5: Source Code Authoritative Principle (Team 011)

Governing rule for coding agents:
```text
When documentation conflicts with executable code, the CODEBASE IS AUTHORITATIVE.
Log documentation drift under PROJECT_CONTEXT Known Ambiguities; do not rewrite docs based on guesses.
```

## Anti-Pattern: Silent Fallback (Team 002 Root Cause)

```python
# ❌ Silent fallback masks runtime regressions
try:
    result = await llm()
except Exception:
    return default_answer  # Regressions go undetected in automated pipelines
```

```python
# ✅ Explicit error logging and telemetry tagging
except Exception as e:
    logger.exception("LLM invocation failed")
    return {"error": str(e), "quality_result": {"status": "FAILED"}}
```
