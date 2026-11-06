# MEASUREMENTS — 2026-11-07

Machine: Windows 11, Python 3.14.0, one run session. Commit: see `git log` at the time of this file. Tools: `evals/measure_docs.py`, `evals/bench_health_check.py`.

## M1 — "All knowledge documents are < 120 lines": NOT TRUE
Command: `python evals/measure_docs.py limit 120`. 34 governed docs (core/, profiles/ without templates and starter), 5 exceed 120 lines:

| file | lines |
| :-- | --: |
| profiles/skills-catalog/curated-agent-skills.md | 264 |
| profiles/design/design-archetypes-catalog.md | 253 |
| profiles/documentation/guides/developer-onboarding-guide.md | 142 |
| profiles/design/visual-dna-prompts.md | 139 |
| profiles/documentation/guides/incident-runbook-template.md | 134 |

The enforced rule (`check_links.py`) only limits architecture profiles to 120 lines.

## M2 — Bootstrap read budget (proxy)
Command: `python evals/measure_docs.py path` (profile `vertical-slice`). Path: BOOTSTRAP, core/README, AGENTS template, discovery, INDEX, profiles/README, one architecture profile, go-live checklist. Total **40,734 bytes, about 10,150 tokens by the chars/4 proxy** (proxy, not a Claude tokenizer). `INDEX.md` alone is 10,800 bytes (about 2,700 tokens by proxy) and is read for routing.

## M3 — English vs Vietnamese: the 40-60% claim is NOT supported by what could be measured
Command: `python evals/measure_docs.py lang 58e5df8`. 11 files that were Vietnamese at 58e5df8 and are English now:
bytes en/vi = 0.92, words en/vi = 0.85, chars en/vi = 1.05.
These are not parallel translations (content changed), and bytes and words are not tokens, so this neither proves nor disproves the token claim. It does show the size difference in raw text is far below 40-60%. A real tokenizer on a parallel corpus is still required (see `benchmark-plan.md`).

## M4 — Health Check speed: target met on synthetic input
Command: `python evals/bench_health_check.py --runs 5`.

| target | runs | median s | min s | max s |
| :-- | --: | --: | --: | --: |
| this repo (381 tracked files) | 5 | 0.84 | 0.81 | 0.99 |
| synthetic 500 files | 3 | 0.38 | 0.35 | 1.09 |
| synthetic 1000 files | 3 | 0.61 | 0.48 | 1.04 |
| synthetic 5000 files | 3 | 1.80 | 1.61 | 4.54 |

The A2 target "5,000 files < 30 s" holds for Python on this machine with small synthetic files. The packaged `.exe` and a clean Windows machine were not measured.
