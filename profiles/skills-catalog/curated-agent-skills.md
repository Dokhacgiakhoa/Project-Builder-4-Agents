---
id: G-005
type: reference
when: "When needing to **select and configure curated skills for Agent** by domain/stack without web searching"
---

# CURATED AGENT SKILLS MATRIX (ZERO-WEB TOKEN OPTIMIZED)

> **Exclusively for AI Coding Agents**: The internet contains millions of scattered, untested skills and prompts. Searching online wastes tens of thousands of tokens, exposes workspaces to malicious code, and risks severe hallucination. This document provides a battle-tested, curated catalog of pure-text skills (in standard `SKILL.md` format) categorized by domain and lifecycle.
> The Agent inspects user requirements, selects relevant skills, and writes `.agents/skills/<skill-name>/SKILL.md` (or `.claude/skills/`) directly into the target project workspace.

---

## 1. Quick Skill Lookup Matrix

| Project Domain / Problem Statement | Recommended Agent Skill | Core Responsibility |
| :-- | :-- | :-- |
| **All Projects (Core Baseline)** | `health-check`<br>`spec-first-task`<br>`kit-consult` | Code health audits, spec-first planning, remote kit consultation |
| **Database & Persistence Layer** | `db-migration-guardian` | Safe schema migrations, anti-N+1 queries, data access isolation |
| **External API / Third-Party Calls** | `defensive-api-client` | Centralized client: timeouts, exponential retries, rate limits, error normalization |
| **Frontend / Web UI Reliability** | `error-boundary-guard`<br>`state-management-architect` | White-screen crash prevention, render optimization, unidirectional state |
| **Authentication & Authorization** | `auth-rbac-guardian` | HttpOnly cookies, session security, role-based access control (RBAC) |
| **Packaging & Production Deployment** | `docker-production-packager`<br>`cloud-free-tier-deployer` | Multi-stage non-root containers, zero-cost cloud deployment (Vercel/Railway/Supabase) |
| **Repeated Bugs / Spaghetti Code** | `anti-patching-debugger` | Root-cause analysis, anti-patching architectural discipline |
| **Automated Verification** | `e2e-scenario-tester` | User journey end-to-end testing scenarios |
| **AI / LLM / RAG Integration** | `rag-agentic-builder` | Safe chunking, vector embeddings, prompt templates, structured tool calls |
| **SaaS Billing & Subscriptions** | `stripe-payment-integration` | Stripe Checkout, cryptographic webhook validation, idempotent transaction handling |
| **Supabase BaaS Backend** | `supabase-rls-architect` | Row Level Security (RLS) policies, multi-tenant data separation |
| **SEO & Discoverability** | `seo-metadata-optimizer` | OpenGraph tags, JSON-LD structured data, canonical URLs, robots.txt, sitemap |
| **Web Performance & Page Speed** | `core-web-vitals-booster` | LCP/CLS/FID optimization, responsive WebP/AVIF imagery, font preloading |
| **Anti-Doom-Loop Prevention** | `git-micro-checkpoint-guard` | Automated green commit checkpoints per step, instantaneous rollback |
| **Tool & Environment Integration** | `mcp-server-configurator` | Secure Model Context Protocol (MCP) server configuration |

---

## 2. Skill Specifications (Direct Injection Ready)

### Skill 1: `anti-patching-debugger`
**Path**: `.agents/skills/anti-patching-debugger/SKILL.md`
```markdown
---
name: anti-patching-debugger
description: Activates when fixing the same bug for the 2nd time or when codebase complexity increases. Forces the Agent to halt superficial patching and address architectural root causes.
---
# Anti-Patching Debugger
1. STOP IMMEDIATELY if you are attempting to patch an error for the 2nd time by adding arbitrary flags, quick if/else conditionals, or empty try/catch blocks.
2. Identify Root Cause: Which layer originated the faulty state (UI state, Domain Service, or Data Access)? Is there a contract violation or type mismatch?
3. Review relevant architectural boundaries in `profiles/architecture/`.
4. Refactor at the source layer: Write a failing unit test reproducing the bug before modifying application logic.
```

### Skill 2: `defensive-api-client`
**Path**: `.agents/skills/defensive-api-client/SKILL.md`
```markdown
---
name: defensive-api-client
description: Use when the application integrates external HTTP APIs or creates a centralized network client. Enforces timeouts, error normalization, and retry mechanisms.
---
# Defensive API Client
1. Never call bare `fetch()` or `axios()` inside UI components. Wrap all calls in a centralized client module.
2. Every outbound request MUST specify an explicit timeout (default: 8000ms).
3. Validate and parse response payloads using schemas (e.g., Zod, Pydantic, or typed DTOs). Never trust external JSON structures blindly.
4. Normalize errors into standard application domain errors (`NetworkError`, `AuthenticationError`, `ValidationError`).
5. Implement exponential backoff retry exclusively for idempotent methods (GET, PUT, DELETE) on 5xx status codes.
```

