---
title: "Demo Day Submission"
weight: 13
---

# Chapter 13: Demo Day Submission

> 📊 **Cohort Evidence —** Feedback from the Cohort 1 Evaluation Committee recorded three revealing statistics: **demo videos were missing in 11/11 teams** (100% of teams lacked one), **82% of teams lacked evaluation evidence**, and **64% of teams lacked a pitch deck**. No team lost points because their "AI was not smart enough" — the overwhelming majority of lost points stemmed from **missing deliverables** and **unprepared demos**. This chapter serves as your roadmap to ensure you do not repeat those mistakes.

## 13.1 Ten Mandatory Deliverables — With Real Cohort Metrics

The AI20K Organizing Committee requires every team to submit **10 deliverables** for Demo Day. The table below correlates each deliverable with the actual status from the previous cohort (per Cohort 1 judge feedback) — so you know precisely where the competitive benchmarks lie:

| # | Deliverable | Previous Cohort Status | Why Teams Frequently Miss It | Fast-Track Execution Tip |
|---|-------------|------------------------|------------------------------|--------------------------|
| 1 | Source Code (GitHub repo) | Mostly submitted | Reluctance to push imperfect code | Push from Week 1; do not wait for perfection |
| 2 | README.md | Mostly submitted | Written at the last minute | Use standard templates; 30 minutes completes 80% |
| 3 | Architecture Diagram | Frequently missing | Dismissed as mere decoration | Generate using Mermaid directly in the README (30 mins) |
| 4 | AI Logs (LangSmith/screenshot) | Mostly submitted | Unsure how to configure instrumentation | Requires only 3 LangSmith env vars; zero extra code |
| 5 | Live URL | Frequently submitted | Deployment delayed until the final day | Deploy in Week 1 even with just `/health`; iterate gradually |
| 6 | Video Demo | **Missing in 11/11 teams (100%)** | Postponed, fear of recording, lack of ownership | Record via Loom/OBS in one Week 5 afternoon — teams with video stand out |
| 7 | Pitch Deck | **Missing in ~64% of teams** | Writing slides perceived as harder than coding | Follow the 10-slide template in Section 13.8; 1 core topic per slide |
| 8 | Development Journal | Mostly submitted | Daily logging seen as redundant overhead | 2–3 sentences daily; 10 minutes per day total |
| 9 | Worklog (commit history) | Mostly submitted | Uncertainty regarding submission format | `git log --oneline > docs/worklog.md` — a single command |
| 10 | Evaluation Evidence | **Missing in ~82% of teams** | Unclear what or how to measure | Follow Chapter 10 Section 10.5 — golden dataset + metrics table |

Quick analysis: The easiest deliverables to secure are AI Logs and Worklog — they require no complex engineering, merely operational discipline. Conversely, the three most frequently omitted deliverables — Video Demo (100% missing), Evaluation Evidence (82% missing), and Pitch Deck (64% missing) — represent the exact assets where **any team that delivers them will outcompete the vast majority of peer teams**. Demo Day is not merely a coding race; it is a discipline in delivering complete product packages.

Each deliverable belongs in its designated location within your GitHub repository:

```
project-root/
├── README.md              ← Deliverable #2
├── docs/
│   ├── architecture.md    ← Deliverable #3 (or .png/.pdf)
│   ├── video-demo.md      ← Deliverable #6 (YouTube link)
│   ├── pitch-deck.pdf     ← Deliverable #7
│   ├── journal.md         ← Deliverable #8
│   ├── worklog.md         ← Deliverable #9
│   └── evaluation.md      ← Deliverable #10
├── src/                   ← Deliverable #1 (Source Code)
├── tests/                 ← Supplies Evaluation Evidence
├── .github/workflows/     ← Bonus points for DevOps
├── Dockerfile             ← Bonus points for DevOps
└── docker-compose.yml     ← Bonus points for DevOps
```

> 🔑 **KEY TAKEAWAY:** 10/10 deliverables = full score under "Deliverable Completeness". Many teams lose marks not due to inferior code, but due to absent deliverables. Looking at real historical data: simply including a Video Demo and Evaluation Evidence instantly differentiates your submission from nearly all competing teams.

### Detailed Deliverable Breakdown

**1. Source Code:** Host all source code in a structured GitHub repository. Maintain clean directory layouts, an accurate `.gitignore`, zero exposed secrets, and no bloated files (>10MB). Judges will clone and execute your code — ensure it runs smoothly after populating required environment variables.

**2. README.md:** The README forms your first impression. It must contain: project title, overview, product screenshots/GIFs, step-by-step setup instructions, execution commands, directory layout, tech stack highlights, and team roster. Why teams miss it: deferred to the final hours. Tip: draft the README in Week 1 and update continuously.

**3. Architecture Diagram:** An architectural visual proving systemic comprehension. Leverage draw.io, Mermaid (embedded natively in markdown), or Excalidraw. Clearly delineate: Frontend, Backend API, LangGraph Agents, Vector Stores, and External APIs. Why it is omitted: deemed purely decorative. In reality, judges examine diagrams before diving into source code — clear schematics elevate technical evaluation marks.

**4. AI Logs:** Verifiable evidence of deterministic agent workflows. The simplest approach: enable LangSmith tracing (3 environment variables, zero extra code). Alternatively, capture terminal traces displaying reasoning steps, tool calls, and outputs.

