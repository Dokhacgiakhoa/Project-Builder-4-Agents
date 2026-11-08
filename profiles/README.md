---
id: K-004
type: router
when: "When needing to **select an architecture profile** matching project requirements"
---
# SELECTING PROJECT PROFILES: ARCHITECTURE, PATTERNS & GUARDRAILS

> For AI Agents. `core/` is universally mandatory. This document guides the selection of **custom profiles** from signals in `docs/project-brief.md` or conversation. **Never quiz users on academic terminology** (e.g., "Do you prefer Clean Architecture?"). Infer from project characteristics, suggest one path with a one-sentence rationale, and confirm.

## 1. Selecting Architecture from Project Signals
Evaluate top-to-bottom; stop at the first matching row.

| Signal in Requirements | Select Profile | Document | Counter-signal (Do NOT choose) |
| :-- | :-- | :-- | :-- |
| Demo, student project, quick MVP, solo developer, CRUD | **Simple Layered** | [architecture/simple-layered.md](architecture/simple-layered.md) | Complex domain logic, multi-year lifespan |
| Multiple independent features developed concurrently | **Vertical Slice** | [architecture/vertical-slice.md](architecture/vertical-slice.md) | Features share heavily coupled core entities |
| Multiple distinct sub-domains, scaling team, strict bounded contexts | **Modular Monolith** | [architecture/modular-monolith.md](architecture/modular-monolith.md) | Small single-purpose app; or microservices required |
| Complex enterprise logic, framework-independent domain models | **Clean Architecture** | [architecture/clean-architecture.md](architecture/clean-architecture.md) | Simple CRUD or prototype |

If ambiguous: **choose the simpler pattern** (Layered for small apps, Clean for real business domains). Upgrading via an ADR later is superior to premature over-engineering.

## 2. Selecting Guardrail Levels
Guardrails are automated constraints the Agent configures so architecture is not eroded as code expands.

| Level | Components | Target Use Case |
| :-- | :-- | :-- |
| **M1** | Working lint + test + build commands; automated CI | Simple Layered |
| **M2** | M1 + boundary enforcement (package split or lint rules prohibiting cross-boundary imports) | Vertical Slice, Clean Architecture |
| **M3** | M2 + mandatory ADRs for contract changes, architectural tests in CI | Modular Monolith, multi-agent projects |

## 3. Supplementary Profiles
| If project requires... | Add Profile | Document |
| :-- | :-- | :-- |
| React web application | Frontend | [frontend/bulletproof-react.md](frontend/bulletproof-react.md), starter [frontend/starter](frontend/starter/README.md) |
| Distinct UI aesthetics & theme tokens | Design System | [design/ui-ux-archetypes-and-presets.md](design/ui-ux-archetypes-and-presets.md) |
| LLMs, Agents, RAG, or MCP tools | AI Applications | [ai-apps/agentic-patterns-and-evals.md](ai-apps/agentic-patterns-and-evals.md) |
| Zero operational cost | Free Tier Stack | [stacks/cloud-free-tier-stack.md](stacks/cloud-free-tier-stack.md) |
| User guides, runbooks, onboarding | Documentation | [documentation/documentation-and-pitch-standards.md](documentation/documentation-and-pitch-standards.md) |

**Design Patterns**: Never pre-select patterns. Consult [patterns/design-patterns-catalog.md](patterns/design-patterns-catalog.md) only when solving concrete structural challenges.

## 4. Record Decision (Mandatory)
1. Architecture ADR: Record signals observed, chosen profile, discarded alternatives, and guardrail level.
2. Update `.builder/kit.json`: `profiles.architecture` (`simple-layered`, `clean-architecture`, `vertical-slice`, `modular-monolith`).
3. Obtain user confirmation before code scaffolding.

## 5. Architectural Drift Indicators (Upgrade/Downgrade via ADR)
| Indicator | Transition Path |
| :-- | :-- |
| Domain tests require running databases; service layer bloats | Layered $\rightarrow$ Clean Architecture |
| Adding one feature requires modifying multiple disparate layers | Layered $\rightarrow$ Vertical Slice |
| Slices cross-import each other; `shared/` directory explodes | Vertical Slice $\rightarrow$ Modular Monolith |
| Excessive boilerplate: small changes require 5 files across abstraction layers | Clean $\rightarrow$ Simple Layered or Vertical Slice |