### Skill 3: `db-migration-guardian`
**Path**: `.agents/skills/db-migration-guardian/SKILL.md`
```markdown
---
name: db-migration-guardian
description: Use when altering database schemas, writing ORM migrations, or optimizing SQL queries. Enforces safety and data integrity.
---
# Database Migration Guardian
1. Never execute destructive DDL commands (`DROP TABLE`, `DROP COLUMN`) directly in production without a 2-step deprecation cycle.
2. Always write migrations with both `up` and `down` rollback scripts.
3. Every Foreign Key column MUST include an index to prevent table-scan performance degradation.
4. Prevent N+1 query patterns: Use eager loading, SQL JOINs, or DataLoader for relational queries.
5. Store all sensitive data (passwords, tokens) using salted cryptographic hashing (e.g., Argon2, bcrypt).
```

### Skill 4: `error-boundary-guard`
**Path**: `.agents/skills/error-boundary-guard/SKILL.md`
```markdown
---
name: error-boundary-guard
description: Use when building frontend interfaces to eliminate white-screen crashes and guarantee graceful degradation.
---
# Error Boundary Guard
1. Wrap top-level route layouts and async UI components in structured React Error Boundaries.
2. Fallback UI must provide: A friendly localized error message, an actionable "Retry" button, and home navigation.
3. Catch and log unhandled promise rejections and client-side runtime errors to monitoring services.
4. Ensure components return valid fallback skeleton loaders or null instead of crashing during undefined state rendering.
```

### Skill 5: `auth-rbac-guardian`
**Path**: `.agents/skills/auth-rbac-guardian/SKILL.md`
```markdown
---
name: auth-rbac-guardian
description: Use when implementing user authentication, session cookies, JWT handling, and role-based access control.
---
# Auth & RBAC Guardian
1. Never store sensitive JWTs or session tokens in browser `localStorage` or `sessionStorage` (XSS vulnerable).
2. Store auth tokens exclusively in `HttpOnly`, `Secure`, `SameSite=Strict` cookies.
3. Validate user permissions on both Frontend (UI gating) and Backend (mandatory endpoint authorization).
4. Apply rate limiting on authentication routes (`/api/login`, `/api/forgot-password`) to prevent brute-force attacks.
5. Invalidate sessions server-side immediately upon logout.
```

### Skill 6: `state-management-architect`
**Path**: `.agents/skills/state-management-architect/SKILL.md`
```markdown
---
name: state-management-architect
description: Use when architecting client-side application state. Prevents unnecessary re-renders and uncontrolled global stores.
---
# State Management Architect
1. Separate Server State (TanStack Query / SWR / caching) from Client UI State (modals, active tabs, drawer toggles).
2. Keep component state local (`useState`) unless at least two distant tree nodes require read/write access.
3. For global state, use atomic or slice-based stores (Zustand) with shallow selectors to prevent global re-renders.
4. State mutations must be immutable; never mutate arrays or objects directly in state.
```

### Skill 7: `docker-production-packager`
**Path**: `.agents/skills/docker-production-packager/SKILL.md`
```markdown
---
name: docker-production-packager
description: Use when containerizing applications for production deployment. Generates secure, minimal, multi-stage Dockerfiles.
---
# Docker Production Packager
1. Always implement multi-stage Docker builds: Separate `builder` stage from minimal `runner` image (Alpine/Distroless).
2. Never run containers as `root`: Create and enforce a non-root user (`USER nonroot` or `USER node`).
3. Leverage Docker layer caching: Copy dependency manifests (`package.json`, `requirements.txt`) before copying source code.
4. Include a valid `.dockerignore` excluding `.git`, `node_modules`, `.env`, tests, and local build artifacts.
5. Expose health checks via `HEALTHCHECK` instruction.
```

### Skill 8: `cloud-free-tier-deployer`
**Path**: `.agents/skills/cloud-free-tier-deployer/SKILL.md`
```markdown
---
name: cloud-free-tier-deployer
description: Use when deploying applications to zero-cost cloud platforms (Vercel, Railway, Supabase, Cloudflare Pages).
---
# Cloud Free-Tier Deployer
1. Review resource constraints: Keep RAM < 512MB and prevent long-running background CPU processes.
2. Route static assets to CDN edge networks to minimize backend container bandwidth.
3. Configure environment variables securely on host dashboard; never commit production credentials.
4. Implement automatic connection pooling (e.g., Supabase PgBouncer) for serverless database connections.
```

### Skill 9: `e2e-scenario-tester`
**Path**: `.agents/skills/e2e-scenario-tester/SKILL.md`
```markdown
---
name: e2e-scenario-tester
description: Use when creating end-to-end integration tests for critical business workflows using Playwright or Cypress.
---
# E2E Scenario Tester
1. Focus E2E tests strictly on critical user journeys (e.g., Signup $\rightarrow$ Checkout $\rightarrow$ Order Confirmation).
2. Use stable test selectors (`data-testid="submit-btn"`) instead of fragile CSS classes or dynamic IDs.
3. Run test suites with headless browsers in CI pipelines before production merges.
4. Isolate test fixtures and reset database state cleanly between test runs.
```

