---
id: G-006
type: reference
when: "When needing to **select and configure MCP Servers (Model Context Protocol)** to connect production tools"
---

# CURATED MCP SERVERS MATRIX FOR AI AGENTS

> **For AI Agents**: The Model Context Protocol (MCP) connects AI Agents directly to infrastructure (Databases, GitHub, Cloud, Headless Browsers) without manual developer intervention. This matrix catalogs battle-tested, secure MCP servers and standardized JSON templates for Claude Code, Cursor, Windsurf, and Antigravity.

---

## 1. Curated MCP Servers by Operational Capability

| Operational Task / Infrastructure | Recommended MCP Server | Agent Capability | Security Level |
| :-- | :-- | :-- | :-: |
| **Git Operations & Issue/PR Management** | `@modelcontextprotocol/server-github` | Inspect issues, generate PRs, traverse GitHub trees | ✅ High (Uses Personal Token) |
| **PostgreSQL / Supabase Database** | `@modelcontextprotocol/server-postgres` | Inspect schemas, verify indexes, run diagnostic queries | ⚠️ Enforce Read-Only when possible |
| **Local SQLite Database** | `mcp-server-sqlite` | Query `.db` files directly, debug local states | ✅ Safe (Local sandbox execution) |
| **Visual QA & Browser Automation** | `mcp-server-playwright` / Chrome DevTools | Headless browser execution, UI screenshots, click tests | ✅ Safe in sandbox |
| **Scoped Filesystem Operations** | `@modelcontextprotocol/server-filesystem` | Direct read/write within whitelisted project folders | ✅ High (Enforces strict root bound) |

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
    "sqlite": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "./data/app.db"]
    },
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
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${env:GITHUB_TOKEN}"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "${env:DATABASE_URL}"]
    }
  }
}
```
