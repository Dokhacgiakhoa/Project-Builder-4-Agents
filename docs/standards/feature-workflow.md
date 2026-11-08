---
id: S-008
type: playbook
when: "Starting a non-trivial feature: staged spec -> clarify -> plan/tasks -> analyze -> implement-until-converged workflow with verification gates"
---
# FEATURE WORKFLOW — STAGED SPEC-DRIVEN DELIVERY WITH GATES

> For AI Agents. Adapts the strong parts of staged spec-driven toolchains (clarify, cross-artifact analysis, converge loop) aiming to avoid their overhead (untested). Deliverable size must match change size: **never write more spec than the change needs**.

## 1. Scale Gate (decide first, tell the user in one line)
| Size | Trigger | Path |
| :-- | :-- | :-- |
| Tiny | 1-2 files, no contract change, obvious behavior | Skip workflow. Tests + verification commands only. |
| Standard | New feature or behavior change inside existing modules | Specify -> Plan (with tasks) -> Implement/Converge -> Close |
| Large | New module, contract change (API, DB schema, routes), multi-session work | Full path: add Clarify, separate `tasks.md`, Analyze |

If unsure, choose Standard. Spec longer than the diff means you chose too high a tier.

## 2. Artifacts
One folder per feature: `specs/features/NNN-slug/` containing `spec.md`, `plan.md` (tasks included; `tasks.md` only for Large). Templates: `specs/features/feature-spec.md`, `specs/features/feature-plan.md`. The spec is the **source of truth**; code follows it, never the reverse.

## 3. Stages and Gates
1. **Specify** — user-visible *what* and *why* only; no stack, libraries, or file names. Write numbered acceptance scenarios (`AS-1`, Given/When/Then) with measurable outcomes. For every unknown write `[NEEDS CLARIFICATION: question]`; never guess a requirement.
2. **Clarify** (Large, or any spec with markers) — ask the user at most 3 questions per turn (see `core/discovery.md`). Record answers under the spec's *Decisions* section and remove the marker. **Gate: zero markers before planning.**
3. **Plan** — technical approach referencing `adrs/` and the active architecture profile; affected files; risks. Contract change -> draft an ADR and stop for user approval. Then list tasks: ordered, each citing the `AS-n` it satisfies, tests first, `[P]` on tasks safe to run in parallel.
4. **Analyze** (Large; Standard when the plan touched >5 files) — read-only pass before coding. Verify: every `AS-n` has >=1 task and a test; every task maps to an `AS-n`; no plan item contradicts `AGENTS.md` rules or ADRs; no markers remain. **Fix artifacts, never code, in this stage.** Report gaps in a short table.
5. **Implement and Converge** — execute tasks in order; after each batch run the verification commands in `AGENTS.md` Section 2. Loop until every `AS-n` has a passing test and the Definition of Done holds (`docs/standards/definition-of-done.md`). Each loop obeys the 2-attempt circuit breaker: second failure on the same issue -> stop, diagnose root cause, ask the user.
6. **Close** — tick each `AS-n` with evidence (test name or command output), run `python scripts/sync_docs.py` and the Health Check, report in the user's language: done, verification result, next step.

## 4. Spec Change Protocol (prevents spec/code drift)
Behavior must change mid-implementation -> edit `spec.md` first, add a dated line under *Decisions*, re-run Analyze if tasks changed, then edit code. Never let code silently diverge from the spec.

## 5. Common Mistakes
* Putting stack or file paths in `spec.md` (belongs in `plan.md`).
* Marking Done without a passing test per `AS-n`.
* Running the Large path for a Tiny change.
* Resolving ambiguity by assumption instead of a marker and a question.
* Editing code first, then rewriting the spec to match.