### Skill 10: `rag-agentic-builder`
**Path**: `.agents/skills/rag-agentic-builder/SKILL.md`
```markdown
---
name: rag-agentic-builder
description: Use when building Retrieval-Augmented Generation (RAG) pipelines, semantic vector search, or autonomous tool-calling agents.
---
# RAG & Agentic Builder
1. Split source documents into semantic chunks (300-500 tokens) with 10-20% chunk overlap.
2. Store vector embeddings with metadata (source ID, timestamp, access level) in PostgreSQL (`pgvector`) or vector stores.
3. Enforce defensive system prompts: Instruct LLMs to explicitly declare when retrieved context is insufficient to answer.
4. Validate all tool-call outputs using strict JSON schemas before executing real functions.
```

### Skill 11: `stripe-payment-integration`
**Path**: `.agents/skills/stripe-payment-integration/SKILL.md`
```markdown
---
name: stripe-payment-integration
description: Use when integrating payment processing with Stripe. Ensures cryptographic webhook security and idempotent processing.
---
# Stripe Payment Integration
1. Never pass raw credit card data through your backend servers. Utilize Stripe Checkout or Stripe Elements.
2. Webhook endpoints MUST cryptographically verify signatures using `stripe.webhooks.constructEvent()` and raw body buffer.
3. Implement database idempotency keys to ensure duplicate webhook deliveries do not double-charge or duplicate orders.
4. Handle payment intent statuses explicitly: `succeeded`, `requires_action`, `payment_failed`.
```

### Skill 12: `supabase-rls-architect`
**Path**: `.agents/skills/supabase-rls-architect/SKILL.md`
```markdown
---
name: supabase-rls-architect
description: Use when architecting PostgreSQL tables in Supabase. Enforces strict Row Level Security (RLS) policies.
---
# Supabase RLS Architect
1. Enable Row Level Security on every newly created table: `ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;`.
2. Restrict operations by user identity: `USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);`.
3. Separate public read data from authenticated modification data via dedicated policies.
4. Never expose `service_role` key on the client; use `anon` key only with RLS enabled.
```

### Skill 13: `seo-metadata-optimizer`
**Path**: `.agents/skills/seo-metadata-optimizer/SKILL.md`
```markdown
---
name: seo-metadata-optimizer
description: Use when optimizing web applications for search engine indexing and social media rich cards.
---
# SEO Metadata Optimizer
1. Provide unique `<title>` (50-60 chars) and `<meta name="description">` (150-160 chars) per route.
2. Implement OpenGraph tags (`og:title`, `og:description`, `og:image`, `og:url`) and Twitter Cards.
3. Set canonical URL tags (`<link rel="canonical" href="..." />`) to eliminate duplicate content penalties.
4. Provide automated `sitemap.xml` and standard `robots.txt` endpoints at domain root.
```

### Skill 14: `core-web-vitals-booster`
**Path**: `.agents/skills/core-web-vitals-booster/SKILL.md`
```markdown
---
name: core-web-vitals-booster
description: Use when optimizing frontend loading speed and responsiveness to achieve top Google PageSpeed scores.
---
# Core Web Vitals Booster
1. Optimize Largest Contentful Paint (LCP < 2.5s): Preload priority hero images with `<link rel="preload" as="image">`.
2. Eliminate Cumulative Layout Shift (CLS < 0.1): Always define explicit `width` and `height` on images and media frames.
3. Modern Image Formats: Serve images in next-gen WebP or AVIF formats with responsive `srcset`.
4. Defer non-critical JavaScript scripts (`defer` or `async`) and self-host web fonts with `font-display: swap`.
```

### Skill 15: `git-micro-checkpoint-guard`
**Path**: `.agents/skills/git-micro-checkpoint-guard/SKILL.md`
```markdown
---
name: git-micro-checkpoint-guard
description: Prevents Vibe Coding Doom Loops. Creates atomic green Git checkpoints after each successful step for instant rollback.
---
# Git Micro-Checkpoint Guard
1. Before starting a new task, ensure working tree is clean.
2. As soon as a step compiles and tests pass green: Create a micro-commit: `git commit -m "checkpoint: <step-summary>"`.
3. If an unexpected failure occurs and 2 fix attempts fail: Rollback to the previous green commit: `git reset --hard HEAD~1`.
4. Never accumulate large uncommitted changes across multiple architectural boundaries.
```

### Skill 16: `mcp-server-configurator`
**Path**: `.agents/skills/mcp-server-configurator/SKILL.md`
```markdown
---
name: mcp-server-configurator
description: Use when configuring Model Context Protocol (MCP) servers for Claude Desktop, Cursor, or Windsurf environments.
---
# MCP Server Configurator
1. Store server definitions in project configuration file (`.cursor/mcp.json` or `.windsurf/mcp.json`).
2. Never hardcode API keys directly into MCP configuration JSON; reference environment variables (`${GITHUB_TOKEN}`).
3. Grant minimal required filesystem tool scopes (restrict paths strictly to target project directory).
4. Verify server responsiveness immediately upon registration.
```
