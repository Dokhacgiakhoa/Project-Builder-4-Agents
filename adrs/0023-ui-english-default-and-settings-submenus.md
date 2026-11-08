# ADR-0023: English-Default UI, Language Setting, and Settings Submenus

- Status: Accepted (2026-11-08)
- Builds on: ADR-0011 (WebView2 shell), ADR-0014 (English as primary language), ADR-0022 (single exe)

## Context
The desktop UI (`scripts/reviewer_shell/static`), the C# shell dialogs and the server/CLI messages were written in Vietnamese, contradicting ADR-0014. The settings dialog was one flat form: theme, provider, API key, model and a knowledge-update button.

## Decision
1. **English is the default and the source language.** All UI strings in `index.html`, `app.js`, `server.py`, `llm_evaluator.py`, `settings_manager.py`, `engine_main.py`, `MainForm.cs` and `Program.cs` are English.
2. **Language setting** (`language`: `en` | `vi`, stored in `~/.starter-kit/settings.json`, default `en`). `static/js/i18n.js` holds a `vi` dictionary keyed by the English text; `t(key, vars)` translates dynamic strings; static HTML is translated by matching leaf text, `title`, `placeholder`, or `data-i18n-html` for mixed markup. Switching previews instantly and re-renders the current audit result; Cancel reverts.
3. **Settings is a dialog with a left submenu**: Appearance, Language, API Keys (provider, key, model, test, include-code), User Guide, About & Version (version from `/api/status`, update check, kit knowledge update).
4. **AI Deep Review replies in the selected language** (`language` is sent to `/api/llm-review`; the prompt itself is English).
5. Pillar labels are rendered from the pillar key, not from the engine-supplied name.

## Consequences
- A new UI string needs an English key in code and a `vi` entry in `i18n.js`; a missing entry falls back to English.
- Severity values are English engine data (`High`/`Medium`/`Low`, see ADR-0026) and are mapped for display only.

## Not covered (known gap)
- **Text produced by the audit engine is still Vietnamese**: finding titles, remediation text, archetype and grade labels, pillar criteria and the scan log (about 800 lines across `scripts/auditor_engine/`, and the generated `project-review.md`). Translating it needs coordinated test and report-format changes; tracked in `TASKS.md`.
- The `vi` dictionary and the English default are checked only in the web UI in a browser on this machine; the rebuilt exe is not yet verified.
