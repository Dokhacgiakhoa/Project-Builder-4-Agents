# C1 — BOOTSTRAP VERIFICATION SCENARIOS WITH REAL AGENTS

> For the kit maintainer. Goal: see whether the Agent **by itself** reads `BOOTSTRAP.md`, interviews the user, chooses a profile and builds the project correctly. Run with **Claude Code** and **Antigravity** (Codex not verified). Record the results in section 5 and update `TASKS.md` (C1, C4).

## 1. Conditions for the test to be valid
* **A fresh session with no context**: do not paste the kit content and do not name files. The Agent has only the prompt sentence in section 2.
* **The trial folder is outside the kit repo** and has no existing `AGENTS.md`/`.agents/` (scenario S1) or only a half-finished project (S2).
* The kit must be reachable: after **B1 (rename the repo) + push**, use the URL; before that, use the local-path variant (section 2b). State which variant was used.
* The tester answers **exactly in the role (section 3)** and gives no extra hints.

## 2. Prompt (exactly one sentence)
a. With a URL: `Please use https://github.com/Dokhacgiakhoa/Project-Builder-4-Agents to build a project for me. I want to make: <description from section 3>`
b. Without a URL (early trial): `Please use the document set at <kit folder path on this machine> to build a project for me, starting from BOOTSTRAP.md. I want to make: <description from section 3>`

## 3. Scenarios and user role
| Code | Trial folder | Description given to the Agent | Expected architecture | Guardrail level |
| :-- | :-- | :-- | :-- | :-: |
| S1 | Empty | "a small web app to record my daily spending, for a course project" | Simple layered | M1 |
| S2 | A half-finished project (for example a small Node/React app with a `package.json`, `src/`, no `AGENTS.md` yet) | "this project is half-done, please set it up properly" | Keep the existing structure; MERGE mode, no overwriting | M1 |
| S3 | Empty | "a booking system for several clinic branches, with pricing rules, to be developed for many years" | Clean Architecture or Modular Monolith, with reasons | M2 or higher |

**User role**: a fresher who knows a little git and does not know architecture terms. When the Agent asks:
* about technology: "I am not familiar with it, you choose for me";
* about budget: "free";
* about who will work on it: "alone" (S1, S2), "a team of 3" (S3);
* an unfamiliar term: ask for an explanation, then agree with the proposal.

## 4. Scoring checklist (each item Pass/Fail + a note)
**Initiative and routing**
1. The Agent opens `BOOTSTRAP.md` by itself (no need to name the file).
2. The Agent looks up `INDEX.md`/`profiles/README.md` and does not ask the user for the architecture name.
3. A reasonable number of kit documents opened (it does not read the whole `knowledge-base/` folder).
4. It chooses the expected profile, states a **one-sentence reason** and the options it rejected.

**Interview**
5. ≤ 3 questions per turn; it starts from the user/problem, not from technology.
6. It has a summary step and **waits for confirmation** before building the skeleton.

**Core skeleton**
7. There are `AGENTS.md`, `CLAUDE.md` (importing `AGENTS.md`), skills where the tool can read them, `docs/project-brief.md`, the stack + architecture ADRs, `.builder/kit.json`.
8. No `{{PLACEHOLDER}}` remains when finished.
9. S2: it does not overwrite or delete the user's files; conflicting files get a `.kit-suggested` copy.
10. It does not `commit`/`push` by itself without agreement.

**Guardrails and verification**
11. The test/lint/build commands in `AGENTS.md` are **real** commands and were run.
12. CI runs exactly those commands (no mock `echo`).
13. It installs the guardrails at the chosen level (M2+: a rule that enforces import boundaries).
14. It runs Analytics; score ≥ 80; Core Baseline B1–B9 pass.
15. The final report to the user is in simple words.

**Safety**
16. No secret is placed in files; there is a `.env.example`.

## 5. Result recording template
| Date | Agent + version | Scenario | Prompt variant | Pass/16 | Analytics score | Where it went wrong/off (checklist item, description) | What to fix in the kit |
| :-- | :-- | :-- | :-: | :-: | :-: | :-- | :-- |
| | | | | | | | |

Attach: the conversation record (or screenshots), the resulting folder tree, `project-review.md`.
