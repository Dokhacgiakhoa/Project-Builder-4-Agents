# TASKS — KẾ HOẠCH HOÀN THIỆN PROJECT-BUILDER-4-AGENTS

> Tệp quản lý công việc của **người bảo trì kit** (không phải tài liệu cho Agent của dự án người dùng). Cập nhật cột *Trạng thái* khi làm; thêm việc mới ở cuối nhóm tương ứng.
> Cập nhật lần cuối: 2026-11-06 · Nền tảng hiện tại: 54 test pass cục bộ; đã đồng bộ toàn diện Project Health Check v2.2.0 (Engine + Web/Desktop UI + `.exe`).

**Trạng thái**: `TODO` chưa làm · `DOING` đang làm · `REVIEW` chờ maintainer duyệt · `BLOCKED` chờ việc khác · `DONE` xong · `HOÃN` chủ động để sau
**Ưu tiên**: `P0` chặn giá trị cốt lõi · `P1` cần trước khi cho người dùng thật dùng · `P2` nên có · `P3` có thì tốt
**Công sức**: `S` ≤ nửa ngày · `M` 1–2 ngày · `L` > 2 ngày
**Người làm**: `Claude` · `Maintainer` (cần quyền/thiết bị/quyết định của maintainer)

---

## Nguyên tắc dẫn đường (đã chốt, mọi việc dưới đây phải tuân theo)
1. Người dùng là fresher/vibe coder: Agent phải **chủ động** chọn tài liệu từ mô tả, người dùng không phải biết tên tệp hay viết prompt.
2. Tài liệu viết **cho Agent**: chỉ chứa **quyết định và ràng buộc**, không dạy lại kiến thức công nghệ Agent đã biết.
3. Core bắt buộc cho mọi repo; Profile tùy biến theo dự án; Library chỉ tra khi cần.
4. Health Check là bước rà soát cố định, offline, **giúp Agent đỡ tốn token**, không thay thế Agent. Báo cáo là một tệp `project-review.md` cho cả người và Agent.
5. Quét an toàn chỉ nhắm **prompt injection trong tệp văn bản**; không làm antivirus.
6. Không có stack profile dạng "dạy công nghệ" (đã bỏ).

---

## Lộ trình theo mốc

| Mốc | Mục tiêu | Nhóm việc | Xong khi |
| :-- | :-- | :-- | :-- |
| 2026-11-07 | **Sửa dương tính giả Frontend 20/20**: engine quét nhầm app React mẫu trong `examples/` và `profiles/*/starter/` nên bật `has_frontend`. Thêm vùng mẫu vào `SKIP_REASONS`/`SKIP_REL_PATTERNS` (`constants.py`, `tree.py`) và `tests/test_sample_zone_exclusion.py`. Kit tự quét: Frontend/Database biến mất, Backend 100% -> 70%, điểm cũ bị thổi phồng. Chưa đo lại bằng Antigravity, chưa lập lại `evals/`. |
| **M0 — Kiểm chứng** | Chứng minh thứ đã viết chạy được với Agent thật | C, B3 | Dựng được dự án từ thư mục rỗng bằng 3 Agent; CI GitHub xanh |
| **M1 — Dùng được** | Người dùng thật cài và dùng không vướng | A, B, E1–E3 | Có bản phát hành, exe chạy trên máy sạch, repo đã đổi tên |
| **M2 — Chắc tay** | Giảm báo thừa, tăng độ phủ, dọn nội dung | D, E4+, F | Bộ eval định tuyến đạt ngưỡng; báo thừa đo được và chấp nhận được |

Thứ tự đề xuất: **C2 → B3 → B1 → B8 (push) → C1 → B2 → A1 → A2 → A3 → E1 → C3 → còn lại**. Lý do: C1/C2 kiểm chứng giả định lớn nhất (Agent thật sự đọc `BOOTSTRAP.md` và định tuyến đúng); sửa nội dung trước khi đóng gói exe thì đỡ phải làm lại.

---

## Nhóm C — Kiểm chứng giá trị cốt lõi (Builder với Agent thật) · MỐC M0

