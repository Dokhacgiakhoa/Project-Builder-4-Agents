---
title: "Software Engineering: Team + AI (tóm tắt)"
source: "SoftwareEngineeringAITeamWork.pdf — Nguyễn Trí Dũng (CTO, AI-native SE), BTC AI20K Build Phase, 11 trang dạng ảnh"
note: "Bản ghi ý để agent tra nhanh. Không thay bản gốc PDF."
---

# Software Engineering: Team + AI — ý chính

## Luận điểm
- Mỗi engineer có "đội quân AI" riêng. Năng suất cá nhân tăng, nhưng câu hỏi là team vận hành thế nào.
- Làm nhỏ (1 người + AI) ≠ làm sản phẩm thật (cần team). Scale thì phải đổi cách làm.
- AI tăng tốc độ, **không đổi quy luật**. AI không có context tổng thể, chỉ tối ưu task cục bộ.
- Thiếu bản vẽ thì xây sai. Không theo chuẩn thì lệch hệ thống. Không phối hợp thì phá công trình.
- Không có quy trình và kiến trúc thì AI giúp **phá nhanh hơn**.

## Quy trình = hệ thống 4 yếu tố (thiếu 1 thì lệch, chậm, tốn)
1. Method: V-model, Agile/Scrum.
2. People: PM, BA, Designer, Dev, Tester. AI kiêm nhiều vai nhưng trách nhiệm phải rõ.
3. Workspace & tools: docs/spec/ADR, Jira/Linear, Git, Slack/Discord.
4. Workflow & rules: Idea → Spec → Dev → Test → Release. Có coding convention, PR review, DoD, security/CI.

## Big picture workflow (lặp theo sprint)
Brainstorm → Specs (domain, feature, role, API contract, business rule) → Architecture (ADR, stack, convention, folder) → Planning (backlog, sprint, story, ước lượng) → Thực thi song song (mỗi người + AI) → Review & merge → Retro.
- Nền chung: repo Git, vai trò rõ (người + AI), tool (CI, test, MCP), rules/DoD.
- AI mạnh khi context rõ: Specs + ADR + Contracts + Rules.

## Repo là nguồn sự thật duy nhất
- Cấu trúc gợi ý: `/specs` (vision, domain, role, feature, api-contract) · `/adrs` · `/planning/sprints` · `/tasks/<ID>.md` · `/src` · `/docs` · `AGENTS.md` · `README.md`.
- Git lưu cả ý tưởng, quyết định, kế hoạch, context, không chỉ code.

## Thực thi mỗi task
1. Pick task: đọc spec, ADR, contract, rule. `git checkout -b feature/<ID>`.
2. AI + dev code: agent đọc context, lập plan, chia subtask. **Agent là trợ lý, không quyết định thay người.**
3. Local test: unit, integration, lint, build. **Chỉ push khi pass local.**
4. Commit và push theo quy ước.
5. PR và review (người hoặc AI): code, test, docs, contract, tuân rule.
6. Merge khi approved: CI chạy đủ test, task chuyển Done.
- Git: `main` luôn ổn định · `feature/*` · `hotfix/*` · `release/*`. Pull mới nhất trước khi làm, commit nhỏ, PR để review, tag release.
- Agent luôn đọc: `/specs`, `/adrs`, `/contracts`, `/tasks/<id>.md`, `AGENTS.md`, `/src`.
- DoD mỗi task: code theo spec · test pass · docs/contract cập nhật · tuân ADR và rule · PR review và merge · task Done. **Chưa đạt DoD thì không merge.**

## 6 nguyên tắc
1. Spec-driven: rõ cái gì, tại sao, thế nào trước khi code.
2. ADR là nền: mọi quyết định kiến trúc, công nghệ, quy tắc đều ghi lại. Muốn đổi thì viết ADR mới.
3. Task đủ lớn (feature-level) để AI tự chia nhỏ. Đừng chia quá vụn.
4. Làm việc qua contract (API/Proto/Event), không dựa vào hiểu ngầm.
5. AI luôn đọc context trước khi code. Cập nhật context là trách nhiệm của cả team.
6. Git là kỷ luật: nhánh rõ, PR và review bắt buộc, mọi thay đổi truy vết được.
- AI ra kết quả sai thì thường do context thiếu hoặc cũ.

## 5 ADR nên có
1. Test strategy / test-first: test là hợp đồng hành vi.
2. Domain split (microservice hoặc modular monolith): chia domain tốt thì chia context tốt.
3. API contract first (OpenAPI, gRPC, event, DTO): scale bằng contract, không bằng hiểu ngầm.
4. Project structure & coding convention (folder, naming, lint, error handling, logging, validation, test style, commit): không có convention thì AI nhân bản hỗn loạn.
5. Definition of Done: done là đủ chuẩn để merge, không phải "code chạy được".
