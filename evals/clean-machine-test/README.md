# Clean-machine test for Project Health Check (TASKS.md, A2)

Goal: check whether `Project-Health-Check.exe` and `engine\reviewer-engine.exe` run on a Windows machine with **no Python and no .NET installed**. Nothing here has been run on a truly clean machine yet; the results file below is where that evidence goes.

## What is tested
| Folder | Contents | Expected on a machine without .NET |
| :-- | :-- | :-- |
| `app-fd` | default shell exe (framework-dependent) + `engine\reviewer-engine.exe` | does **not** start (needs the .NET 10 Desktop Runtime) |
| `app-sc` | shell exe built with `python scripts/build_exe.py --shell-only --self-contained` (about 50 MB) + the same engine | starts, shows the UI, closes cleanly |

These expectations come from Microsoft's .NET deployment documentation and a stripped-environment run on a development machine. They are hypotheses until the clean-machine run confirms them.

## Binaries are not in git
The engine is git-ignored and the self-contained exe is about 50 MB, so neither is committed. Get them from the maintainer as `HealthCheck-clean-test.zip` (it already contains `app-fd`, `app-sc` and these scripts), or build them on a machine with Python 3.12+, PyInstaller and the .NET 10 SDK and copy the results to the clean machine. Do not build on the machine under test: that would install the dependencies being tested.

## Run
1. Use a Windows machine without Python and without .NET (check `python --version` and `dotnet --list-runtimes` fail). Windows 11 or 10 with Edge/WebView2 is expected.
2. Put `app-fd`, `app-sc` and the three scripts from this folder in one directory outside any repo.
3. Double-click `run-test.cmd`. Each variant takes about 40 seconds and opens a window. Do not click anything.
4. Collect the `results\fd` and `results\sc` folders (`result.txt`, `screen.png`).

## Write the report
Create `evals/results/<YYYY-MM-DD>-clean-machine-test.md` with these sections, then commit it:
1. **Machine**: Windows edition and build, physical or VM, Python/.NET/WebView2 status copied from `result.txt`.
2. **Result per variant**: started or not, window title, engine processes, exit code, what `screen.png` shows.
3. **Verdict per hypothesis** in the table above: confirmed, contradicted, or not tested.
4. **Not verified**: anything not exercised (for example SmartScreen behaviour, a missing WebView2 runtime, running an audit from the UI).
5. **Next step**, only if the result requires one.

Rules for the report: state facts from the files, quote the exact error text when something fails, and do not claim a variant "works" beyond what `result.txt` shows. A machine that already has Python or .NET does not prove the clean-machine claim; say so.

After the report is committed, update `TASKS.md` item A2 and add a row to the progress log.
