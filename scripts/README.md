---
id: K-005
type: reference
when: "When checking \"what is wrong with project\", before opening PR, or analyzing `project-review.md`"
---
# PROJECT BUILDER ANALYTICS — STATIC CODEBASE AUDITOR & GUARDRAIL

> The second core product of this repository (ADR-0012). Scans a project workspace with language-agnostic file-level heuristics (file tree and regex; no AST parsing), **offline, no network, no model calls**, outputting a machine-readable **`project-review.md`** report at project root and providing a modern Desktop/Web dashboard.

## Execution Options
| Method | Command | Target Audience |
| :-- | :-- | :-- |
| GUI (Windows Desktop) | Launch `Project-Builder-Analytics.exe`, choose workspace directory | Human Vibe Coder |
| Single-exe CLI (No Python required) | `Project-Builder-Analytics.exe audit <target_dir>` | Agent / CI on Windows |
| Python 3.12+ (CLI) | `python scripts/project_auditor.py <target_dir>` | Agent / CI / Linux / macOS |
| Linux/macOS Shell | `./Project-Builder-Analytics.sh <target_dir>` | Agent / CI |

Default invocation (with no directory argument) audits this kit repository itself.

**Packaging note (ADR-0022)**: the deliverable is **one file**, `Project-Builder-Analytics.exe`. The PyInstaller engine (`engine/reviewer-engine.exe`, build-time intermediate, git-ignored) is embedded in it and extracted to `%TEMP%\ProjectHealthCheck\engine` at run time; no Python needed and no `engine\` folder to ship. `build_exe.py` refuses to build the shell without an engine. The shell is by default framework-dependent and needs the .NET 10 Desktop Runtime; build with `python scripts/build_exe.py --self-contained` (about 61 MB with the engine) to run on a machine without .NET. Verified on a machine that has Python and .NET installed, with a minimal `PATH` and `DOTNET_ROOT` pointed at an empty folder; not yet verified on a truly clean Windows install (`TASKS.md`, A2).

## How AI Agents & Humans Parse `project-review.md`
1. **Frontmatter & Header**: Total health score (`0–100`), Letter Grade (`A+`, `A`, `B+`...), `kit_ref`, active `declared_architecture`, and `guardrail_level` (`M1–M3`) from `.builder/kit.json`.
2. **Section 0 (Safety & Prompt Injection Scan)**: Always review first. Scans text files (`.md`, `.json`, `.html`, `.txt`, `.yaml`, `.mdc`...) for prompt injection directives (`SAFE-001`), hidden zero-width/bidi characters (`SAFE-002`), hidden HTML comments/elements (`SAFE-003`), obfuscated base64 blobs (`SAFE-004`), and unverified MCP/hook shell commands (`SAFE-005`). Remediation: [core/untrusted-content.md](../core/untrusted-content.md).
3. **Section 2 (Actionable Findings & Remediation Routing)**: Every finding specifies a stable **code** (`SEC-*`, `AC-*`, `ARCH-001..008`, `AGT-*`, `DOC-001..003`, `BASE-B1..B9`, `WLOG-001..002`, `HYG-002`, `SUP-001..004`, `SPEC-001`), **severity** (`High` / `Medium` / `Low`), **location** (`file:line`), and a direct **remediation document** in [INDEX.md](../INDEX.md).
4. **Section 3 (12 Adaptive Architecture Pillars)**: Evaluates Readme & Living Docs (`S-007`), Backend, Frontend, Database, Security, Cloud/DevOps, Microservices, Data/Caching, Observability, Runtime Anti-Crash, AI Agent Ecosystem, and API Contracts/ADRs.
5. **Section 4 (Core Baseline B1–B9 & Guardrail Verification)**: Verifies mandatory agent governance files (`AGENTS.md`, `CLAUDE.md`, `.agents/skills/`, `docs/project-brief.md`, `adrs/`, `docs/standards/`, CI workflows, `.gitignore`/`.env.example`, `.builder/kit.json`, PR templates) plus profile folder alignment (`ARCH-007`) and M1–M3 boundary guardrails (`ARCH-008`).
6. **Section 7 (Audit Scope)**: Lists indexed code directories, skipped build/vendor directories with reasons (so Agents never waste tokens reading them), entry files to read first, and detected Agent instruction files.

## Extended Checks (offline heuristics, no score impact; ADR-0016, ADR-0017)
| Code | Severity | Signal |
| :-- | :-: | :-- |
| `WLOG-001` / `WLOG-002` | Medium / Low | No work log / work log without dated entry ([S-009](../core/standards/worklog.md)). Gated: `WLOG-001` only evaluates projects that declare agent instructions (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`, etc.) |
| `SEC-005` | High | Committed `.env` or private keys (`*.p12`, `id_rsa`, `.pem` with `PRIVATE KEY`) tracked by git. Excludes `.env.example`, `.env.sample`, `.env.test`, templates, and test fixture paths |
| `HYG-002` | Medium | `*.log` files tracked by git |
| `SUP-001` | High | `preinstall`/`install`/`postinstall` that downloads, decodes or evals remote content |
| `SUP-002` | Medium | Unpinned dependencies (`*`, `latest`, git/URL without commit or tag) in `package.json`/`requirements*.txt` |
| `SUP-003` | Medium | `requirements` index outside PyPI or over plain `http` (dependency confusion) |
| `SUP-004` | Low | Executables/binaries (`.exe`, `.dll`, `.so`, `.jar`...) tracked by git; contents are not inspected |
| `AGT-004` / `AGT-005` | Medium | MCP config uses a package known to be missing/deprecated / `npx` without a pinned version |
| `SPEC-001` | Medium | `[NEEDS CLARIFICATION]` left in specs/tasks ([S-008](../core/standards/feature-workflow.md)) |

