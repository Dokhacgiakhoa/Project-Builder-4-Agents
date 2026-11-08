---
title: "Troubleshooting Guide"
description: "Resolving common engineering errors in AI Agent development"
weight: 99
---

# Troubleshooting — Common Engineering Errors

This guide synthesizes common failure modes encountered during agent environment setup, execution, testing, and deployment, accompanied by actionable remediation steps.

---

## Python & Environment

### `ModuleNotFoundError: No module named 'xxx'`

**Root Cause:** Virtual environment is not activated, or packages were installed to system Python.

**Remediation:**
```bash
# 1. Verify python interpreter path is inside .venv
which python
# Output must point to .venv, e.g.: /path/to/project/.venv/bin/python

# 2. Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1

# 3. Reinstall dependencies
pip install -r requirements.txt
```

**If issues persist:**
```bash
# Rebuild virtual environment from scratch
rm -rf .venv
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### `python3.11: command not found`

**Root Cause:** Python 3.11 is not installed or absent from system PATH.

**Remediation (macOS):**
```bash
brew install python@3.11
```

**Remediation (Ubuntu/WSL):**
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev
```

### Slow `pip install` or Timeout Failures

**Remediation:** Use alternative reliable PyPI mirrors or configure timeout thresholds:
```bash
pip install -r requirements.txt --default-timeout=100
```

### `ERROR: Could not build wheel for xxx`

**Root Cause:** Missing C compiler toolchains or development headers.

**Remediation (macOS):**
```bash
xcode-select --install
```

**Remediation (Ubuntu/WSL):**
```bash
sudo apt install build-essential python3.11-dev
```

---

## FastAPI & Server

### `uvicorn: command not found`

**Root Cause:** `uvicorn` is uninstalled or virtual environment is deactivated.

**Remediation:**
```bash
source .venv/bin/activate
pip install uvicorn
```

### `ERROR: [Errno 48] Address already in use` (Port 8000 Conflict)

**Root Cause:** An existing background process is binding port 8000.

**Remediation:**
```bash
# Identify PID holding port 8000
lsof -i :8000  # On Windows: netstat -ano | findstr :8000

# Terminate process
kill -9 <PID>

# Or bind to an alternative port
uvicorn src.api.main:app --reload --port 8001
```

### `openai.AuthenticationError: Invalid API Key`

**Root Cause:** Missing, expired, or improperly parsed API keys.

**Remediation:**
```bash
# 1. Ensure .env exists
ls -la .env
# If missing: cp .env.example .env

# 2. Verify key syntax (no extraneous quotes or whitespace)
grep OPENAI_API_KEY .env

# 3. Quick verification script
python -c "from openai import OpenAI; c=OpenAI(); print(c.models.list().data[:1])"
```

### `pydantic.ValidationError` on Application Startup

**Root Cause:** Environment variables do not match expected types (e.g. `API_PORT="abc"` instead of integer).

**Remediation:** Verify `.env`:
- Integers are numeric (e.g. `8000`)
- Booleans are `true` / `false`
- Enums match declared values (`development` / `staging` / `production`)

---

## LangGraph & Agents

### `ImportError: cannot import name 'StateGraph' from 'langgraph'`

**Root Cause:** Outdated or incomplete LangGraph installation.

**Remediation:**
```bash
pip install --upgrade langgraph langchain-core
```

### `GraphRecursionError: Recursion limit reached`

**Root Cause:** Unbounded loop where conditional edges continuously route back to an antecedent node without reaching `END`.

**Remediation:**
1. Maintain an explicit `iteration` counter in state with a strict recursion ceiling:
```python
def should_continue(state: AgentState) -> str:
    if state.get("iteration", 0) >= 3:
        return END
    if state.get("needs_more_research"):
        return "research"
    return END
```
2. Verify routing functions contain comprehensive fallback defaults.

### `TypeError: expected string or bytes-like object` in Routing Logic

**Root Cause:** Routing function returns a value missing from the mapping dictionary passed to `add_conditional_edges`.

**Remediation:** Ensure all return variants are mapped:
```python
def route(state) -> str:
    if state.get("type") == "search":
        return "search"
    return "answer"  # Fallback

graph.add_conditional_edges(
    "router",
    route,
    {"search": "search", "answer": "answer"}
)
```

---

## Docker & Containers

### `docker: command not found`

**Remediation:** Install Docker Desktop (macOS/Windows) or container engine on Ubuntu:
```bash
sudo apt update
sudo apt install docker.io docker-compose-v2
sudo usermod -aG docker $USER
```

### `docker build` Fails During Package Installation

**Remediation:**
```bash
# Force fresh build without cached layers
docker build --no-cache -t my-agent .
```

### `docker compose up` Unhealthy Service State

**Remediation:**
```bash
# Inspect container logs
docker compose logs api
docker compose logs db

# Clean rebuild
docker compose down -v
docker compose up -d --build
```

---

## Git & Version Control

### `! [rejected] main -> main (fetch first)`

**Remediation:**
```bash
git pull origin main --rebase
# Resolve any merge conflicts
git rebase --continue
git push origin main
```

### `fatal: not a git repository`

**Remediation:**
```bash
git init
git add .
git commit -m "feat: initial repository bootstrap"
git remote add origin https://github.com/your-org/your-repo.git
git push -u origin main
```

---

## Deployment & Production

### API Returns `403 Forbidden` / CORS Errors Post-Deploy

**Root Cause:** Missing production origin in CORS whitelist.

**Remediation:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-frontend.vercel.app",  # Production domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## General Diagnostic Checklist

1. **Examine Tracebacks Thoroughly:** Python stack traces explicitly identify file names and exact line numbers.
2. **Audit Environment Variables:** Over 80% of production deployment failures stem from missing or malformed `.env` keys.
3. **Run Verification Commands:** Execute full test and link validation suites locally before pushing commits.
4. **Clean Rebuild:** When obscure cache issues arise, rebuild the virtual environment and reinstall pinned packages.