| ID | Việc | Ưu tiên | Công sức | Người | Phụ thuộc | Trạng thái |
| :-- | :-- | :-: | :-: | :-- | :-- | :-: |
| C0 | **Soạn kịch bản và checklist C1** (`evals/c1-bootstrap-protocol.md`: 3 kịch bản, vai người dùng, 16 mục chấm, mẫu ghi kết quả) | P0 | S | Claude | — | DONE |
| C0.1 | **Triển khai ADR-0013 & Zero-Clone Remote Hub**: MANIFEST.json, llms.txt, HOW_IT_WORKS.md, curated-skills, curated-mcp | P0 | M | Claude | — | DONE |
| C0.2 | **Triển khai ADR-0014 & English-First Standardization**: Chuyển ngữ toàn diện bộ khung core/profiles/templates/index sang tiếng Anh để tiết kiệm ~50% tokens | P0 | M | Claude | — | DONE |
| C0.3 | **Đóng gói Playbook Visual Reverse-Engineering (D-006)**: Giao thức Screenshot-to-Code chống UI Doom Loop, tích hợp luật thực chứng (Rule 10 & 11 trong AGENTS.md) | P0 | S | Claude | — | DONE |
| C1 | **Chạy thử BOOTSTRAP thật** với **Claude Code** và **Antigravity** (Codex chưa kiểm chứng): S1 thư mục rỗng, S2 dự án dở, S3 dự án phức tạp. Chạy trong phiên mới không ngữ cảnh. Dùng URL sau khi B1 + push; trước đó dùng biến thể đường dẫn cục bộ | P0 | M | Claude (phiên mới) + Maintainer (Antigravity, và Claude Code nếu muốn) | C0; URL cần B1 + B8 | TODO |
| C2 | **Xác minh định dạng cấu hình Agent** theo tài liệu chính thức: `AGENTS.md`, import trong `CLAUDE.md`, đường dẫn skills (`.agents/skills`, `.claude/skills`), rule/workflow của Antigravity (đường dẫn global còn mâu thuẫn giữa các nguồn). Sửa `BOOTSTRAP.md` bước 1.3 theo kết quả | P0 | S | Claude | — | DONE |
| C3 | **Bộ eval định tuyến**: 20 câu mô tả dự án của người không chuyên → kỳ vọng (profile, mức rào chắn, tài liệu đã tra). Chạy với từng Agent, đo tỉ lệ chọn đúng | P1 | M | Claude viết, Maintainer chạy | C1 | TODO |
| C4 | **Sửa nội dung theo kết quả C1/C3**: chỗ Agent bỏ qua, hiểu sai, đọc thừa; chỉnh `BOOTSTRAP.md`, `INDEX.md` ("Khi nào dùng"), `profiles/README.md` | P1 | M | Claude | C1, C3 | BLOCKED |
| C7 | **README ghi rõ Codex chưa kiểm chứng** (hiện ghi "Dùng được với Claude Code · Antigravity · Codex") cho tới khi có người chạy thử | P2 | S | Claude | — | TODO |
| C5 | **Adapter theo công cụ**: sinh rule/workflow riêng cho Antigravity và Codex từ `AGENTS.md` (một nguồn sự thật) khi C2 xác nhận định dạng | P2 | M | Claude | C2 | BLOCKED |
| C6 | **Gói Claude Code plugin/marketplace** để cài không cần clone (nếu C2 xác nhận cơ chế phù hợp) | P3 | M | Claude | C2, quyết định Q3 | HOÃN |

**Nghiệm thu C1** (chấm bằng checklist 16 mục trong `evals/c1-bootstrap-protocol.md`): với mỗi Agent, từ một câu duy nhất ("dùng <URL repo> dựng dự án giúp mình, mình muốn làm ...") Agent tự: đọc `BOOTSTRAP.md` → dựng Core → phỏng vấn ≤ 3 câu/lượt → chọn profile kèm lý do → cài rào chắn → chạy Health Check. Điểm Health Check của dự án sinh ra ≥ 80 và Core Baseline B1–B9 đạt.
**Nghiệm thu C3**: ≥ 85% câu chọn đúng profile; 100% câu có dấu hiệu "nhỏ/đồ án" không bị đẩy lên Clean Architecture.

---

## Nhóm B — Repo, CI và phát hành kit · MỐC M0/M1