**5. Live URL:** A publicly accessible internet endpoint. Deploy backends to Render and frontends to Vercel. Free tiers are fully acceptable. Ensure availability throughout Demo Day plus an additional 7 days. Use UptimeRobot or similar health pingers to prevent free-tier instances from idling.

**6. Video Demo:** A 3–5 minute high-definition screencast covering primary use cases. Upload to YouTube (unlisted). Key segments: team intro, core user journey walkthrough, architecture explanation, and edge-case handling. Why 100% of teams in the prior cohort omitted this: lack of designated ownership. Tip: appoint a video owner by Week 4; this screencast also acts as Tier-2 backup during live demo disruptions (see Section 13.4).

**7. Pitch Deck:** Presentation deck for Demo Day. Typically 10 slides allocated across 10 minutes. See the structured template in Section 13.8. Why 64% omit it: teams invest all bandwidth into coding, leaving zero runway for presentation design. Tip: draft rough bullet-point slides in Week 3 and refine incrementally.

**8. Development Journal:** Engineering logs documenting architectural trade-offs, roadblocks encountered, resolution steps, and technical retrospectives. Keep entries concise — 2–3 sentences daily suffice. This document provides prime raw material for the "Challenges & Learnings" slide.

**9. Worklog:** Development commit timeline demonstrating steady team velocity. Simplest command: `git log --oneline --since="2026-01-01" > docs/worklog.md`. Exporting GitHub contribution activity is also acceptable.

**10. Evaluation Evidence:** Quantitative assessment of agent performance — golden dataset results, benchmark metrics, and human evaluation feedback. Reference [Chapter 10](chapter-10.md) Section 10.5 and 8.6. Given that 82% of past teams failed to provide this deliverable, it yields the highest return on effort across all criteria.

## 13.2 Detailed Preparation Checklist

Use this systematic checklist to ensure zero deliverables are overlooked. Export or copy to Notion/Trello and verify each item before final submission.

### Source Code Checklist

- [ ] GitHub repository is public or has added judges as collaborators
- [ ] Code runs successfully after configuring environment variables (README contains clear setup commands)
- [ ] `.gitignore` is correctly configured (excludes `.env`, `__pycache__`, `.venv`, IDE folders)
- [ ] No hardcoded secrets (API keys, service tokens, passwords)
- [ ] No oversized binary assets committed (model weights or raw datasets >10MB)
- [ ] `requirements.txt` or `pyproject.toml` pins exact package versions
- [ ] Code includes comprehensive type annotations
- [ ] Core functions and classes include descriptive docstrings
- [ ] Automated test suite includes at least one functional pytest test file

### README.md Checklist

- [ ] Project title and concise value proposition clearly stated
- [ ] Application screenshot or animated demonstration GIF included
- [ ] Step-by-step installation instructions documented
- [ ] Local run instructions (and Docker Compose commands if applicable)
- [ ] Project directory tree structure illustrated
- [ ] Technology stack detailed via table or badges
- [ ] Required environment variables listed (variable names only, never secrets)
- [ ] API documentation present (endpoints, request payloads, responses)
- [ ] Team members listed alongside respective responsibilities
- [ ] Prominent link to public Live URL

### Architecture Diagram Checklist

- [ ] Diagram is visually legible and well-structured
- [ ] Illustrates all major tiers (Frontend, Backend, Agent Graph, Database, External APIs)
- [ ] Directional arrows clarify data and control flow
- [ ] File format: PNG or SVG (embedded directly in README)
- [ ] Accompanied by a concise narrative summary

### AI Logs Checklist

- [ ] Publicly shared LangSmith project link or export bundle
- [ ] Alternatively: terminal screenshots capturing agent step-by-step reasoning
- [ ] Includes at least 5–10 representative trace sessions
- [ ] Every trace displays: initial prompt, LLM call, retrieval context, output

### Live URL Checklist

- [ ] Base URL returns HTTP 200 OK upon access
- [ ] Health probe endpoint functions as expected (`/health`)
- [ ] Primary API endpoints respond correctly
- [ ] Live URL is clearly referenced in the README
- [ ] Service availability is maintained (no sleep timeouts — pinged via UptimeRobot)

### Video Demo Checklist

- [ ] Duration: 3–5 minutes, recorded in high definition
- [ ] Uploaded to YouTube (public or unlisted)
- [ ] Link provided in README or `docs/video-demo.md`
- [ ] Content includes: team intro, core user journey, edge-case demo
- [ ] Clear voiceover audio, optionally supported by subtitles

### Pitch Deck Checklist

- [ ] 10-slide deck aligning with the standard template (Section 13.8)
- [ ] Exported as PDF (avoid raw PowerPoint to prevent rendering quirks)
- [ ] Stored under `docs/pitch-deck.pdf`
- [ ] Rehearsed within a strict 10-minute presentation window

### Journal + Worklog Checklist

- [ ] Journal contains at least 5–7 substantial entries (2–3 sentences each)
- [ ] Worklog captures complete Git commit logs or engineering milestone logs
- [ ] Both files persisted under the `docs/` directory

### Evaluation Evidence Checklist

- [ ] Automated test summary reports (pytest outputs + test coverage metrics)
- [ ] Evaluation benchmark tables evaluated against a golden dataset (pass@k, pass^k, or RAGAS)
- [ ] Comparative benchmark analysis against human baselines or existing tools
- [ ] Real user feedback summaries (from at least 3–5 external users)
- [ ] Test traceability mapping test cases back to declared product features

