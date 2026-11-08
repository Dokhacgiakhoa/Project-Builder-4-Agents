---
title: "Nodes & Edges"
description: "Defining execution nodes and edges in LangGraph"
weight: 2
---

## Nodes

Each node is an async function receiving state and returning updated fields:

```python
async def analyze_node(state: AgentState) -> dict:
    """Analyze user input query."""
    query = state.get("query", "")
    analysis = await process_query(query)
    return {"analysis": analysis}
```

### Node Best Practices

1. **Single Responsibility per Node** — Keep each step focused
2. **Return only updated fields** — Reducers merge keys into state
3. **Defensive Error Handling** — Catch exceptions and populate error states
4. **Docstrings** — Clearly describe node functionality

```python
async def safe_analyze_node(state: AgentState) -> dict:
    """Analyze query and handle errors gracefully."""
    try:
        query = state.get("query", "")
        result = await llm_service.analyze(query)
        return {"analysis": result}
    except Exception as e:
        return {"error": f"Analysis failed: {e}"}
```

## Edges

### Linear Edges

```python
graph.add_edge("analyze", "respond")
```

### Conditional Edges (Routing)

```python
def route_after_analyze(state: AgentState) -> str:
    if state.get("error"):
        return "respond"
    if state.get("needs_search"):
        return "search"
    return "respond"

graph.add_conditional_edges("analyze", route_after_analyze)
```

## Graph Construction

```python
from langgraph.graph import END, StateGraph

def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)

    # 1. Add nodes
    graph.add_node("analyze", analyze_node)
    graph.add_node("search", search_node)
    graph.add_node("respond", respond_node)

    # 2. Set entry point
    graph.set_entry_point("analyze")

    # 3. Add edges
    graph.add_conditional_edges("analyze", route_after_analyze)
    graph.add_edge("search", "respond")
    graph.add_edge("respond", END)

    return graph.compile()

agent = build_graph()
```

## Agent Patterns

### ReAct Pattern (Recommended)

```
Query → Analyze → [Call Tool → Observe → Re-analyze]* → Respond
```

### Plan-and-Execute Pattern

```
Query → Plan → [Execute Step 1 → ... → Step N] → Respond
```

### Multi-Agent Pattern

```
Query → Router → [Agent A | Agent B | Agent C] → Synthesize → Respond
```
