# Project Charter & Weekly Reporting Templates (VinUni / AI20K)

> Comprehensive Markdown representation of the official AI20K & VinUni project charter and reporting spreadsheet.

---

## Sheet 1: Team Operating Rules

| Operating Rules & Governance — Build Phase | Column B |
| --- | --- |
| 1. Working Hours & Availability |  |
| Commitment | Full-time: minimum 40 hours/week, Monday through Saturday |
| Core Hours | 09:00–11:30 and 14:00–17:00 — all team members must be active and reachable |
| Daily Standup | 09:00 every morning (15 minutes). Format: what done / doing / blockers |
| Absence Policy | Notify team lead and mentor 24 hours in advance. Maximum 2 days across 6 weeks |
| 2. Reporting & Accountability |  |
| Daily Standup Report | Submit daily updates on Discord/chat: done / doing / blockers |
| Weekly Report | Consolidate before Wednesday Mentor Review. Use 'Weekly Report Template' |
| Mandatory Contents | Progress, Metrics, Blockers, Next Week Plan, Screenshots, SSOT Sheet Link |
| Delinquency Policy | First notice on missed report. 3 missed reports → formal mentor review |
| Mentor Sync Meetings | Wednesday evening: joint cohort sync (mandatory). Saturday: team sync (mandatory) |
| 3. Parallel Project Artifacts |  |
| GitHub Repository | Source code + README.md + Architecture diagrams. Daily commits on active coding days |
| Central Project Sheet | Google Sheets or Excel: Canonical links, specs, sprint tracking, risks, notes |
| Branching Strategy | GitHub Flow. Pull Requests require review by at least one other member |
| Documentation | Continuous README updates. Architecture diagrams updated when components mutate |
| Testing | Automated tests for core logic. Unit test coverage on critical business workflows |
| 4. Stakeholder Engagement |  |
| Identify Stakeholders | Finalize during Week 1 with mentor assistance |
| Engagement Cadence | W1 (Discovery) → W2 (Solution proposal) → End W3 (Demo 1) → End W5 (Demo 2) |
| Feedback Capture | Log all feedback in Central Project Sheet and weekly status reports |
| Professional Standards | Punctual attendance, prepared agendas, follow-up minutes after meetings |
| 5. Issue Resolution & Escalation |  |
| Technical Blockers | Post in #support → mentors respond within 24 hours |
| Stakeholder Blockers | Notify mentor immediately for relationship facilitation |
| Team Friction | Team lead mediates first. Unresolved issues escalate to mentor |
| 6. Evaluation & Scoring |  |
| Core Criteria | 1) Working V1 on real data <br> 2) Stakeholder satisfaction <br> 3) Code quality <br> 4) Team collaboration & accountability |
| Continuous Review | Mentors provide ongoing feedback each sync rather than waiting for Demo Day |
| Final Evaluation (W6) | Live Demo + Q&A defense based on Impact Report and Presentation |
| 7. Cultural Principles |  |
| Ownership | End-to-end accountability. Own your assigned deliverables |
| Candor | Honest reporting. Surfacing bad news early is essential |
| Working Code First | Deployable working software in production outweighs theoretical perfection |
| Fail Fast, Learn Fast | Mistakes are acceptable; failing to remediate rapidly is not |
| Mutual Respect | Respect teammate time; commit to punctuality and reliable execution |

---

## Sheet 2: Internal Team Compact