| ID | Việc | Ưu tiên | Công sức | Người | Phụ thuộc | Trạng thái |
| :-- | :-- | :-: | :-: | :-- | :-- | :-: |
| B1 | **Đổi tên repo GitHub** thành `Project-Builder-4-Agents` (mọi link trong tài liệu và mã đã trỏ tên mới; `origin` cục bộ đã đổi) | P0 | S | Maintainer | — | DONE |
| B8 | **Push** các commit lên GitHub (hiện mới commit cục bộ; Agent không lấy được kit qua URL khi chưa push) | P0 | S | Maintainer | B1 | DONE |
| B2 | **Dọn tên cũ còn sót**: URL `Project-Starter-Kit` đã thay; còn đường dẫn máy cứng trong `scripts/build_brand_assets.py` và `generate_icon.py`, thư mục cấu hình `~/.starter-kit`, demo URL trong pitch deck, tên gói `ai-native-frontend-starter-kit` | P2 | S | Claude | — | TODO |
| B3 | **Chạy CI trên GitHub lần đầu** (ma trận Python 3.12/3.14, pytest, eslint/tsc/vitest, `check_links`); sửa mọi lỗi lộ ra | P0 | S | Claude (maintainer push) | — | DOING |
| B4 | **Gắn tag phiên bản** `v0.1.0` + `CHANGELOG.md`; `kit_ref` trong `kit.json` mẫu ghim tag thay vì `main` | P1 | S | Claude | B3 | BLOCKED |
| B5 | **Lệnh thay `make` trên Windows**: ghi lệnh tương đương (`python -m pytest tests -q`, `python scripts/check_links.py`) vào README; kiểm tra Makefile trên Linux/macOS | P2 | S | Claude | — | TODO |
| B6 | **Bảo vệ nhánh `main`** (yêu cầu CI xanh), bật Dependabot cho npm/pip/actions | P2 | S | Maintainer | B3 | TODO |

**Nghiệm thu B3**: workflow xanh trên `main`; `check_links` chạy và fail khi cố ý làm hỏng một link/khuôn.

---

## Nhóm A — Health Check: đóng gói và phát hành · MỐC M1

| ID | Việc | Ưu tiên | Công sức | Người | Phụ thuộc | Trạng thái |
| :-- | :-- | :-: | :-: | :-- | :-- | :-: |
| A1 | **Build lại exe** bằng `python scripts/build_exe.py` (PyInstaller engine + vỏ .NET 10). Mã C# `MainForm.cs`/`PythonRuntime.cs` **chưa từng được biên dịch**: sửa lỗi biên dịch nếu có | P0 | M | Maintainer cài .NET 10 SDK + PyInstaller, Claude sửa lỗi | — | DONE |
| A2 | **Thử trên máy Windows sạch** (Windows Sandbox/VM, không Python): exe self-contained đã kiểm chứng chạy trên môi trường tước sạch PATH (không Python, không .NET, không PyLauncher); ra `project-review.md` có Mục 0/7 và cờ SAFE-001; shell CDP reload giữa chừng được kiểm chứng (PID engine giữ nguyên); engine force-kill được watchdog 180s dọn sạch. Còn thiếu: thử khi máy thiếu WebView2 | P0 | S | Maintainer | A1 | DONE |
| A3 | **Phát hành exe qua GitHub Releases** (một file exe duy nhất có engine nhúng, ADR-0022, + `SHA256SUMS`; không ship `engine/`; workflow tự tạo release khi gắn tag) thay vì commit nhị phân vào git; gỡ `Project-Health-Check.exe` bản cũ khỏi repo, sửa README trỏ tới trang Releases. **v0.1.0 đã phát hành (2026-11-08) với exe SHA-256 `1ab95081…`**: giao diện test thủ công OK, G1/G2 đạt, số liệu README đã sửa theo số đo (báo cáo `evals/results/2026-11-08-release-v0.1.0-verification-016.md`). Chưa chạy lại cho bản này: máy sạch, watchdog, reload | P1 | M | Claude (workflow), Maintainer (duyệt) | A2, B4 | DONE |
| A4 | **Giao diện web hiển thị Mục 0/7**: kiểm tra `static/js` và API đã trả dữ liệu an toàn và phạm vi; nếu chưa thì thêm tab | P1 | M | Claude | — | DONE |
| A5 | **Linux/macOS**: quyết định có đóng gói engine PyInstaller cho hai nền tảng không, hay giữ `.sh` + Python 3.12+; sửa thông báo "THÀNH CÔNG" luôn hiện trong shell script khi quét lỗi | P2 | M | Claude | Q2 | HOÃN |
| A6 | **Ký số/SmartScreen**: ghi hướng dẫn người dùng khi Windows cảnh báo; cân nhắc ký số khi có người dùng thật | P3 | S | Maintainer | A3 | HOÃN |

**Nghiệm thu A2**: exe chạy trên máy không cài Python; thời gian quét repo 5.000 tệp < 30 giây; không mở cổng ngoài `127.0.0.1`.

---

## Nhóm E — Health Check: engine và báo cáo · MỐC M1/M2

