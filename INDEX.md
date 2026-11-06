# INDEX — INTENT-TO-DOCUMENT ROUTING TABLE (FOR AI AGENTS)

> Users **do not know** which documents exist in this repository. Read the **"When to use"** column, match it with the user's intent or current task, and open the exact document. Read at most 2–3 documents per query. Raw base URL: `https://raw.githubusercontent.com/Dokhacgiakhoa/Project-Builder-4-Agents/<ref>/<path>`.
> Tier: **C** = Core (Mandatory for all projects) · **P** = Profile (Selected per project domain) · **L** = Library (Reference & optional).

## 1. Bootstrap & Lifecycle
| ID | Tier | When to use | Document |
| :-- | :-: | :-- | :-- |
| K-001 | C | When starting a **new project** or setting up standard scaffolding for an existing workspace | [BOOTSTRAP.md](BOOTSTRAP.md) |
| K-002 | C | When needing to **interview user** to clarify project, lock user journeys, and select stack | [core/discovery.md](core/discovery.md) |
| K-003 | C | When needing to know **mandatory baseline standards** for any agent-driven repository | [core/README.md](core/README.md) |
| K-004 | C | When needing to **select an architecture profile** matching project requirements | [profiles/README.md](profiles/README.md) |
| K-005 | C | When checking "what is wrong with project", before opening PR, or analyzing `project-review.md` | [scripts/README.md](scripts/README.md) |
| K-006 | C | When opening **untrusted repos/files**, handling `SAFE-` security warnings, or prompt injection | [core/untrusted-content.md](core/untrusted-content.md) |
| K-007 | C | When needing to understand **Zero-Clone remote mechanics and Hosted Agent Brain** architecture | [HOW_IT_WORKS.md](HOW_IT_WORKS.md) |

## 2. Working Standards (Core)
| ID | Tier | When to use | Document |
| :-- | :-: | :-- | :-- |
| S-001 | C | Writing code: naming, explicit error handling, defensive crash guards, zero hardcoded values | [core/standards/coding-conventions.md](core/standards/coding-conventions.md) |
| S-002 | C | Designing automated tests, resolving test gaps, choosing test levels (unit/integration/e2e) | [core/standards/test-strategy.md](core/standards/test-strategy.md) |
| S-003 | C | Verification criteria before reporting "Done" or opening PR | [core/standards/definition-of-done.md](core/standards/definition-of-done.md) |
| S-004 | C | Repeated bug fixes, surface patching, or untangling spaghetti code | [knowledge-base/tu-duy/anti-patching-architectural-thinking.md](knowledge-base/tu-duy/anti-patching-architectural-thinking.md) |
| S-005 | L | Avoiding common pitfalls and anti-patterns when collaborating with AI agents | [knowledge-base/technical-book/anti-patterns/common-mistakes.md](knowledge-base/technical-book/anti-patterns/common-mistakes.md) |
| S-006 | P | When Agent is **caught in a debugging doom loop**, where fixes produce new errors and corrupt architecture | [profiles/playbooks/anti-doom-loop-guide.md](profiles/playbooks/anti-doom-loop-guide.md) |

## 3. Architecture Profiles
| ID | Tier | When to use | Document |
| :-- | :-: | :-- | :-- |
| A-001 | P | Small MVPs, student projects, prototypes, simple CRUD | [profiles/architecture/simple-layered.md](profiles/architecture/simple-layered.md) |
| A-002 | P | Complex business logic, framework-independent domain models, long-term evolvability | [profiles/architecture/clean-architecture.md](profiles/architecture/clean-architecture.md) |
| A-003 | P | Target folder layout for Clean Architecture in .NET / Python / TypeScript | [profiles/architecture/clean-architecture-layout.md](profiles/architecture/clean-architecture-layout.md) |
| A-004 | P | Systems with multiple independent, feature-sliced capabilities developed in parallel | [profiles/architecture/vertical-slice.md](profiles/architecture/vertical-slice.md) |
| A-005 | P | Monolithic systems growing in scale requiring strict bounded contexts and module boundaries | [profiles/architecture/modular-monolith.md](profiles/architecture/modular-monolith.md) |
| A-006 | P | Selecting and cross-referencing design patterns, refactoring code | [profiles/patterns/design-patterns-catalog.md](profiles/patterns/design-patterns-catalog.md) |
| A-007 | L | Macro system design, C4 diagrams, distributed architectures | [knowledge-base/technical-book/architecture/system-design.md](knowledge-base/technical-book/architecture/system-design.md) |
| A-008 | P | Writing or updating **system architecture documentation** (components, key flows) | [profiles/documentation/system-architecture.md](profiles/documentation/system-architecture.md) |

## 4. UI & Design Systems (Profile)
| ID | Tier | When to use | Document |
| :-- | :-: | :-- | :-- |
| D-001 | P | Building scalable React frontend with feature-based modular structure | [profiles/frontend/bulletproof-react.md](profiles/frontend/bulletproof-react.md) |
| D-002 | P | Scaffolding frontend starter codebase (Vite + React + TS + Tailwind) | [profiles/frontend/starter/README.md](profiles/frontend/starter/README.md) |
| D-003 | P | Selecting UI archetype presets, light/dark themes, and design tokens | [profiles/design/ui-ux-archetypes-and-presets.md](profiles/design/ui-ux-archetypes-and-presets.md) |
| D-004 | P | Browsing UI aesthetic archetype catalog | [profiles/design/design-archetypes-catalog.md](profiles/design/design-archetypes-catalog.md) |
| D-005 | P | Prompts for generating matching visual styles and design tokens | [profiles/design/visual-dna-prompts.md](profiles/design/visual-dna-prompts.md) |
| D-006 | P | When translating screenshots or UI references into code without falling into visual doom loops | [profiles/design/screenshot-to-code-reverse-engineering.md](profiles/design/screenshot-to-code-reverse-engineering.md) |

