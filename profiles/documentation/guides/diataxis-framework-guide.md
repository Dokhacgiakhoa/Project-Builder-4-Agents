---
id: O-006
type: reference
when: "Categorizing docs via **Diátaxis** (tutorial, how-to, reference, explanation)"
---
# 📚 THE DIÁTAXIS DOCUMENTATION FRAMEWORK

> **The international standard for structuring technical documentation**  
> Diátaxis (Greek for *arrangement, organization*) is the documentation architecture framework officially adopted by leading technology organizations such as the **Python Official Docs, Canonical (Ubuntu), Cloudflare, NumPy, Django, and Gatsby**.

---

## 🧭 1. WHY USE DIÁTAXIS?

The biggest problem of software project documentation is **"mixed-up content"**: an installation guide that also explains the architecture philosophy, an API lookup table full of long hands-on steps. This overloads both developers and users, and they cannot find the information they need.

Diátaxis solves this problem thoroughly by splitting documentation into **4 Quadrants** based on 2 axes:
* **Horizontal axis**: serves **Learning (Learning-oriented)** ⟷ serves **Real work (Work-oriented)**.
* **Vertical axis**: focuses on **Theory / Principles (Theoretical)** ⟷ focuses on **Practical action (Practical)**.

```
                   PRACTICAL
                       ▲
                       │
       TUTORIALS       │         HOW-TO GUIDES
   (Learning / Intro)  │    (Solving a specific problem)
                       │
LEARNING ──────────────┼────────────────── WORKING
(Learning-oriented)    │              (Work-oriented)
                       │
       EXPLANATION     │          REFERENCE
 (Explaining principles / Why) │  (Looking up technical specs)
                       │
                       ▼
                   THEORETICAL
```

---

## 🧩 2. THE 4 DOCUMENTATION QUADRANTS IN DETAIL

### Quadrant 1: TUTORIALS (Introductory / Learning guides)
* **Goal**: Help a beginner reach a first success (First Win) right away and build confidence.
* **Characteristics**:
  - Like **teaching a child to cook**: hand-holding, step by step from A to Z.
  - No rambling theory; not too many options (do not say "you can choose Option A or Option B"). Give ONLY ONE path that works immediately.
  - The end result is a real working product.
* **Examples in the project**:
  - *"Build your first Todo List feature in 10 minutes with an AI Agent"*.
  - *"Run the full-stack system locally for the first time"*.

---

### Quadrant 2: HOW-TO GUIDES (Solving a specific situation)
* **Goal**: Help an experienced person solve a specific problem or use case in real work.
* **Characteristics**:
  - Like a **recipe book (Recipe Book)**: "How do I make a pizza?".
  - Starts with a clear user goal: *"How to..."*.
  - Assumes the reader already knows the basic concepts (no need to explain again what an environment variable or Git is).
  - Focuses on the sequence of concrete action steps to reach the result.
* **Examples in the project**:
  - *"How to integrate a new LLM into the Multi-Agent system?"*.
  - *"How to switch the interface style to Cyberpunk HUD?"*.
  - *"How to roll back a faulty release on production?"*.

---

### Quadrant 3: REFERENCE (Technical lookup documents)
* **Goal**: Provide accurate, concise and objective technical description for users to look up while working.
* **Characteristics**:
  - Like an **encyclopedia or a technical map**.
  - Contains no advice, no work steps, no lead-in story.
  - Pure technical facts: function names, input parameters (arguments), data types (types), returned error codes (HTTP status codes), configuration variables.
  - The structure must be consistent and can be generated automatically from source code (like Swagger/OpenAPI, TypeDoc).
* **Examples in the project**:
  - `specs/contracts/api-contract-template.yaml` (API endpoint specification).
  - The environment variable catalog `.env.example`.
  - The command catalog of the `Makefile`.

---

### Quadrant 4: EXPLANATION (Explanatory & in-depth analysis documents)
* **Goal**: Help the reader deeply understand the overall picture, the reasons behind design decisions and the architecture philosophy.
* **Characteristics**:
  - Like **a lecture or a historical/scientific analytical essay**.
  - Answers the questions: *"Why was it done this way?" (Why)*, *"What is the historical background?"*, *"For what reasons were the alternative solutions rejected?"*.
  - Contains no line-by-line hands-on commands.
* **Examples in the project**:
  - The whole `adrs/` folder (Architecture Decision Records).
  - `profiles/documentation/system-architecture.md` (explains why a Modular Monolith was chosen over Microservices).
  - The philosophy of the Anti-Crash Standard in `README.md`.

---

## 📋 3. CLASSIFICATION MATRIX & QUICK WRITING RULES

| Core question | Document type | Writing style | Audience |
| :--- | :---: | :--- | :--- |
| **"Show me how to get started"** | **Tutorial** | Hand-holding, sequential steps, no long explanations | Beginner |
| **"How do I solve problem X?"** | **How-To Guide** | Goal-oriented, focused on practical action | Working engineer (Practitioner) |
| **"What attributes does this have?"** | **Reference** | Objective, concise, accurate on every technical parameter | Engineer who needs a quick lookup (Lookup) |
| **"Why is the system designed this way?"** | **Explanation** | Critical thinking, analysis of context and trade-offs | Tech Lead, Architect, Reviewer |

---

## 🚫 4 TRAPS TO AVOID ABSOLUTELY (DOCUMENTATION ANTI-PATTERNS)
1. **Mixing a Tutorial into a How-To Guide**: putting too many complicated options in a lesson for beginners confuses them and makes them give up.
2. **Mixing Explanation into Reference**: inserting rambling philosophy into an API parameter table makes developers lose time searching.
3. **Unversioned documents (Out-of-date Docs)**: docs sit on a scattered external wiki page instead of directly in the Git repo next to the source code.
4. **Writing docs without runnable sample code**: every guide must come with a snippet that can be copy-pasted and tested automatically in CI.
