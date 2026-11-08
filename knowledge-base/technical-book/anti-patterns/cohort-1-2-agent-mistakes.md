---
title: "Cohort 1 & 2 — Agent Practice Mistakes"
description: "Agent engineering mistakes and configuration failures — MUST AVOID"
weight: 2
---

# Cohort 1 & 2 — Agent Engineering Mistakes

Complementary to [Common Mistakes](common-mistakes.md) (code quality). This section catalogs specific **agent engineering anti-patterns** involving prompts, evals, guardrails, and tool configuration.

## 1. Hardcoded Absolute Machine Paths (Team 005)

```json
// ❌ Breaks when teammates clone to different directory paths
"command": "python /Users/developer/A20-App-005/scripts/log_hook.py"
```

```json
// ✅ Use repository-relative paths
"command": "bash scripts/_pyrun.sh scripts/log_hook.py --tool=claude"
```

## 2. Disabling Hooks via `.bak` Renaming (Team 007)

Renaming `.claude/settings.json.bak` disables telemetry and safety hooks without tracking reasons. If temporarily disabling hooks, document the rationale in comments rather than hiding configuration files.

## 3. Disconnected Stub Files Causing Confusion (Teams 005, 006, 008)

Leaving a generic boilerplate `src/agent.py` ("You are a helpful assistant") when active logic lives in `src/retrieval/agent.py` misleads AI tools exploring the codebase.

→ Delete unused stubs or clearly mark them `# DEPRECATED — Canonical implementation in src/...`.

## 4. Silent Error Fallback (Team 002)

```python
# ❌ Masks regressions in automated test loops
except Exception:
    logger.exception("...")
    return default_answer
```

Always log the failure and return an explicit error state (`status: "FAILED"`).

## 5. Redundant Multi-Folder Workflow Duplication (Team 008)

Duplicating the same prompt file across `.claude/commands/`, `.codex/skills/`, and `.github/prompts/` creates maintenance drift. Maintain one canonical source and reference it.

## 6. Absent Evaluation Suites (10 of 12 Teams)

Leaving `eval/results/` empty results in severe deductions in Evaluation Evidence. Adopt structured evaluation suites (golden datasets + automated runners).

## 7. Single-Layer Prompt Guardrails (11 of 12 Teams)

Prompt-only safeguards are vulnerable to jailbreaks. Enforce defence-in-depth with deterministic code checks.

## 8. Overly Permissive Execution Permissions (Team 002)

Auto-allowing blanket shell commands (`rm`, `git push --force`) creates severe risk of data loss. Enforce explicit permission deny lists.

## 9. Missing Citation Contracts (9 of 12 Teams)

Agents outputting claims without provenance citations prevent users from verifying correctness. Enforce strict `[cite:chunk_id]` contracts.

## 10. Stale Documentation Drift (9 of 12 Teams)

When architecture evolves from Node/Gemini to FastAPI/OpenAI without updating docs, agents ingest contradictory context and generate broken code. Maintain a "Known Ambiguities" log in `PROJECT_CONTEXT.md`.
