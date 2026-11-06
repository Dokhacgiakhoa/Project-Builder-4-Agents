# Clean-machine test, run of `run-test.cmd` (A2), 2026-11-07

Source: zip of `origin/fix/health-check-remediation` (head `d66f9a5`, 73,491,476 bytes) downloaded from GitHub and extracted into a scratch directory outside the repo. Script run: `evals/clean-machine-test/run-test.cmd` → `run-all.ps1` → `run-test.ps1` for `app-fd` and `app-sc`.

## Verdict
**The test is invalid. It did not measure the exe at all, and the machine is not clean.** Do not use this run as evidence for or against the A2 hypotheses.

## 1. Machine
Taken from `results\*\result.txt`:
- Windows 11 Pro, build 10.0.26300.0 (physical/VM not recorded).
- Python on PATH: **True**; `py` launcher: **True**.
- dotnet on PATH: **True**; WindowsDesktop runtime **10.0.14** present.
- WebView2 runtime: 157.0.4341.42.

This is the maintainer's development machine, so it already has everything the test needs to be absent.

## 2. Result per variant
Both `app-fd` and `app-sc` gave the same outcome:
- The zip has no `app-fd` or `app-sc` folder. `evals/clean-machine-test` holds only `README.md`, `run-all.ps1`, `run-test.cmd`, `run-test.ps1`. The README says the binaries are not in git and come from the maintainer as `HealthCheck-clean-test.zip`.
- Headless audit: `audit failed: The term '...\app-<v>\engine\reviewer-engine.exe' is not recognized as the name of a cmdlet, function, script file, or operable program.`
- `exe sha256:` empty (file missing).
- `Start-Process` failed, so `$p` was null. The script then logged `shell alive: True`, `window title: []`, `engine processes: 0` and `shell had to be force-closed (a dialog was probably open)`. **`shell alive: True` is a false positive** (`-not $null.HasExited` evaluates to True). The script's final `Stop-Process -Id $null` also raised an error.
- `screen.png` was saved for each variant; I did not inspect it, and it shows this desktop, not an app.

## 3. Verdict per hypothesis
| Hypothesis | Verdict |
| :-- | :-- |
| `app-fd` does not start without the .NET 10 Desktop Runtime | **Not tested** (exe absent; .NET is installed here) |
| `app-sc` starts, shows the UI, closes cleanly | **Not tested** (exe absent) |

## 4. Not verified
- Everything about the exes: startup, window title, engine port and `/api/status`, audit output, SmartScreen, missing WebView2.
- Behaviour on a machine without Python and .NET.

## 5. Next step
1. Get `HealthCheck-clean-test.zip` from the maintainer (or build per the README on another machine) and run `run-test.cmd` on a Windows machine without Python and .NET.
2. Fix `run-test.ps1` so a missing exe is reported as an error. Check `Test-Path $exe` before launching and skip the "shell alive" lines when `$p` is null. Today a missing binary produces a misleading "alive".

---

# Run 2 (after uninstalling the .NET runtimes)

## What changed
- At the user's request I removed .NET: the "Microsoft Windows Desktop Runtime 10.0.14" bundle uninstalled itself and its dependent Host, Host FX Resolver and Runtime entries. Afterwards `C:\Program Files\dotnet` no longer exists and no .NET entries remain in the uninstall registry keys.
- Python had already been removed by the user. `python` still resolves to the Microsoft Store stub (`...\WindowsApps\python.exe`, "Python was not found"), so `python on PATH: True` in the log is the stub, not an interpreter. `py` launcher: False. A leftover `Python312` folder (5 items, no `python.exe`) remains.
- WebView2 157.0.4341.42 was kept (it ships with Windows 11).

## Binaries used
The branch zip has no `app-fd`/`app-sc`, so I used the binaries already in the repo root, copied into a fresh folder: `Project-Health-Check.exe` (1,450,257 bytes, modified 2026-11-05 08:57, sha256 `840F91EF...97C127`) and `engine\reviewer-engine.exe` (9,147,334 bytes). They are older than the branch's rebuild and are framework-dependent, so only the `app-fd` variant was tested. **`app-sc` was not tested**: a self-contained exe needs the .NET SDK to build, which is now removed.

## Results (`run-test.ps1`, app-fd)
- Environment: dotnet on PATH False, WindowsDesktop runtimes `none`.
- Headless audit of `reviewer-engine.exe` ran with no Python and no .NET: exit code 0, score line "45/100 - F", report written. The report did not contain section 0 or section 7 or `SAFE-001`, which the script expects; this is consistent with an older engine build, but I did not verify that.
- Shell: `shell alive: False`, `shell exit code: -2147450749` (0x80008083) within 25 s; no engine process was started. No window title. I did not open `screen.png`, so I cannot say what dialog, if any, was shown.