> 💡 **TIP:** Establish your GitHub Project or Notion tracking board in Week 1. Check off items incrementally. Leaving these tasks to the final week inevitably results in skipped demo videos and missing engineering journals.

## 13.3 Demo Day Evaluation Rubric — 6 Criteria × 5 Performance Tiers

> 📌 **CRITICAL NOTE:** This rubric represents the official AI20K Demo Day evaluation framework (transcribed directly from committee rubrics). **Re-verify against official guidelines released at the start of each cohort** — while criteria names and tier descriptions remain consistent, precise scoring weights may be calibrated per cohort; always treat the current committee publication as authoritative.

The rubric evaluates **6 criteria**, each scored across **5 performance tiers**:

| Score Range | Classification |
|-------------|----------------|
| 9–10 | Excellent |
| 7–8 | Good |
| 5–6 | Average |
| 3–4 | Weak |
| 1–2 | Poor |

| # | Criterion | Implicit Question Asked by Judges |
|---|-----------|-----------------------------------|
| 1 | Product Maturity & Completeness (Demo) | Does the live demo run reliably and error-free? |
| 2 | AI Engineering & Application Depth | Is this genuine AI engineering or merely a trivial API wrapper? |
| 3 | Evaluation & Efficacy Evidence | Are there rigorous empirical metrics demonstrating agent performance? |
| 4 | User Interface & User Experience (UX) | Is the UI clean, intuitive, and responsive? |
| 5 | Innovation & Real-World Viability | Does the product solve an authentic problem for genuine users? |
| 6 | Presentation & Pitch Delivery | Is the narrative compelling, well-paced, and backed by strong Q&A handling? |

The playbook below details **specific engineering actions required to hit the 9–10 (Excellent) tier alongside mandatory supporting evidence.** This represents the north star of this entire book.

### Criterion 1: Product Maturity & Completeness (Demo)

- **Excellent (9–10):** The demo executes smoothly without runtime failures, all advertised features function end-to-end, and boundary edge cases are gracefully handled.
- **Average (5–6):** Core functions work, but intermittent errors appear or non-primary flows break.
- **Poor (1–2):** The live demonstration crashes or fails to execute.

| Action Items | Required Evidence |
|--------------|-------------------|
| Identify 10–15 explicit edge cases with corresponding automated tests in repo (see [Chapter 7](chapter-07.md)) | Dedicated `tests/` directory with test files named after specific edge cases |
| Incomplete features must be **hidden or explicitly flagged** — never leave "SOON" placeholders on core flows | UI screenshots verifying absence of dead buttons or broken links |
| Automated smoke-testing of demo accounts following every deployment in CI | Green GitHub Actions deployment logs |
| End-to-end validation across the primary user workflow (e.g. Playwright) | `tests/e2e/` test suites committed to repo |

> Historical Note: Team Gamma experienced regression during final submission — an unexpected bug appeared right after fixing an earlier issue due to missing regression testing. "Completeness" is not "it worked once today" but "tests prove it works on every build."

### Criterion 2: AI Engineering & Application Depth

- **Excellent (9–10):** Purposeful adoption of advanced AI/Agent techniques — RAG architectures, multi-agent collaboration, structured guardrails, and systematic evaluation.
- **Weak (3–4):** Basic single-turn API invocation relying on generic prompting.

| Action Items | Required Evidence |
|--------------|-------------------|
| Enforce minimum 2-tier guardrails: prompt-level + code-level (Pydantic schema locks, regex filters) — 11/12 previous teams had prompt-only filters | Guardrail modules in `src/`, automated jailbreak test cases in `tests/` |
| When RAG is used, measure both retrieval quality and generation fidelity (RAGAS, see [Chapter 10](chapter-10.md) Section 10.6) | RAGAS metrics table documented in `docs/evaluation.md` |
| Dynamic graphs with true conditional routing (routing functions altering execution branch based on state) | LangSmith execution trace showing distinct branched pathways |
| Hallucination mitigation built on systemic verification (source citations, grounding checks), not prompt instructions alone | Screenshots of model answers containing clickable, verifiable citations |

### Criterion 3: Evaluation & Efficacy Evidence

- **Excellent (9–10):** Empirical test suites on realistic evaluation sets, quantitative metric reporting, comparative benchmark baselines, and structured user feedback.
- **Weak (3–4):** Zero quantitative data or empirical validation.

| Action Items | Required Evidence |
|--------------|-------------------|
| Golden dataset comprising ≥30 on-topic prompts + 15 adversarial/off-topic prompts from target users ([Chapter 10](chapter-10.md)) | Committed dataset file `eval/datasets/golden.jsonl` |
| Measure pass@k and pass^k; use an LLM-as-a-judge model distinct from the generator | Output logs in `eval/results/` and summary metric tables |
| Comparative benchmarks against human baselines or competing market solutions | 3-column benchmark comparison table in `docs/evaluation.md` |
| Before-and-after progression: baseline measured in Week 4 vs improved metrics in Week 6 | Two-column comparison against the exact same evaluation dataset |

Because 82% of past teams submitted zero evaluation evidence, this criterion represents the highest leverage opportunity for top marks. See [Chapter 10](chapter-10.md) Section 10.5 for implementation templates.

