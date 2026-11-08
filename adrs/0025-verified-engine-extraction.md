# ADR-0025: Verified, Content-Addressed Engine Extraction

- Status: Accepted (2026-11-08)
- Refines: ADR-0022 (single exe with embedded engine)

## Context
ADR-0022 embeds `reviewer-engine.exe` in the shell and extracts it to `%TEMP%\ProjectHealthCheck\engine\reviewer-engine.exe`. The first implementation reused an existing file **when its length equalled the embedded length** and wrote with `FileMode.Create` / `FileShare.None`. Review of reports 013 and 014 found three defects (none exercised by the tests, because the sizes always matched):
1. A rebuilt engine with the same length is ignored and the old engine runs silently.
2. Any process of the same user can put a same-length file there and the shell runs it.
3. If an older instance still runs (file locked), extracting a newer engine fails, the error is swallowed and the shell reports "Core Engine Missing".

## Decision
`tools/ProjectReviewer/EngineExtractor.cs`:
1. Hash the embedded resource (SHA-256). Extract to `...\engine\<first 16 hex of the hash>\reviewer-engine.exe`, one folder per build, so a running older engine never blocks a newer one.
2. Reuse an existing file only if its SHA-256 equals the embedded one; otherwise delete it (if possible) and publish again.
3. Publish by writing a unique `.tmp` file and `File.Move(..., overwrite: false)`; a named mutex per build (`Local\ProjectHealthCheck.engine.<prefix>`) serializes check, delete and publish across instances.
4. If the wrong file cannot be replaced (locked) or the lock times out (20 s), run a verified private copy under `own-<pid>\` instead of failing.
5. After publishing, best-effort prune other build folders and the legacy flat file (a running engine keeps its folder).
6. `engine\` beside the exe is still preferred when present (development), unchanged from ADR-0022.

## Verification (2026-11-08, on the author's machine, signed Microsoft .NET SDK 10.0.403)
- `dotnet run --project tools/EngineExtractorCheck`: 9 scenarios (fresh, reuse, same-size tampered, tampered and locked, same-length rebuild, pruning, newer build while older is locked, 16 concurrent extractions, missing resource). 60 consecutive runs, 0 failures. An earlier version without the mutex failed scenario 8 in about 10% of runs (a thread deleted a file another thread had just published); a version that overwrote on move failed scenario 4.
- The shell compiles. **Not yet verified:** the rebuilt single exe end to end (handoff 015).

## Consequences
- Startup hashes the 9 MB resource (and the extracted file on reuse); expected cost is tens of milliseconds, not yet measured in the shell.
- Old build folders accumulate only if they are locked at prune time.

## Not covered
- Time-of-check/time-of-use: a same-user process can still swap the file between verification and launch. Defending against that needs a protected location (not `%TEMP%`) or signature verification; out of scope here.
- `%TEMP%` that is read-only or full: extraction fails and the shell shows the existing "Core Engine Missing" dialog.
- The `engine\` beside-the-exe preference means a stale `engine\` folder next to the exe overrides the embedded engine.
