---
id: K-005
type: reference
when: "When checking \"what is wrong with project\", before opening PR, or analyzing `project-review.md`"
---
# PROJECT HEALTH CHECK — STATIC CODEBASE AUDITOR & GUARDRAIL

> The second core product of this repository (ADR-0012). Scans a project workspace with language-agnostic file-level heuristics (file tree and regex; no AST parsing), **offline, no network, no model calls**, outputting a machine-readable **`project-review.md`** report at project root and providing a modern Desktop/Web dashboard.

## Execution Options
| Method | Command | Target Audience |
| :-- | :-- | :-- |
| GUI (Windows Desktop) | Launch `Project-Health-Check.exe`, choose workspace directory | Human Vibe Coder |
| Bundled Engine (No Python required) | `engine\reviewer-engine.exe audit <target_dir>` | Agent / CI on Windows |
| Python 3.12+ (CLI) | `python scripts/project_auditor.py <target_dir>` | Agent / CI / Linux / macOS |
| Linux/macOS Shell | `./Project-Health-Check.sh <target_dir>` | Agent / CI |

Default invocation (with no directory argument) audits this kit repository itself.

## How AI Agents & Humans Parse `project-review.md`
1. **Frontmatter & Header**: Total health score (`0–100`), Letter Grade (`A+`, `A`, `B+`...), `kit_ref`, active `declared_architecture`, and `guardrail_level` (`M1–M3`) from `.builder/kit.json`.
2. **Section 0 (Safety & Prompt Injection Scan)**: Always review first. Scans text files (`.md`, `.json`, `.html`, `.txt`, `.yaml`, `.mdc`...) for prompt injection directives (`SAFE-001`), hidden zero-width/bidi characters (`SAFE-002`), hidden HTML comments/elements (`SAFE-003`), obfuscated base64 blobs (`SAFE-004`), and unverified MCP/hook shell commands (`SAFE-005`). Remediation: [core/untrusted-content.md](../core/untrusted-content.md).
3. **Section 2 (Actionable Findings & Remediation Routing)**: Every finding specifies a stable **code** (`SEC-*`, `AC-*`, `ARCH-001..008`, `AGT-*`, `DOC-001..003`, `BASE-B1..B9`), **severity** (`Cao` / `Trung bình` / `Thấp`), **location** (`file:line`), and a direct **remediation document** in [INDEX.md](../INDEX.md).
4. **Section 3 (12 Adaptive Architecture Pillars)**: Evaluates Readme & Living Docs (`S-007`), Backend, Frontend, Database, Security, Cloud/DevOps, Microservices, Data/Caching, Observability, Runtime Anti-Crash, AI Agent Ecosystem, and API Contracts/ADRs.
5. **Section 4 (Core Baseline B1–B9 & Guardrail Verification)**: Verifies mandatory agent governance files (`AGENTS.md`, `CLAUDE.md`, `.agents/skills/`, `docs/project-brief.md`, `adrs/`, `docs/standards/`, CI workflows, `.gitignore`/`.env.example`, `.builder/kit.json`, PR templates) plus profile folder alignment (`ARCH-007`) and M1–M3 boundary guardrails (`ARCH-008`).
6. **Section 7 (Audit Scope)**: Lists indexed code directories, skipped build/vendor directories with reasons (so Agents never waste tokens reading them), entry files to read first, and detected Agent instruction files.

## Codebase Architecture
* `project_auditor.py`: Thin CLI wrapper.
* `auditor_engine/`: Pure business logic (`auditor.py`, `profiler.py`, `tree.py`, `baseline.py`, `safety.py`, `remediation.py`, `pillars_*.py`). Python 3.12+ stdlib only, zero external dependencies, covered by `tests/`.
* `reviewer_app.py` + `reviewer_shell/`: Local web server & Antigravity 2.0 UI (binds strictly to `127.0.0.1` with anti-CSRF/DNS rebinding defense, exposing Overview, Actionable Findings, Core Baseline B1–B9, Safety & Scope, 12 Pillars, and optional AI Deep Review).
* `engine_main.py`: Entry point for packaged PyInstaller engine binary (`serve` | `audit`).
* `build_exe.py`: Packaging script building `engine/reviewer-engine.exe` + `.NET 10` WinForms/WebView2 host (`tools/ProjectReviewer`) into `Project-Health-Check.exe`.
* `sync_docs.py` & `check_links.py`: Living documentation auto-sync pipeline (`S-007`) and `INDEX.md` schema/link verifier.

## Token Monitor (live token usage while chatting with the agent)

Shows, in real time, how many tokens a Claude Code session uses, so a vibe coder can see when the conversation gets expensive. Read-only: it only reads Claude Code's local transcript files (`~/.claude/projects/<project>/*.jsonl`); no network, no model calls.

```bash
python scripts/token_monitor_cli.py --watch        # live view for the current folder
python scripts/token_monitor_cli.py --all --json   # all sessions of this project as JSON
```

It reports: current context size (what each turn re-reads), totals split into fresh input / cache write / cache read / output, recent burn rate, per-model turn counts, and the heaviest turns. Logic is in `scripts/token_monitor/engine.py` (pure, tested in `tests/test_token_monitor.py`); the CLI is only presentation.

* **Verified** (2026-11-07): totals equal an independent computation on a real 114-turn session. Transcripts write each API response several times, so naive summing overcounts about 2.3x; the engine de-duplicates by message id + request id.
* **Not supported / not verified**: Codex, Cursor, Antigravity, Windsurf (their local log formats were not checked). No price or cost calculation (prices change and were not verified). Figures come from local logs, not from the provider's bill.
* **Dashboard** (`python scripts/token_dashboard_cli.py`, then open http://127.0.0.1:8999/ - it must be opened through the local server, not as a file): a local, loopback-only, read-only page that refreshes every 2 s and focuses on **input and output tokens**: totals for the selected scope (new input, input re-read from cache, output) with today's share, cost of **each message you send** (model calls, new input, cache read, output, duration, message preview), a stacked chart per message, cumulative input/output over time, per-model table and a table view. Current context size is shown only as one tile because the Claude app already has a detailed Context panel. No warning threshold by default. Verified in a real browser (desktop, 375 px mobile, light/dark) on this repository's live session (2026-11-07). Not yet a tab in the Health Check UI or in the `.exe` (see `TASKS.md`, group H).
