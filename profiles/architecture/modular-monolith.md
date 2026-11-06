---
id: A-005
type: decision
when: "Monolithic systems growing in scale requiring strict bounded contexts and module boundaries"
not_when: "Small projects with few domains; or systems already requiring independent container deployment per service"
---
# PROFILE: MODULAR MONOLITH

## When to choose
* System scope is growing and requires explicit module boundaries for task parallelization (humans or AI agents), but single-deployment operational simplicity is preferred.
* Internal architecture can leverage Clean Architecture or Vertical Slice **inside** each individual module.

## When not to choose
* Small projects with single simple domains: use [simple-layered.md](simple-layered.md) or [vertical-slice.md](vertical-slice.md).
* Strict operational requirements for independent scaling/deployment per service: requires microservices ADR and explicit user consultation.

## Target directory
```text
src/
├── modules/<domain-name>/   # Each module: Public API contract + private internal implementation
├── shared/                  # Minimal universal kernel (types, logging, telemetry)
└── app.*                    # Host application wiring and composition root
```
Domain mappings are maintained in `specs/domains.md`.

## Constraints
* Modules interact with other modules **exclusively via Public API contracts** (interfaces, DTOs, or domain events). Direct import of another module's internal files is strictly prohibited.
* Database tables must not be shared directly across module boundaries (access via module APIs).
* `shared/` must never contain domain business logic.
* Guardrail Level M3 (see [../README.md](../README.md)): Enforce package boundaries or lint rules prohibiting private internal imports; ADR required for boundary changes.

## Adding a feature
1. Identify the owning domain module. If new, create module and register it in `specs/domains.md`.
2. Implement feature logic entirely inside that module.
3. If data from another module is needed: expose a method via that module's **Public API**, never bypass via internal imports.

## Common mistakes
* Cross-importing private internal directories of foreign modules.
* Leaking domain business logic into `shared/`.
* Monolithic god-modules conflating multiple distinct business subdomains.