| Internal Team Compact Template | Column B | Column C | Column D | Column E | Column F |
| --- | --- | --- | --- | --- | --- |
| Completed by each team during Week 1 with Team Lead. Updated as needed. |  |  |  |  |  |
| 1. Team Information |  |  |  |  |  |
| Team Cohort | [Alpha / Beta / Gamma / Delta] |  |  |  |  |
| Product / Project Name | [Product Name] |  |  |  |  |
| Date Established | [DD/MM/YYYY] |  |  |  |  |
| Last Revision | [DD/MM/YYYY] |  |  |  |  |
| 2. Team Member Roster |  |  |  |  |  |
| Member Name | Primary Role | Secondary Role | Specific Responsibilities | Weekly Hours | Notes |
| [Name] | Team Lead | Architecture | Coordination, mentor sync, PR review | 40 |  |
| [Name] | Backend Engineer | DevOps | API, database, server runtime, CI/CD | 40 |  |
| [Name] | Frontend Engineer | UI/UX | Web interface, responsive client, styling | 40 |  |
| [Name] | AI / ML Engineer | Evaluation | LangGraph agent, RAG pipeline, benchmarks | 40 |  |
| 3. Task Delegation & Cadence |  |  |  |  |  |
| Assignment Authority | Team Lead delegates primary tasks with team alignment. |  |  |  |  |
| Task Clarity | Single owner per task, specific deadline, explicit acceptance criteria. Avoid ambiguous tasks. |  |  |  |  |
| Acceptance Window | Assignees acknowledge tasks within 2 hours. Ask clarifying questions immediately. |  |  |  |  |
| Slippage Warnings | Flag potential delays at least 4 hours before deadline. |  |  |  |  |
| Code Reviews | PRs require at least 1 approval before merge. Limit PRs to < 400 lines. |  |  |  |  |
| 4. Communication Channels |  |  |  |  |  |
| Channel | Purpose | Response Window | Operating Rules |  |  |
| Discord — #team-chat | Daily async chat, quick Q&A | Within 2 business hours | Tag relevant members; no spam |  |  |
| Discord — #team-standup | Morning standup text | Submit by 09:30 | Follow 3-question standup template |  |  |
| Voice Sync / Discord Call | Urgent unblocking discussions | Scheduled as needed | Document decisions in text channel |  |  |
| GitHub Issues / PRs | Code reviews, bug tracking, specs | Within 1 business day | PRs link to issues with testing steps |  |  |
| Email | Formal mentor and partner communications | Within 24 hours | Keep formal record of commitments |  |  |
| 5. Git & Code Governance |  |  |  |  |  |
| Main Branch | main contains only tested, approved code. Direct push to main is prohibited. |  |  |  |  |
| Branch Naming | feature/feature-name · bugfix/bug-name · hotfix/fix-name |  |  |  |  |
| Commit Syntax | Conventional Commits in English (feat: ..., fix: ..., docs: ..., refactor: ...). |  |  |  |  |
| Hygiene (.gitignore) | Never commit: node_modules, .env, keys, build artifacts, temporary logs. |  |  |  |  |
| 6. Signatures & Commitments |  |  |  |  |  |
| Member Name | Role | Confirmed (Yes/No) | Date | Signature |  |
| [Name] | Team Lead | Yes | [DD/MM/YYYY] | [Signed] |  |
| [Name] | Backend | Yes | [DD/MM/YYYY] | [Signed] |  |
| [Name] | Frontend | Yes | [DD/MM/YYYY] | [Signed] |  |
| [Name] | AI Engineer | Yes | [DD/MM/YYYY] | [Signed] |  |

---

## Sheet 3: Weekly Progress Report

| Weekly Status Report — Build Phase | Column B | Column C | Column D |
| --- | --- | --- | --- |
| Consolidated prior to Wednesday Mentor Review |  |  |  |
| Part 1: General Info |  |  |  |
| Team Cohort: | [Alpha / Beta / Gamma / Delta] |  |  |
| Sprint Week: | [W1–W6] — [Start Date] to [End Date] |  |  |
| Reporter: | [Team Lead Name] |  |  |
| Submission Date: | [DD/MM/YYYY] |  |  |
| Part 2: Deliverable Progress |  |  |  |
| No. | Planned Objective / Task | Status | Notes |
| 1.0 | [Task description] | Done / In Progress / Blocked | [Diagnostic notes] |
| 2.0 | [Task description] | Done / In Progress / Blocked | [Diagnostic notes] |
| 3.0 | [Task description] | Done / In Progress / Blocked | [Diagnostic notes] |
| 4.0 | [Task description] | Done / In Progress / Blocked | [Diagnostic notes] |
| Part 3: Metrics & KPIs |  |  |  |
| Metric | Value | Target / Notes |  |
| Features Completed | [X / Y] | MVP scope tracking |  |
| Open Bugs | [Count] | Unresolved defects |  |
| Stakeholder Meetings | [Count] | User interviews |  |
| Deployment State | [Local / Staging / Production] | Runtime environment |  |
| SSOT Updated? | [Yes / No] | Sheet link attached |  |
| Part 4: Blockers & Risks |  |  |  |
| [Detail active blockers, technical risks, and requested escalations. If none, specify 'No blockers.'] |  |  |  |
| Part 5: Next Week Commitment |  |  |  |
| No. | Target Task | Assignee | Priority |
| 1.0 | [Task description] | [Name] | High / Medium / Low |
| 2.0 | [Task description] | [Name] | High / Medium / Low |
| 3.0 | [Task description] | [Name] | High / Medium / Low |
| Part 6: Verification Artifacts |  |  |  |
| [Links to screenshots, live recording, PR diffs, or SSOT tracker. Minimum 1 verified screenshot/week.] |  |  |  |

---

## Sheet 4: Project Charter Template

