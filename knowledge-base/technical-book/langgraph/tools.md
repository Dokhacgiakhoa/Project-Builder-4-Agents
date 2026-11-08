---
title: "Agent Tools"
description: "Tool definition and binding in LangGraph agents"
weight: 3
---

## Tool Definition

```python
from langchain_core.tools import tool

@tool
def search_knowledge(query: str) -> str:
    """Search the knowledge base for relevant context.

    Args:
        query: User search query string

    Returns:
        Text search results
    """
    results = vector_store.similarity_search(query, k=3)
    return "\n".join([r.page_content for r in results])
```

## Core Principles

1. **Always provide docstrings** — Agents use docstrings to decide tool applicability
2. **Type hints for all parameters** — Ensures correct argument schemas
3. **Return string** — Easiest for LLMs to ingest into conversational state
4. **Handle errors internally** — Return error descriptions rather than throwing unhandled exceptions

## Tool Types

### Search Tool (RAG)

```python
@tool
def search_documents(query: str) -> str:
    """Search for relevant documents."""
    docs = vector_store.similarity_search(query, k=5)
    if not docs:
        return "No relevant documents found."
    return "\n---\n".join([d.page_content for d in docs])
```

### API Call Tool

```python
@tool
def call_external_api(endpoint: str, params: dict) -> str:
    """Invoke external API."""
    try:
        response = httpx.post(endpoint, json=params)
        return response.text
    except Exception as e:
        return f"API error: {e}"
```

### Calculator Tool

```python
@tool
def calculate(expression: str) -> str:
    """Evaluate mathematical expressions."""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Calculation error: {e}"
```

## Binding Tools to the Agent

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools([search_documents, calculate])
```