### Criterion 4: User Interface & User Experience (UX)

- **Excellent (9–10):** Polished, intuitive, accessible, and fully responsive across form factors.
- **Poor (1–2):** Rudimentary, clunky, or difficult to navigate.

| Action Items | Required Evidence |
|--------------|-------------------|
| Visual loading indicators on all asynchronous LLM calls (spinners/skeletons) and informative user-facing errors (never dump raw tracebacks) | Visual captures of all 3 application states: loading, success, error |
| Fully responsive layout — verified on actual mobile screens, not merely resized desktop viewports | Side-by-side screenshots across mobile and desktop viewports |
| Prevent raw reasoning tokens from leaking into user chat bubbles | Clean chat interface screenshots |
| Functional `/privacy` routing (no broken `#` links) when handling personal information — follow privacy checklists in [Chapter 11](chapter-11.md) | Working privacy policy link describing data retention and handling |

### Criterion 5: Innovation & Real-World Viability

- **Excellent (9–10):** Directly solves a verified, acute pain point for an identifiable user base.
- **Weak (3–4):** Artificial toy demonstration without practical relevance.

| Action Items | Required Evidence |
|--------------|-------------------|
| Comprehensive competitive analysis evaluating at least 3 alternatives; clear justification for why existing solutions fall short | Competitor breakdown matrix in pitch deck |
| Structured discovery interviews with ≥5 real users capturing genuine user questions (feeds directly into golden dataset) | Interview interview notes and summarized question analysis |
| Consistent metrics across all documentation surfaces (hero banner, docs, pitch deck all report identical numbers) | Unified figures across all collateral |
| Core USP clearly articulated and demonstrated end-to-end from public UI to final output ([Chapter 5](chapter-05.md)) | Dedicated USP walkthrough featured in demo video |

> Historical Note: Solutions are evaluated on how effectively users **experience core AI value**, not the absolute quantity of features. Team Gamma produced strong documentation, yet users "progressed through initial steps without ever unlocking core AI capabilities."

### Criterion 6: Presentation & Pitch Delivery

- **Excellent (9–10):** Articulate storytelling, convincing value proposition, seamless live demo, and authoritative Q&A defense.

| Action Items | Required Evidence |
|--------------|-------------------|
| Structure narrative around AIDA principles rather than dry feature checklists (see Section 13.4) | `presentation/demo_script.md` |
| Implement 3-tier presentation fallback: Live demo → Video recording → Annotated screenshots (Section 13.4) | Unlisted YouTube video link + annotated screenshot slides |
| Conduct full rehearsal before a mock evaluation panel **exactly 1 week before Demo Day** (official recommendation from past judges) | Documented feedback log from mock panel with recorded resolutions |
| Minimum 3 comprehensive practice runs + structured Q&A preparation across anticipate questions | Recorded video of final rehearsal session |

### Overall Scoring Strategy

Golden principle: **Secure Good (7–8) across all 6 criteria first, then push 2–3 selected criteria to Excellent (9–10).** Select target excellence criteria aligned with team strengths — keep in mind that the largest untapped scoring margins exist in **Evaluation Evidence** (82% missing) and **Presentation** (11/11 teams missing videos), meaning moderate effort here easily propels your project into top rankings.

> 🔑 **KEY TAKEAWAY:** Do not hyper-optimize a single category while neglecting the remaining five. Judges evaluate overall holistic engineering maturity — a consistent 7-7-7-7-7-7 profile outscores an unbalanced 10-10-4-4-4-4 submission.

## 13.4 The Art of the Demo — Storytelling Over Feature Cataloging

> Source: "How to Demo Like a Pro" Workshop (Loc Dang, VinUni AI Talents Workshop 2026). Foundational principle: "Failed demos are not caused by bad products — they are caused by lack of preparation."

### The "Demo Curse" Is Real

"Anything that can go wrong during a live demo will go wrong." The catalog of common demo failures is well known: auditorium Wi-Fi drops, LLM API keys hit rate limits or timeouts, morning code merges trigger fresh regressions, presenters lose their train of thought, and operating systems launch unexpected updates. Historical data shows virtually no teams prepare structured fallbacks. This section eliminates every single failure mode.

### AIDA Storytelling Framework — 3 to 5 Minute Demo Structure

The most common trap: presenting a dry **feature inventory** — "Feature 1 is... Feature 2 is... Feature 3 is...". Audiences forget features; they remember **emotional resonance and tangible problems solved**. Shift focus from "what this software does" to "the user journey and transformed outcome."

| Phase | Designation | Presentation Strategy | Concrete Example |
|-------|-------------|-----------------------|------------------|
| **A** | Attention | High-impact hook: striking metric, provocative question, or relatable struggle | "Every time your team submits a group report, how many hours do you waste compiling 5 separate files?" |
| **I** | Interest | Why it matters: who experiences this pain? How often? What is the cost? | "A survey of 200 students revealed: an average of 2.3 wasted hours per submission — every single week." |
| **D** | Desire | Present the demo as the NATURAL resolution of the story — not a feature checklist | Live demo: "With our agent, the entire group edits concurrently, submitting in 1 click — done in 5 minutes." |
| **A** | Action | Direct call to action: prompt the audience to engage immediately | "Experience it right now at bit.ly/your-app or scan the QR code on screen." |

### 4 Demo Frameworks — Match Your Audience

