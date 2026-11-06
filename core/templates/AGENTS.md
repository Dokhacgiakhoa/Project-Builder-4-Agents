# AGENTS.md — INSTRUCTIONS FOR AI AGENT (SINGLE SOURCE OF TRUTH)

> All AI agents (Claude Code, Antigravity, Codex, Cursor, Windsurf) working in this repository **must read and strictly adhere to** this document. `CLAUDE.md` simply imports this file. Keep this document concise: only document critical constraints that agents frequently violate.

## 1. Project Summary
<!-- Agent fills after discovery interview; details in docs/project-brief.md -->
* **Name**: {{PROJECT_NAME}}
* **One-Line Purpose**: {{ONE_LINE_PURPOSE}}
* **Stack**: {{STACK}} (Decision: `adrs/0001-*.md`)
* **Architecture**: {{ARCHITECTURE_PROFILE}} (Decision: `adrs/0002-*.md`; target folder tree: `docs/project-brief.md`)

## 2. Verification Commands (Mandatory before reporting "Done")
<!-- Agent fills real stack commands. Never leave TODOs once Phase 3 begins. -->
| Task | Command |
| :-- | :-- |
| Install dependencies | `{{INSTALL_CMD}}` |
| Dev run | `{{RUN_CMD}}` |
| Test | `{{TEST_CMD}}` |
| Lint / format | `{{LINT_CMD}}` |
| Build | `{{BUILD_CMD}}` |

## 3. Working Rules (Mandatory across all projects)
1. **Read before edit.** Read relevant files thoroughly; never guess. Review `docs/project-brief.md` and related ADRs before developing new features.
2. **Spec before code** for non-trivial changes: summarize objective, acceptance criteria, affected files (template: `tasks/task-spec.md`). Never modify architectural **contracts** (APIs, DB schema, routes, shared types) without an ADR and explicit user approval.
3. **Defensive boundaries**: Validate all external inputs (user inputs, network responses, files, DB queries, JSON parsing), handle errors explicitly with structured logs, **never swallow errors silently**, and provide safe fallback defaults. See `docs/standards/coding-conventions.md`.
4. **Tests accompany code**: At least 1 happy path test + 2 edge/failure cases. Run commands in Section 2; report "Done" only when all checks pass green. Verify against `docs/standards/definition-of-done.md`.
5. **2-Attempt Circuit Breaker**: If fixing the same issue (bug, UI glitch, network error) fails on the second attempt $\rightarrow$ **STOP immediately**. Do NOT attempt a 3rd blind patch. Analyze architectural root causes and propose options for user decision.
6. **Stop & Ask the user** when: requirements are ambiguous, changes break backwards compatibility, performing destructive/irreversible actions, or introducing heavy external dependencies outside the agreed stack.
7. **Never commit secrets/API keys**. Use `.env` (enforced in `.gitignore`), and update `.env.example` when adding variables.
8. Small, atomic commits per logical feature; format PRs according to `.github/PULL_REQUEST_TEMPLATE.md`.
9. Preserve unrelated comments, docstrings, and existing code formatting.
10. **Empirical Verification**: Never guess or speculate about libraries or APIs without verification. When converting screenshots or mockups to code, strictly follow the Visual Reverse Engineering Protocol (`screenshot-to-code-reverse-engineering.md`) and avoid blind-patching styles.

## 4. User Communication
The user may be a vibe coder or fresher. Explain concepts in concise, plain language. Clearly report: what was done, verification results, and recommended next steps. **Always respond in the user's preferred language** (e.g., Vietnamese, English, etc.).

## 5. KNOWLEDGE ROUTER — Proactively Consult Project-Builder-4-Agents
This project was scaffolded with **Project-Builder-4-Agents**. Configured in `.builder/kit.json`.

* Knowledge Hub: `{{KIT_REPO_URL}}` (Pinned version: `{{KIT_REF}}`)
* Intent-Routed Index: `{{KIT_RAW_BASE}}/INDEX.md`

**Core Rule**: The user is unfamiliar with kit internal files. When facing any scenario below where local guidelines are missing, **automatically fetch `INDEX.md`, match the intent under "When to use", read the document, and apply its constraints**. Never invent conventions.

| Scenario | Action |
| :-- | :-- |
| Adding major features, new modules, or changing directory structure | Consult chosen architecture profile (`.builder/kit.json`) |
| Choosing design patterns, refactoring, or untangling spaghetti code | Consult design pattern catalog + anti-patching playbook |
| Designing UI, colors, typography, theme, or design systems | Consult `design` group in INDEX |
| Replicating UI from screenshots, mocks, or avoiding visual doom loops | Consult `profiles/design/screenshot-to-code-reverse-engineering.md` |
| Implementing LLM / Agent / RAG capabilities | Consult `ai-apps` group in INDEX |
| Writing tests, setting up CI, or enforcing DoD | Consult `docs/standards/` then `core/standards` in INDEX |
| Addressing issues found in `project-review.md` | Consult remediation docs cited next to each finding |
| Injecting additional rules, skills, or workflows for Agent | Consult `agents` & `skills-catalog` in INDEX |
| Needing authoritative tools, keywords, or precision search vectors | Consult `profiles/knowledge-map/agent-ecosystem-taxonomy.md` |

After major milestones and before opening PRs, execute **Project Health Check** to refresh `project-review.md`, resolve High/Medium severity findings, or record them in backlog.

## 6. Technology Selection Gate
Before adding any new library, framework, or cloud service, record a concise evaluation table in an ADR:
1. Performance & rendering characteristics suited to application type.
2. Configuration & theming decoupled from source code (no hardcoding).
3. Secure secret and environment variable management.
4. Future evolution: AI/LLM readiness, testability, and zero bloat.
Tools failing these criteria must not be adopted.

## 7. Decouple Core Logic from UI Presentation
All utility tools, business scripts, and modules must isolate **pure logic** (testable without headless browsers or UI state) from the **presentation layer**. Never create monolithic files mixing UI components, state machines, and direct DB queries.
