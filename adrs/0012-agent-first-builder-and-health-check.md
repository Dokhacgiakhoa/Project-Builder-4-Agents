# ADR 0012: AGENT-FIRST BUILDER KIT & PROJECT HEALTH CHECK

* **Status**: Approved (Accepted)
* **Decision date**: 2026-11-05
* **Replaces the earlier positioning of**: the Starter Kit "clone it and type the commands yourself" (the old ADR-0001..0010 were turned into documents in `core/` and `profiles/`)

---

## 1. CONTEXT
* The target users are **IT freshers and "vibe coders"** who know only a little git. They **do not know which files the repo contains**, so they cannot point the Agent at a specific document.
* They use a **coding Agent** (Claude Code, Antigravity, Codex). Most of the time they ask the Agent to write and review, and rarely read code themselves. The documents in the repo are mostly **for Agents to read** (~90%), for humans ~10%.
* Different projects need **different Clean Architecture styles, design patterns, rules and skills**. There cannot be one deep configuration shared by all.

## 2. DECISION

### 2.1. Two products in one repo
| | **Project-Builder-4-Agents** | **Project Builder Analytics** (formerly Project Health Check) |
|---|---|---|
| What it is | A knowledge base + procedure for Agents to build and accompany a project | A tool (exe/CLI) that checks what is wrong with a project |
| Who uses it | Agents, through conversation with the user | The user clicking the exe, or an Agent running the command line |
| Output | A project with a standard skeleton, rules, skills, workflows | A **`project-review.md`** file for both humans and Agents |

### 2.2. The Agent takes the initiative; the user never has to name a file
* The single entry point: `README.md` → `BOOTSTRAP.md` (the procedure for Agents) → `INDEX.md` (a routing table **intent → document**).
* The user only states their wish in plain language. The Agent matches it against `INDEX.md` to choose which documents to read.
* Once built, the project carries a **Knowledge Router** in `AGENTS.md` (the kit address + the rule "when situation X comes up, look it up in INDEX"), so the Agent stays proactive in later steps.

### 2.3. Three content tiers (separating what is mandatory from what is customizable)
1. **Core Baseline** (`core/`): mandatory for **every** repo that works with Agents, independent of language/architecture.
2. **Profiles** (`profiles/`): deep configuration, **chosen per project** after the interview (architecture style, stack, pattern, design system, application type).
3. **Library** (`knowledge-base/`, `templates/`): reference documents and optional modules (pitch deck, project management...).

### 2.4. A shared Agent standard with a thin compatibility layer
* Single source of truth: **`AGENTS.md`** and **Agent Skills** (`SKILL.md`, an open standard). Codex and Antigravity read `AGENTS.md`; Claude Code reads `CLAUDE.md`, so create a `CLAUDE.md` that only imports `AGENTS.md`.
* Skills live at `.agents/skills/<name>/SKILL.md` (Codex, Antigravity); Claude Code reads `.claude/skills/`, so **copy** them there.
* Tool-specific rules/workflows are only a thin layer generated from the common source.
* **Re-verify** the paths against the official documentation when the Agent executes, because the tools change fast (some sources still contradict each other about Antigravity's global path).

### 2.5. Analytics produces `project-review.md`
* A single Markdown file readable by humans and Agents: overall score, each finding with a **stable code, severity, file:line location** and the **remediation document in the kit** (path + URL).
* The Agent reads the report, looks up the document it points to, fixes in priority order, and reruns to confirm.
* Analytics is **profile-aware** (`.builder/kit.json`); it does not impose one architecture style on every project.
* The engine is packaged so users **do not need to install Python**; Python is only the route for CI/Linux/macOS and for developers of the kit.

## 3. CONSEQUENCES
* **Positive (expected, not yet verified with real users)**: newcomers only need to chat; each project receives a right-sized configuration; documents can be found by intent; the report closes the loop "detect → look up → fix → recheck".
* **Limits**: the Agent must be able to fetch files from GitHub; quality depends on `INDEX.md` always being correct (`scripts/check_links.py` runs in CI); the Agent formats must be watched periodically.
* **Next**: concrete stack packs (Profiles), profile-aware Analytics checks, a release process (GitHub Releases: exe + engine + checksum).
