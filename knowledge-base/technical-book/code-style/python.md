---
title: "Python Code Style"
description: "Python coding standards and quality conventions"
weight: 1
---

## Python Style Guide

### 1. Type Hints — MANDATORY

```python
# ✅ GOOD — Full type hints
async def analyze_sentiment(text: str) -> dict[str, float]:
    """Analyze text sentiment."""
    result = await model.predict(text)
    return {"positive": result.pos, "negative": result.neg}

# ❌ BAD — Missing type hints
def process(data):
    x = model.run(data)
    return x
```

### 2. Function Rules

- **Max 30 lines** per function — decompose if longer
- **Max 3 parameters** — use Pydantic models for larger inputs
- **Always declare return type hints**
- **Docstring** cho public functions

### 3. Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| File | snake_case | `analyze_node.py` |
| Function | snake_case | `def analyze_query()` |
| Class | PascalCase | `class AgentState` |
| Constant | UPPER_SNAKE | `MAX_RETRIES = 3` |

### 4. Import Order

```python
# 1. Standard library
import os
from typing import Optional

# 2. Third-party
from fastapi import APIRouter, HTTPException
from langchain_core.tools import tool

# 3. Local
from src.config import get_settings
from src.models.schemas import ChatRequest
```

### 5. Error Handling

```python
# ✅ GOOD — Specific exception
try:
    result = await llm.ainvoke(prompt)
except openai.APIError as e:
    logger.error(f"LLM call failed: {e}")
    return {"error": str(e)}

# ❌ BAD — Bare except (masks all failures)
try:
    result = await llm.ainvoke(prompt)
except:  # Masks all errors!
    pass
```

### 6. Lint with Ruff

```bash
# Check
ruff check src/ tests/

# Auto-fix
ruff check --fix src/ tests/
```

Ruff executes automatically in CI — commits failing lint checks are rejected.