| ID | Việc | Ưu tiên | Công sức | Người | Phụ thuộc | Trạng thái |
| :-- | :-- | :-: | :-: | :-- | :-- | :-: |
| E1 | **Phát hiện `ARCH-008`: thiếu rào chắn** theo mức M1–M3 mà dự án khai báo (không có luật lint/ranh giới import hoặc tách project; CI không chạy kiểm tra kiến trúc). Thêm tài liệu khắc phục + test | P1 | M | Claude | — | DONE |
| E2 | **Mở rộng `ARCH-007`** (`PROFILE_EXPECTATIONS`) cho cả 4 profile, kể cả cấu trúc theo ngôn ngữ (.NET/Python/TS); thêm fixture test | P1 | M | Claude | — | DONE |
| E3 | **Giảm báo thừa**: đưa `examples/`, thư mục fixture test và `*.min.*`, `*.map` vào danh sách bỏ qua kèm lý do (hiển thị ở Mục 7) | P1 | S | Claude | — | DONE |
| E4 | **Khai báo `kit.json` trong báo cáo**: ghi `kit_ref` đang dùng và cảnh báo khi cũ hơn bản kit mới nhất | P2 | S | Claude | B4 | DONE |
| E5 | **Bộ test hồi quy bằng dự án mẫu** (empty, bootstrapped, dở dang, có tín hiệu SAFE): kết quả kỳ vọng cố định để giữ cam kết "cùng đầu vào, cùng kết quả" | P2 | M | Claude | — | TODO |
| E6 | **Mã thoát theo ngưỡng** (`--fail-under N`) và `--output <đường dẫn>` cho CI | P3 | S | Claude | — | HOÃN |
| E7 | **Tách báo cáo dài**: khi > N phát hiện, giữ bảng tóm tắt + nhóm theo tài liệu khắc phục để Agent đọc ít token hơn | P2 | M | Claude | — | TODO |
| E8 | **Mô hình Archetype "Library/Framework"**: bổ sung nhận diện cho thư viện thuần túy không có điểm vào ứng dụng trong `analysis.py` | P2 | M | Claude | — | TODO |
| E9 | **Tối ưu tốc độ quét repo lớn**: litellm (~15k tệp) hiện tốn ~35s đơn luồng; nghiên cứu đa luồng hoặc lazy regex trong các trụ cột | P2 | M | Claude | — | TODO |
| E10 | **Chi phí khởi động nguội trên HDD**: 4.000 tệp tốn ~30s đọc vật lý lần đầu; đánh giá giải pháp pre-warm hoặc chỉ báo loại ổ đĩa | P3 | S | Claude | — | TODO |

**Nghiệm thu E1**: dự án khai báo `vertical-slice` + M2 nhưng không có luật chặn import chéo → báo `ARCH-008` kèm tài liệu khắc phục; có luật → hết báo.

---

## Nhóm F — Quét an toàn (prompt injection) · MỐC M2

| ID | Việc | Ưu tiên | Công sức | Người | Phụ thuộc | Trạng thái |
| :-- | :-- | :-: | :-: | :-- | :-- | :-: |
| F1 | **Đo báo thừa/bỏ sót** trên một tập tệp thật: ≥ 20 repo công khai (README, docs, cấu hình agent) + một bộ mẫu tấn công tự viết (đa ngôn ngữ, biến thể diễn đạt). Ghi tỉ lệ vào `tests/` hoặc tài liệu | P1 | M | Claude (maintainer cho phép tải) | — | TODO |
| F2 | **Bổ sung mẫu** từ kết quả F1 (biến thể diễn đạt, ngôn ngữ khác tiếng Anh/Việt, kỹ thuật che giấu như đổi dạng ký tự) | P2 | M | Claude | F1 | BLOCKED |
| F3 | **Quy tắc cho Agent khi gặp `SAFE-`**: đưa phần "dừng và hỏi" vào `core/templates/AGENTS.md` và skill `health-check` để dự án sinh ra mang sẵn | P1 | S | Claude | — | TODO |
| F4 | **Tài liệu cố ý nói về injection** (như `core/untrusted-content.md`) tự bị gắn cờ khi quét chính kit: ghi chú trong báo cáo kit hoặc chấp nhận có chủ đích | P3 | S | Claude | — | HOÃN |
| F5 | **Harness kiểm chứng Agent (Handoff 002)**: triển khai Phase 0 kịch bản đo lường tương tác thật của Agent với Health Check theo maintainer handoff 002 (private) | P1 | M | Claude + Maintainer | — | TODO |
| F6 | **Mở rộng chuẩn hóa Unicode NFC/NFD**: theo dõi và bổ sung chuẩn hóa cho các bộ ký tự mở rộng ngoài tiếng Việt và Thổ Nhĩ Kỳ | P2 | S | Claude | — | TODO |