## 5. AI & LLM Applications (Profile)
| ID | Tier | When to use | Document |
| :-- | :-: | :-- | :-- |
| I-001 | P | Building apps with Agents, tool calling, RAG, MCP; evaluating quality (evals) | [profiles/ai-apps/agentic-patterns-and-evals.md](profiles/ai-apps/agentic-patterns-and-evals.md) |
| I-002 | L | Reference RAG patterns and vector search templates | [knowledge-base/technical-book/patterns/rag-pattern.md](knowledge-base/technical-book/patterns/rag-pattern.md) |

## 6. Agent Configuration: Rules, Skills, MCP
| ID | Tier | When to use | Document |
| :-- | :-: | :-- | :-- |
| G-001 | C | Configuring multi-tool agent setups (Claude Code, Codex, Antigravity, Cursor) | [knowledge-base/technical-book/agent-practices/multi-tool-config.md](knowledge-base/technical-book/agent-practices/multi-tool-config.md) |
| G-002 | L | Managing agent context window drift during long conversations | [knowledge-base/technical-book/agent-practices/context-management.md](knowledge-base/technical-book/agent-practices/context-management.md) |
| G-003 | L | Applying security guardrails and execution limits for agents | [knowledge-base/technical-book/agent-practices/guardrails.md](knowledge-base/technical-book/agent-practices/guardrails.md) |
| G-004 | L | Authoring effective instructions and prompts for Claude Code | [knowledge-base/claude-code.md](knowledge-base/claude-code.md) |
| G-005 | P | When needing to **select and configure curated skills for Agent** by domain/stack without web searching | [profiles/skills-catalog/curated-agent-skills.md](profiles/skills-catalog/curated-agent-skills.md) |
| G-006 | P | When needing to **select and configure MCP Servers (Model Context Protocol)** to connect production tools | [profiles/agent-configs/curated-mcp-matrix.md](profiles/agent-configs/curated-mcp-matrix.md) |
| G-007 | P | When needing to **look up authoritative ecosystem tools, keywords, and precision search queries** | [profiles/knowledge-map/agent-ecosystem-taxonomy.md](profiles/knowledge-map/agent-ecosystem-taxonomy.md) |

## 7. Infrastructure, Documentation, Governance
| ID | Tier | When to use | Document |
| :-- | :-: | :-- | :-- |
| T-001 | P | Free-tier cloud infrastructure stack for small MVPs | [profiles/stacks/cloud-free-tier-stack.md](profiles/stacks/cloud-free-tier-stack.md) |
| T-002 | P | Running local Postgres & Redis via Docker Compose | [profiles/stacks/postgres-redis.docker-compose.yml](profiles/stacks/postgres-redis.docker-compose.yml) |
| T-003 | L | Docker packaging and CI/CD pipelines | [knowledge-base/technical-book/devops/docker-cicd.md](knowledge-base/technical-book/devops/docker-cicd.md) |
| T-004 | L | Production deployment guide | [profiles/documentation/deployment-guide.md](profiles/documentation/deployment-guide.md) |
| T-005 | P | When preparing to **deploy product to real production (Go-Live / Production Deploy)**, beyond localhost | [profiles/deployment/go-live-production-checklist.md](profiles/deployment/go-live-production-checklist.md) |
| O-001 | P | Authoring user and operational documentation via Diátaxis framework and incident runbooks | [profiles/documentation/documentation-and-pitch-standards.md](profiles/documentation/documentation-and-pitch-standards.md) |
| O-002 | L | Pitch deck and investor presentation templates | [templates/pitch-deck/pitch-deck-template.md](templates/pitch-deck/pitch-deck-template.md) |
| O-003 | L | Project management, sprint workflows, and retrospectives | [knowledge-base/quan-tri-du-an/README.md](knowledge-base/quan-tri-du-an/README.md) |
| O-004 | C | Establishing project roadmap, backlog, and sprint boards | [core/templates/planning/roadmap.md](core/templates/planning/roadmap.md) |
| O-005 | L | Environment debugging and common runtime issue troubleshooting | [knowledge-base/technical-book/troubleshooting.md](knowledge-base/technical-book/troubleshooting.md) |
| O-006 | P | Categorizing docs via **Diátaxis** (tutorial, how-to, reference, explanation) | [profiles/documentation/guides/diataxis-framework-guide.md](profiles/documentation/guides/diataxis-framework-guide.md) |
| O-007 | P | Operational incident triage runbook template | [profiles/documentation/guides/incident-runbook-template.md](profiles/documentation/guides/incident-runbook-template.md) |
| O-008 | P | End-user application guide template | [profiles/documentation/guides/user-guide-template.md](profiles/documentation/guides/user-guide-template.md) |
| O-009 | P | Onboarding guide template for new team members | [profiles/documentation/guides/developer-onboarding-guide.md](profiles/documentation/guides/developer-onboarding-guide.md) |
