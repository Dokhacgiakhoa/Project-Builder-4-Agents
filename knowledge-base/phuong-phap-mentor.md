# AI Product Engineering Methodology — Notes from Mentor Sessions

> Reusable engineering methodology extracted from mentor guidelines. Technical mentors serve as high-weight references for engineering decisions.

## 1. AI Engineering & Product Lifecycle
- **3 Pillars:** Backend (gateway, services, message queues, databases, caches) · AI Systems (LLMs, RAG pipelines, agents, fine-tuning, evals) · Ops (containers, CI/CD, GPUs, model serving, telemetry). AI is a system (LLMs + planning + tools + state/memory + retrieval), not merely an isolated model.
- **Operations Landscape:** DevOps (platform health) · MLOps (model lifecycle) · LLMOps (gateway routing, prompt versioning, distributed tracing, production evals).
- **Team Dynamics with Coding Agents:** Teams become leaner; software engineers shift toward orchestration, architecture review, and spec-setting. QA boundaries shift left to developers; engineering leverage concentrates on requirements and system design.
- **Sprint Lifecycle:** Problem Discovery → Planning → Technical Design → AI-Assisted Implementation → Code Review → Automated Testing → Deployment → Production Monitoring. Requirements evolving mid-sprint is normal; technical design docs should be concise (1–2 pages). Any emergency hotfix mandates a root-cause postmortem.
- **Deployment Environments:** Local Dev → Test → Staging/UAT → Production. Guardrails and deployment permissions tighten with each successive tier.

## 2. From Vision to Requirements (Product Ownership)
- Ground every initiative in target users and measurable pain points. Address 5 core questions: Who is the user? What is the measurable pain point? How is it handled today? How much better is this solution? Is it worth prioritizing (Impact × Confidence / Effort)?
- **Persona Definition:** User segment + operational context + existing tooling/workflows + core objectives + technical literacy + peripheral stakeholders. MVPs should focus on a single primary persona supported by 3–5 real user interviews.
- **Pain Point Formalization:** `[Actor]` performing `[Task]` through `[Current Workflow]` encounters `[Failure]` resulting in `[Cost × Frequency]` backed by concrete evidence and root-cause analysis.
- **Input Specifications:** Scope all user/data inputs across 6 dimensions: Format · Payload Size · Language/Encoding · Quality/Noise · Volume/Throughput · Source System. Collect real sample files early.
- **Mini-PRD Structure (What & Why, not How):** Problem Statement · SMART Goals · Explicit Non-Goals · Target Persona · User Stories & Acceptance Criteria (AC) · Non-Functional Requirements · MoSCoW Scoping (`Must` = MVP) · Open Questions with assigned owners and resolution deadlines.
- **PRD Definition of Done:** Complete · Unambiguous · Measurable · Testable · Feasible · Prioritized · Aligned. Validate using the "explain-back" and "test-case derivation" checks. Red flags: adjectives without numbers, premature technical implementations, missing non-goals.
- **Scope Trimming:** Trim feature depth rather than horizontal workflow steps: 3–5 Must-have capabilities, each with 4–6 ACs including unhappy error paths. Team capacity: `Features × Estimates ≤ Team Velocity × Remaining Days`.
- **User Stories:** `As a [role], I want [action] so that [benefit]`. Acceptance criteria in Given/When/Then format. Follow INVEST criteria. Stories estimated > 3–4 days must be split (SPIDR). Maintain bi-directional traceability and 3 Amigos alignment.

## 3. System Architecture & Technical Design (Tech Lead)
- Design before code. Evaluate 5 structural questions: What are the workload characteristics? Which components are chosen and why (including rejected alternatives)? What are the module contracts? What happens on failure? Does the timeline fit team capacity?
- **Technical Design Document (1–2 pages):** Context · System Architecture Diagram · Component Rationale · API Contracts / Interfaces · Data Models · Workload Profile · Risks & Mitigations · Open Architectural Questions. An unreviewed design is not a design.
- **Architecture Diagrams:** Single responsibility per box, labeled arrows (protocols + payload types), clear sync vs. async demarcations, and explicit trust boundaries.
- **Component Selection:** Match workload characteristics (long-running jobs → background queues + workers; latency-sensitive queries → read caches + streaming). Prefer managed APIs initially. Remember: every added infrastructure component increases operational surface area.
- **Top-Down Decomposition:** Identify shared cross-cutting capabilities serving ≥ 2 features. Validate through a Feature × Component matrix.
- **Avoid Over-Engineering:** Avoid premature microservices, distributed streaming (Kafka), or complex multi-agent orchestration when simple deterministic patterns suffice. Follow the progression: Prompt Engineering → RAG → Fine-tuning. Respect YAGNI.
- **Contract-First Development:** `/v1` routes, standardized error envelopes, backward-compatible schemas, OpenAPI contracts. Frontends mock against contracts while backends build in parallel. Detailed API specs serve as high-precision prompts for AI coding agents.
- **Architecture Review Checklist:** Covers all PRD requirements · Matches workload characteristics · Identifies and mitigates Single Points of Failure (SPOF) · Defines clear contracts · Aligns with team bandwidth. Once approved, enforce **Design Freeze**: changes require documented justifications, impact assessments, and cost estimations.
- **Feature Depth ("Follow the Data"):** Every state mutation represents an architectural layer. Evaluate: Synchronous vs. Background? Failure fallbacks? User experience during latency? Idempotency and retry semantics?
- **Core Patterns:** Repository, Factory, Adapter (multi-LLM abstraction), Strategy (model routing), Orchestrator-Worker, Circuit Breaker.