**Nghiệm thu F1**: báo thừa ≤ 2% số tệp văn bản thông thường trên tập repo công khai; phát hiện ≥ 90% mẫu tấn công trong bộ mẫu tự viết.
**Giới hạn đã chấp nhận**: không quét mã nguồn, không tìm virus; báo cáo luôn ghi "không có tín hiệu ≠ an toàn".

---

## Nhóm H — Token Monitor (theo dõi token khi vibe coder chat với agent)

| ID | Việc | Ưu tiên | Công sức | Người | Phụ thuộc | Trạng thái |
| :-- | :-- | :-: | :-: | :-- | :-- | :-: |
| H1 | **Engine + CLI** đọc log Claude Code, loại trùng, tính ngữ cảnh/tốc độ/lượt nặng (`scripts/token_monitor/`, `token_monitor_cli.py`, 15 test) | P1 | M | Claude | — | DONE |
| H2 | **Dashboard Web theo thời gian thực** (`scripts/token_dashboard/`, `token_dashboard_cli.py`): trang độc lập, loopback, chỉ đọc; xem thử trên trình duyệt desktop/mobile/sáng/tối; 10 test dịch vụ + máy chủ | P1 | M | Claude | H1 | DONE |
| H2b | **Gắn dashboard vào `reviewer_shell`** như một tab (hiện là trang riêng, tránh sửa giao diện Health Check chưa có test giao diện) | P2 | S | Claude | H2 | TODO |
| H3 | **Đưa vào `.exe`**: build lại vỏ .NET để có tab/cửa sổ monitor; thử trên máy sạch | P1 | M | Maintainer cài .NET 10, Claude sửa | H2, A1 | TODO |
| H4 | **Adapter Codex** (`~/.codex/sessions/**/rollout-*.jsonl`, sự kiện `token_count` là bộ đếm lũy kế nên phải trừ lượt trước). Chưa có dữ liệu Codex để kiểm chứng trên máy này | P2 | M | Claude + Maintainer (cần log Codex thật) | H1 | TODO |
| H5 | **Khảo sát Cursor/Antigravity/Windsurf**: có lưu token cục bộ không? Nếu không thì ghi rõ giới hạn, không đoán | P2 | S | Claude (tìm kiếm) | — | TODO |
| H6 | **Cảnh báo chủ động** (ví dụ ngữ cảnh vượt ngưỡng): thông báo desktop hoặc dòng trạng thái cho Claude Code (`statusLine`) | P3 | S | Claude | H1 | HOÃN |
| I1 | **Dịch văn bản do engine sinh ra sang tiếng Anh** (tiêu đề phát hiện, remediation, nhãn archetype/hạng, tiêu chí pillar, log quét, `project-review.md`; khoảng 800 dòng trong `scripts/auditor_engine/`), kèm cơ chế chọn ngôn ngữ báo cáo. Hiện giao diện đã là tiếng Anh (ADR-0023) nhưng nội dung engine vẫn tiếng Việt | P1 | L | Claude (dịch), Antigravity (chạy test) | — | DONE (2026-11-08, ADR-0026: engine emits English; Vietnamese is a language pack; verified identical to the previous engine on 23 projects) |
| I2 | **Dựng lại exe và kiểm chứng giao diện cài đặt mới** (một file, ngôn ngữ mặc định tiếng Anh, menu con Cài đặt): maintainer handoff 013 (private); kiểm chứng xong qua báo cáo 013-015 (exe 3EA6CF08..., engine giải nén có kiểm tra SHA-256, ADR-0025). Còn lại: phát hành exe qua Releases (A3), không commit nhị phân | P0 | S | Antigravity | A1 | DONE |

**Nghiệm thu H1**: tổng khớp phép tính độc lập trên log thật (đã đạt ngày 2026-11-07: 114 lượt khớp từng con số). **Giới hạn đã chấp nhận**: chỉ token, không quy ra tiền (giá đổi và chưa được kiểm chứng); số liệu từ log cục bộ, không phải hoá đơn.

---

## Nhóm D — Nội dung kit · MỐC M2

