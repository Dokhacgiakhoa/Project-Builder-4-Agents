---
title: "BMAD-v6 Overview"
description: "Overview of the BMAD Method and agent-driven development workflows"
weight: 1
---

## What is the BMAD Method?

**BMAD** (Breakthrough Method for Agile AI-Driven Development) is an open framework for AI-driven software development.

- **GitHub:** github.com/bmad-code-org/BMAD-METHOD
- **Docs:** docs.bmad-method.org
- **License:** MIT (free)
- **IDE:** Claude Code, Cursor, Codex CLI

## 6 Core Agent Personas

| Agent | Name | Role |
|-------|------|------|
| Analyst | Mary | Business Analyst |
| PM | John | Product Manager |
| Architect | Winston | System Architect |
| Developer | Amelia | Senior Developer |
| UX Designer | Sally | UX Designer |
| Tech Writer | Paige | Technical Writer |

## 4-Phase Workflow

### Phase 1: Analysis
- Brainstorming, research, product briefs

### Phase 2: Planning
- PRD creation, UX design

### Phase 3: Solutioning
- Architecture, ADRs, epic/story breakdown

### Phase 4: Implementation
- Sprint planning, story implementation, code review

## Folder Structure

```
project/
├── _bmad/                    ← BMAD core
│   ├── _config/              ← Config
│   ├── bmm/                  ← Module config
│   ├── custom/               ← Customizations
│   └── scripts/              ← Helper scripts
├── _bmad-output/             ← Output
│   ├── planning-artifacts/   ← Phase 1-3
│   └── implementation-artifacts/ ← Phase 4
├── docs/                     ← Documentation
└── src/                      ← Source code
```

## When to Apply BMAD?

- **YES** — Complex systems requiring detailed upfront planning
- **YES** — Teams requiring structured multi-agent coordination
- **NO** — Lightweight prototypes and quick single-file experiments
- **NO** — Teams unfamiliar with agent-assisted development paradigms
