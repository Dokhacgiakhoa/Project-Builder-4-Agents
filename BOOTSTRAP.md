# BOOTSTRAP — PROCEDURE FOR AI AGENTS BOOTSTRAPPING A PROJECT

> **You are an AI coding agent** (Claude Code, Antigravity, Cursor, Windsurf, Codex...). The user is typically a vibe coder or fresher who **does not know repository internals** and may not be a Git expert. You must **proactively** execute this workflow based on their conversation and requirements. Never ask them to type complex terminal commands or guess filenames.
> **Language Rule**: Read and process this kit in English to minimize token consumption. **Always converse with the human user in their preferred language** (e.g., Vietnamese if prompted in Vietnamese).

* Knowledge Hub: `https://github.com/Dokhacgiakhoa/Project-Builder-4-Agents`
* Intent-Routed Index: [INDEX.md](INDEX.md)
* Machine-Readable File Tree: [MANIFEST.json](MANIFEST.json) & [llms.txt](llms.txt)
* Operating Specification: [HOW_IT_WORKS.md](HOW_IT_WORKS.md)

---

## STEP 0 — Preparation (Zero-Clone Remote Access)

1. Determine the **Target Project Directory**: Current user working directory, or ask if ambiguous. **NEVER clone the entire kit repository into the user's project directory.**
2. Inspect directory state:
   * **Empty / Fresh**: Clean bootstrap.
   * **Existing files (in-progress project)**: **MERGE MODE** — Only **add** missing files. **Never overwrite** existing user files. If filename collides, write kit version as `<filename>.kit-suggested` and notify the user.
3. **Remote Fetch Methods (Choose 1, keep user machine clean)**:
   * **Method A (Recommended - On-Demand Fetch)**: Look up [MANIFEST.json](MANIFEST.json) for raw URLs (`https://raw.githubusercontent.com/Dokhacgiakhoa/Project-Builder-4-Agents/main/<path>`). Fetch only the specific files needed directly into the target project.
   * **Method B (Temporary Shallow Clone)**: Run `git clone --depth 1 https://github.com/Dokhacgiakhoa/Project-Builder-4-Agents <tmp_dir>` into OS temporary folder (`%TEMP%` or `/tmp`). Copy required files, then **immediately delete the temporary clone directory**.
   * Record the commit hash or tag as `kit_ref`.

## STEP 1 — Phase 0: Agent Self-Configuration & Core Baseline
This step is **mandatory across all stacks and architectures** (specified in [core/README.md](core/README.md)).

1. Copy from `core/templates/` into project root (preserving folder structure):
   * `AGENTS.md`, `CLAUDE.md`, `docs/project-brief.md`, `adrs/0000-template.md`
   * `.agents/skills/` (3 core baseline skills: `kit-consult`, `spec-first-task`, `health-check`)
   * `specs/`, `planning/`, `tasks/`
   * `.github/` (PR template, issue forms, SECURITY, CONTRIBUTING...) — CI workflow is created in Step 3.
   * `.editorconfig`, `.env.example`
   * `gitignore.tpl` $\rightarrow$ rename to `.gitignore` (if `.gitignore` exists: **append missing lines only**, do not replace)
   * `.builder/kit.json`
2. Copy `core/standards/*` $\rightarrow$ `docs/standards/`.
3. **Agent Runtime Compatibility Layer**:
   * `Codex` & `Antigravity`: Read `AGENTS.md` directly.
   * `Claude Code`: Reads `CLAUDE.md` (which imports `AGENTS.md`). Copy skills to `.claude/skills/` (avoid symlinks on Windows).
   * `Cursor`: Create `.cursor/rules/agent-constitution.mdc` (`description: "Project Constitution", alwaysApply: true`, referencing `AGENTS.md`).
   * `Windsurf`: Create `.windsurfrules` referencing `AGENTS.md`.
   * **Anti-Doom-Loop Setup**: Always adhere to the 3 operating loops in [profiles/playbooks/anti-doom-loop-guide.md](profiles/playbooks/anti-doom-loop-guide.md) (Spec-First Loop, CI Green Loop, Git Micro-Checkpoint Loop).
4. Fill known `{{PLACEHOLDER}}` values (project name, date, `kit_ref`).
5. Initialize git if not already a repo: `git init`. Do not commit/push without user consent.

## STEP 2 — Phase 1: Discovery Interview, Tech Selection & Skill Injection
Follow [core/discovery.md](core/discovery.md): Ask concise questions, suggest sensible defaults, explain trade-offs simply. Output:
1. `docs/project-brief.md` filled out (including explicit assumptions).
2. Tech Stack ADR (`adrs/0001-*.md`) and Architecture Profile ADR (`adrs/0002-*.md`).
3. **Inject Curated Skills**: Consult [profiles/skills-catalog/curated-agent-skills.md](profiles/skills-catalog/curated-agent-skills.md). Based on project features (Database, External APIs, Frontend UI, Auth, Payments, or Production Deploy), copy matching skill definitions into `.agents/skills/` (and `.claude/skills/`). **Zero web searching required.**
4. Present a concise summary for **user confirmation** before proceeding.

## STEP 3 — Phase 2: Apply Architecture Profile & Setup Guardrails
1. Read [profiles/README.md](profiles/README.md): Select architecture based on signals in `docs/project-brief.md` (do not quiz user on architecture terminology). Select guardrail level M1–M3, and read the chosen profile document via [INDEX.md](INDEX.md).
2. Scaffold **directory structure** matching the architecture profile; configure build/test/lint tools and boundaries.
3. Fill "Verification Commands" in `AGENTS.md` with **real, tested commands**.
4. Generate `.github/workflows/ci.yml` running these real commands (no fake `echo` steps).
5. Update `.builder/kit.json` (`profiles`).

## STEP 4 — Verification
1. Run test, lint, and build commands; iterate until all pass green.
2. Execute **Project Health Check** (see [scripts/README.md](scripts/README.md)) $\rightarrow$ `project-review.md`. Resolve all High-severity findings.
3. Report progress to the user in simple language: what was created, verification results, and next actions.

## STEP 5 — Continuous Lifecycle & Go-Live Readiness
1. **System Thinking & Governance**: The project carries the **Knowledge Router** in `AGENTS.md`. When encountering architectural challenges (Clean Architecture, module boundaries), UI design patterns, AI apps, or `project-review.md` findings, **proactively consult [INDEX.md](INDEX.md)** (via `kit-consult` skill).
2. **Production Go-Live**: Guide the user beyond `localhost` towards real-world deployment:
   * Multi-stage, non-root Docker packaging.
   * Free-tier / low-cost cloud deployment via `profiles/stacks/cloud-free-tier-stack.md` (Vercel, Railway, Supabase...).
   * Follow the 5 Go-Live Gates in `profiles/deployment/go-live-production-checklist.md`.
3. **Periodic Health Audits**: Re-run Health Check after major milestones and before PR merges to maintain an A+ (100/100) score.

---

## Golden Rules
* **Never overwrite** user files. **Never delete** user code. Ask before making irreversible changes.
* **Never commit** secrets or API keys. Always use `.env`.
* When uncertain $\rightarrow$ choose the safe default, document it under "Assumptions" in `docs/project-brief.md`, and inform the user.
