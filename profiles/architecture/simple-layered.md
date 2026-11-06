---
id: A-001
type: decision
when: "Small MVPs, student projects, prototypes, simple CRUD"
not_when: "Complex business logic, multi-year lifespans, deep domain testing independent of frameworks"
---
# PROFILE: SIMPLE LAYERED ARCHITECTURE

## When to choose
* Solo developer or small team, lightweight business logic, rapid prototype delivery required.
* Primarily CRUD data access; zero need to decouple database or framework.

## When not to choose
* Complex business rules requiring framework-independent domain unit tests: use [clean-architecture.md](clean-architecture.md).
* Multiple independent features developed in parallel: use [vertical-slice.md](vertical-slice.md).

## Target directory
```text
src/
├── routes/ (or controllers/, pages/)  # Handles HTTP requests, calls services. NO business logic
├── services/                          # Application business logic
├── data/ (or repositories/, models/)  # Database and external API access
├── lib/                               # Shared utilities (logging, validation)
└── config/                            # Environment configuration singleton
tests/                                 # Mirrors src/ directory structure
```

## Constraints
* Dependency flow: `routes → services → data`. Reverse direction is **strictly prohibited**; `routes` never query the DB directly.
* `lib/` and `config/` are shared helpers and must not depend on the three layers above.
* Guardrail Level M1 (see [../README.md](../README.md)): Working lint + test + build running in CI.

## Adding a feature
1. Record objective and acceptance criteria in `tasks/task-spec.md`.
2. Write unit tests for `services` (1 happy path + 2 edge/failure cases).
3. Implement business logic function in `services`, accessing storage via `data`.
4. Create a thin route handler calling the service; validate inputs at the route layer.
5. Run test/lint/build verification commands; update `docs/project-brief.md` if user journeys change.

## Common mistakes
* Route layer containing direct SQL/ORM queries or complex calculations (layer leakage).
* Monolithic god-files > 350 lines combining UI, state, and database queries.
* Committing credentials; missing `.env.example`.
* Swallowing errors silently; bare `JSON.parse` without error handling.

## Upgrade Indicators
When `services` bloats and unit tests require spinning up real databases, transition to Clean Architecture via an ADR (isolating `domain` from `data`).