| ID | Việc | Ưu tiên | Công sức | Người | Phụ thuộc | Trạng thái |
| :-- | :-- | :-: | :-: | :-- | :-- | :-: |
| D1 | **Khung chọn công nghệ** (tài liệu `router`): tiêu chí quy mô, kỹ năng người dùng, chi phí, thời gian, rủi ro; bắt Agent nêu lý do và phương án đã loại. Liên kết với Technology Selection Gate | P1 | S | Claude | — | TODO |
| D2 | **Rà `INDEX.md`**: thêm cột/ghi chú điều kiện loại trừ cho các dòng dễ chọn nhầm; kiểm tra "Khi nào dùng" viết theo lời người dùng | P1 | S | Claude | C3 | BLOCKED |
| D3 | **Tài liệu tham khảo dài** (`design-archetypes-catalog` 248 dòng, `visual-dna-prompts` 134, `design-patterns-catalog`): thêm tóm tắt đầu trang + mục lục để Agent đọc có chọn lọc, hoặc chia nhỏ | P2 | M | Claude | — | TODO |
| D4 | **Đánh dấu `knowledge-base/`, `templates/pitch-deck`** là Library "không đọc trừ khi được yêu cầu"; xác định tệp nào chuyển ra khỏi đường đi của Agent | P2 | S | Claude | Q4 | TODO |
| D5 | **Mẫu rào chắn M2/M3 theo ngôn ngữ**: chỉ ghi *tiêu chí đạt* (ví dụ "có luật chặn import chéo, chạy trong CI") chứ không dạy cấu hình; Agent tự chọn công cụ | P2 | S | Claude | E1 | TODO |
| D6 | **Profile bổ sung theo nhu cầu thật** (API backend, CLI, mobile, dữ liệu/ML): chỉ viết khi C1/C3 cho thấy Agent chọn sai hoặc thiếu căn cứ | P3 | M | Claude | C1, C3 | HOÃN |
| D7 | **ADR-0013** ghi các quyết định đã chốt: bỏ stack profile, định vị "quyết định và ràng buộc", phạm vi quét an toàn, kênh phát hành exe | P2 | S | Claude | Q1 | TODO |

---

## Quyết định cần maintainer chốt

| ID | Câu hỏi | Lựa chọn | Đề xuất | Chặn việc |
| :-- | :-- | :-- | :-- | :-- |
| Q1 | Phát hành exe bằng cách nào? | (a) commit vào git; (b) GitHub Releases | **ĐÃ CHỐT (b)** ngày 2026-11-05: phát hành qua GitHub (Releases). Nếu ý định là commit nhị phân vào git thì báo lại | A3, D7 |
| Q2 | Có hỗ trợ Health Check dạng đóng gói cho Linux/macOS không? | (a) chỉ Windows + Python cho hệ khác; (b) đóng gói cả ba | **(a)** trước, (b) khi có yêu cầu thật | A5 |
| Q3 | Có đóng gói thành Claude Code plugin không? | (a) có; (b) chưa, chỉ dùng URL repo | **(b)** cho tới khi C1/C2 xong | C6 |
| Q4 | Những tệp Library nào có thể gỡ khỏi repo? (pitch deck, `PLAN.md` lưu trữ; `reference-slides/` và `templates/project-management/` đã xóa 2026-11-08 vì trùng byte với `tu-duy/` và `quan-tri-du-an/raw/`) | giữ hết / chuyển sang repo riêng / xóa | Giữ, chỉ đánh dấu không-đọc; xóa cần maintainer duyệt (theo quy tắc dừng-hỏi) | D4 |
| Q5 | Chạy C1 với Agent nào? | Claude Code, Codex, Antigravity | **ĐÃ CHỐT** ngày 2026-11-05: Claude Code (Claude chạy trong phiên mới) + Antigravity (maintainer chạy). Codex để sau | C1, C3 |

---

