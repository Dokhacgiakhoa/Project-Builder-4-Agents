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

## M3b — Real-tokenizer measurement (after `claude auth login`)
Command: `python evals/measure_docs.py --counter cli lang 58e5df8`. Method: differential token count through `claude -p` with skills, MCP and settings disabled (fixed overhead about 180 tokens; baseline subtracted). 9 near-parallel pairs (word ratio 0.75-1.25); 2 pairs skipped because content diverged.

| file | tokens vi | tokens en | en/vi |
| :-- | --: | --: | --: |
| core/discovery.md | 1635 | 1452 | 0.89 |
| core/README.md | 1598 | 1307 | 0.82 |
| core/standards/coding-conventions.md | 837 | 661 | 0.79 |
| core/standards/definition-of-done.md | 553 | 451 | 0.82 |
| core/standards/test-strategy.md | 433 | 358 | 0.83 |
| profiles/architecture/clean-architecture-layout.md | 1153 | 1089 | 0.94 |
| profiles/architecture/simple-layered.md | 987 | 851 | 0.86 |
| profiles/architecture/vertical-slice.md | 894 | 880 | 0.98 |
| profiles/README.md | 1601 | 1678 | 1.05 |
| **total** | **9691** | **8727** | **0.90** |

English used about **10% fewer tokens** (per file from 21% fewer to 5% more). The 40-60% claim is contradicted for these docs. Limits: near-parallel, not exact translations (the English versions were also edited); 9 files; one model tokenizer (Sonnet) and date; markdown and code-heavy text dilutes the language effect.

Observation: a default `claude -p` call in this maintainer's environment cost 57,543 input tokens for the word "hello" (about $0.35 notional) because skills, MCP tools and settings are loaded; with those disabled it cost 178 tokens. Large skill/tool catalogs have a real per-session context cost. The split between skills, MCP tools and the base prompt was not decomposed.

## M4 — Health Check speed: target met on synthetic input
Command: `python evals/bench_health_check.py --runs 5`.

| target | runs | median s | min s | max s |
| :-- | --: | --: | --: | --: |
| this repo (381 tracked files) | 5 | 0.84 | 0.81 | 0.99 |
| synthetic 500 files | 3 | 0.38 | 0.35 | 1.09 |
| synthetic 1000 files | 3 | 0.61 | 0.48 | 1.04 |
| synthetic 5000 files | 3 | 1.80 | 1.61 | 4.54 |

The A2 target "5,000 files < 30 s" holds for Python on this machine with small synthetic files. The packaged `.exe` and a clean Windows machine were not measured.
