# Report 017: English engine output and language packs (v0.2.0)

Run by the reviewer (Claude) on 2026-11-08. Raw data: `evals/results/raw/017*`. Decision record: `adrs/0026-english-source-language-and-language-packs.md`.

## Change
The audit engine now emits English only; the Vietnamese UI text comes from a pack translated from English (`static/js/lang/vi.engine.js`: 481 exact strings, 123 templates). Severity values are `High/Medium/Low`; the report front matter keys are `findings: {high, medium, low}`. The legacy Vietnamese-keyed dictionary (`VI_TO_EN`) was removed. 615 literals in `scripts/auditor_engine/` were translated; the 36 remaining Vietnamese literals are detection patterns for Vietnamese content inside scanned projects and were kept on purpose.

## Subject
* Exe: `Project-Builder-Analytics.exe`, SHA-256 `ed6d0d7325cd20cfc16f9a779ec2847a98b80ca795828de314956f70ef2e0168`, 61,548,122 bytes; `CURRENT_VERSION` 0.2.0.
* Machine: same machine class as report 016.

## Gates

| Gate | Observation | Result |
| :-- | :-- | :-- |
| G1 | `pytest tests -q`: 175 passed (3 new in `tests/test_engine_english.py`); `check_links.py`: 0 broken links, 0 structure errors. | Holds |
| G2 | Exe vs `python scripts/engine_main.py` on 21 corpus repos + P-062 + this repo, same environment: score equal 23/23, report identical (timestamps normalised) 23/23 (`raw/017d-exe-identity.txt`). | Holds |
| Behaviour preserved | Engine before the change (commit `bb641a9`) vs after, on the same 23 targets: score and the multiset of findings (code, level, location) identical on 23/23 (`raw/017-final-head.json`, `raw/017-final-new.json`; descriptions are not compared because their language changed). | Holds |

The comparison against the old engine found two real defects during the work, both fixed before this result: a remediation pattern that was too broad (React "Error Boundary" findings were re-classified as `ARCH-004`) and case-sensitive substring checks that lost a score bonus when text casing changed (garak 50 vs 49). They are the reason the comparison was run on all 23 targets instead of a sample.

## Measurements (no pass/fail)
* English test: on a synthetic project the old engine's report has 106 lines containing Vietnamese letters, the new engine's report has 0 of 174 lines; the new test fails on the old engine.
* Browser check of the UI served from source (English mode): 0 elements with Vietnamese text across all tabs and all sidebar categories, on 4 audited projects.
* Vietnamese mode: of 377 distinct engine strings from 4 audited projects, 297 are translated, 80 are shown in English. Of the 80: 11 are sentences quoted from the kit's own English documents (profile constraints), the rest are English labels and code snippets that were English before the change (for example `Readme & Onboarding`, `DTO Validation`). Sampling was manual.

## Not covered
* UI: the maintainer tested the interface manually on `ed6d0d73...` (same file, hash checked again before release) and reported it fine.
* Vietnamese code comments and docstrings remain (not user-visible), as do Vietnamese titles of knowledge-base documents shown in the analysis tab.
* Clean-machine behaviour, watchdog and reload were not re-run for this build.
* The Vietnamese pack was generated from the engine's former strings and the old dictionary; its wording was not reviewed by a Vietnamese reader for this report.
