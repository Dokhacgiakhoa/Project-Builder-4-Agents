---
id: A-006
type: reference
when: "Selecting and cross-referencing design patterns, refactoring code"
---
# REFERENCE HANDBOOK OF DESIGN PATTERNS IN SOFTWARE & AI
*(Software & AI Agentic Design Patterns Catalog)*

---

## 🏛️ PART 1: GOF CLASSIC DESIGN PATTERNS

### 1. Creational Patterns
* **Factory Method**: Encapsulates object creation, letting subclasses decide which type of object to create.
  - *Use Case*: Creating LLM Providers (`get_llm(provider="mistral" | "gemini" | "groq")`).
* **Builder**: Separates the construction of a complex object from its representation.
  - *Use Case*: Building Prompt Templates or Agent State Configuration.

### 2. Structural Patterns
* **Adapter (Wrapper)**: Converts the interface of a class into another interface the client expects.
  - *Use Case*: Wrapping third-party APIs (Stripe, SendGrid) into the Domain's standard Interfaces.
* **Decorator**: Attaches new responsibilities to an object flexibly without inheritance.
  - *Use Case*: Adding Logging, Caching, or Rate Limiting to an API Service.
* **Facade**: Provides a simple interface to a complex subsystem.

### 3. Behavioral Patterns
* **Mediator**: Defines an object that encapsulates how a set of objects interact with each other.
  - *Use Case*: The MediatR library in CQRS to send a Command/Query to the matching Handler.
* **Strategy**: Defines a family of algorithms, encapsulates each one and makes them interchangeable.
  - *Use Case*: Text chunking strategies in RAG (Fixed-size, Recursive, Semantic chunking).
* **Observer / Domain Events**: When an object changes state, all dependent components are notified automatically.

---

## 🏢 PART 2: ENTERPRISE & ARCHITECTURAL PATTERNS

### 1. Repository & Unit of Work Pattern
* **Repository**: Acts as an in-memory collection of entities, hiding the details of the database.
* **Unit of Work**: Keeps the list of business changes in a transaction and commits them together.

### 2. Outbox Pattern
* Guarantees data consistency (Guaranteed Delivery) between saving to the DB and sending an Event to a Message Broker (Kafka/RabbitMQ) without losing data when the network connection drops.

### 3. Circuit Breaker Pattern
* Automatically cuts the temporary connection to an external service when it keeps failing or timing out, avoiding exhaustion of the main system's resources.

---

## 🤖 PART 3: AI-NATIVE & AGENTIC DESIGN PATTERNS

| Design Pattern | Description & Essence | Real Use Case |
| :--- | :--- | :--- |
| **ReAct Loop** | Combines Reasoning and Action (Tool execution) | An agent looks up web data or queries SQL step by step |
| **Semantic Router** | Routes requests by vector embedding similarity | Routes a user's question to the right specialized domain |
| **Supervisor Swarm** | A main agent coordinates independent sub-agents | Coordinates the workflow between a Coder Agent and a Reviewer Agent |
| **RAG Triad Eval** | Three measurement criteria: Faithfulness, Relevance, Precision | Evaluates the quality of an automated semantic search pipeline |
| **Model Context Protocol (MCP)** | An open standard connecting LLMs to Tools and Data Sources | Lets an Agent access databases, terminals and APIs uniformly |
| **Human-in-the-Loop (HITL)** | A safety gate requiring human confirmation | Approves a payment transaction or a production code deploy |
