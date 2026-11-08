# ADR-0022: Single-Executable Delivery (Engine Embedded in Shell)

- Status: Accepted (2026-11-07)
- Refines: ADR-0011 (Decoupled Core Engine + WebView2 Shell), ADR-0012 (Release channel), ADR-0013 (Zero-Clone)

## Context
ADR-0011 required the Core Engine and the shell to be decoupled in *code*. `build_exe.py` implemented that as two *artifacts*: `Project-Health-Check.exe` (shell) plus `engine/reviewer-engine.exe` (PyInstaller), with `engine/` required beside the exe. `engine/` is git-ignored, so a user who downloaded only the exe had no engine and was prompted to install Python. This contradicted the product goal: the user downloads **one file**; everything else (knowledge, remediation docs) is read online (Zero-Clone).

The goal was never written as a constraint, so the two-file layout passed review.

## Decision
1. **Deliverable = exactly one file**: `Project-Health-Check.exe`. Code separation (ADR-0011) is kept; physical separation is not.
2. The engine is built first and embedded in the shell as an `EmbeddedResource` (`reviewer-engine.exe`). At runtime the shell uses `engine\` beside the exe if present (dev), otherwise extracts it to `%TEMP%\ProjectHealthCheck\engine\<hash>` with SHA-256 verification (ADR-0025).
3. The same exe supports CLI mode: `Project-Health-Check.exe audit <dir>` / `serve`, forwarded to the embedded engine.
4. **Build gate**: `build_exe.py` fails if `engine/reviewer-engine.exe` is missing before compiling the shell; it never emits a shell without an engine. `--shell-only` is allowed only when an engine already exists.
5. Release (TASKS A3) ships the single exe plus `SHA256SUMS`; no `engine/` folder.
6. Knowledge/remediation docs remain online (raw GitHub); the offline `knowledge_pack.json` inside the engine is only a fallback.

## Consequences
- Download size = shell + engine (measured 61.5 MB for the self-contained build on 2026-11-07; framework-dependent size not measured).
- First run pays an extraction cost to `%TEMP%`; later runs reuse the extracted file when its SHA-256 matches (ADR-0025; the original size-only check was replaced).
- Antivirus may flag a self-extracting exe more often. Not yet measured.

## Not yet verified
- Single exe on a clean Windows machine (no Python, no .NET, no `engine\` folder): pending Antigravity handoff.
- Extraction behavior when `%TEMP%` is read-only or the engine is already running.
