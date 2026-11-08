# ADR-0024: Cloud/DevOps Pillar Applies Only to Deployable Projects

- Status: Accepted (2026-11-08)
- Builds on: ADR-0020 (sample zones; Frontend pillar N/A precedent), ADR-0012 (Health Check)

## Context
`profiler.py` set `has_cloud` whenever it saw a Dockerfile, a compose file, k8s/helm files **or any CI workflow**. The Cloud/DevOps pillar then scored Docker-specific criteria (multi-stage build, non-root user, health endpoint, compose/IaC). A knowledge or library repository with only CI therefore got a pillar it cannot satisfy, and this kit added a Dockerfile and a compose file (commit `4ba577d`, "achieve 100/100 project health") that nothing used and that did not even build until 2026-11-08. The files existed to earn points.

## Decision
1. `has_cloud` is resolved at the end of `profile()`:
   `has_cloud = container_intent or (has_ci and deployable)`
   - `container_intent`: Dockerfile, compose file, or k8s/helm files.
   - `deployable`: `has_backend or has_frontend or has_microservices`.
2. CI alone on a knowledge repo, library, CLI or docs project no longer activates the pillar (it is skipped, like Frontend in ADR-0020).
3. The kit's unused `Dockerfile` and `docker-compose.yml` are removed.

## Measured effect (2026-11-08)
- Kit self-score: 90/100 (with the Docker files) -> 78/100 (files removed, old rule) -> **87/100 (files removed, new rule)**.
- Profile flags on 23 repos (this kit, P-062 and the 21 repos in `D:\Github\_corpus`): `has_cloud` changed for 7: this kit, awesome-cursorrules, httpx, jinja, mkdocs, pydantic, requests. All are libraries or non-service repos with CI only. No repo gained the pillar; the other 16 are unchanged. Raw flags: scratch files, not archived.

## Consequences
- The kit's score is lower than before and reflects its real shape (no deployable service).
- Tests: `tests/test_cloud_pillar_applicability.py` (6 cases).

## Not covered
- A real service in a framework the profiler does not detect (so `deployable` is false) with CI only gets no Cloud pillar. This is a false N/A; detection gaps are not addressed here.
- Full audits (not only profile flags) were not rerun on the 22 other repos; only the kit's score was re-measured.
