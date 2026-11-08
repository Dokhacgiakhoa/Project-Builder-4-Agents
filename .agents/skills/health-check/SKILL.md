---
name: health-check
description: Use when the user asks about project health, before opening PRs, after major milestones, or when project-review.md is generated. Runs Project Builder Analytics, reads report, consults remediation docs, and fixes issues by severity.
---

# Project Builder Analytics Protocol

1. If no fresh report exists: run Project Builder Analytics on the workspace (`Project-Builder-Analytics.exe`, or `python scripts/project_auditor.py <target_dir>` from Project-Builder-4-Agents). Output: `project-review.md` at project root.
2. Read `project-review.md`: prioritize findings in order of **High $\rightarrow$ Medium $\rightarrow$ Low**.
3. For each finding, open the **remediation doc** listed beside it (in kit; use `kit-consult` skill if needed).
4. Apply the recommended fix, run verification commands in `AGENTS.md`, and re-run Project Builder Analytics to verify improved score.
5. Record unfixed findings in `planning/backlog.md` with explicit justification.
