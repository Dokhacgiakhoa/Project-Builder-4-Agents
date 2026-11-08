# ADR-0018: Project analysis model and offline Knowledge Pack

- Status: Accepted (2026-11-07)
- Supersedes the positioning of ADR-0012 for the Health Check: it stops being only a rule-based file checker.

## Context
Health Check scored projects by checking whether files or folders exist. Measured defects (this repo scanned by itself):
- Languages came from manifest files, so a Python tool repo with one `.csproj` was reported as C# / ASP.NET Core.
- Sample code (`examples/`, `profiles/*/starter/`) switched on whole pillars (false Frontend 20/20).
- Architecture came from folder names only; no import was ever read.
- Remediation only printed static links to kit docs; kit content was never compared with the project.
- "AI Deep Review" received scores and gaps, never code or structure, so it paraphrased rule output.

## Decision
The scan flow becomes: **Scan → Project Model → match Knowledge Pack → Insights → report → (optional) AI Deep Review**.

1. **Project Model** (`auditor_engine/analysis.py`, pure stdlib): languages by source lines, frameworks from real imports plus declared dependencies, component graph from imports (Python, JS/TS, C#, Java/Kotlin, Go), cycles, layer direction, hotspots, test ratio, project kind. Every statement carries evidence (file, count).
2. **Knowledge Pack** (`auditor_engine/knowledge_pack.json`): versioned snapshot of `INDEX.md` rows and the decision/constraint sections of kit docs. Bundled with the engine so offline and air-gapped use work. `knowledge.update_pack()` may refresh it from GitHub when online; the report states the pack version used.
3. **Insights** (`auditor_engine/insights.py`): compare the Project Model with the pack (profile `when` / `not_when`, constraints, common mistakes), emit strengths, bottlenecks and recommendations with evidence and doc ids. Template-based, no model call.
4. **AI Deep Review** stays a separate, online, opt-in layer. It receives the Project Model and Insights (never only scores). Code excerpts are sent only with explicit consent and with secrets masked.
5. Rule scores remain but are labelled as a secondary indicator.

## Consequences
- The engine can state what a project is and why a recommendation applies, offline.
- Heuristic limits are explicit: import graphs are static, dynamic imports and reflection are invisible; confidence is reported.
- The pack must be rebuilt (`scripts/build_knowledge_pack.py`, run by `sync_docs.py`) whenever kit docs change; tests fail if the pack drifts.
- Measuring accuracy on a corpus of real projects is delegated to `evals/` (see handoff brief).

## Evidence that would disprove the value
If, on a corpus of real vibe-coder projects, the inferred language/stack/architecture disagrees with human labels in more than ~20% of cases, or users ignore the insights, the analysis layer is not worth its complexity.
