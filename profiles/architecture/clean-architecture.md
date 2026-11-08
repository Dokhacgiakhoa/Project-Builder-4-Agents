---
id: A-002
type: decision
when: "Complex business logic, framework-independent domain models, long-term evolvability"
not_when: "Small demos, simple CRUD, solo prototypes with minimal business logic"
---
# PROFILE: CLEAN ARCHITECTURE (+ OPTIONAL DDD)

## When to choose
* Rich enterprise business rules requiring consistent invariants across a long product lifecycle.
* Need to execute high-speed unit tests on core business logic without spinning up databases or HTTP web servers.
* Infrastructure volatility (anticipating swaps of database, cloud providers, or UI frameworks).

## When not to choose
* Demos, prototypes, simple CRUD: use [simple-layered.md](simple-layered.md); DTO and interface boilerplate exceeds benefits.
* Systems best structured around independent feature workflows: use [vertical-slice.md](vertical-slice.md).

## Target directory
Four concentric layers: `Domain → Application → Infrastructure → Presentation`. Detailed folder mappings for .NET / Python / TypeScript are specified in [clean-architecture-layout.md](clean-architecture-layout.md). Maintain idiomatic language naming conventions while preserving layer boundaries.

## Constraints
* **Dependency Rule: All dependencies point inward.** `Domain` must not import anything from outer layers or external frameworks. `Application` depends only on `Domain` and its own declared interfaces.
* `Domain`/`Application` defines repository interfaces; `Infrastructure` provides concrete implementations. Wire dependencies via Dependency Injection (DI) at a single **Composition Root**.
* Enforce domain invariants and state mutations **inside rich entities** (avoid anemic data bags).
* Guardrail Level M2 (see [../README.md](../README.md)): Enforce package boundaries or linting rules prohibiting inward dependency leaks.

## Adding a feature
1. Domain: Define or extend entities, value objects, domain events, and core invariants.
2. Application: Implement the use case and declare necessary repository/gateway interfaces.
3. Infrastructure: Implement repository interfaces against database or external APIs.
4. Presentation: Expose a thin HTTP endpoint that dispatches directly to the use case.
5. Automated Testing: Write domain and use case unit tests first (no database fixtures needed).

## Common mistakes
* Controllers or routes querying the database directly (`ARCH-001`).
* `Domain` importing ORM libraries, database drivers, or HTTP clients.
* Anemic entities (getters/setters only) with procedural business logic leaked into services.
* Missing composition root; ad-hoc DI registration scattered across the codebase.
