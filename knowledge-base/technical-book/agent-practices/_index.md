---
title: "Agent Engineering Practices"
description: "Best practices from Cohorts 1 & 2 — prompts, evals, guardrails, multi-tool config"
weight: 7
---

# Agent Engineering Practices — Lessons from 12 Cohort Teams

This section consolidates **engineering practices** extracted from analyzing 12 repositories from Cohorts 1 & 2. These patterns ensure teams excel across AI Agent robustness, Code Quality, and Evaluation Evidence.

> Each practice provides **cohort evidence** ("X/12 teams implemented this") alongside **before/after comparisons** to explain the architectural rationale, not merely the mechanics.

> 📄 **Cohort Synthesis Report** (templates + guidebook + anti-patterns + inspiration map): [Cohort 3 Synthesis Report](https://github.com/hailoc12/ai20k-agent-template/blob/main/docs/COHORT3_REPORT.md).

## Subsections

- [Prompt Engineering](prompts.md) — XML structure, SAFEGUARDS, citation, external files
- [Evaluation Framework](evals.md) — golden dataset, runner, LLM-as-Judge, cost benchmark
- [Guardrails & Anti-Hallucination](guardrails.md) — defence-in-depth, verbatim sacred
- [Context Management](context-management.md) — PROJECT_CONTEXT, handoff, ADR
- [Multi-Tool Config](multi-tool-config.md) — .claude/.codex/.gemini mirror, permissions

## Quick Overview

| Pattern | High Performing Teams | Common Omissions | Risk of Omission |
|---|---|---|---|
| Structured XML prompt | 002, 004, 007 | Majority | Unstable outputs, difficult debugging |
| Eval framework | 002, 008, 009, 011 | 10/12 | Deduction in Evaluation Evidence |
| Defence-in-depth guardrail | 005, 007 | 11/12 | Safeguard jailbreak bypass |
| PROJECT_CONTEXT | 001, 008, 011 | 9/12 | Agent drift, stale doc hallucinations |
| Citation contract | 006, 009, 012 | 9/12 | Users cannot verify source provenance |

Read sequentially. Each section requires ~5-10 minutes.\n