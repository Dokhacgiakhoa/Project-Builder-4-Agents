# TASKS — PLAN TO COMPLETE PROJECT-BUILDER-4-AGENTS

> Task tracker of the **kit maintainer** (not a document for the Agent of a user's project). Update the *Status* column as you work; add new tasks at the end of the matching group.
> Last updated: 2026-11-06 · Current baseline: 54 tests pass locally; Project Health Check v2.2.0 fully synchronized (Engine + Web/Desktop UI + `.exe`). The product is now called Project Builder Analytics.

**Status**: `TODO` not started · `DOING` in progress · `REVIEW` awaiting maintainer review · `BLOCKED` waiting on other work · `DONE` finished · `DEFERRED` postponed on purpose
**Priority**: `P0` blocks the core value · `P1` needed before real users use it · `P2` should have · `P3` nice to have
**Effort**: `S` ≤ half a day · `M` 1–2 days · `L` > 2 days
**Owner**: `Claude` · `Maintainer` (needs the maintainer's permission/device/decision)

---

## Guiding principles (settled; all work below must follow them)
1. Users are freshers/vibe coders: the Agent must **proactively** pick documents from a description; users should not need to know file names or write prompts.
2. Documents are written **for the Agent**: they contain only **decisions and constraints**, not a re-teaching of technology knowledge the Agent already has.
3. Core is mandatory for every repo; Profiles are customized per project; the Library is consulted only when needed.
4. Analytics is a fixed, offline review step that **helps the Agent spend fewer tokens**; it does not replace the Agent. The report is one `project-review.md` file for both humans and Agents.
5. The safety scan targets only **prompt injection in text files**; it is not an antivirus.
6. There are no "teach the technology" stack profiles (removed).

---

## Roadmap by milestone

| Milestone | Goal | Task groups | Done when |
| :-- | :-- | :-- | :-- |
| 2026-11-07 | **Fix the Frontend false positive 20/20**: the engine mistakenly scanned sample React apps in `examples/` and `profiles/*/starter/`, which turned on `has_frontend`. Added sample zones to `SKIP_REASONS`/`SKIP_REL_PATTERNS` (`constants.py`, `tree.py`) and `tests/test_sample_zone_exclusion.py`. Kit self-scan: Frontend/Database disappeared, Backend 100% -> 70%, the old score was inflated. Not yet re-measured with Antigravity, `evals/` not rebuilt. |
| **M0 — Validation** | Prove that what was written works with real Agents | C, B3 | A project is built from an empty folder with 3 Agents; GitHub CI is green |
| **M1 — Usable** | Real users install and use it without friction | A, B, E1–E3 | A release exists, the exe runs on a clean machine, the repo has been renamed |
| **M2 — Solid** | Reduce false alarms, raise coverage, clean up content | D, E4+, F | The routing eval reaches its threshold; false alarms are measured and acceptable |

Suggested order: **C2 → B3 → B1 → B8 (push) → C1 → B2 → A1 → A2 → A3 → E1 → C3 → the rest**. Reason: C1/C2 validate the biggest assumption (the Agent really reads `BOOTSTRAP.md` and routes correctly); fixing content before packaging the exe avoids rework.

---

## Group C — Validate the core value (Builder with real Agents) · MILESTONE M0

| ID | Task | Priority | Effort | Owner | Depends on | Status |
| :-- | :-- | :-: | :-: | :-- | :-- | :-: |
| C0 | **Write the C1 scenarios and checklist** (`evals/c1-bootstrap-protocol.md`: 3 scenarios, user roles, 16 scoring items, result template) | P0 | S | Claude | — | DONE |
| C0.1 | **Implement ADR-0013 & the Zero-Clone Remote Hub**: MANIFEST.json, llms.txt, HOW_IT_WORKS.md, curated-skills, curated-mcp | P0 | M | Claude | — | DONE |
| C0.2 | **Implement ADR-0014 & English-First Standardization**: translate the whole core/profiles/templates/index skeleton to English to save ~50% of tokens | P0 | M | Claude | — | DONE |
| C0.3 | **Package the Visual Reverse-Engineering Playbook (D-006)**: a Screenshot-to-Code protocol against the UI Doom Loop, integrating the evidence rules (Rules 10 & 11 in AGENTS.md) | P0 | S | Claude | — | DONE |
| C1 | **Run a real BOOTSTRAP trial** with **Claude Code** and **Antigravity** (Codex not verified): S1 empty folder, S2 half-finished project, S3 complex project. Run in a fresh session with no context. Use the URL after B1 + push; before that, use a local-path variant | P0 | M | Claude (new session) + Maintainer (Antigravity, and Claude Code if desired) | C0; the URL needs B1 + B8 | TODO |
| C2 | **Verify the Agent configuration formats** against official documentation: `AGENTS.md`, the import in `CLAUDE.md`, skills paths (`.agents/skills`, `.claude/skills`), Antigravity rules/workflows (the global path still conflicts between sources). Fix `BOOTSTRAP.md` step 1.3 according to the result | P0 | S | Claude | — | DONE |
| C3 | **Routing eval set**: 20 project descriptions from non-experts → expectation (profile, guardrail level, documents consulted). Run with each Agent and measure the share of correct choices | P1 | M | Claude writes, Maintainer runs | C1 | TODO |
| C4 | **Fix content from the C1/C3 results**: where the Agent skipped, misread or over-read; adjust `BOOTSTRAP.md`, `INDEX.md` ("When to use"), `profiles/README.md` | P1 | M | Claude | C1, C3 | BLOCKED |
| C7 | **README states clearly that Codex is not verified** (it currently says "Works with Claude Code · Antigravity · Codex") until someone runs a trial | P2 | S | Claude | — | TODO |
| C5 | **Per-tool adapters**: generate separate rules/workflows for Antigravity and Codex from `AGENTS.md` (one source of truth) once C2 confirms the formats | P2 | M | Claude | C2 | BLOCKED |
| C6 | **A Claude Code plugin/marketplace package** to install without cloning (if C2 confirms a suitable mechanism) | P3 | M | Claude | C2, decision Q3 | DEFERRED |

**Acceptance of C1** (scored with the 16-item checklist in `evals/c1-bootstrap-protocol.md`): for each Agent, from a single sentence ("use <repo URL> to build a project for me, I want to make ..."), the Agent by itself: reads `BOOTSTRAP.md` → builds the Core → interviews with ≤ 3 questions per turn → chooses a profile with reasons → installs guardrails → runs Analytics. The generated project's Analytics score is ≥ 80 and Core Baseline B1–B9 pass.
**Acceptance of C3**: ≥ 85% of the questions choose the right profile; 100% of the questions with a "small/student project" signal are not pushed up to Clean Architecture.

---

## Group B — Repo, CI and kit release · MILESTONE M0/M1

| ID | Task | Priority | Effort | Owner | Depends on | Status |
| :-- | :-- | :-: | :-: | :-- | :-- | :-: |
| B1 | **Rename the GitHub repo** to `Project-Builder-4-Agents` (every link in the documents and code already points to the new name; the local `origin` was changed) | P0 | S | Maintainer | — | DONE |
| B8 | **Push** the commits to GitHub (so far only committed locally; the Agent cannot get the kit by URL until pushed) | P0 | S | Maintainer | B1 | DONE |
| B2 | **Clean up leftover old names**: the `Project-Starter-Kit` URL was replaced; still left are hard-coded machine paths in `scripts/build_brand_assets.py` and `generate_icon.py`, the config folder `~/.starter-kit`, demo URLs in the pitch deck, the package name `ai-native-frontend-starter-kit` | P2 | S | Claude | — | TODO |
| B3 | **Run CI on GitHub for the first time** (matrix Python 3.12/3.14, pytest, eslint/tsc/vitest, `check_links`); fix every error that shows up | P0 | S | Claude (maintainer pushes) | — | DOING |
| B4 | **Tag a version** `v0.1.0` + `CHANGELOG.md`; the sample `kit.json` `kit_ref` pins the tag instead of `main` | P1 | S | Claude | B3 | BLOCKED |
| B5 | **A replacement for `make` on Windows**: write the equivalent commands (`python -m pytest tests -q`, `python scripts/check_links.py`) in the README; check the Makefile on Linux/macOS | P2 | S | Claude | — | TODO |
| B6 | **Protect the `main` branch** (require green CI), enable Dependabot for npm/pip/actions | P2 | S | Maintainer | B3 | TODO |

**Acceptance of B3**: the workflow is green on `main`; `check_links` runs and fails when a link/format is deliberately broken.

---

## Group A — Analytics: packaging and release · MILESTONE M1

| ID | Task | Priority | Effort | Owner | Depends on | Status |
| :-- | :-- | :-: | :-: | :-- | :-- | :-: |
| A1 | **Rebuild the exe** with `python scripts/build_exe.py` (PyInstaller engine + .NET 10 shell). The C# code `MainForm.cs`/`PythonRuntime.cs` **has never been compiled**: fix compile errors if any | P0 | M | Maintainer installs the .NET 10 SDK + PyInstaller, Claude fixes errors | — | DONE |
| A2 | **Try on a clean Windows machine** (Windows Sandbox/VM, no Python): the self-contained exe was verified to run in an environment with a stripped PATH (no Python, no .NET, no PyLauncher); it produces `project-review.md` with Sections 0/7 and the SAFE-001 flag; a mid-run shell CDP reload was verified (engine PID unchanged); a force-killed engine is cleaned up by the 180s watchdog. Still missing: trying a machine without WebView2 | P0 | S | Maintainer | A1 | DONE |
| A3 | **Release the exe through GitHub Releases** (a single exe with the engine embedded, ADR-0022, + `SHA256SUMS`; do not ship `engine/`; the workflow creates the release on a tag) instead of committing binaries to git; remove the old `Project-Health-Check.exe` from the repo, make the README point to the Releases page. **v0.1.0 was released (2026-11-08) with exe SHA-256 `1ab95081…`**: manual UI test OK, G1/G2 pass, README numbers corrected to the measurements (report `evals/results/2026-11-08-release-v0.1.0-verification-016.md`). Not re-run for this build: clean machine, watchdog, reload | P1 | M | Claude (workflow), Maintainer (review) | A2, B4 | DONE |
| A4 | **The web UI shows Sections 0/7**: check that `static/js` and the API return the safety and scope data; if not, add a tab | P1 | M | Claude | — | DONE |
| A5 | **Linux/macOS**: decide whether to package the PyInstaller engine for both platforms, or keep `.sh` + Python 3.12+; fix the "SUCCESS" message that always shows in the shell script when the scan fails | P2 | M | Claude | Q2 | DEFERRED |
| A6 | **Code signing/SmartScreen**: write guidance for users when Windows warns; consider signing once there are real users | P3 | S | Maintainer | A3 | DEFERRED |

**Acceptance of A2**: the exe runs on a machine without Python installed; scanning a 5,000-file repo takes < 30 seconds; no port other than `127.0.0.1` is opened.

---

## Group E — Analytics: engine and report · MILESTONE M1/M2

| ID | Task | Priority | Effort | Owner | Depends on | Status |
| :-- | :-- | :-: | :-: | :-- | :-- | :-: |
| E1 | **Detect `ARCH-008`: missing guardrails** for the M1–M3 level the project declares (no lint/import-boundary rules or project split; CI does not run architecture checks). Add a remediation document + tests | P1 | M | Claude | — | DONE |
| E2 | **Extend `ARCH-007`** (`PROFILE_EXPECTATIONS`) to all 4 profiles, including per-language structures (.NET/Python/TS); add test fixtures | P1 | M | Claude | — | DONE |
| E3 | **Reduce false alarms**: put `examples/`, test fixture folders and `*.min.*`, `*.map` in the skip list with a reason (shown in Section 7) | P1 | S | Claude | — | DONE |
| E4 | **Declare `kit.json` in the report**: record the `kit_ref` in use and warn when it is older than the latest kit version | P2 | S | Claude | B4 | DONE |
| E5 | **A regression test set with sample projects** (empty, bootstrapped, half-finished, with SAFE signals): fixed expected results to keep the promise "same input, same result" | P2 | M | Claude | — | TODO |
| E6 | **Exit code by threshold** (`--fail-under N`) and `--output <path>` for CI | P3 | S | Claude | — | DEFERRED |
| E7 | **Split a long report**: when there are more than N findings, keep a summary table + group by remediation document so the Agent reads fewer tokens | P2 | M | Claude | — | TODO |
| E8 | **A "Library/Framework" archetype model**: add detection in `analysis.py` for pure libraries with no application entry point | P2 | M | Claude | — | TODO |
| E9 | **Speed up scanning large repos**: litellm (~15k files) currently takes ~35s single-threaded; research multithreading or lazy regex in the pillars | P2 | M | Claude | — | TODO |
| E10 | **Cold-start cost on an HDD**: 4,000 files take ~30s of physical reading the first time; evaluate a pre-warm solution or a drive-type indicator | P3 | S | Claude | — | TODO |

**Acceptance of E1**: a project declaring `vertical-slice` + M2 but with no cross-import blocking rule → reports `ARCH-008` with a remediation document; with the rule → no longer reported.

---

## Group F — Safety scan (prompt injection) · MILESTONE M2

| ID | Task | Priority | Effort | Owner | Depends on | Status |
| :-- | :-- | :-: | :-: | :-- | :-- | :-: |
| F1 | **Measure false alarms/misses** on a real file set: ≥ 20 public repos (README, docs, agent configs) + a self-written attack sample set (multilingual, wording variants). Record the rates in `tests/` or a document | P1 | M | Claude (maintainer allows downloads) | — | TODO |
| F2 | **Add patterns** from the F1 results (wording variants, languages other than English/Vietnamese, hiding techniques such as character-form changes) | P2 | M | Claude | F1 | BLOCKED |
| F3 | **Rules for the Agent on meeting `SAFE-`**: put the "stop and ask" part in `core/templates/AGENTS.md` and the `health-check` skill so generated projects carry it | P1 | S | Claude | — | TODO |
| F4 | **Documents that talk about injection on purpose** (like `core/untrusted-content.md`) get flagged when the kit scans itself: add a note in the kit report or accept it deliberately | P3 | S | Claude | — | DEFERRED |
| F5 | **An Agent verification harness (Handoff 002)**: implement Phase 0, a scenario that measures an Agent's real interaction with Analytics, per maintainer handoff 002 (private) | P1 | M | Claude + Maintainer | — | TODO |
| F6 | **Extend Unicode NFC/NFD normalization**: track and add normalization for extended character sets beyond Vietnamese and Turkish | P2 | S | Claude | — | TODO |

**Acceptance of F1**: false alarms ≤ 2% of ordinary text files on the public repo set; ≥ 90% of the attack samples in the self-written set are detected.
**Accepted limits**: it does not scan source code and does not look for viruses; the report always says "no signal ≠ safe".

---

## Group H — Token Monitor (track tokens while a vibe coder chats with an agent)

| ID | Task | Priority | Effort | Owner | Depends on | Status |
| :-- | :-- | :-: | :-: | :-- | :-- | :-: |
| H1 | **Engine + CLI** that reads Claude Code logs, removes duplicates, and computes context/rate/heaviest turns (`scripts/token_monitor/`, `token_monitor_cli.py`, 15 tests) | P1 | M | Claude | — | DONE |
| H2 | **Real-time web dashboard** (`scripts/token_dashboard/`, `token_dashboard_cli.py`): standalone page, loopback, read-only; viewed in desktop/mobile/light/dark browsers; 10 service + server tests | P1 | M | Claude | H1 | DONE |
| H2b | **Attach the dashboard to `reviewer_shell`** as a tab (currently a separate page, to avoid editing the Analytics UI, which had no UI tests) | P2 | S | Claude | H2 | TODO |
| H3 | **Put it in the `.exe`**: rebuild the .NET shell to have a monitor tab/window; try on a clean machine | P1 | M | Maintainer installs .NET 10, Claude fixes | H2, A1 | TODO |
| H4 | **Codex adapter** (`~/.codex/sessions/**/rollout-*.jsonl`; the `token_count` event is a cumulative counter, so the previous turn must be subtracted). No Codex data yet to verify on this machine | P2 | M | Claude + Maintainer (needs real Codex logs) | H1 | TODO |
| H5 | **Survey Cursor/Antigravity/Windsurf**: do they store tokens locally? If not, state the limit clearly, do not guess | P2 | S | Claude (search) | — | TODO |
| H6 | **Proactive warnings** (e.g. context over a threshold): a desktop notification or a status line for Claude Code (`statusLine`) | P3 | S | Claude | H1 | DEFERRED |
| I1 | **Translate the text the engine generates into English** (finding titles, remediation, archetype/grade labels, pillar criteria, scan logs, `project-review.md`; about 800 lines in `scripts/auditor_engine/`), with a mechanism to choose the report language. The UI was already English (ADR-0023) but the engine content was still Vietnamese | P1 | L | Claude (translation), Antigravity (runs tests) | — | DONE (2026-11-08, ADR-0026: the engine emits English; Vietnamese is a language pack; verified identical to the previous engine on 23 projects) |
| I2 | **Rebuild the exe and verify the new settings UI** (one file, default language English, Settings submenus): maintainer handoff 013 (private); verified through reports 013-015 (exe 3EA6CF08..., engine extraction with SHA-256 check, ADR-0025). Still to do: release the exe through Releases (A3), do not commit binaries | P0 | S | Antigravity | A1 | DONE |
| I3 | **Make every file in the repo English** (language packs and Vietnamese-detection patterns excepted; `tests/test_repo_english.py` guards it). Done: scripts, tests, tools, ADRs, TASKS, profiles, templates, evals protocol; old Vietnamese evidence and AI20K binaries moved to the private lab. Still pending: `knowledge-base/` (about 5,000 Vietnamese lines in 60 files) and `examples/before-vibe-code/` (about 390 lines); when a pending path is translated, the guard keeps it from regressing only after its prefix is removed from `PENDING_PREFIXES` | P1 | L | Claude | I1 | DOING |

**Acceptance of H1**: the totals match an independent calculation on real logs (reached on 2026-11-07: 114 turns matched number by number). **Accepted limits**: tokens only, not converted to money (prices change and were not verified); figures come from local logs, not an invoice.

---

## Group D — Kit content · MILESTONE M2

| ID | Task | Priority | Effort | Owner | Depends on | Status |
| :-- | :-- | :-: | :-: | :-- | :-- | :-: |
| D1 | **A technology-selection framework** (a `router` document): criteria for scale, user skills, cost, time, risk; make the Agent state its reasons and the options it rejected. Linked to the Technology Selection Gate | P1 | S | Claude | — | TODO |
| D2 | **Review `INDEX.md`**: add a column/notes with exclusion conditions for rows that are easy to pick by mistake; check that "When to use" is written in the user's own words | P1 | S | Claude | C3 | BLOCKED |
| D3 | **Long reference documents** (`design-archetypes-catalog` 248 lines, `visual-dna-prompts` 134, `design-patterns-catalog`): add a summary at the top + a table of contents so the Agent reads selectively, or split them | P2 | M | Claude | — | TODO |
| D4 | **Mark `knowledge-base/`, `templates/pitch-deck`** as a Library "do not read unless asked"; decide which files move out of the Agent's path | P2 | S | Claude | Q4 | TODO |
| D5 | **M2/M3 guardrail templates per language**: write only the *acceptance criteria* (for example "has a cross-import blocking rule, run in CI") and do not teach configuration; the Agent picks the tool | P2 | S | Claude | E1 | TODO |
| D6 | **Additional profiles on real demand** (API backend, CLI, mobile, data/ML): write them only when C1/C3 show the Agent chose wrongly or lacked grounds | P3 | M | Claude | C1, C3 | DEFERRED |
| D7 | **ADR-0013** records the settled decisions: dropping stack profiles, positioning as "decisions and constraints", the safety scan scope, the exe release channel | P2 | S | Claude | Q1 | TODO |

---

## Decisions the maintainer must make

| ID | Question | Options | Suggestion | Blocks |
| :-- | :-- | :-- | :-- | :-- |
| Q1 | How should the exe be released? | (a) commit it to git; (b) GitHub Releases | **SETTLED (b)** on 2026-11-05: release through GitHub (Releases). If the intent is to commit binaries to git, say so | A3, D7 |
| Q2 | Should packaged Analytics be supported for Linux/macOS? | (a) Windows only + Python for other systems; (b) package all three | **(a)** first, (b) when there is real demand | A5 |
| Q3 | Should it be packaged as a Claude Code plugin? | (a) yes; (b) not yet, only the repo URL | **(b)** until C1/C2 are done | C6 |
| Q4 | Which Library files can be removed from the repo? (pitch deck, the archived `PLAN.md`; `reference-slides/` and `templates/project-management/` were deleted on 2026-11-08 as byte-identical to `tu-duy/` and `quan-tri-du-an/raw/`) | keep all / move to a separate repo / delete | Keep, only mark them do-not-read; deleting needs maintainer approval (per the stop-and-ask rule) | D4 |
| Q5 | Which Agents should run C1? | Claude Code, Codex, Antigravity | **SETTLED** on 2026-11-05: Claude Code (Claude runs in a new session) + Antigravity (the maintainer runs). Codex later | C1, C3 |

---

## Plan change log
| Date | Change |
| :-- | :-- |
| 2026-11-07 | **Final engine packaging, 180s Watchdog, Safety pre-gating & Clean-Machine verification (ADR-0019..0021)**: switched the engine lifetime mechanism to a 2000ms heartbeat + 180s watchdog (against hung orphan child processes); delimited SAFETY_IGNORE_DIRS (22 entries) to preserve the safety scan on sample/mock folders; a literal directive pre-gate filter cut scan time 2x-5x (P-062 from 28.9s -> 5.9s, litellm from 69s -> 35.4s) while keeping 100% of the findings across 23 repos; Unicode NFC normalization & Turkish character handling; packaged the reviewer-engine.exe build (9.35 MB), which passed the clean-machine test (A2 DONE) and a mid-run CDP shell reload (Page.reload at 5s, 15s and F5 at 8s on LiteLLM). Added the extension items E8..E10 and F5..F6. |
| 2026-11-07 | **ADR-0018: Health Check moved from file checking to project analysis.** Added `analysis.py` (languages by lines of code, frameworks by real imports, dependency graph, cycles, layer direction, project type), `knowledge_pack.json` + `build_knowledge_pack.py` (prepackaged, optional online update), `insights.py` (strengths/bottlenecks/recommendations with evidence, profile constraint cross-check), section `1.1 Project analysis` in the report and a "Project analysis" tab in the UI. AI Deep Review receives the Project Model instead of just the score, with a connection test button, an optional send-code option (secrets masked), saving `project-review-ai.md`; the API key is DPAPI-encrypted on Windows. Fixed a wrong C#/ASP.NET detection for Python repos. 134 tests pass; **accuracy on real projects not yet measured** (brief maintainer handoff 004 (private) assigned to Antigravity), exe not rebuilt yet, UI/AI not yet tried with a real key. |
| 2026-11-07 | Extended offline Health Check (ADR-0017, `hygiene.py`): `SEC-005` (.env/private key committed), `HYG-002` (log committed), `SUP-001..004` (install script downloading remote content, unpinned dependencies, index other than PyPI, binary committed), `AGT-004/005` (wrong/deprecated MCP packages, unpinned npx), `SPEC-001` (leftover `[NEEDS CLARIFICATION]`). Detection only, no score change. 15 new tests. Tried on 2 real repos: P-062 reported 30 committed log files, the kit reported its own `.exe` (SUP-004). Not done: F1/F2 (measure false alarms/misses of SAFE- on ≥ 20 public repos, needs permission to download), CVE lookup, typosquatting. |
| 2026-11-07 | Added the work log check (ADR-0016): standard `core/standards/worklog.md` (S-009), template `docs/worklog.md`, Working Rule 12 in the sample AGENTS.md; Health Check emits `WLOG-001` (no work log, Medium) and `WLOG-002` (file exists but has no dated entry, Low), no score change. 98 tests pass (8 new). Not checked: entry freshness, false alarm rate on real repos. |
| 2026-11-07 | A2 (partial): tested on a machine without real .NET/Python (a dev machine, with the .NET 10 Desktop Runtime removed). The framework-dependent exe exited with code 0x80008083 and showed the "You must install .NET Desktop Runtime" dialog (confirmed). The `--self-contained` exe (52 MB, built with a portable SDK): it ran, the window responded, the engine `/api/status` was ready on 127.0.0.1, and it closed cleanly. Not verified: a truly clean machine, missing WebView2, scanning from the UI, an engine built from a branch (the old engine's audit report lacked Sections 0/7/SAFE-001). Fixed `run-test.ps1`: when the exe/engine is missing it reports INVALID, exit 2 instead of writing "shell alive: True". Report: `evals/results/2026-11-07-clean-machine-test.md`. |
| 2026-11-07 | Token Dashboard (H2): a local web page refreshing every 2 seconds; checked in a real browser (desktop, mobile 375px, light/dark), fixed the odd axis (6.250) and horizontal overflow on mobile; a 2-color palette passed the validate_palette check (CVD ΔE ≥ 24). 79 tests pass. Claude Code only. |
| 2026-11-07 | Added the Token Monitor (group H): a pure engine + a `--watch` CLI, 15 tests. Found that Claude Code logs each response several times, so a raw sum over-counts about 2.3x; the engine deduplicates by (message.id, requestId) and matched an independent calculation on a real 114-turn session. No Web tab/exe yet, no other agents supported yet. |
| 2026-11-07 | Measured tokens with the real Claude tokenizer (after `claude auth login`, fixed `measure_docs.py`: find `claude` with `shutil.which`, disable skills/MCP so the overhead is 180 tokens instead of 57,543): 9 near-parallel document pairs, English uses about 10% fewer tokens (2–21% per file). The 40–60% claim was refuted for the kit's documents. |
| 2026-11-07 | Added the measurement tools `measure_docs.py` (private), `bench_health_check.py` (private), `benchmark-plan.md` (private) and the result `evals/results/2026-11-07-measurements.md`. Result: the claim "every document < 120 lines" is FALSE (5/34 exceed it); the 40-60% token saving is NOT proven (a proxy shows 0.92x bytes, 0.85x words); Health Check on 5,000 synthetic files median 1.8 s (meets the A2 threshold < 30 s, only on Python/this machine). |
| 2026-11-07 | Empirical verification: (1) 333/340 raw URLs in the MANIFEST return 200, the other 7 are files not yet pushed, no errors on pushed files; (2) a review of tool/MCP coordinates with the npm/PyPI/GitHub API: found that `@modelcontextprotocol/server-playwright` does not exist, `server-github` and `server-postgres` are marked deprecated (archived, "no security guarantees"), `steipete/agent-rules` is archived; replaced with `@playwright/mcp`, `github/github-mcp-server`, `crystaldba/postgres-mcp`. Not done: C1/C3, trying the exe on a clean machine, real token measurement. |
| 2026-11-06 | Integrated the strengths of GitHub Spec Kit (ADR-0015): added `core/standards/feature-workflow.md` (S-008), the templates `feature-spec.md`/`feature-plan.md`, an upgraded `spec-first-task` skill (Scale Gate, Clarify, Analyze, converge loop). Next, not yet done: a Health Check detection for leftover `[NEEDS CLARIFICATION]` markers / scenarios lacking evidence. |
| 2026-11-06 | Completed the **Project Health Check v2.2.0** upgrade (A1, A4, E1, E2, E4 DONE): updated `remediation.py` with all the new documents (`S-007`, `D-006`, `G-005..007`, `K-001..007`), added the `ARCH-008` check (M1–M3 guardrails), extended `ARCH-007` (`PROFILE_EXPECTATIONS`), wrote `kit_ref`/`guardrail_level` into `project-review.md`, upgraded `server.py` + the Web UI to all 12 pillars with the Section 0/2/4/7 tabs, and repackaged `Project-Health-Check.exe` + `engine/reviewer-engine.exe` (54 tests pass; score 100/100 measured by the kit's own tool, not yet tried on a clean Windows machine). |
| 2026-11-06 | B8 DONE (pushed). B3 DOING: CI was red at `sync_docs.py --check` because `generate_manifest.py` walked the folders, so the file count differed between the dev machine (336/337) and CI (335); switched to `git ls-files` for a stable result, regenerated README/MANIFEST. Needs a push to confirm green CI. |
| 2026-11-05 | The repo was renamed to `Project-Builder-4-Agents` (B1 DONE). Replaced `Project-Builder-Kit` and the `Project-Starter-Kit` URL in 22 files. B8 (push) remains before running C1 by URL. |
| 2026-11-05 | Settled Q1 (GitHub Releases) and Q5 (Claude Code + Antigravity). Added C0 (scenarios, DONE), C7, B8 (push); C1 depends on B1 + B8 because the Agent must get the kit by URL. |
| 2026-11-05 | First plan after commit `a8ba04d`. Already done before (not listed again): restructuring into Core/Profiles/Library, `project-review.md`, the safety scan (Section 0), the scan scope (Section 7), the document format + automatic checks, the project-type selection table. |