| Project Charter — PMP Standard Template | Column B | Column C | Column D | Column E |
| --- | --- | --- | --- | --- |
| Completed by team in Week 1 prior to first mentor review |  |  |  |  |
| 1. Project Overview |  |  |  |  |
| Project Title | [Product or Initiative Name] |  |  |  |
| Team Cohort | [Alpha / Beta / Gamma / Delta] |  |  |  |
| Author | [Team Lead Name] |  |  |  |
| Date Created | [DD/MM/YYYY] |  |  |  |
| Document Version | 1.0 |  |  |  |
| 2. Problem Statement & Objectives |  |  |  |  |
| Problem Statement | [Concrete business pain point being solved with quantitative costs] |  |  |  |
| Proposed Solution | [Concise scope of the AI system being engineered and target users] |  |  |  |
| SMART Goals (6 weeks) | [Specific, Measurable, Achievable, Relevant, Time-bound milestones] |  |  |  |
| 3. Project Scope |  |  |  |  |
| No. | In-Scope (Committed MVP) | Out-of-Scope (Explicitly Deferred) |  |  |
| 1.0 | [Core capability to build] | [Feature explicitly excluded from 6-week scope] |  |  |
| 2.0 | [Core capability to build] | [Feature explicitly excluded from 6-week scope] |  |  |
| 3.0 | [Core capability to build] | [Feature explicitly excluded from 6-week scope] |  |  |
| 4. Stakeholder Map |  |  |  |  |
| Role | Organization / Contact | Influence | Engagement Cadence |  |
| Executive Sponsor | [Sponsor Name] | High | Bi-weekly review |  |
| End User Persona | [Target User Group] | High | Weekly feedback |  |
| Team Lead | [Full Name] | High | Daily management |  |
| Technical Mentor | [Mentor Name] | High | Weekly coaching |  |
| 5. Core Milestones |  |  |  |  |
| Milestone | Week | Target Date | Deliverables | Owner |
| Kickoff & Charter | W1 | End of W1 | Charter + Team Compact | Team Lead |
| Solution Architecture | W2 | End of W2 | Tech Specs + Architecture | Tech Lead |
| Demo 1 (Prototype) | W3 | End of W3 | Working Prototype + Feedback | Team |
| Feature Hardening | W4–W5 | End of W5 | Complete System + Deploy | Team |
| Demo 2 (Final System) | W5 | End of W5 | Rehearsal Demo + Metrics | Team |
| Final Evaluation | W6 | Demo Day | Impact Report + Pitch Deck | Team Lead |
| 6. Success Criteria |  |  |  |  |
| No. | Criterion | Weight | Measurement Method |  |
| 1.0 | Working V1 with Real Data | 40% | Production deployment without crash on real test sets |  |
| 2.0 | Stakeholder Satisfaction | 25% | Stakeholder rating after Demo 2 (scale 1–10) |  |
| 3.0 | Code & Architecture Quality | 20% | PR reviews, test coverage, clean architecture |  |
| 4.0 | Teamwork & Accountability | 15% | Punctual standups, reliable delivery, proactive escalation |  |

---

## Sheet 5: Daily Standup Template

| Daily Standup Reporting Format | Column B | Column C | Column D |
| --- | --- | --- | --- |
| Submit daily before 09:30 on Discord #team-standup or present during 15-minute sync |  |  |  |
| 3 Core Questions |  |  |  |
| No. | Question | Response Guideline |  |
| 1.0 | What did I complete yesterday? | Concrete completed tasks; link PRs/commits |  |
| 2.0 | What will I accomplish today? | Concrete focus items for the day |  |
| 3.0 | What is currently blocked? | Explicit blockers + specific help required (or 'None') |  |
| Daily Message Format Example: <br><br> 🟢 Standup [DD/MM] — [Name] <br> ✅ Yesterday: Implemented login API and opened PR #12 <br> 📅 Today: Build dashboard frontend and connect auth state <br> 🚫 Blockers: None |  |  |  |

---

## Sheet 6: Infrastructure & Resource Requests

| Infrastructure & Cloud Compute Catalog | Column B | Column C | Column D | Column E |
| --- | --- | --- | --- | --- |
| Prioritize free tier quotas first |  |  |  |  |
| Resource Type | Description | Free Tier Options | Paid Tier | Notes |
| Server / Hosting | Cloud hosting for API + Web + DB | Render (free), Railway ($5 credit), Vercel | VPS (Ramnode, Hetzner ~$5–10/mo) | Free tier first; upgrade on scale |
| GPU / AI Compute | Model inference, embeddings, eval | Google Colab, Hugging Face Spaces, Groq | RunPod (~$0.4/hr) or cloud GPU | Prefer managed model APIs |
| AI API Keys | LLMs for agent reasoning & RAG | Groq free, Gemini free tier, OpenRouter | OpenAI / Anthropic APIs | Track usage across team |
| Storage / CDN | Object storage for user assets | Cloudflare R2 (10GB free), Supabase Storage | S3 Standard | Optimize payload sizes |
| Observability | Error tracking and agent telemetry | Sentry free tier, Langfuse self-hosted | Paid observability suites | Mandatory starting Week 3 |
