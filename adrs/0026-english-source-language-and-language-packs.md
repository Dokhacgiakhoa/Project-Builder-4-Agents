# ADR-0026: English Is the Source Language; Other Languages Are Packs

- Status: Accepted (2026-11-08)
- Refines: ADR-0014 (English as primary language), ADR-0023 (UI English by default)

## Context
The audit engine wrote its findings, report and summaries in Vietnamese. The UI was English by default, so it translated Vietnamese to English with a hand-maintained dictionary (`VI_TO_EN`) plus regular expressions. Every sentence missing from that dictionary leaked through as Vietnamese (the Analysis summary, finding descriptions), and the dictionary could never be complete because many sentences carry variable numbers and names. The direction was also wrong for the goal of supporting more languages (Chinese, Russian, Hindi, Japanese, Korean, ...): each new language would need a translation from Vietnamese.

## Decision
1. **The engine emits English only**: findings, section headings of `project-review.md`, summaries, log lines, pillar names. Severity values are `High`, `Medium`, `Low` (they were `Cao`, `Trung bình`, `Thấp`); the report front matter uses `findings: {high, medium, low}`.
2. **Other languages are packs translated from English.** A pack is `scripts/reviewer_shell/static/js/lang/<code>.engine.js` registering `window.I18N_ENGINE_PACKS[<code>] = { exact: {english: translated}, templates: [{en, tr}] }`.
   * `exact` maps a whole English string to its translation.
   * `templates` cover sentences with variable parts, written `{p1}`, `{p2}`, ... so word order can differ per language. A captured value is itself translated (also item by item for `a; b` / `a, b` lists).
   * `i18n.js` looks up the string exactly, then by template, then sentence by sentence for paragraphs the engine joined; anything without a translation is shown in English.
3. **Adding a language** = add `lang/<code>.engine.js`, load it in `index.html` before `i18n.js`, add the UI strings under `DICT.<code>` in `i18n.js`. No engine change.
4. **Detection patterns keep their own language.** Regular expressions that look for Vietnamese phrases inside the *scanned project* (prompt-injection phrases in `safety.py`, README/agent-rule keywords in `pillars_docs.py`) stay Vietnamese: they describe the content under test, not the engine's output. The same holds for the `remediation.py` rules, which match the engine's own English text and therefore use English keywords.
5. **Engine sentences must be complete per variant.** When the engine appends an optional part to a sentence, the pack needs a template for each variant (see the two composed templates in `vi.engine.js`).

## Constraints
* Never compare engine text case-sensitively in logic (`DESIGN TOKENS` vs `Design tokens`); `Criterion.__contains__` is case-insensitive.
* `tests/test_engine_english.py` fails if the report or the UI data contains Vietnamese, and checks every pack for English keys and consistent placeholders.
* The change was verified against the previous engine on 23 projects: identical score and identical findings (code, level, location).

## Consequences
* Anything reading `project-review.md` sees English headings, `High/Medium/Low` and new front-matter keys: a breaking change, released as 0.2.0.
* Not covered: titles of knowledge-base documents that are written in Vietnamese (shown as is), Vietnamese code comments, and labels that were already English identifiers.
