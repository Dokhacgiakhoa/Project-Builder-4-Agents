# AGENTS.md — INSTRUCTIONS FOR AI AGENTS MAINTAINING PROJECT-BUILDER-4-AGENTS

> This document applies strictly when you are **maintaining or modifying this kit repository**. If a user wants to **bootstrap their own project** using this kit, follow [BOOTSTRAP.md](BOOTSTRAP.md). The instructions that target projects receive are located in [core/templates/AGENTS.md](core/templates/AGENTS.md).

## What is this Kit (See HOW_IT_WORKS.md, ADR-0012, ADR-0013, ADR-0014)
A centralized **Hosted Agent Brain & Remote Knowledge Hub** on GitHub engineered for AI Coding Agents and Vibe Coders via **Zero-Clone** mechanics (users never clone the entire multi-stack repo; Agents inspect remotely, advise on tech stack, and fetch only what is required).
Two Core Products:
1. **Builder**: Knowledge + protocols + system thinking framework for Agents (`BOOTSTRAP.md`, `INDEX.md`, `MANIFEST.json`, `llms.txt`, `core/`, `profiles/`, `knowledge-base/`, `templates/`).
2. **Project Health Check**: Zero-token static workspace auditor and guardrail engine (`scripts/`, `tools/`).
All documentation is **Agent-Readable first**. Operational specifications: [HOW_IT_WORKS.md](HOW_IT_WORKS.md).

Kit task roadmap and progress tracker: [TASKS.md](TASKS.md). Update it when completing or pivoting a milestone.

## Rules for Maintaining This Kit
1. **Content Tiers**: Core = Mandatory across all repos; Profile = Selected per project domain; Library = Reference/optional. Never push stack-specific or architecture-specific concerns into `core/`.
2. **Every document must have a row in `INDEX.md`** with an intent-driven "When to use" description. When adding/renaming/deleting docs $\rightarrow$ update `INDEX.md` and execute `python scripts/check_links.py`.
3. **Document Formats**: Every document in `core/` and `profiles/` (except `core/templates/` and `profiles/frontend/starter/`) must have frontmatter `id`, `type` (`decision|router|playbook|reference`), and `when` matching its row in `INDEX.md`. Architecture profiles are `type: decision`: must include `not_when`, all mandatory sections (*When to choose / When not to choose / Target directory / Constraints / Adding a feature / Common mistakes*), max 120 lines. Documents contain **decisions and constraints only**, never redundant syntax tutorials. `check_links.py` verifies this automatically.
4. **Health Check Modifications**: Engine logic in `scripts/auditor_engine/` must be pure business logic with zero UI coupling. Every new finding must define **code + severity + remediation doc** in `remediation.py` (verified by automated tests).
5. **Python 3.12+**. Zero runtime dependencies for the engine (standard library only).
6. Any architectural or positioning pivot $\rightarrow$ record an ADR in `adrs/`.
7. **Primary Language is English (ADR-0014)**: All knowledge files, skills (`SKILL.md`), rules, playbooks, catalogs, and templates must be authored in concise, technical English to minimize token consumption (~50% token reduction) and maximize LLM reasoning fidelity. When conversing with the human vibe coder, Agents dynamically respond in the user's preferred language.
8. Run `make test` and `make check-links` before declaring completion. Never ignore a failing test.
9. 2-Attempt Circuit Breaker: Stop and ask before breaking backwards compatibility, deleting knowledge files, or introducing heavy runtime dependencies.
10. **Empirical Verification Before Assertion**: Never dismiss, speculate, or make factual claims about external tools, libraries, community skills, or competitor repositories without first performing an explicit tool search (`search_web`, GitHub lookup). Ground all assessments in verifiable facts, not probability-based memory recall.
11. **Continuous Self-Improvement & Knowledge Feedback Loop**: When a user corrects an agent's assumption, identifies a knowledge gap, or clarifies a recurring pain point, the agent must NOT merely apologize in conversation. The agent is strictly obligated to codify that learning into the repository (updating rules, writing new playbooks, or refining guardrails) so that no future agent repeats the mistake.
