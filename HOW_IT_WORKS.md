# HOW IT WORKS — OPERATIONAL SPECIFICATION FOR PROJECT-BUILDER-4-AGENTS

> **Comprehensive operational specification defining the purpose, architecture, and lifecycle mechanism of Project-Builder-4-Agents.**
> Written primarily for **AI Coding Agents** (Claude Code, Antigravity, Cursor, Windsurf, Codex) and contributors developing this kit.

---

## 1. Core Nature: Exclusively Engineered for AI Agents

### 🎯 Key Differentiators
* **Designed for the Vibe Coder's AI Agent**: A traditional human developer not using AI will find this repository unconventional. It is not an end-user tutorial; it is an **Agent-Readable Operating System**: high information density, strict structured formatting, and optimized for LLM Context Windows.
* **Pure Text, Zero External Links**: All rules, skill matrices, architecture constraints, and playbooks are self-contained **pure markdown text** within the repository. Agents never need to traverse external websites, eliminating broken links, web-crawling latency, and malicious code injection risks.
* **Remote Knowledge Hub (Zero-Clone)**: Vibe coders never need to clone this multi-language repository onto their local machines. Their AI Agent reads the knowledge hub remotely on GitHub and pulls only the exact files required for their specific stack.

### 🏛️ The Triad Collaboration Model (Client — Translator — Company)
```
┌─────────────────────────────────┐
│     CLIENT (Vibe Coder)         │
│  - Product vision & user goals  │
│  - No engineering jargon        │
│  - "I want a clean, fast app"   │
└────────────────┬────────────────┘
                 │
                 │ (Plain human language)
                 ▼
┌────────────────────────────────────────────────────────┐
│        TRANSLATOR / PRINCIPAL SOLUTION ARCHITECT       │
│               (Project-Builder-4-Agents)               │
│                                                        │
│  1. Guides Client to Prompt Correctly:                 │
│     - 3-question Discovery, measurable Definition of   │
│       Done, translates "clean UI" into Design Tokens   │
│                                                        │
│  2. Enforces Company to Execute with Discipline:       │
│     - Delivers architectural blueprints (Clean/Slice)  │
│     - Supplies Ecosystem Taxonomy & Curated Skills     │
│     - Enforces circuit breakers (Anti-Doom-Loop)       │
│     - Generates 0-token audit score (Health Check A+)  │
└────────────────┬───────────────────────────────────────┘
                 │
                 │ (Machine contracts & architectural constraints)
                 ▼
┌─────────────────────────────────┐
│   COMPANY / DEV HOUSE (Agent)   │
│  - Massive code generation rate │
│  - Prone to hacking if unguided │
│  - Follows blueprints strictly  │
└─────────────────────────────────┘
```
Without the Translator, the Client and the Dev House talk past each other: the client gives vague visual feedback, the dev house patches quick superficial hacks, and the codebase rapidly deteriorates into a Doom Loop. Project Builder serves as the durable translation layer and quality guarantor.

---

## 2. Core Objective: Minimizing Execution Time & Token Consumption

Modern AI models already excel at writing code syntax (`if/else`, loops, functions). This repository does not teach basic coding. Instead, it serves as a **Decision Acceleration Engine**:

1. **Minimizing Time-to-Execution**: Instead of wasting dozens of back-and-forth prompt turns trying to clarify project scope or trial-and-erroring architectures, the kit provides deterministic decision rails to finalize tech stack, directory layouts, and rules within seconds.
2. **Minimizing Token Consumption (ADR-0014)**: English is the primary language across all documents. English achieves optimal token density (~1.3 tokens/word vs. 2–4 tokens per syllable in accented languages), saving **40% to 60% of context tokens**. All knowledge documents are constrained to < 120 lines.
3. **Solving the "1 Million Random Skills" Dilemma**: The internet is filled with thousands of untested prompts and skills. The kit provides a **Curated Skills Matrix (`curated-agent-skills.md`)** categorized by lifecycle and domain. Agents immediately pick and inject production-ready skills into their workspace without web searches.

---

## 3. End-to-End Operational Lifecycle: Prompt to Go-Live

When a Vibe Coder opens an empty folder and prompts their Agent:
```text
"Bootstrap a SaaS dashboard, refer to https://github.com/Dokhacgiakhoa/Project-Builder-4-Agents, plan and build from A to Z"
```

The Agent executes the following phased sequence:

