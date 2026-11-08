---
title: "Multi-Tool Configuration"
description: ".claude/.codex/.gemini mirrors, permissions, and scope guards — cohorts 1 & 2"
weight: 5
---

# Multi-Tool Agent Configuration

## The Challenge

Engineering teams utilize multiple AI assistants (Claude Code, Cursor, Codex, Gemini CLI, Copilot, Antigravity). Each tool maintains distinct configuration schemas. Without standardization, telemetry logging breaks, dangerous shell permissions are granted, and workflows become fragmented.

## Pattern 1: Multi-Tool Telemetry Hooks

Standardize hooks across tool configurations to route execution telemetry to a shared script `scripts/log_hook.py`:
- `.claude/settings.json` — Claude Code
- `.cursor/hooks.json` — Cursor
- `.codex/hooks.json` — Codex CLI
- `.gemini/settings.json` — Gemini CLI
- `.github/hooks/hooks.json` — Copilot Workspace
- `.agents/rules/` — Antigravity / Cursor rules

## Pattern 2: Defensive Fallback (`|| true`) (Team 003)

Telemetry logging hooks must never block local developer tasks if logging servers are temporarily offline:

```json
"command": "bash scripts/_pyrun.sh scripts/log_hook.py --tool=claude 2>/dev/null || true"
```

## Pattern 3: Differentiated Tool Mirroring (Team 011 CareerPulse)

Configure tool entry points to leverage individual model strengths:
- `.claude/` — Deep architectural refactoring and validation
- `.codex/` — Rapid implementation and boilerplate scaffolding
- `.gemini/` — Large-context repository auditing and documentation drift detection

## Pattern 4: Explicit Allow/Deny Permission Lists (Team 011)

Configure `.claude/settings.json` with a curated deny list to prevent accidental security breaches:

```json
"deny": [
  "Read(.env)",
  "Read(**/*credential*)",
  "Bash(rm -rf:*)",
  "Bash(git push --force:*)",
  "Bash(sudo:*)",
  "Bash(* --no-verify*)"
]
```

## Pattern 5: Repository Scope Guards (Team 009 VibeMaster)

Bash pre-execution hooks to prevent commands escaping the repository boundary:

```bash
BLOCKED_PATTERNS=(
  'cd[[:space:]]+\.\./'
  'rm[[:space:]]+-rf[[:space:]]+/'
  'sudo[[:space:]]'
)
```

## Anti-Patterns to Avoid

- Hardcoded absolute machine paths (`/Users/username/...`) — breaks on peer machines.
- Disabling hooks by renaming to `.bak` — leaves gaps in development audit logs.
- Triplicating identical documentation files rather than maintaining single canonical sources.