## 4. Task Breakdown & Execution
- **Story Granularity:** 1 Story = 1 Actor + 1 Intent + 1 Observable Outcome. Invisible intermediate steps are implementation tasks, not user stories. Validation checks: testable ACs · demonstrable in UI/API · subtasks fit within ≤ 1 day (or mandate a 1-day exploratory spike).
- **Essential Tasks Often Missed:** Formal contract lock (start of story) · Integration assembly and E2E validation (end of story).
- **3-Tier Definition of Done:**
  - Task DoD: Code complete, unit tests pass, PR approved and merged, zero temporary TODOs.
  - Story DoD: All ACs pass verification, demonstrated on shared staging environment.
  - Feature DoD: All Must-have stories completed, eval benchmarks hit, self-service verification verified by external peers.
- **Issue Board as Source of Truth:** 1 Issue = 1 Story · Labels = Feature + MoSCoW · PRs explicitly declare "Closes #n" · Cards stagnant > 2 days must be flagged in daily standups.
- **Daily Standup:** Current focus · Completed items · Active blockers · Root cause analysis. Practice backward planning from deployment deadlines.

## 5. Development Workflow & Build Loops
- Code repository mirrors architectural diagrams. Commit `.env.example`; never commit credentials or production keys. Ensure `docker compose up` spins up the entire local development stack. Enforce CI lint and test gates on all PRs. README serves as a self-contained runbook verifiable within 15 minutes.
- **DevOps Foundations:** Infrastructure → Resilient Components → Container Runtime → CI/CD Pipelines. Multi-stage Dockerfiles without embedded secrets. Configure container restart policies (`restart: unless-stopped`) and healthcheck probes. Verification test: terminate any container and observe automated restart.
- **Continuous Integration / Continuous Deployment:** On merge to main → lint and test → build image tagged with git SHA → automated deployment to dev/staging → smoke test `/health`. Prohibit unrecorded manual production deployments.
- **Walking Skeleton First:** Establish an end-to-end path: 1 UI screen → 1 backend endpoint → 1 AI invocation → 1 database record, running in a shared environment. If this takes too long, prune scope immediately.
- **Coding Cadence with Agents:** Developer specifies interface and test harness → AI Agent generates implementation → Developer reviews diff and runs tests → Merge small, focused PRs.
- **PR Governance:** < 400 lines of diff · 1 PR = 1 focused task · Reviewed within 24 hours · Green CI required · PR description links "Closes #n" with manual testing steps. Approvers share equal responsibility with authors.
- **Mocking Strategy for Parallel Work:** Frontend mocks OpenAPI schemas; backend mocks LLM endpoints during automated tests (happy path, safety refusal, timeout); shared seed data includes dirty edge cases.

## 6. Testing, Evaluation & Reliability
- Design every module to be mockable. Test matrices: Happy path · Boundary/Edge conditions · Error handling · Concurrency · Security/Injection. Maintain a healthy pyramid: Unit tests (broadest base) → Integration tests → Manual E2E checks as final acceptance.
- **AI System Evaluation:** Raw LLM output · RAG fidelity (retrieval precision/recall, context groundedness) · Agent trajectories (task completion rate, tool call validity) · Safety guardrails (prompt injection defenses). Run golden evaluation sets through the pipeline and execute regression sweeps whenever prompts, tools, or model versions change.
- **Operational Baselines:** ≥ 2 service replicas, health probes, zero-downtime rollback via container image tags, structured logging + distributed traces + system metrics, dedicated LLM observability (Langfuse / LangSmith).