```
[Vibe Coder sends prompt]
         │
         ▼
[PHASE 0: AGENT SELF-CONFIGURATION]      ──► 1. Self-configure Agent (Constitution AGENTS.md, baseline skills)
         │                                   2. Scaffold Core Baseline B1-B9 (specs, planning, docs)
         ▼
[PHASE 1: BRAINSTORM & SYSTEM DESIGN]    ──► 1. Clarify requirements & define Task Spec
         │                                   2. Technology Selection Gate & Architecture Profile selection
         │                                   3. Inject domain skills from Curated Skills Matrix
         ▼
[PHASE 2: DEEP SCAFFOLDING & GUARDRAILS] ──► Scaffold directory layout, configure real test/lint/build, CI/CD
         │
         ▼
[PHASE 3: SPRINT ACCELERATION]           ──► Knowledge Router queries INDEX.md: Anti-patching, Design tokens
         │
         ▼
[PHASE 4: PRODUCTION-READINESS & GO-LIVE]──► Docker multi-stage build, Cloud Free-Tier deploy, Health Check A+
```

---

### Phase Breakdown

#### Phase 0: Agent Self-Configuration & Core Baseline
* **Principle**: *Before writing a single line of business logic, configure the Agent's own constitution and guardrails.*
* The Agent fetches remote manifests via `BOOTSTRAP.md` or `MANIFEST.json`.
* Sets up the Core Baseline (B1–B9):
  * **Agent Constitution**: `AGENTS.md` (Codex/Antigravity), `CLAUDE.md` (Claude Code), `.cursor/rules/*.mdc` (Cursor), `.windsurfrules` (Windsurf).
  * **Core Guardrail Skills**: `.agents/skills/health-check/`, `spec-first-task/`, `kit-consult/`.
  * **Governance Framework**: `docs/project-brief.md`, `adrs/`, `specs/`, `planning/`, `tasks/`.
* Result: The Agent is fortified with a 2-attempt circuit breaker, self-verification commands, and defensive boundary habits.

#### Phase 1: Brainstorming, Detailed Planning & System Architecture
* The Agent conducts a concise discovery interview with the user: Problem, Core Audience, Key Journeys (1-3), Constraints.
* **System & Product Mindset**:
  * Divides boundaries cleanly: Frontend, Backend, Persistence, Cloud.
  * Consults `profiles/README.md` to select the architecture pattern (Simple Layered, Clean Architecture, Vertical Slice, Modular Monolith).
  * Consults `profiles/skills-catalog/curated-agent-skills.md` to **inject domain skills** (e.g., `db-migration-guardian`, `defensive-api-client`, `auth-rbac-guardian`).
  * Finalizes Tech Stack ADR (`adrs/0001-*.md`) and Architecture ADR (`adrs/0002-*.md`).

#### Phase 2: Deep Scaffolding & Guardrail Enforcement (Levels M1–M3)
* Pulls only the selected Architecture Profile files into the project.
* Configures real verification commands (`npm test`, `npm run lint`, `npm run build`...).
* Generates an actionable CI pipeline (`.github/workflows/ci.yml`).

#### Phase 3: Continuous Sprints & Anti-Doom-Loop Execution
* As features are implemented, the Agent autonomously consults [INDEX.md](INDEX.md) via the remote GitHub raw URL pinned in `AGENTS.md`.
* **Anti-Doom-Loop Protocol**: Governed by `profiles/playbooks/anti-doom-loop-guide.md` (Spec-First Loop, CI Green Loop, Git Micro-Checkpoint Loop). If a fix fails on attempt 2 $\rightarrow$ Stop & Ask, preventing codebase corruption.
* Complex debugging $\rightarrow$ activates `anti-patching-debugger`.
* UI development $\rightarrow$ consults `ui-ux-archetypes-and-presets.md`.

#### Phase 4: Production-Readiness & Real-World Go-Live
* Prepares the project for live production:
  * Adheres to the 5 Go-Live Gates in `profiles/deployment/go-live-production-checklist.md`.
  * Multi-stage, non-root Docker packaging.
  * Zero-cost cloud deployment via `profiles/stacks/cloud-free-tier-stack.md` (Vercel, Railway, Supabase, Cloudflare).
  * Runs **Project Health Check** to audit the codebase, achieving a 100/100 A+ score before launch.

---

## 4. Curated Skills Matrix & MCP Integration

To eliminate the overhead of filtering through thousands of fragmented web skills, the kit includes:
1. **Curated Skills Matrix (`profiles/skills-catalog/curated-agent-skills.md`)**: 16 battle-tested, copy-pasteable `SKILL.md` files covering DB migrations, API defense, Auth RBAC, State Management, Docker, Stripe, and SEO.
2. **Curated MCP Matrix (`profiles/agent-configs/curated-mcp-matrix.md`)**: Pre-configured JSON templates for GitHub, Postgres, SQLite, Playwright, and Filesystem MCP servers for Claude Desktop, Cursor, and Windsurf.

---

## 5. Living Knowledge Hub & Automated Manifest Maintenance

* Every file added, updated, or removed in the kit is indexed in `INDEX.md`.
* `scripts/generate_manifest.py` scans the repository to generate `MANIFEST.json`, recording file paths, content hashes (SHA-256), and direct raw URLs.
* Remote agents parse `MANIFEST.json` or `llms.txt` to access the exact resources they need with zero guesswork.