## Verdicts
| Hypothesis | Verdict |
| :-- | :-- |
| `app-fd` does not start without the .NET 10 Desktop Runtime | **Confirmed** (framework-dependent build). The user's screenshot of the dialog shows the exact text "You must install .NET Desktop Runtime to run this application." with a "Download now" button, matching exit code 0x80008083. |
| `app-sc` starts, shows the UI, closes cleanly | **Not tested** |

## Caveats
- Not a truly clean machine: this is the dev machine with the Store `python` stub, a leftover Python folder, and the repo and tools present. It is a Windows 11 install with WebView2.
- The tested exe is not the one built from branch `d66f9a5`.
- `run-all.ps1`/`run-test.cmd` were not used for this run (they need `app-fd` and `app-sc`); I ran `run-test.ps1` directly for `app-fd`.

## Next step
Build `app-sc` (`python scripts/build_exe.py --shell-only --self-contained`) on a separate machine, or get `HealthCheck-clean-test.zip`, and test it here, where .NET is now absent.

## Addendum: dialog seen by the user
The user's screenshot shows the shell exe titled `Project-Health-Check.exe` with the text "You must install .NET Desktop Runtime to run this application." and a "Download now" link. This means the default (framework-dependent) exe is not usable by a user without .NET. It is the packaging gap that the branch's `--self-contained` option (commit `972c850`) is meant to close, but that variant has still not been built or run, so the gap is not yet shown to be fixed. Until `app-sc` passes on this machine, docs should not describe the exe as standalone.

---

# Run 3: self-contained build (`app-sc`), same machine without .NET

## Build
Built from the branch zip (`d66f9a5`) with a portable .NET SDK 10.0.403 unpacked in a scratch folder (nothing installed system-wide): `dotnet publish tools/ProjectReviewer/ProjectReviewer.csproj -c Release -r win-x64 --self-contained true -p:EnableCompressionInSingleFile=true`. Output `Project-Health-Check.exe`, 52,110,108 bytes, sha256 `BB8AF232...CC5A61`. Build warnings: MSB3277 WindowsBase version conflict only. The engine is the older `reviewer-engine.exe` from the repo root (Python not available to rebuild), so the engine is not the branch's build. Test folder: `D:\Github\health-check-test\app-sc`.

## Machine state
dotnet on PATH False, no `C:\Program Files\dotnet`, WindowsDesktop runtimes `none`, WebView2 157.0.4341.42. Not fully clean: a stale PATH entry `C:\Program Files\dotnet\`, a leftover `%LOCALAPPDATA%\Programs\Python\Python312` (Lib, Scripts, etc.) with its PATH entries, and a Store `python` stub (so `python on PATH: True` is the stub).

## Result (`results\sc\result.txt`)
- Shell started: `shell alive: True`, window title `[Project Health Check — Project-Builder-4-Agents]`, `responding: True`.
- Engine: 2 `reviewer-engine` processes; pid 21992 on 127.0.0.1:53885 answered `{"status": "ready", "version": "2.1.0"}`.
- Closed cleanly: 0 engine processes left.
- Headless audit: exit 0, "45/100 - F"; report still lacks section 0, section 7 and `SAFE-001` (old engine, not verified).
- `screen.png` shows the whole desktop but I could not see the app window in it, so the UI contents are not confirmed visually; the evidence is the log lines above.

## Verdict
| Hypothesis | Verdict |
| :-- | :-- |
| `app-sc` starts, shows the UI, closes cleanly | **Confirmed on this machine** (no .NET runtime), with the caveats above. Not confirmed on a fully clean machine. |

## Not verified
Rendering of the UI, running an audit from the UI, SmartScreen, machine without WebView2, the branch's rebuilt engine.

## Fix made after this test
`evals/clean-machine-test/run-test.ps1` now checks that `Project-Health-Check.exe` and `engine\reviewer-engine.exe` exist before testing. If not, it logs `ERROR: binary not found: <path>` and `INVALID: binaries missing, nothing was tested`, and exits with code 2. Before, run 1 reported `shell alive: True` for a missing exe. Checked by running it against a nonexistent folder (exit 2, INVALID) and against the real `app-sc` (same results as run 3). `run-all.ps1` was not re-run. Still open: the engine used here is the older one; rebuild it on a machine with Python to check Section 0, Section 7 and `SAFE-001`.
