---
id: K-003
type: reference
when: "When needing to know **mandatory baseline standards** for any agent-driven repository"
---
# CORE BASELINE — MANDATORY FOUNDATION FOR ALL AGENT REPOSITORIES

> For AI Agents. Applies to **every** project regardless of programming language or architecture profile. Deeper configurations belong to `../profiles/` and are selected after the discovery phase (`discovery.md`).

## Mandatory Component Catalog

| Code | Component | Location in User Project | Source in Kit |
| :-- | :-- | :-- | :-- |
| B1 | **Agent Instructions** (Single source of truth) | `AGENTS.md` | `templates/AGENTS.md` |
| B2 | **Agent Compatibility Layer** | `CLAUDE.md` (imports `AGENTS.md`); skills at `.agents/skills/` (and `.claude/skills/`) | `templates/CLAUDE.md`, `templates/.agents/skills/` |
| B3 | **Project Brief** (Discovery outcome: persona, problem, core journeys, stack, constraints) | `docs/project-brief.md` | `templates/docs/project-brief.md` |
| B4 | **Architectural Decision Records** (ADR): At minimum tech stack + architecture profile | `adrs/` | `templates/adrs/0000-template.md` |
| B5 | **Working Standards** | `docs/standards/` (coding conventions, test strategy, Definition of Done) | `standards/` |
| B6 | **Real Verification Commands** (test, lint, build) and **Automated CI** | `AGENTS.md` Section 2 + `.github/workflows/ci.yml` | `templates/.github/` |
| B7 | **Repository Hygiene**: Zero secrets in code | `.gitignore`, `.env.example`, `.editorconfig` | `templates/gitignore.tpl`, `templates/.env.example`, `templates/.editorconfig` |
| B8 | **Kit Profile Ledger** (Active profile, kit version) | `.builder/kit.json` | `templates/.builder/kit.json` |
| B9 | **PR / Issue Templates** | `.github/PULL_REQUEST_TEMPLATE.md`, `ISSUE_TEMPLATE/` | `templates/.github/` |
| B10 | **Periodic Health Check**: Results in `project-review.md` | Project root | Project Builder Analytics tool |

## Core Working Principles (Embedded in `AGENTS.md` Template)
1. **Read before edit**: Never guess context.
2. **Spec before code** for non-trivial changes; contract alterations (API, DB schema, routes) require an ADR and user sign-off.
3. **Defensive boundaries**: Validate input, handle errors explicitly, never swallow exceptions silently, use safe fallback defaults.
4. **Tests accompany code**: Run verification commands before reporting completion.
5. **2-Attempt Circuit Breaker**: If fixing the same failure on attempt 2 fails $\rightarrow$ stop, diagnose architectural causes, and never attempt a 3rd blind patch.
6. **Stop & Ask** when requirements are ambiguous, breaking changes occur, performing destructive operations, or introducing heavy dependencies.
7. **Never commit secrets**.
8. **Proactively consult kit** via Knowledge Router instead of inventing conventions.

## What is NOT in Core (Customized per Project)
Architecture profiles (Clean/Hexagonal/Modular Monolith/Vertical Slice/Simple Layered), programming languages and frameworks, UI design systems, application types (Web, Mobile, AI/Agent apps), data persistence strategies, and specialized domain skills. See `../profiles/README.md`.