| Framework | Best Suited For | Target Setting |
|-----------|-----------------|----------------|
| AIDA | Short 3–5 min presentations | Pitch competitions, hackathons, AI20K Demo Day |
| Problem → Solution → Proof | Technical deep dives | Audiences composed of software engineers and researchers |
| Before / After / Bridge | Workflow transformations | Replacing legacy processes with automated agent workflows |
| Hero's Journey | Extended startup pitches | Investor pitch sessions, multi-stakeholder enterprise stories |

Rule: **Commit to a single framework and execute it cleanly** — one cohesive story outperforms fragmented hybrids. For AI20K Demo Day (10-minute presentation before a blended panel of engineers and business leaders), AIDA serves as the optimal default.

### Showcase Mode — Never Demo on Raw Unseeded Data

Golden rule: **never rely on blank databases or unvetted live user inputs during an inaugural demo**. Build a dedicated Showcase Mode pre-seeded with curated dummy data — realistic, polished, yet containing zero sensitive personal information.

Showcase Mode Checklist:

- **Database:** Dummy data pre-seeded? Data looks authentic? Devoid of real PII?
- **Account:** Dedicated demo account provisioned? Authenticated in advance? Professional display name and avatar?
- **Application State:** App primed at the exact target view? No visible console errors? Load states completed?

Direct your shared demo links (QR codes/short links) **straight into this pre-populated showcase state** — do not force evaluators through multi-step onboarding before they experience your product's core value.

### 3-Tier Demo Resilience — Surviving Any Technical Failure

| Tier | Format | Activation Scenario |
|------|--------|---------------------|
| 1. Live Demo | Real application running in Showcase Mode | Default operating plan |
| 2. Pre-recorded Video | Complete 3–5 minute high-definition walkthrough stored locally & hosted on YouTube | Live network failure, upstream API downtime, rate-limiting |
| 3. Step-by-Step Screenshots | Slide deck capturing every stage annotated with callout arrows | Both live application and video playback fail |

The pre-recorded video backup (Tier 2) doubles directly as Deliverable #6 — solving two requirements at once. Preparing step-by-step screenshots (Tier 3) offers a hidden advantage: capturing every screen forces a comprehensive manual test pass across your entire user journey. Recommended tools: Loom, OBS Studio (free, open source), QuickTime, Screen Studio; screenshot capture: CleanShot X, Snagit, Greenshot.

### Dedicated Demo Accounts — Keep Personal Accounts Off Stage

Best practices:

- Create `demo@yourapp.com` with a clear, professional identity
- Sign in prior to stepping on stage
- Profile details: polished avatar, clean professional display name
- Disable all operating system notifications on presentation laptops
- Verify OAuth authentication flows 24 hours prior; note credentials offline

Anti-patterns: using personal accounts (leaks personal communications/names), leaving desktop notifications enabled, presenting messy test data, walking through live registration on stage, and forgetting credentials under pressure.

Always display a shortened link (e.g., bit.ly) and persistent QR code on the final slide, **leaving it visible throughout the entire Q&A session**. Attach UTM tags to track post-pitch evaluator engagement.

### 24 Hours Before Demo Day Checklist

APPLICATION:

- [ ] Deploy stable production release (freeze code merges on presentation morning)
- [ ] Re-seed showcase test data
- [ ] Confirm demo account is logged in and verified
- [ ] Run one final end-to-end user journey test
- [ ] Verify zero console errors or unresolved exceptions

BACKUP ASSETS:

- [ ] Demo video recorded and verified
- [ ] Step-by-step annotated screenshots embedded in backup slides
- [ ] Presentation slides accessible offline
- [ ] Video file stored locally on hard drive (eliminating network dependencies)
- [ ] Shortened demonstration URLs and QR codes verified

### Presenter Mindset: 3 Rehearsals + Q&A Preparation

- **Three Rehearsals:** Run the end-to-end presentation at least three times — solo in front of a mirror, with teammates, and finally during mock trials.
- **Anticipate Q&A Queries:** Prepare concise responses for: "How does this architecture scale to 1,000 concurrent users?", "Why was this framework chosen over alternatives?", "What is the product roadmap?", and "How are hallucinations mitigated?" Pre-assign specific team owners to domain questions.
- **When Disruptions Occur:** Transparently acknowledge the issue, seamlessly transition to backup assets, and maintain narrative momentum. Never panic, avoid prolonged silence, and avoid repetitive apologies.
- **Time Allocation:** Spend 70% of presentation time establishing problem context, user value, and outcomes; reserve 30% for technical mechanics and Q&A defense. A demo is an engaging story, not an execution log.

## 13.5 Six-Week Roadmap to Demo Day

Deliverables are not a final-week sprint — every item above correlates with an explicit milestone in the 6-week development cycle. Key recommendation from prior judges: **conduct a formal pitch and demo dress rehearsal before mock evaluators at least 1 week prior to Demo Day** (Week 5), gathering actionable feedback with ample runway for remediation.

