---
title: "State Management"
description: "Defining State schemas for LangGraph agents"
weight: 1
---

## State Schema

State serves as the shared memory bus passed between graph execution nodes:

```python
from typing import TypedDict

class AgentState(TypedDict, total=False):
    query: str        # User input query
    context: str      # Retrieved RAG context
    analysis: str     # Structured analysis output
    response: str     # Final user response
    error: str        # Diagnostic error details
    metadata: dict    # Operational telemetry
```

## State Design Principles

### 1. Use TypedDict

```python
# ✅ RECOMMENDED — TypedDict for LangGraph state definitions
class AgentState(TypedDict, total=False):
    query: str
    response: str

# ❌ AVOID — Do not use Pydantic models for raw LangGraph state
class AgentState(BaseModel):
    query: str  # LangGraph reducers expect TypedDict schemas
```

### 2. Configure `total=False` for Optional Fields

```python
class AgentState(TypedDict, total=False):
    query: str           # Invariant input (always present)
    context: str         # Optional — populated during retrieval steps
    error: str           # Optional — populated during failure handling
```

### 3. Maintain High State Hygiene

- Every state attribute represents data communicated between execution steps.
- Avoid treating state as an arbitrary catch-all container.
- Document the schema and lifecycle of each state property.

### 4. Incremental State Mutation Pattern

```python
# Each node returns only the mutated keys it updates
async def analyze_node(state: AgentState) -> dict:
    query = state.get("query", "")
    analysis = await process(query)
    return {"analysis": analysis}  # Updates only "analysis" in shared state
```
