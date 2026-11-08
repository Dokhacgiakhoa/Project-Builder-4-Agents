# ADR 0013: REMOTE KNOWLEDGE HUB AND THE ZERO-CLONE BOOTSTRAP MECHANISM FOR VIBE CODERS

* **Status**: Approved (Accepted)
* **Decision date**: 2026-11-06
* **Builds on**: [ADR-0012](0012-agent-first-builder-and-health-check.md)

---

## 1. CONTEXT
* The target users are **Vibe Coders / Freshers**: when starting a new project they open a completely empty folder and ask their AI Agent (Claude Code, Antigravity, Cursor, Codex...) to read the kit's GitHub repo to initialize the project.
* A vibe coder may work on different problems with completely different tech stacks (Python, .NET, TypeScript, Go...). If they are made to clone the whole kit repo:
  1. It clutters and weighs down the user's machine with hundreds of files for other languages they never use.
  2. It makes it easy for the Agent to misunderstand the structure and copy unsuitable template files into the project.
* At the same time, modern AI Agents are strong enough at code syntax but often lack **system design thinking, architecture boundaries (Clean Architecture), a Product Mindset and crash defense (Anti-Crash)**. The goal is not just to run `localhost` but to aim for a **real Go-Live** in a Production environment.

---

## 2. DECISION

### 2.1. Positioning as a Remote Knowledge Hub (a remote knowledge library; just files on GitHub, no service running)
* The `Project-Builder-4-Agents` repo acts as a **centralized knowledge base on GitHub**, not as a boilerplate template for users to clone.
* It provides standardized machine-readable interfaces:
  * `llms.txt` and `llms-full.txt`: an open standard for LLMs/Agents to read the whole structure and intent of the repo quickly in one request.
  * `MANIFEST.json`: a machine-readable file tree with raw download links `raw.githubusercontent.com/...` so the Agent sees every file in the repo without scraping GitHub's HTML interface.
  * `HOW_IT_WORKS.md`: a detailed specification of how it operates so developers and Agents do not misunderstand it.

### 2.2. The 4-Phase Zero-Clone Process
1. **Phase 1: Discovery & Tech Selection Gate**: the Agent acts as a Tech Lead, interviews the user, and proposes a suitable stack and architecture. **Absolutely no file is downloaded to the machine until the user has decided.**
2. **Phase 2: Set up the Core Baseline skeleton & apply a Profile**: pull only the Core (B1–B9) and the architecture Profile of the chosen language through an HTTP raw fetch or a shallow clone into the operating system's temp folder (`%TEMP%` or `/tmp`), then delete it right away.
3. **Phase 3: Accompany every Sprint**: the project carries an `AGENTS.md` containing a Knowledge Router that automatically looks up `INDEX.md` on GitHub when it needs to solve an architecture, design system, AI app or error-defense problem.
4. **Phase 4: Production-Readiness & Go-Live**: guidance on Docker packaging, CI/CD, Cloud Free-Tier configuration, running Project Builder Analytics and handling High/Medium findings before release (the score reflects static signals only).

---

## 3. CONSEQUENCES
* **Positive**:
  - Expected: fewer unused files on the vibe coder's machine (Method B still uses a temp folder; not yet verified).
  - The Agent fetches files remotely by raw URL instead of scraping GitHub's HTML (the routing accuracy has not been measured).
  - Goal: a project with a clear architecture direction aimed at real deployment. This is an unverified hypothesis.
* **Trade-offs / Constraints**:
  - The `MANIFEST.json` and `llms.txt` must be kept consistent through an automatic check script in CI.
  - The Agent needs an internet connection to download documents from GitHub while following the process.
