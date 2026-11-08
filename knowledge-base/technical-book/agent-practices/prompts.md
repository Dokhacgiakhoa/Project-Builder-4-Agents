---
title: "Prompt Engineering"
description: "Structured XML prompts, SAFEGUARDS, citation contracts — lessons from cohorts 1 & 2"
weight: 1
---

# Prompt Engineering

## Cohort Lessons

3 of 12 teams (002 DevCoach, 004 MeeA, 007 Activation Engine) structured prompts using explicit XML tags → producing consistent outputs that were easy to debug. Teams relying on generic 1-2 line prompts suffered frequent model drift and lost evaluation points.

## Pattern 1: Structured XML Tags

**Bad** (Common in low-scoring projects):
```text
You are a helpful assistant. Answer the user's question.
```

**Good** (Teams 002, 004):
```xml
<role>
You are the AI20K Agent — an accurate, grounded assistant.
</role>

<context>
You receive Context from the knowledge base via RAG. Always prioritize Context over internal parametric memory.
</context>

<instructions>
1. Inspect Context first.
2. Accompany every domain assertion with [cite:chunk_id].
3. Adhere strictly to the JSON schema.
</instructions>

<rules>
- Do not speculate when evidence is absent.
- Ensure clear, concise phrasing.
</rules>

<output_format>
{ "verdict": "...", "answer": "...", "citation_ids": [...] }
</output_format>

<verification>
Prior to emitting output, self-verify: Are all cited chunk IDs present in context? Is the verdict consistent with retrieved evidence?
</verification>
```

Why it works: Isolated XML tags assign clear semantic roles to prompt sections. The `<verification>` tag prompts the model to self-evaluate before generating output, significantly reducing hallucinations.

## Pattern 2: Isolated SAFEGUARDS Blocks (Team 005 NestAI)

Do not mix safety constraints into conversational personality directives. Maintain a dedicated section:

```text
<safeguards>
EMERGENCY: If the user indicates life-threatening or dangerous symptoms,
emit an immediate RED ALERT and decline general conversational advice.
Never speculate on medication dosages or critical treatments.
</safeguards>
```

## Pattern 3: External Prompt Templates (Team 004 MeeA)

Store prompts in `prompts/*.md` using `{{placeholder}}` variables rather than hardcoded Python strings:

```markdown
<role>...</role>
<context>{{context}}</context>
```

Loader (`src/agents/prompts.py`): Decorate with `@lru_cache` and apply `str.replace`. Benefits: prompts can be tuned without modifying or redeploying code; mentors can review prompts directly; git diffs remain clean.

## Pattern 4: Centralized SHARED_RULES (Team 002)

Define cross-cutting directives (response constraints, output brevity, citation rules) as a single shared constant and inject it across multiple prompt templates to stay DRY.

## Anti-Patterns to Avoid

- Generic "Be helpful" directives → replace with explicit output schemas.
- "Don't hallucinate" → "Cite only from chunks listed under Context; declare uncertainty if evidence is absent".
- Hardcoded business data in prompts → isolate volatile data into external reference files or retrieval indexes.

## Template References

Reference `prompts/system_prompt.md`, `safeguards.md`, and `citation_rules.md` in `ai20k-agent-template`.
