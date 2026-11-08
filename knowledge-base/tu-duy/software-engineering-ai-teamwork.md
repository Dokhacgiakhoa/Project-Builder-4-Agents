---
title: "Software Engineering: Team + AI (Executive Summary)"
source: "SoftwareEngineeringAITeamWork.pdf — Nguyen Tri Dung (CTO, AI-native SE), AI20K Build Phase"
note: "Key insights captured for agent reference."
---

# Software Engineering: Team + AI — Core Concepts

## Core Theses
- Every engineer now commands an "AI workforce". Individual throughput skyrockets, but the fundamental challenge is how the team operates collaboratively.
- Solo experimentation (1 developer + AI) $\neq$ Production engineering (team-based). Scaling requires fundamentally restructured engineering disciplines.
- AI accelerates velocity; it **does not alter engineering laws**. AI lacks global context and optimizes solely for localized subtasks.
- Without an architectural blueprint, AI builds the wrong structure. Without shared standards, components diverge. Without coordination, collaborative construction collapses.
- Without clear workflows and architecture, AI simply enables teams to **break systems faster**.

## Process = 4-Pillar System (Missing any pillar causes drift, latency, and waste)
1. **Methodology**: Agile/Scrum, iterative verification.
2. **People & Roles**: Product Owner, Business Analyst, Designer, Software Engineer, QA. AI assistants adopt multiple roles, but human accountability must remain unambiguous.
3. **Workspace & Tooling**: Specs, ADRs, Contracts, Issue Trackers, Git, CI/CD pipelines.
4. **Workflows & Governance**: Idea → Spec → Development → Verification → Release. Enforced coding conventions, code review, Definition of Done, automated security gates.

## Big Picture Lifecycle (Iterative Sprint Loop)
Problem Definition → Specifications (Domain, Features, Roles, API Contracts, Business Invariants) → Architecture (ADRs, Stack, Folder Conventions) → Planning (Backlog, Sprints, User Stories, Estimates) → Parallel Execution (Developer + Agent pairs) → Review & Integration Merge → Retrospective.
- **Shared Foundation**: Canonical Git repository, explicit roles (Human + AI), automated tooling (CI, Linters, Test Runners, MCP servers), clear Definition of Done.
- **Context is King**: AI succeeds when context is unambiguous: Specs + ADRs + Contracts + Behavioral Rules.

## The Repository as the Single Source of Truth
- Recommended topology: `/specs` (vision, domain, roles, features, contracts) · `/adrs` · `/planning/sprints` · `/tasks/<ID>.md` · `/src` · `/docs` · `AGENTS.md` · `README.md`.
- Git tracks not only code, but also intent, architectural decisions, planning roadmaps, and contextual invariants.

## Executing Each Task
1. **Pick Task**: Review specs, relevant ADRs, API contracts, and rules. `git checkout -b feature/<ID>`.
2. **AI + Developer Pair**: Agent reads context, outlines implementation plan, and decomposes subtasks. **The Agent is an assistant; it does not replace human decision authority.**
3. **Local Verification**: Unit tests, integration suites, linting, and build validation. **Never push code that fails local checks.**
4. **Atomic Commit & Push**: Adhere strictly to Conventional Commits.
5. **Pull Request & Multi-Perspective Review**: Human or Automated Agent verifies code quality, test coverage, documentation updates, and architectural compliance.
6. **Merge Upon Approval**: CI passes all tests; task transitions to Done.
- **Branch Conventions**: `main` remains permanently deployable · `feature/*` · `hotfix/*` · `release/*`. Pull latest changes before work, keep commits granular, enforce PR reviews, tag releases.
- **Context Agents Must Read**: `/specs`, `/adrs`, `/contracts`, `/tasks/<id>.md`, `AGENTS.md`, `/src`.
- **Definition of Done (DoD)**: Implemented per spec · All tests pass · Docs/contracts updated · Conforms to ADRs and rules · PR approved and merged. **Do not merge if DoD is unmet.**

## 6 Foundational Principles
1. **Spec-Driven**: Clarify what, why, and acceptance criteria before writing code.
2. **ADRs as Foundations**: Record all architectural decisions, technology selections, and conventions. Changes require a new ADR.
3. **Task Granularity**: Frame tasks at feature level so AI can decompose subtasks. Avoid micromanaged task fragmentation.
4. **Contract-First**: Interface via explicit contracts (OpenAPI, Protobuf, Event schemas) rather than implicit assumptions.
5. **Mandatory Context Ingestion**: AI must inspect existing context before modifying files. Keeping context fresh is a collective team responsibility.
6. **Git Discipline**: Clean branches, mandatory PR reviews, fully auditable history.
- When an AI agent outputs incorrect code, the root cause is almost always missing, stale, or contradictory context.

## 5 Recommended ADRs
1. **Test Strategy / Test-First**: Tests serve as verifiable behavioral contracts.
2. **Domain Boundaries**: Clean separation (modular monolith or microservices) enables clean context boundaries.
3. **API Contract First**: OpenAPI, gRPC, event schemas, DTOs—scale through contracts, not verbal assumptions.
4. **Project Structure & Coding Conventions**: Folder layouts, naming, linting, error handling, logging, validation, commit standards. Without conventions, AI replicates chaos.
5. **Definition of Done**: "Done" means production-grade quality ready to merge, not "it compiles on my machine".