Limits: git-based checks need `git` and a `.git` directory (skipped otherwise); no CVE lookup, no typosquat list, no malware scanning; the known-bad MCP package table is a small hand-verified list (2026-11-07), not a live registry check. "No finding" is not a safety statement.

## Safety Scan & Performance Hardening (ADR-0021)
* **Directive Pre-Gating**: Safety scanner evaluates a fast literal containment pre-gate (`_DIRECTIVE_GATE_LITERALS`) before regex compilation, reducing CPU regex calls across 23 repositories while preserving 100% invariant findings (`evals/results/raw/011-nonsafe-identity.txt`).
* **Unicode & Context Awareness**:
  - Turkish dotted `İ` and dotless `ı` case normalization; Unicode NFC normalization for all non-ASCII lines.
  - `SAFE-002`: Context-aware rule evaluating hidden zero-width/bidi control characters inside visible markdown quotes vs standalone code.
  - `SAFE-003`: Flags hidden directives (zero-font, CSS `display:none`, HTML comments `<!-- ... -->`); text without an explicit noun is flagged when concealed in hidden markup.
* **Measured Scan Speeds**:
  - P-062 (5,470 files), rerun 2026-11-08: mean scan latency **15.1s -> 4.3s (3.51x)**, 5 runs per side (`evals/results/raw/016-ab-speed.json`). An earlier run (report 010) measured 28.9s -> 5.9s (4.88x); the runs differ and were not reconciled.
  - LiteLLM (15,227 files), rerun 2026-11-08: mean scan latency **58.2s -> 18.6s (3.14x)** (`evals/results/raw/016-ab-benchmark-pillars.json`). An earlier run (report 010) measured 69.0s -> 35.4s (~2.0x).
  - Cold Run HDD Penalty: 4,000 files on physical mechanical HDD took **30.32s cold vs 0.28s warm (109x)** for pure file reading; pre-warmed audit (**8.86s**) matched warm audit (**8.80s**) within 0.06s (`evals/results/raw/011-cold-warm.json`).

## Server Lifetime & Asynchronous Audit Protocol (ADR-0019)
* **Watchdog Lifetime Management**:
  - Engine accepts `--watchdog=SECONDS` (default: **180s**; `--watchdog=0` disables).
  - Background daemon monitors heartbeat pings (`GET /api/heartbeat` sent every 2,000ms by the UI); if no heartbeat arrives within 180s, the engine exits cleanly, eliminating orphaned processes after shell force-close or crash.
  - Watchdog shutdown is strictly suppressed while an audit is actively running (`is_auditing` flag), and auto-re-arms on clock jumps (system sleep/stall).
* **Asynchronous Audit API**:
  - `POST /api/run-audit`: Initiates background scan asynchronously, returning immediately.
  - `GET /api/audit-status`: Returns incremental progress (`status`, `pct`, `title`, `stage`, `findings_count`). Mid-scan UI reloads (F5, `Page.reload`) preserve the engine PID and resume polling without restarting or crashing the audit.

## Sample Zones (ADR-0018)
* **Designated Folders**: `examples`, `example`, `fixtures`, `samples`, `profiles/*/starter`, and `core/templates`.
* **Excluded Scope**: Pruned from general workspace indexing (`ProjectTree`). Excluded from archetype classification, architecture pillar evidence evaluation, and anti-crash AST inspection. Sample apps (such as embedded React templates or demonstration snippets) must never pollute the host project's archetype or active pillars.
* **Active Safety & Hygiene Scope**: Sample zones **are still fully scanned** by `scan_safety` (detecting prompt injections `SAFE-001`, hidden unicode `SAFE-002`, HTML comments `SAFE-003`, base64 `SAFE-004`) and git-based hygiene checks (`git ls-files` detects tracked secrets `SEC-005` or binaries `SUP-004` regardless of folder location).
* **Impact on Kit Self-Score**: Because this kit (`Project-Builder-4-Agents`) provides an embedded React starter in `profiles/frontend/starter` but has no frontend application of its own, the frontend pillar is legitimately marked N/A. This makes the kit's self-score **90/100 (Grade A)** instead of 100/100.

## Codebase Architecture
* `project_auditor.py`: Thin CLI wrapper.
* `auditor_engine/`: Pure business logic (`auditor.py`, `profiler.py`, `tree.py`, `baseline.py`, `safety.py`, `hygiene.py`, `remediation.py`, `pillars_*.py`). Python 3.12+ stdlib only, zero external dependencies, covered by `tests/`.
* `reviewer_app.py` + `reviewer_shell/`: Local web server & Antigravity 2.0 UI (binds strictly to `127.0.0.1` with anti-CSRF/DNS rebinding defense, exposing Overview, Actionable Findings, Core Baseline B1–B9, Safety & Scope, 12 Pillars, and optional AI Deep Review).
* `engine_main.py`: Entry point for packaged PyInstaller engine binary (`serve` | `audit`).
* `build_exe.py`: Packaging script building `engine/reviewer-engine.exe` then embedding it into the `.NET 10` WinForms/WebView2 host (`tools/ProjectReviewer`) to produce the single `Project-Builder-Analytics.exe` (ADR-0022).
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