```mermaid
timeline
    title 6-Week Timeline to Demo Day
    Week 1 : Clone template, deploy /health to cloud : Open 10 deliverables checklist (Notion/GitHub Issues) : Write initial README draft
    Week 2 : Submit proposal (problem, user, USP) : Research 3 competitors + interview 5 real users : Start collecting golden dataset
    Week 3 : Build core features, green CI/CD : Draft 10-slide pitch deck rough outline : Daily journal 2-3 sentences
    Week 4 : Internal midway demo following AIDA : Round 1 eval measurements (baseline "before") : Assign demo video recording owner
    Week 5 : Rehearsal before judging panel (exactly 1 week prior) : Record backup video + step-by-step screenshots : Refine pitch deck based on feedback
    Week 6 : Demo Day — seed showcase mode : Pre-login demo account, disable notifications : 3rd rehearsal + Q&A prep
```
> [📊 Open diagram on Mermaid Live / AI Editor](https://mermaid.live/edit#pako:eNplVMFS2zAQ_ZUdHzrpkAx2QsiQW4gZShkYKLQnX2RpHWuQJdeSQj0M_96VnECa5hLZefve09vdvCXcCEyWkDjZoJIaCw30cdIphHNwvvAZsoWGwqdZloWnstKQY2MgZ_2Afv5AZbCEtTIawWHTKuZwDAJbZXo4rZEpV4MiphSZBq6MF4S_C8WiAl4jf1HSOshSKlJyix0rFVoY3RsnjT69lu6bL-HGWo_2K5X-koMhBz-uVvndFZTRyOzQLlv4Y5dTKr2PqhcttJ1pjWUKRnQiuWYM3mI3hp9PD0Hjth44DdjoPHMwO6AXmQQXIbiAE2jjkVd6A9tYN9cwj4Q7FBOOSC_jkXz_45MgHjZGCdQgmGMW3bH1WSj2Uglw0Y3QNehAks5Iktf7l2NY35yuc_jDCLCEvAtilKtVUiC00vGaMuYvn4m5WFudEfq78Z2mRJp4wYUEvYm8aQ_TyQx4fJj-F2sovZPilfVETfOhh4jloCEuSAINrG7yFQHjxVMDuCWhbZSe0g0yGJV07zCJUCQlVqbDIgl9eBjuNtWDfnVG6OgrK9PILyT89qS9pRua6ODY4JxoniN2TsXC97FXCweuO-ApOVxe38Jo3xrSYtHZxzIEO4-fUiXjL76l5lveIWpbGwfWYTsp-0n4DjsxjMUFNeMg-5hHhSRJDMdmz0PbdmtGaU3T7AwsYYH4XzllBA2tbgimw4kyG6mH1Bnnxms3DgMyzJim7akkZ2GH7D4CJtqwivupOoHHLyvaBWyTMSQNdg2TIvwvvAVfRUJWG2oE9S0RWDGvXJEU-j2AmXfmqdecfnSdp4VPfEvTi7lkm441u9fvfwHkpWut)

Three non-negotiable checkpoints: **Week 2 proposal submission** (delays risk building the wrong solution), **Week 4 midway demo** (vital for catching presentation breakdowns early), and **Week 5 panel rehearsal** (provides a mandatory 1-week buffer to address critique before final grading).

## 13.6 Common Anti-Patterns to Avoid

Field experience highlights frequent engineering pitfalls across cohorts. Proactively avoiding these traps is the fastest way to safeguard your score.

### Top 5 Most Common Mistakes

**Mistake #1: Missing CI/CD Pipeline**

Many teams neglect CI/CD entirely. Lacking automated CI means code is never systematically tested or formatted upon commit, leaving deployments vulnerable and skipping automated smoke tests for demo credentials.

```yaml
# INCORRECT: Missing .github/workflows/
# (directory does not exist)

# CORRECT: .github/workflows/ci.yml
name: CI
on:
  push:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v
```

**Mistake #2: Zero Automated Testing**

Submitting repositories with empty test folders yields 0% test coverage. Evaluators cannot verify software correctness, and teams fail to detect regressions internally — in previous cohorts, all CRITICAL and HIGH defects were uncovered by external QA rather than the teams themselves.

```python
# INCORRECT: Missing tests/ directory
# (or empty tests/ folder)

# CORRECT: tests/test_api.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
```

**Mistake #3: Bare Exceptions and Silent Fallbacks**

Swallowing exceptions with blanket `except:` or unlogged `except Exception:` statements hides system failures. Past teams masked LLM regressions by silently returning fallback strings, leaving degraded behavior undetected during live evaluation.

```python
# INCORRECT: Bare exception handling
try:
    result = llm.invoke(prompt)
except:  # Swallows all errors, obscuring root cause
    pass

# CORRECT: Explicit handling with structured logging
import logging
logger = logging.getLogger(__name__)

try:
    result = llm.invoke(prompt)
except openai.APIError as e:
    logger.error(f"LLM API error: {e}")
    raise HTTPException(status_code=503, detail="AI service unavailable")
except openai.RateLimitError:
    logger.warning("Rate limit hit, retrying...")
    # Exponential backoff retry logic
except ValidationError as e:
    logger.error(f"Validation error: {e}")
    raise HTTPException(status_code=422, detail=str(e))
```

**Mistake #4: Hardcoded Secrets**

Committing plain-text API keys to GitHub leads to compromised credentials, security flags, and unexpected cloud bills.

```python
# INCORRECT: Hardcoded credentials
openai_client = OpenAI(api_key="sk-proj-abc123...")
DATABASE_URL = "postgresql://admin:password123@localhost/db"

# CORRECT: Read from environment variables
import os
from dotenv import load_dotenv

load_dotenv()
openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///local.db")
```

```text
# .gitignore (ensure this entry is present)
.env
```

**Mistake #5: Omission of Evaluation Evidence**

82% of past cohort teams provided no quantitative evaluation evidence. While frequently skipped, this represents the single most impactful scoring differentiator — implement golden dataset tests as outlined in [Chapter 10](chapter-10.md) Section 10.5 in 1–2 days.

## 13.7 Field-Tested Scoring Strategies

Retrospectives from top-performing teams reveal consistent patterns that drive competitive advantage.

### Common Habits of Top Teams

**1. Complete Deliverable Sets:** Winning submissions deliver all 10 deliverables in full (or 9–10/10). Complete submissions send an undeniable signal of engineering rigor.

**2. Modular Code Architecture:** Codebases are structured thoughtfully: `app/api/`, `app/agent/`, `app/core/`, `app/models/`. Avoid monolithic single-file scripts; maintain clear separations of concerns.

```text
# Recommended clean structure
app/
├── __init__.py
├── main.py              # FastAPI application factory
├── api/
│   ├── health.py        # Health probe endpoints
│   └── chat.py          # Chat & agent endpoints
├── agent/
│   ├── graph.py         # LangGraph workflow definitions
│   ├── nodes.py         # Graph node implementations
│   ├── state.py         # State definitions
│   └── tools.py         # Agent tool definitions
├── core/
│   ├── config.py        # Centralized settings & environment variables
│   └── logging_config.py
└── services/
    └── vector_store.py  # Vector database services

# Anti-pattern structure
app.py                   # Everything dumped in a single file
agent.py                 # Monolithic unmaintainable agent logic
```

**3. Professional README:** The README is the first artifact evaluated — enrich it with architecture diagrams, installation guides, API references, and team roles to establish immediate credibility.

**4. Meaningful Test Suites:** Leading teams implement 5–10 comprehensive unit and integration tests verifying both nominal flows and boundary edge cases.

**5. Stable Deployments:** Reproducible Dockerfiles, validated live URLs, and responsive health endpoints.

### Tactical Tips

**Tip 1: The High-ROI README** — Crafting an exceptional README takes ~30 minutes and yields higher immediate scoring returns than spending 3 hours hacking marginal features.

**Tip 2: Deploy Early** — Deploy a live skeleton in Week 1 containing only `/health`. Late deployments on Demo Day eve routinely trigger unfixable configuration panics.

**Tip 3: Visual Evidence** — Capture images of everything: working interfaces, API Swagger docs, passing test suites, LangSmith traces, and passing CI badges. Concrete visuals carry far more weight than unverified text.

**Tip 4: Disciplined Git Hygiene** — Maintain steady daily commits with informative semantic messages. A sequence of 50 structured commits over 4 weeks reflects far greater teamwork than 3 bulk commits pushed on the final night.

```bash
# High quality: clear semantic commit history
git commit -m "feat: add RAG retrieval node with ChromaDB"
git commit -m "fix: handle empty query in chat endpoint"
git commit -m "test: add integration tests for chat API"

# Poor quality: vague commit messages
git commit -m "update"
git commit -m "fix"
git commit -m "wip"
```

**Tip 5: Submit Quantitative Evaluation Evidence** — 82% of teams omit this. Execute pytest against your golden dataset, chart results in markdown, and document precision/recall/latency metrics.

**Tip 6: Record Demo Video in Week 5** — Record early rather than scrambling the night before. This fulfills Deliverable #6 while supplying your Tier-2 live presentation backup.

## 13.8 Pitch Deck Structure

The pitch deck structures your 10-minute presentation — budgeted at approximately 1 minute per slide across 10 slides. 64% of past teams failed to submit one. Polished slides combined with compelling delivery build immediate evaluator confidence.

### 10-Slide Template

**Slide 1: Title**
- Project name
- One-line value proposition / tagline
- Team name and brand logo
- Demo Day date

**Slide 2: Problem**
- Concrete pain point description
- Clearly identified target user persona
- Problem frequency and severity
- Supporting quantitative statistics (e.g., "70% of students struggle to navigate complex course catalogs")

**Slide 3: Solution**
- How your solution uniquely resolves the identified problem
- Core differentiation from existing approaches
- High-level product mockup or interface teaser

**Slide 4: Product Demo**
- Key UI screenshots or animated workflow previews
- Highlight of primary features
- Core user journey progression

**Slide 5: Architecture**
- Clean, readable architecture diagram
- Technical rationale behind key architectural selections
- Justification: Why LangGraph? Why this specific vector store?

**Slide 6: AI & LLM Approach**
- RAG pipeline design, multi-agent orchestration, and prompting strategy
- LangGraph state workflow visual
- Quantitative evaluation metrics (golden dataset pass@k, RAGAS scores)

**Slide 7: Technical Highlights**
- Automated CI/CD pipeline
- Test suite coverage metrics
- Throughput and latency performance
- 2-tier guardrails (code-level schema validation + prompt filters)

**Slide 8: Demo Video**
- Embedded video preview or direct YouTube QR code
- 2–3 minute demonstration of core use cases

**Slide 9: Challenges & Learnings**
- Primary technical hurdles encountered and how they were overcome
- Key architectural retrospectives
- What architectural decisions would you change if rebuilding from scratch?

**Slide 10: Team & Roadmap**
- Team members, academic background, and technical roles
- Upcoming product roadmap
- Acknowledgments, Q&A invitation, and interactive live demo QR code

### Presentation Design & Delivery Guidelines

**Slide Design:**
- Restrict each slide to a single core concept
- Maintain a minimum font size of 24pt for visibility from judging tables
- Prioritize visuals over text (diagrams convey architecture faster than bullets)
- Dark backgrounds paired with crisp light typography project clearly
- Keep text density below 30 words per slide

**Delivery:**
- Rehearse the complete presentation at least 3 times (Section 13.4)
- Maintain strict pacing: 10 slides × 1 minute = 10 minutes total
- Designate a single primary speaker; avoid reading text directly from slides
- Ensure 3-tier live demo fallbacks are prepped and verified (Section 13.4)
- Balance presentation time: 70% on problem narrative and product value, 30% on technical architecture and Q&A defense

> 💡 **TIP:** Anticipate technical scrutiny from engineering judges. Prepare concise explanations for: "Why did you choose LangGraph over CrewAI/AutoGen?", "How do you systematically prevent hallucinations?", "What is your average inference cost per query?", and "How does this architecture handle 1,000 concurrent requests?"

## Chapter Exercise

**Exercise 9.1 (Output: `presentation/demo_script.md`) — 3-Minute AIDA Demo Script.** Author a line-by-line script for your team's 3-minute demo, structured across the 4 AIDA phases:

- **Attention (15 seconds):** Open with an engaging hook or metric that immediately captures judging attention. Avoid starting with generic greetings like "Hello, we are team...".
- **Interest (30 seconds):** Delineate user pain points, occurrence frequency, and associated costs — ground this with real user interview findings from Chapter 5.
- **Desire (2 minutes):** Step-by-step walkthrough executed in Showcase Mode — every script line must indicate `[CLICK action] → [SCREEN displayed] → [SPOKEN narrative]`. Avoid feature lists; ensure every interaction advances the user story.
- **Action (15 seconds):** Present a shortened URL and QR code, prompting judges to test the live application immediately.

Peer Review Rule: Have an external team read your script without looking at your screen — if they comprehend the product's value purely from the script, the narrative succeeds. This script also serves as the recording storyboard for Deliverable #6.

## Chapter Exit-Test (Self-Assessment Checklist)

1. What are the three most frequently omitted deliverables based on past cohort data (including percentages), and do they belong to technically difficult or operationally manageable categories? In which development week should each be locked down?
2. Among the 6 Demo Day evaluation criteria, which specific category does your team intend to elevate to the Excellent (9–10) tier? What exact file in your repository serves as supporting evidence, and in which project week is it produced?
3. What are the three layers in the 3-tier demo resilience strategy? Which deliverable number from the mandatory 10 deliverables does Tier 2 fulfill? (Hint: See Section 13.4 and Section 13.1).
4. Why do experienced judges recommend conducting full mock rehearsals one full week prior to Demo Day rather than 2 days before? What regression breakdown affected Team Gamma when changes were introduced without adequate regression testing runway?

## Summary

This chapter equipped you with the operational playbook needed to achieve Demo Day success:

- **10 Mandatory Deliverables Backed by Cohort Data** — With 100% of past teams missing video demos, 82% lacking evaluation evidence, and 64% omitting pitch decks, delivering these three assets creates an immense competitive edge.
- **Systematic Checklists** for every deliverable ensuring zero items fall through the cracks.
- **6 Criteria × 5 Performance Tiers** official evaluation rubric accompanied by concrete action plans and evidence requirements for reaching the Excellent tier.
- **The Art of the Demo** — Transition from dry feature catalogs to AIDA storytelling, leverage Showcase Mode with pre-seeded data, enforce 3-tier resilience fallbacks, utilize dedicated demo credentials, run 24-hour pre-flight checks, and conduct rigorous rehearsals.
- **6-Week Execution Roadmap** — Proposal submission in Week 2, midway demo check in Week 4, and full panel dress rehearsal in Week 5.
- **Top 5 Pitfalls** — Eliminating missing CI/CD, absent test suites, bare exceptions, hardcoded API secrets, and omitted evaluation evidence.
- **10-Slide Pitch Deck Blueprint** — Complete template and delivery guidance tailored for competitive hackathons.

Always keep in mind: Demo Day evaluates comprehensive software engineering and teamwork, not merely raw model calls. Complete deliverables + compelling narrative demonstration + resilient technical fallbacks = winning outcome.

## Final Pre-Submission Checklist

- [ ] All 10/10 mandatory deliverables fully completed?
- [ ] README includes screenshots, setup instructions, and API docs?
- [ ] Live URL is active and verified in incognito windows?
- [ ] Automated test suites pass cleanly (`pytest` passes with zero failures)?
- [ ] No hardcoded secrets present in codebase?
- [ ] No bare `except:` blocks or silent fallbacks hiding regressions?
- [ ] Multi-stage Docker image builds successfully?
- [ ] GitHub Actions CI pipeline passes with green status?
- [ ] Git commit history reflects steady, continuous development?
- [ ] Pitch deck rehearsed at least 3 times within time limits?
- [ ] High-definition demo video recorded (Tier-2 backup verified)?
- [ ] Showcase Mode pre-seeded with clean dummy data; demo account signed in?
- [ ] Full panel rehearsal completed at least 1 week prior to Demo Day?
