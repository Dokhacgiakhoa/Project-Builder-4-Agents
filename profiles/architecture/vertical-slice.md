---
id: A-004
type: decision
when: "Systems with multiple independent, feature-sliced capabilities developed in parallel"
not_when: "Features share heavily coupled core entities and strict transactional invariants"
---
# PROFILE: VERTICAL SLICE ARCHITECTURE (FEATURE-BASED)

## When to choose
* Multiple relatively independent features; goal is to add or modify a feature without touching other features.
* Small team or multiple parallel AI agents collaborating on different features concurrently.

## When not to choose
* Features share heavily coupled domain models and business invariants: use [clean-architecture.md](clean-architecture.md) or [modular-monolith.md](modular-monolith.md).
* Very small, single-purpose projects: [simple-layered.md](simple-layered.md) is sufficient.

## Target directory
```text
src/
├── features/
│   ├── create-order/        # ONE vertical slice: request → validation → business logic → data access → response
│   │   ├── handler.*        # Feature entry point
│   │   ├── validator.*      # Input schema validation
│   │   ├── logic.*          # Feature-specific business rules
│   │   ├── data.*           # Feature-specific persistence queries
│   │   └── create-order.test.*
│   └── list-orders/
├── shared/                  # ONLY truly universal concerns (auth, logging, config, core primitives)
└── app.*                    # Composition root (routing, middleware setup)
```

## Constraints
* Slices **never import** other feature slices. If duplication occurs, extract to `shared/` only after **2–3 real use cases emerge** (rule of three, avoid premature abstraction).
* `shared/` must never depend on `features/` and must never host feature-specific business rules.
* Guardrail Level M2 (see [../README.md](../README.md)): Enforce lint rules prohibiting cross-feature imports between `features/*` folders.

## Adding a feature
1. Scaffold `features/<action-verb-name>/` (name folders after user actions).
2. Write vertical slice tests first (from handler invocation to mocked or isolated persistence).
3. Implement `validator` $\rightarrow$ `logic` $\rightarrow$ `data` $\rightarrow$ `handler`.
4. Register the new feature handler in `app.*` router.

## Common mistakes
* One feature directly importing types or handlers from another feature slice.
* `shared/` degenerating into a catch-all dumping ground containing feature-specific logic.
* Inconsistent error handling or logging across slices due to missing `shared/` conventions.
