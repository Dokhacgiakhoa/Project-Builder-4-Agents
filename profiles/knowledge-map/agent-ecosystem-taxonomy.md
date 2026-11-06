---
id: G-007
type: reference
when: "When needing to **look up authoritative ecosystem tools, keywords, and precision search queries**"
---

# AGENT ECOSYSTEM TAXONOMY & SEARCH COMPASS

> **Verification log (2026-11-07)**: coordinates for shadcn-ui/ui, Leonxlnx/taste-skill, nextlevelbuilder/ui-ux-pro-max-skill, jdan/98.css, botoxparty/XP.css, nostalgic-css/NES.css, magicuidesign/magicui, microsoft/playwright-mcp, ChromeDevTools/chrome-devtools-mcp, github/github-mcp-server, crystaldba/postgres-mcp were confirmed via the GitHub API and are active; steipete/agent-rules is archived; RonenNess/RPGUI (960 stars, last push 2023-10-08, zlib license) exists but is inactive; Aceternity UI has no official GitHub component repo found by search (copy-paste from its website). Existence and activity are not endorsements of quality.
>
> **For AI Agents**: When facing unfamiliar technical domains, naive agents guess vague search queries (`"how to make UI pretty"`), wasting tokens crawling low-quality pages. This document provides a pre-computed map of commonly referenced open-source tools (coordinates not re-verified; confirm a tool exists and is maintained before adopting it), exact repository coordinates, related search vectors, and one-hit precision queries.
> **Role in the Triad Model**: Acts as the Translator's technical dictionary, providing the AI Agent (Company) with exact industry terminology to fulfill the Vibe Coder's (Client's) intent without hallucination.

---

## 1. UI, Aesthetics & Visual Systems

| Subdomain | Authoritative Tools & Coordinates | Related Concept Vectors | Precision Search Query |
| :-- | :-- | :-- | :-- |
| **Generative Art Direction** | `Leonxlnx/taste-skill`<br>(tasteskill.dev) | `design-taste-frontend`, `DESIGN_VARIANCE`, `MOTION_INTENSITY`, `VISUAL_DENSITY` | `site:github.com "Leonxlnx/taste-skill"` |
| **Comprehensive UI/UX Intelligence** | `nextlevelbuilder/ui-ux-pro-max-skill` | Bento Grid, Glassmorphism, Neumorphism, Google Font pairings, UX guidelines | `site:github.com "nextlevelbuilder/ui-ux-pro-max-skill"` |
| **Modern Component Primitives** | `shadcn/ui`, `magicui`, Aceternity UI (copy-paste site aceternity.com; no official component repo found) | Radix primitives, Tailwind CSS v4, accessible ARIA, unstyled headless | `site:github.com/shadcn-ui/ui` |
| **Retro & Niche Archetypes** | `98.css`, `XP.css`, `NES.css`, `RonenNess/RPGUI` | Nostalgic UI, pixel-art styling, brutalist paper CSS | `site:github.com "98.css" OR "XP.css"` |
| **Screenshot Replication** | `profiles/design/screenshot-to-code-reverse-engineering.md` | Replicative mode, Design Tokens first, 1px subtle borders (`border-white/10`), Mirror test | Local kit doc (`D-006`) |

*Search Traps to Avoid*: Do not search generic terms like `"clean modern UI"`. Query exact package names and token standards.

---

## 2. Agent Governance, Discipline & Guardrails

| Subdomain | Authoritative Tools & Coordinates | Related Concept Vectors | Precision Search Query |
| :-- | :-- | :-- | :-- |
| **Multi-Agent Coding Rules** | `steipete/agent-rules`<br>(Peter Steinberger; repo archived, last push 2026-05-03) | `agentic engineering`, parallel coding agents, non-destructive git, standing brief | `site:github.com/steipete/agent-rules` |
| **Native Context Ingestion** | Anthropic Claude Code `CLAUDE.md`<br>Cursor `.cursor/rules/*.mdc` | Progressive disclosure, 100-token discovery frontmatter, single source of truth | `site:anthropic.com "CLAUDE.md" standing brief` |
| **Anti-Doom-Loop Enforcement** | `profiles/playbooks/anti-doom-loop-guide.md` | Spec-First Loop, CI Green Loop, Git Micro-Checkpoint Loop, 2-attempt circuit breaker | Local kit doc (`S-006`) |
| **Prompt Injection Defense** | `core/untrusted-content.md` | `SAFE-001`…`SAFE-005`, zero-width characters, hidden HTML comments, unverified MCP hooks | Local kit doc (`K-006`) |

*Search Traps to Avoid*: Avoid prompt-only collections with empty slogans ("be a 10x engineer"). Focus on deterministic constraint frameworks.

---

## 3. Architecture, Clean Code & Quality Auditing

| Subdomain | Authoritative Tools & Coordinates | Related Concept Vectors | Precision Search Query |
| :-- | :-- | :-- | :-- |
| **Static Codebase Auditor** | `scripts/project_auditor.py`<br>(Project Health Check) | offline static scan (no model calls): file-tree and regex heuristics, partial architecture-boundary and hardcoded-secret checks, 0-100 score | Local kit tool (`K-005`) |
| **Clean Architecture & DDD** | `profiles/architecture/clean-architecture.md` | Concentric layers, inward dependency rule, rich domain models, composition root | Local kit doc (`A-002`) |
| **Feature-First Architecture** | `profiles/architecture/vertical-slice.md` | Vertical slice, Jimmy Bogard, zero cross-slice imports, rule of three | Local kit doc (`A-004`) |
| **Root-Cause Debugging** | `knowledge-base/tu-duy/anti-patching-architectural-thinking.md` | Anti-patching mindset, surface fix vs architectural fix, regression test first | Local kit doc (`S-004`) |

---

## 4. Browser Automation, Visual QA & Model Context Protocol (MCP)

| Subdomain | Authoritative Tools & Coordinates | Related Concept Vectors | Precision Search Query |
| :-- | :-- | :-- | :-- |
| **Browser Visual Inspection** | `@playwright/mcp`<br>`chrome-devtools-mcp` | Headless browser, DOM snapshot, visual diff, screenshot comparison, page audit | `site:github.com "microsoft/playwright-mcp"` |
| **Database Direct Query MCP** | `crystaldba/postgres-mcp` (use `--access-mode=restricted`) | Schema introspection, foreign key verification, index analysis, read-only mode | `site:github.com "crystaldba/postgres-mcp"` |
| **GitHub Automation MCP** | `github/github-mcp-server` | Issue triage, PR generation, tree inspection, branch protection | `site:github.com "github/github-mcp-server"` |

*Search Traps to Avoid*: Never download untrusted MCP servers executing arbitrary binary shell commands without verifying the publisher.

---

## 5. Persistence, Auth & Cloud Infrastructure

| Subdomain | Authoritative Tools & Coordinates | Related Concept Vectors | Precision Search Query |
| :-- | :-- | :-- | :-- |
| **Serverless Database & RLS** | `Supabase PostgreSQL`, `Turso SQLite` | Row Level Security (RLS) policies, PgBouncer pooling (port 6543), edge replication | `site:supabase.com "Row Level Security"` |
| **Defensive API Clients** | `profiles/skills-catalog/curated-agent-skills.md` | Explicit 8000ms timeout, Zod/Pydantic validation, exponential backoff, error normalization | Local kit doc (`G-005`) |
| **Secure Authentication** | `HttpOnly Cookie Auth` | Zero JWT in localStorage, SameSite=Strict, CSRF tokens, session invalidation | `site:owasp.org "JSON Web Token Cheat Sheet"` |
| **Production Packaging** | Docker Multi-Stage Builds | Non-root `appuser`, Alpine/Distroless runner image, layer caching, zero-secret images | Local kit doc (`T-005`) |
| **Free-Tier Cloud Hosting** | Vercel, Cloudflare Pages, Railway, Render | Free-tier RAM limits (<512MB), edge routing, GitHub continuous deployment | Local kit doc (`T-001`) |

---

## 6. Two-Tier Precision Search Protocol (Token Guard)

When an Agent needs to verify or retrieve an external technical dependency:
1. **Tier 1 (Lookup Without Web Search)**: Consult this taxonomy table first. If the tool coordinates and architectural constraints are already listed, proceed immediately without searching.
2. **Tier 2 (Targeted Single-Hit Query)**: If documentation details or updated installation commands are required, execute **exactly one query** using the Precision Search Query pattern above. Never crawl more than 2 pages.
