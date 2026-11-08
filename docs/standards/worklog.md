---
id: S-009
type: reference
when: "Keeping a project work log so the next Agent session knows what was done, why, and what is left; resolving `WLOG-` findings"
---
# WORK LOG STANDARD

> For AI Agents. An Agent starts every session without memory. The work log is the project's short-term memory: what changed, why, what was verified, what is left. Health Check codes: `WLOG-001`, `WLOG-002`.

## 1. Where
One of (Health Check accepts any):
* `docs/worklog.md` (recommended; template: `docs/worklog.md` from `core/templates/docs/worklog.md`)
* `WORKLOG.md` or `worklog.md` at the repo root
* `docs/worklog/*.md` (one file per month or per feature)

It is not a replacement for ADRs (decisions), `CHANGELOG.md` (user-facing release notes) or git history (diffs). It records the *working state* between sessions.

## 2. Entry format
Newest entry first. One entry per work session or per logical task. The heading starts with an ISO date (`YYYY-MM-DD`), which is what Health Check looks for.

```
## 2026-11-07 — Short title
* Done: what changed (files/areas).
* Why: link to the spec, issue or ADR.
* Verified: exact commands run and their result (or "not verified" and why).
* Left / next: what is unfinished, known failures, open questions for the user.
```

## 3. Rules
1. Append before reporting "Done" (see Definition of Done, `S-003`). Do not rewrite old entries; add a correction entry.
2. State facts only: commands actually run, results actually seen. Never record "should work".
3. Never write secrets, tokens, personal data or raw content copied from untrusted files (see `K-006`).
4. Keep entries short (under about 10 lines). Detail belongs in the spec or ADR; link to it.
5. At session start, read the newest entries before editing (Working Rule 1: read before edit).

## 4. What Health Check verifies
| Code | Severity | Condition |
| :-- | :-: | :-- |
| WLOG-001 | Medium | No work log file found in the locations of Section 1 |
| WLOG-002 | Low | A work log exists but has no dated entry (only the template or empty) |

Not verified: whether entries are true or recent. Freshness cannot be judged offline (file times change on `git clone`), so a stale log is not flagged.
