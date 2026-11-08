---
id: G-006
type: reference
when: "When needing to **select and configure MCP Servers (Model Context Protocol)** to connect production tools"
---

# CURATED MCP SERVERS MATRIX FOR AI AGENTS

> **For AI Agents**: The Model Context Protocol (MCP) connects AI Agents directly to infrastructure (Databases, GitHub, Cloud, Headless Browsers) without manual developer intervention. This matrix catalogs commonly used MCP servers (not independently security-audited; review each before installing) and standardized JSON templates for Claude Code, Cursor, Windsurf, and Antigravity.

---

## 1. Curated MCP Servers by Operational Capability

> **Verification log (2026-11-07, npm registry + GitHub API + upstream READMEs)**: package names, maintenance status, and install forms below were checked on that date. Re-verify before use; these servers change quickly. "Security" is not rated here: none of these servers was audited by this kit.

| Operational Task / Infrastructure | MCP Server (verified exists) | Agent Capability | Status on 2026-11-07 |
| :-- | :-- | :-- | :-- |
| **Git Operations & Issue/PR Management** | `github/github-mcp-server` (MIT, official GitHub; remote URL `https://api.githubcopilot.com/mcp/` or Docker image `ghcr.io/github/github-mcp-server`) | Issues, PRs, repository tree | Active. Use a least-privilege token. |
| **PostgreSQL Database** | `crystaldba/postgres-mcp` (PyPI `postgres-mcp`, MIT; `--access-mode=restricted` = read-only) | Schema inspection, index analysis, queries | Active, third-party. Prefer `restricted` outside local dev. |
| **Visual QA & Browser Automation** | `@playwright/mcp` (npm, `microsoft/playwright-mcp`) or `chrome-devtools-mcp` (npm, `ChromeDevTools/chrome-devtools-mcp`) | Browser control, screenshots, DOM/console inspection | Both active. Run against local/dev targets only. |
| **Scoped Filesystem Operations** | `@modelcontextprotocol/server-filesystem` (npm) | Read/write inside listed directories | Active, maintained in `modelcontextprotocol/servers`. |

**Do not use (checked 2026-11-07)**: `@modelcontextprotocol/server-github` and `@modelcontextprotocol/server-postgres` are marked deprecated on npm ("Archived and unmaintained; no security guarantees"). `@modelcontextprotocol/server-playwright` does not exist on npm. The official SQLite server (`mcp-server-sqlite` on PyPI) is from the archived servers repo; the npm package with the same name is a different, unofficial 0.0.2 package. No maintained SQLite MCP server was verified, so none is recommended.

---

## 2. MCP Security Principles for Vibe Coders
1. **Zero Bloat**: Enable only the specific MCP servers required for the active stack to preserve context window tokens.
2. **Principle of Least Privilege**: For database MCP servers, never connect with superuser credentials that permit `DROP DATABASE`. Use accounts restricted to `SELECT`, `INSERT`, `UPDATE`.
3. **Zero Secrets in Git**: Never commit personal access tokens or passwords in workspace JSON configs. Reference environment variables (`${env:GITHUB_TOKEN}`).

---

## 3. Production MCP JSON Configuration Templates

### Template 1: Configuration for Claude Desktop / Claude Code (`claude_desktop_config.json`)
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "./src", "./docs"]
    }
  }
}
```

### Template 2: Configuration for Cursor / Windsurf (`.cursor/mcp.json` or `.windsurf/mcp.json`)
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"]
    },
    "postgres": {
      "command": "uvx",
      "args": ["postgres-mcp", "--access-mode=restricted"],
      "env": {
        "DATABASE_URI": "${env:DATABASE_URL}"
      }
    }
  }
}
```
