---
id: K-005
type: reference
when: "When checking \"what is wrong with project\", before opening PR, or analyzing `project-review.md`"
---
# PROJECT HEALTH CHECK — STATIC CODEBASE AUDITOR & GUARDRAIL

> The second core product of this repository (ADR-0012). Scans any project workspace (any language), **100% offline, zero network, zero tokens consumed**, outputting a machine-readable **`project-review.md`** report at project root.

## Execution Options
| Method | Command | Target Audience |
| :-- | :-- | :-- |
| GUI (Windows) | Launch `Project-Health-Check.exe`, choose workspace directory | Human Vibe Coder |
| Bundled Engine (No Python required) | `engine\reviewer-engine.exe audit <target_dir>` | Agent / CI on Windows |
| Python 3.12+ (CLI) | `python scripts/project_auditor.py <target_dir>` | Agent / CI / Linux / macOS |
| Linux/macOS Shell | `./Project-Health-Check.sh <target_dir>` | Agent / CI |

Default invocation (with no directory argument) audits this kit repository itself.

## How AI Agents Parse `project-review.md`
1. Header: Total health score, Letter Grade (A+, A, B...), and active **architecture profile** from `.builder/kit.json`.
2. **Actionable Findings**: Each finding specifies **code**, **severity** (High / Medium / Low), **location** (`file:line`), and a **remediation doc** (kit path and raw URL).
3. Open the referenced remediation document (or invoke `kit-consult` skill), resolve findings in order of severity, and re-run Health Check.
4. **Section 0 (Safety & Security Alerts)**: Always review first. Health Check scans text files (md, json, html, txt, yaml...) for prompt injection, zero-width characters, hidden HTML comments, and unverified MCP shell hooks (`SAFE-001`…`SAFE-005`). Detailed remediation: [core/untrusted-content.md](../core/untrusted-content.md).
5. **Section 7 (Audit Scope)**: Scanned folders, skipped directories with rationale, and unverified files.

## Codebase Architecture
* `project_auditor.py`: Thin CLI wrapper.
* `auditor_engine/`: Pure business logic (tree scanner, profiler, pillars, markdown reporter, finding-to-doc mapping in `remediation.py`). Python stdlib only, fully headless, covered by `tests/`.
* `reviewer_app.py` + `reviewer_shell/`: Local web UI (binds strictly to `127.0.0.1` with anti-CSRF/DNS rebinding defense).
* `engine_main.py`: Entry point for packaged engine binary (`serve` | `audit`).
* `build_exe.py`: Packaging script (PyInstaller + .NET host wrapper in `tools/ProjectReviewer`).
* `check_links.py`: Documentation integrity and schema linter (enforces zero broken links in `INDEX.md`).
