---
id: K-002
type: playbook
when: "When needing to **interview user** to clarify project, lock user journeys, and select stack"
---

# DISCOVERY — BRAINSTORMING, PLANNING & SCOPE LOCK PLAYBOOK

> Exclusively for AI Agents. Objective: From a brief prompt by a Vibe Coder, the Agent acts as **Tech Lead & Product Architect** to brainstorm, shape system boundaries, finalize an **A-to-Z Execution Plan**, select **Tech Stack & Architecture Profile**, and **inject Curated Skills**.

## 1. Dialogue Principles (Optimized for Vibe Coders)
* **Ask few questions, suggest concrete defaults**: At most 3 questions per turn. Start with *user persona and core problem*, never with engineering jargon.
* **Provide recommended defaults with one-line rationales**: ("I recommend Stack X because it runs smoothly, costs $0 to host, and deploys easily — sounds good?").
* **Proactively assume safe defaults**: When user states "not sure" or "up to you", adopt the safest industry default and record it under Assumptions in `docs/project-brief.md`.
* **Never ask the user to run terminal commands**: The Agent creates files, tests environments, and writes configs directly.

## 2. Discovery Sequence: From Concept to A-Z Plan
1. **Product Mindset (Who & What Problem)**:
   * Persona and core pain point.
   * Measurable Definition of Done in one sentence.
2. **Core User Journeys**:
   * 3–5 primary interaction steps from start to finish.
3. **System Thinking Breakdown**:
   * **Frontend**: Web, mobile, or dashboard? Responsive layout and light/dark theme requirements?
   * **Backend & Logic**: Complex business rules? External AI APIs or third-party webhooks?
   * **Persistence & Auth**: Authentication needed (JWT, OAuth)? Database required (PostgreSQL/SQLite) or local state?
   * **Cloud & Go-Live**: Real-world deployment plan ($0 tier via Vercel, Railway, Supabase).
4. **Sprint Roadmap Setup**:
   * Scaffold `planning/roadmap.md` and `planning/backlog.md`: Sprint 1 (Working MVP), Sprint 2 (Business Logic & UI Polish), Sprint 3 (Hardening, Security, E2E & Go-Live).

## 3. Architecture Selection & Skill Injection
* **Architecture Selection**: Consult [../profiles/README.md](../profiles/README.md) to match project signals (Simple Layered, Clean Architecture, Vertical Slice, Modular Monolith) and guardrail level (M1–M3).
* **Inject Curated Skills**: Consult [../profiles/skills-catalog/curated-agent-skills.md](../profiles/skills-catalog/curated-agent-skills.md). Copy relevant skills into `.agents/skills/` (and `.claude/skills/`):
  * Database needed $\rightarrow$ inject `db-migration-guardian`.
  * External network calls $\rightarrow$ inject `defensive-api-client`.
  * Frontend UI $\rightarrow$ inject `error-boundary-guard`.
  * Production ready $\rightarrow$ inject `docker-production-packager`, `cloud-free-tier-deployer`.
  * *Zero tokens wasted on random internet searches.*

## 4. Mandatory Deliverables of Phase 1
1. `docs/project-brief.md`: Filled with core problem, user journeys, and explicit assumptions.
2. `planning/roadmap.md` & `planning/backlog.md`: Phased sprints and prioritized backlog.
3. `adrs/0001-stack-selection.md` & `adrs/0002-architecture-selection.md`: Pinned decisions.
4. `.agents/skills/` (and `.claude/skills/`): Injected domain skills.
5. `.builder/kit.json`: Pinned active profile.
6. **User Confirmation Summary**: Concise proposal presented to the user for sign-off before entering code scaffolding in Phase 2.
