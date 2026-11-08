# ADR 0016: WORK LOG STANDARD AND HEALTH CHECK FINDINGS

* **Status**: Accepted
* **Date**: 2026-11-07
* **Builds on**: [ADR-0012](0012-agent-first-builder-and-health-check.md), [ADR-0015](0015-staged-feature-workflow-with-verification-gates.md)

---

## 1. Context

* An Agent session starts without memory. The kit had ADRs (decisions), specs (plans) and git history (diffs), but no place for working state between sessions: what was done, what was verified, what is left.
* Health Check had no check for it. A review on 2026-11-07 confirmed no `worklog` handling in `scripts/auditor_engine`.

## 2. Decision

* Add Core standard `S-009` (`core/standards/worklog.md`) and a template `docs/worklog.md`; add Working Rule 12 to the project `AGENTS.md` template.
* Health Check emits `WLOG-001` (Medium: no work log in the accepted locations) and `WLOG-002` (Low: a work log without any dated entry). Both findings carry remediation docs `S-009` (and `S-003` for `WLOG-001`).
* The check does **not** change the score and is **not** part of Core Baseline B1-B9, so existing scores and the "9 baseline items" contract stay unchanged.

## 3. Consequences

* Projects scaffolded from the kit get a work log by default; older projects get a Medium finding with a fix path.
* Not checked: whether entries are accurate or recent. Freshness is skipped because file times change on `git clone`; a git-aware check would need `git` at runtime and is deferred.
* The false-positive rate on real repositories is unmeasured. A repo that keeps its work log under another name (for example `TASKS.md`) is flagged `WLOG-001` until it adds a work log or the accepted locations are extended.
