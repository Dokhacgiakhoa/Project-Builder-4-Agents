# Project-Builder-4-Agents

<!-- AUTO-GEN:STATS -->
[![Health Score](https://img.shields.io/badge/Health_Score-100%2F100_A%2B-brightgreen)](project-review.md)
[![Automated Tests](https://img.shields.io/badge/Tests-52_passed-blue)](tests/)
[![Indexed Files](https://img.shields.io/badge/Indexed_Files-340_files-purple)](MANIFEST.json)
[![Architecture](https://img.shields.io/badge/Architecture-Remote_Knowledge_Hub-emerald)](HOW_IT_WORKS.md)
<!-- /AUTO-GEN:STATS -->

<div align="center">

  <img src="assets/banner.svg" alt="Project-Builder-4-Agents" width="100%" />

  <h3>Project-Builder-4-Agents</h3>
  <p><b>Hosted Agent Brain & Living Knowledge Hub — Enables AI Coding Agents to self-configure, select production stacks, and bootstrap vibe coding projects remotely (Zero-Clone).</b></p>
  <p>Seamlessly compatible with <b>Claude Code · Antigravity · Cursor (.cursor/rules/*.mdc) · Windsurf · Codex</b></p>

</div>

---

> ## 🤖 FOR AI CODING AGENTS (REMOTE ACCESS & ZERO-CLONE)
> If a user sends you this repo URL to bootstrap their project:
> 1. **DO NOT ask the user to clone the whole repository**: Read remotely via [BOOTSTRAP.md](https://raw.githubusercontent.com/Dokhacgiakhoa/Project-Builder-4-Agents/main/BOOTSTRAP.md) or inspect the tree at [MANIFEST.json](https://raw.githubusercontent.com/Dokhacgiakhoa/Project-Builder-4-Agents/main/MANIFEST.json) / [llms.txt](https://raw.githubusercontent.com/Dokhacgiakhoa/Project-Builder-4-Agents/main/llms.txt).
> 2. **Never download until Stack is finalized**: Ingest `core/discovery.md` to interview the user, then consult `profiles/README.md` to match an architecture pattern.
> 3. **Selective pull**: Fetch only the Core Baseline (B1–B9) and the chosen Architecture Profile into the target workspace (via direct raw HTTP fetch or shallow temp clone).
> 4. **Continuous Companion & Go-Live**: Consult [INDEX.md](https://raw.githubusercontent.com/Dokhacgiakhoa/Project-Builder-4-Agents/main/INDEX.md) during sprints; run [Project Health Check](scripts/README.md) to maintain an A+ production score.
> Full operational specifications: [HOW_IT_WORKS.md](HOW_IT_WORKS.md).

---

## How to Use (For Human Vibe Coders)

1. Open Claude Code, Antigravity, Cursor, or Codex in an empty folder (or an in-progress project).
2. Paste this single prompt:
   > "Use https://github.com/Dokhacgiakhoa/Project-Builder-4-Agents to bootstrap this project. I want to build a [describe your product vision in 1–2 sentences]."
3. Your Agent will fetch `BOOTSTRAP.md`, ask up to 3 clarifying questions, recommend the right architecture profile, install guardrails, and wire up `AGENTS.md`.

---

## What's Inside

Three distinct tiers, so you never drown your Agent in irrelevant context:

| Tier | Where | Contents |
| :-- | :-- | :-- |
| **Core** — Mandatory for all agent-driven repos | [core/](core/README.md) | `AGENTS.md` Constitution, Agent compatibility layer, project brief, ADR templates, coding standards, verification commands, PR template |
| **Profiles** — Selected per project domain | [profiles/](profiles/README.md) | Architecture patterns (Layered, Clean Architecture, Vertical Slice, Modular Monolith), Curated 16+ Skills Matrix, Curated MCP Matrix, Go-Live Checklist, Anti-Doom-Loop Playbook |
| **Library** — Reference & Optional | `knowledge-base/`, `templates/` | Technical playbooks, system design philosophy, project management, pitch decks |

Deep architectural profiles, rules, and skills are **never dumped together**: Your Agent picks only the relevant subset after the Phase 1 interview. Only Core is universally applied.

## Configuration & Environment Variables (.ENV)

Project-Builder-4-Agents and its companion Project Health Check engine operate offline with zero tokens and zero external secrets required. For local environment overrides or port customizations, copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

## Project Health Check

Scans **any project workspace** (any language), offline, with zero token consumption, generating **`project-review.md`** for both humans and agents. Each finding includes a **unique code, severity, file:line location, and a direct remediation doc** in the kit.

| Execution Method | Notes |
| :-- | :-- |
| `Project-Health-Check.exe` (Windows) | GUI: Select folder, inspect findings |
| `python scripts/project_auditor.py <target_dir>` | Requires Python 3.12+ (Linux/macOS/CI) |
| `./Project-Health-Check.sh <target_dir>` | Linux/macOS shell script |

Details: [scripts/README.md](scripts/README.md). Build standalone executable: `make build-exe`.

## For Kit Contributors

```bash
make test         # Run pytest + vitest
make check-links  # Verify INDEX.md routing and format constraints
make review       # Run Health Check against this repository
```
Contribution rules: [AGENTS.md](AGENTS.md) · Architecture Decisions: [ADR-0012](adrs/0012-agent-first-builder-and-health-check.md), [ADR-0013](adrs/0013-remote-knowledge-hub-and-zero-clone-bootstrap.md), [ADR-0014](adrs/0014-english-as-primary-language-for-token-efficiency.md).

## License
[MIT](LICENSE).
