# ADR-0019: Reviewer Engine Lifetime Management via Heartbeat and Watchdog

- Status: Accepted (2026-11-07)
- Builds on: ADR-0011 (Desktop and Tooling Architecture)

## Context
In previous iterations, the C# WebView2 desktop shell relied on a `beforeunload` browser event beacon to notify the Python background engine (`reviewer-engine.exe`) to shut down when the window closed.
This mechanism suffered from critical reliability failures:
1. **Mid-scan navigation or reload kill**: Refreshing the UI (F5, Ctrl+R, or `Page.reload`) fired `beforeunload`, killing the engine mid-audit and causing orphaned UI spinners.
2. **Abrupt process termination**: If the shell crashed, hung, or was forcefully terminated (`taskkill /F`, Task Manager), `beforeunload` never executed. As measured in Handoff 007, orphaned engine processes remained running indefinitely (+200s observed), consuming system resources and holding port bindings.
3. **Timer throttling in background tabs**: Browsers throttle timers (`setInterval`) when tabs are backgrounded or occluded, making aggressive sub-minute timeouts prone to false shutdowns.

## Decision
We replace the fragile `beforeunload` shutdown beacon with an active client-driven heartbeat coupled with a server-side watchdog timer:

1. **Heartbeat ping protocol**: The desktop UI emits an HTTP `GET /api/heartbeat` every 2,000 ms. Each heartbeat resets the engine's internal `last_heartbeat` timestamp.
2. **Watchdog timer**: The engine runs a background daemon thread checking `time.monotonic() - last_heartbeat > watchdog_timeout`.
   - Default timeout is **180 seconds** (configurable via `--watchdog=SECONDS`; `--watchdog=0` disables the watchdog).
   - The watchdog **never fires during an active audit scan** (`is_auditing` flag suppresses timeout shutdown).
   - Re-arms automatically on sudden clock jumps (e.g., system sleep or CPU stall).
3. **Rationale for 180 seconds**: Accommodates aggressive Chromium/WebView2 timer throttling on hidden windows while guaranteeing orphan cleanup. As measured in clean-machine tests (`evals/results/raw/007-watchdog-timing.json`), orphaned engines exit cleanly at ~180.72s after parent shell termination.

## Consequences
- UI reloads (F5, `Page.reload`) no longer terminate the engine process; the same engine PID handles re-connection cleanly (verified in maintainer lab record 012-shell-reload, not published).
- If the shell is killed abruptly without sending a shutdown command, the engine cleanly exits within 180s.
- Clean application exit via `WM_CLOSE` posts an explicit `/api/shutdown` call, terminating all processes in < 0.5s.

## What is Not Covered
- Linux and macOS daemon lifetime management (current implementation focuses on Windows WebView2 shell).
- Direct OS-level parent process PID monitoring (Job Objects or `proc.Handle` binding) if the shell does not pass a parent PID flag.