## Nhật ký thay đổi kế hoạch
| Ngày | Thay đổi |
| :-- | :-- |
| 2026-11-07 | **Đóng gói Engine cuối cùng, Watchdog 180s, Tiền lọc An toàn & Kiểm chứng Clean-Machine (ADR-0019..0021)**: Chuyển đổi cơ chế vòng đời engine sang heartbeat 2000ms + watchdog 180s (chống treo tiến trình con mồ côi); phân định ranh giới SAFETY_IGNORE_DIRS (22 mục) bảo toàn quét an toàn trên sample/mock; tiền lọc literal directive pre-gate giảm thời gian quét 2x-5x (P-062 từ 28.9s -> 5.9s, litellm từ 69s -> 35.4s) với 100% bảo toàn kết quả phát hiện trên 23 kho; chuẩn hóa Unicode NFC & xử lý ký tự Thổ Nhĩ Kỳ; đóng gói bản build reviewer-engine.exe (9.35 MB) vượt qua kiểm thử máy sạch (A2 DONE) và CDP shell reload giữa chừng (Page.reload ở 5s, 15s và F5 ở 8s trên LiteLLM). Thêm các mục mở rộng E8..E10 và F5..F6. |
| 2026-11-07 | **ADR-0018: Health Check chuyển từ kiểm tra tệp sang phân tích dự án.** Thêm `analysis.py` (ngôn ngữ theo dòng mã, framework theo import thực, đồ thị phụ thuộc, vòng, hướng tầng, loại hình), `knowledge_pack.json` + `build_knowledge_pack.py` (đóng gói sẵn, cập nhật online tùy chọn), `insights.py` (điểm mạnh/nghẽn/đề xuất kèm bằng chứng, đối chiếu ràng buộc profile), mục `1.1 Phân tích dự án` trong báo cáo và tab "Phân tích dự án" trong UI. AI Deep Review nhận Project Model thay vì chỉ điểm, có nút kiểm tra kết nối, tùy chọn gửi mã (che bí mật), lưu `project-review-ai.md`; API key mã hóa DPAPI trên Windows. Sửa nhận diện sai C#/ASP.NET cho repo Python. 134 test pass; **chưa đo độ chính xác trên dự án thật** (brief maintainer handoff 004 (private) giao Antigravity), chưa build lại exe, chưa chạy thử UI/AI bằng key thật. |
| 2026-11-07 | Mở rộng Health Check offline (ADR-0017, `hygiene.py`): `SEC-005` (.env/khóa riêng bị commit), `HYG-002` (log bị commit), `SUP-001..004` (script cài đặt tải từ xa, phụ thuộc không ghim, index ngoài PyPI, nhị phân bị commit), `AGT-004/005` (gói MCP sai/deprecated, npx không ghim), `SPEC-001` (`[NEEDS CLARIFICATION]` còn sót). Chỉ phát hiện, không đổi điểm. 15 test mới. Thử trên 2 repo thật: P-062 báo 30 tệp log bị commit, kit tự báo `.exe` (SUP-004). Chưa làm: F1/F2 (đo báo thừa/bỏ sót SAFE- trên ≥ 20 repo công khai, cần được phép tải), tra CVE, typosquat. |
| 2026-11-07 | Thêm kiểm tra work log (ADR-0016): chuẩn `core/standards/worklog.md` (S-009), mẫu `docs/worklog.md`, Working Rule 12 trong AGENTS.md mẫu; Health Check phát `WLOG-001` (thiếu work log, Trung bình) và `WLOG-002` (có tệp nhưng chưa có mục theo ngày, Thấp), không đổi điểm. 98 test pass (8 test mới). Chưa kiểm: độ mới của mục, tỉ lệ báo thừa trên repo thật. |
| 2026-11-07 | A2 (một phần): chạy test máy không có .NET/Python thật (máy dev, đã gỡ .NET 10 Desktop Runtime). Exe framework-dependent: thoát mã 0x80008083, hộp thoại "You must install .NET Desktop Runtime" (xác nhận). Exe `--self-contained` (52 MB, build bằng SDK portable): chạy, cửa sổ phản hồi, engine `/api/status` ready trên 127.0.0.1, đóng sạch. Chưa kiểm chứng: máy sạch thật, thiếu WebView2, quét từ UI, engine build từ nhánh (báo cáo audit của engine cũ thiếu Mục 0/7/SAFE-001). Sửa `run-test.ps1`: thiếu exe/engine thì báo INVALID, exit 2 thay vì ghi "shell alive: True". Báo cáo: `evals/results/2026-11-07-clean-machine-test.md`. |
| 2026-11-07 | Dashboard Token (H2): trang web cục bộ làm mới 2 giây; kiểm tra bằng trình duyệt thật (desktop, mobile 375px, sáng/tối), sửa trục số lẻ (6.250) và tràn ngang trên mobile; palette 2 màu qua kiểm tra validate_palette (CVD ΔE ≥ 24). 79 test pass. Chỉ Claude Code. |
| 2026-11-07 | Thêm Token Monitor (nhóm H): engine thuần + CLI `--watch`, 15 test. Phát hiện log Claude Code ghi mỗi phản hồi nhiều lần nên cộng thô đếm dư khoảng 2,3 lần; engine loại trùng theo (message.id, requestId) và khớp phép tính độc lập trên phiên thật 114 lượt. Chưa có tab Web/exe, chưa hỗ trợ agent khác. |
| 2026-11-07 | Đo token bằng tokenizer Claude thật (sau `claude auth login`, sửa `measure_docs.py`: tìm `claude` bằng `shutil.which`, tắt skills/MCP để overhead 180 token thay vì 57.543): 9 cặp tài liệu gần song song, tiếng Anh dùng ít hơn khoảng 10% token (2–21%/tệp). Tuyên bố 40–60% bị bác bỏ cho tài liệu của kit. |
| 2026-11-07 | Thêm công cụ đo `measure_docs.py` (private), `bench_health_check.py` (private), `benchmark-plan.md` (private) và kết quả `evals/results/2026-11-07-measurements.md`. Kết quả: tuyên bố "mọi tài liệu < 120 dòng" SAI (5/34 vượt); tiết kiệm 40-60% token CHƯA được chứng minh (proxy cho thấy 0.92x byte, 0.85x từ); Health Check 5.000 tệp tổng hợp trung vị 1,8 s (đạt ngưỡng A2 < 30 s, chỉ trên Python/máy này). |
| 2026-11-07 | Kiểm chứng thực nghiệm: (1) 333/340 URL raw trong MANIFEST trả 200, 7 còn lại là tệp chưa push, không có lỗi trên tệp đã push; (2) rà toạ độ công cụ/MCP bằng npm/PyPI/GitHub API: phát hiện `@modelcontextprotocol/server-playwright` không tồn tại, `server-github` và `server-postgres` đã bị đánh dấu deprecated (archived, "no security guarantees"), `steipete/agent-rules` đã archived; đã thay bằng `@playwright/mcp`, `github/github-mcp-server`, `crystaldba/postgres-mcp`. Việc chưa làm: C1/C3, thử exe trên máy sạch, đo token thực. |
| 2026-11-06 | Tích hợp ưu điểm của GitHub Spec Kit (ADR-0015): thêm `core/standards/feature-workflow.md` (S-008), mẫu `feature-spec.md`/`feature-plan.md`, nâng cấp skill `spec-first-task` (Scale Gate, Clarify, Analyze, converge loop). Việc tiếp theo chưa làm: phát hiện Health Check cho marker `[NEEDS CLARIFICATION]` còn sót / kịch bản thiếu bằng chứng. |
| 2026-11-06 | Hoàn thành nâng cấp **Project Health Check v2.2.0** (A1, A4, E1, E2, E4 DONE): cập nhật `remediation.py` với toàn bộ tài liệu mới (`S-007`, `D-006`, `G-005..007`, `K-001..007`), thêm kiểm tra `ARCH-008` (M1–M3 guardrails), mở rộng `ARCH-007` (`PROFILE_EXPECTATIONS`), ghi `kit_ref`/`guardrail_level` vào `project-review.md`, nâng cấp `server.py` + Web UI đủ 12 trụ cột kèm các tab Mục 0/2/4/7, và đóng gói lại `Project-Health-Check.exe` + `engine/reviewer-engine.exe` (54 test pass; điểm 100/100 do chính công cụ của kit tự đo, chưa thử trên máy Windows sạch). |
| 2026-11-06 | B8 DONE (đã push). B3 DOING: CI đỏ ở `sync_docs.py --check` vì `generate_manifest.py` duyệt thư mục nên số tệp khác giữa máy dev (336/337) và CI (335); đổi sang `git ls-files` để kết quả ổn định, sinh lại README/MANIFEST. Cần push để xác nhận CI xanh. |
| 2026-11-05 | Repo đổi tên thành `Project-Builder-4-Agents` (B1 DONE). Đã thay `Project-Builder-Kit` và URL `Project-Starter-Kit` trong 22 tệp. Còn B8 (push) trước khi chạy C1 bằng URL. |
| 2026-11-05 | Chốt Q1 (GitHub Releases) và Q5 (Claude Code + Antigravity). Thêm C0 (kịch bản, DONE), C7, B8 (push); C1 phụ thuộc B1 + B8 vì Agent cần lấy kit qua URL. |
| 2026-11-05 | Lập kế hoạch lần đầu sau commit `a8ba04d`. Đã hoàn thành trước đó (không liệt kê lại): tái cấu trúc Core/Profiles/Library, `project-review.md`, quét an toàn (Mục 0), phạm vi quét (Mục 7), khuôn tài liệu + kiểm tra tự động, bảng chọn kiểu dự án. |
