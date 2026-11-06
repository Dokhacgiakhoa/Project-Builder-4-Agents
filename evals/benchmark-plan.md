# BENCHMARK PLAN — MEASURING THE KIT'S CLAIMS AND COMPARING WITH OTHER PROJECTS

> Status: plan only. Tools marked **EXISTS** are in `evals/` and were run on 2026-11-07; tools marked **TO BUILD** are not written yet. No claim below is supported until its measurement is run. Per `AGENTS.md` rule 13, comparisons must come from these measurements, not assertion.

## 1. Claims, how each is measured, and tool status

| # | Claim | Measurement | Tool | Status |
| :-- | :-- | :-- | :-- | :-- |
| M1 | Docs are small (< 120 lines each) | Count lines of governed docs | `evals/measure_docs.py limit 120` | EXISTS. Result: 5 of 34 exceed (see results file) |
| M2 | Bootstrap read budget is small | Sum size of the bootstrap path docs | `evals/measure_docs.py path` | EXISTS (proxy estimate; real tokens need counter `api` or `cli`) |
| M3 | English docs cost 40-60% fewer tokens than Vietnamese | Token count with a real Claude tokenizer | `measure_docs.py --counter cli lang 58e5df8` | MEASURED on 9 near-parallel docs: about 10% fewer (claim contradicted). A frozen exact-translation corpus is still TO BUILD for a tighter number |
| M4 | Health Check is fast (A2: 5,000 files < 30 s) | Wall-clock on synthetic and real repos, repeated runs | `evals/bench_health_check.py` | EXISTS |
| M5 | Health Check finds real problems without noise (F1: false positives <= 2%, detection >= 90%) | Labeled corpus: >= 20 public repos + self-written attack samples; precision/recall per finding code | TO BUILD (`evals/bench_detection.py` + labeled corpus) | TODO |
| M6 | Agents read BOOTSTRAP.md, interview, pick the right profile (C1/C3) | Fresh-session agent runs, scored by checklist and a 20-prompt routing set | `evals/c1-bootstrap-protocol.md` (manual), runner TO BUILD | TODO |
| M7 | Using the kit yields better projects than not using it | A/B trials, section 2 | runner TO BUILD | TODO |
| M8 | Kit vs Spec Kit vs ECC | Same trials, extra conditions | runner TO BUILD | TODO |

## 2. A/B trial design (M7, M8)

* **Conditions**: (a) no kit, (b) this kit, (c) GitHub Spec Kit, (d) ECC. Same agent, same model, same prompt, fresh empty directory, no memory.
* **Tasks (two kinds, to avoid favoring the kit)**: T1 build a small new app from a one-paragraph brief (kit's best case); T2 add a feature with a changed requirement to an existing seeded repo (Spec Kit/ECC's best case).
* **Repetitions**: >= 5 per condition per task, because outputs are non-deterministic. Report median and spread, not a single run.
* **Neutral scoring (not the kit's own Health Check)**: hidden acceptance tests written before any run; build/lint/test pass; count of agent turns; input+output tokens and cost from the run log; wall time; a third-party static security scan; number of human interventions required.
* **Blinding**: score outputs without knowing the condition; strip tool-specific files before scoring.
* **Invalidation rules**: discard and rerun when the agent crashes or rate-limits; never drop a run for a bad result.
* **Reporting**: publish raw run logs and all conditions, including where this kit loses.

## 3. Tools still to build, in order

1. `evals/make_parallel_corpus.py`: pair each kit doc with a Vietnamese translation produced once, reviewed, and frozen, so M3 compares equal meaning exactly (needs a person to review the translation).
2. `evals/run_trial.py`: create a temp dir, run `claude -p` (headless, fresh session) with the condition's setup and prompt, capture JSON usage/cost/turns, then run the hidden acceptance tests. Needs a logged-in Claude Code or an API key; must be tried on one trial before trusting it.
3. `evals/bench_detection.py`: run the safety scan and the auditor over a labeled corpus, output a confusion matrix per finding code.

## 4. Known limits

* Token counts from `measure_docs.py --counter proxy` are chars/4 and **not** a Claude tokenizer; they underestimate non-English text.
* Synthetic Health Check inputs are small files of four languages; real repos may be slower.
* Results depend on the model version and date; record both.
