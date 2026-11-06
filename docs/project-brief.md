# PROJECT BRIEF — Project-Builder-4-Agents

> Long-term memory for Project-Builder-4-Agents maintainers and AI Agents.

## 1. Problem & Target Audience
* **Target Audience / Persona**: Vibe Coders, junior developers, and AI Coding Agents (Claude Code, Antigravity, Cursor, Windsurf, Codex).
* **Core Pain Point**: Vibe coders experience visual and architectural doom loops; AI agents burn tokens crawling random internet skills and hallucinating unmaintainable spaghetti code.
* **Definition of Done**: A remote knowledge library (read without cloning) plus a local static Health Check, intended to help AI agents self-configure, choose an architecture, and audit static project signals. Not yet validated with real agents or users (see README Validation Status).

## 2. Core User Journeys (3–5 journeys, start-to-finish)
1. **Zero-Clone Bootstrap**: Vibe coder prompts their agent with kit URL $\rightarrow$ Agent reads `llms.txt` / `MANIFEST.json` remotely $\rightarrow$ Agent self-configures rules and baseline skills $\rightarrow$ Scaffolds clean workspace.
2. **Discovery & Architecture Selection**: Agent conducts 3-question interview $\rightarrow$ Maps requirements to Simple Layered, Clean Architecture, Vertical Slice, or Modular Monolith $\rightarrow$ Injects curated skills.
3. **Anti-Doom-Loop Development**: Agent works in 3 operating loops (Spec-First, CI Green, Git Checkpoint) with a 2-attempt circuit breaker.
4. **Visual Reverse-Engineering**: Vibe coder provides UI screenshot $\rightarrow$ Agent executes 5-step replication protocol with subtle 1px borders and 4-state completeness.
5. **Quality Audit & Go-Live**: Project Health Check runs offline (about 1 second on this repo, single run on the maintainer's machine) $\rightarrow$ Outputs `project-review.md` scoring 0-100 with remediation docs $\rightarrow$ Deploys to a free-tier cloud.

## 3. Data & Authentication
* **Architecture**: Standalone static Python 3.12+ stdlib engine + .NET 10 desktop host wrapper.
* **Sensitive Data**: No hardcoded secrets in the repo; the engine does local file-tree scanning with regex heuristics (no AST parsing).

## 4. Constraints
* Zero runtime external dependencies for the engine (Python standard library only).
* Core knowledge documents are kept self-contained (few external links) to limit token use and untrusted fetches.
* English-first primary language for all agent documentation (ADR-0014).

## 5. Technical Decisions (Summary; details in `adrs/`)
* **Stack**: Python 3.12+ (Auditor Engine) + C# / .NET 10 (ProjectReviewer UI wrapper) + TypeScript / React (Design showcase).
* **Architecture Profile**: Clean Architecture / Modular Monolith separating pure CLI logic from UI presentation.
* **Decisions**: ADR-0011 (Desktop & Tooling), ADR-0012 (Agent-First Builder & Health Check), ADR-0013 (Zero-Clone Remote Hub), ADR-0014 (English Primary Language).

## 6. Assumptions
* Agents have HTTP raw fetch or shallow git clone capabilities.
* Users have Python 3.12+ for CLI auditor or use the bundled `.exe`.

## 7. Out of Scope
* Direct online code hosting platform (uses GitHub).
* Antivirus / binary disassembly scanning.
