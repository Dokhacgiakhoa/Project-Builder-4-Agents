/* Lightweight i18n. English strings are the keys (and the default); other languages map key -> text.
   t("English text {name}", {name: value}). Static HTML: leaf elements whose text equals a key are translated
   automatically (title/placeholder too); mixed markup uses data-i18n-html="<English html>". */
(function () {
  const DICT = { vi: {
 "CRITICAL": "NGUY HIỂM",
 "CRITICAL RISK": "LỖI NGUY HIỂM",
 "RED ALARM: {n} High-Severity Risk": "BÁO ĐỘNG ĐỎ: {n} LỖI NGUY HIỂM",
 "Quality Gate Passed": "Đạt chuẩn an toàn (Quality Gate Passed)",
 "Contains critical issue": "Chứa lỗi nguy hiểm mức Cao",
 "•••••••• (saved — leave blank to keep)": "•••••••• (đã lưu — để trống để giữ nguyên)",
 "Enter API Key": "Nhập API Key",
 "Settings saved.": "Cấu hình đã được lưu thành công.",
 "Could not save settings: ": "Lỗi lưu cấu hình: ",
 "Connection error while saving settings: ": "Lỗi kết nối lưu cấu hình: ",
 "Run a deep architecture review with Senior Architect AI": "Kích hoạt phân tích kiến trúc chuyên sâu bằng Senior Architect AI",
 "Configure an API Key in Settings (top right) to enable AI Review": "Cần cấu hình API Key trong Cài đặt (góc trên bên phải) để kích hoạt AI Review",
 "Enter an API Key in Settings > API Keys to enable AI Deep Review.": "Vui lòng nhập API Key trong Cài đặt > API Key để kích hoạt tính năng AI Deep Review.",
 "Select a project folder before running a review.": "Vui lòng chọn thư mục dự án trước khi thực hiện Review.",
 "Running Analytics first to collect audit data for the AI...": "Đang chạy Analytics trước để thu thập dữ liệu thẩm định cho AI...",
 "Running Health Check first to collect audit data for the AI...": "Đang chạy Health Check trước để thu thập dữ liệu thẩm định cho AI...",
 "Audit stages ({count} pillars)": "Các chặng đo kiểm tiêu chuẩn ({count} Hạng mục)",
 "not measured": "chưa đo",
 "{n} pts": "{n}đ",
 "Measured": "Đã đo",
 "Measuring…": "Đang đo…",
 "Queued": "Chờ đo",
 "Project: {dir}": "Dự án: {dir}",
 "Auditing source architecture...": "Đang thẩm định kiến trúc mã nguồn...",
 "Scanning...": "Đang quét...",
 "Detecting project architecture to decide which pillars to measure...": "Đang nhận diện kiến trúc dự án để xác định các hạng mục sẽ đo...",
 "Audit stages": "Các chặng đo kiểm tiêu chuẩn",
 "Initializing audit modules...": "Đang khởi tạo các module kiểm tra...",
 "Starting": "Khởi động",
 "Folder selected: {path}": "Đã chọn thư mục: {path}",
 "Opening the Windows folder picker...": "Đang mở hộp thoại chọn thư mục Windows...",
 "Folder selection cancelled.": "Đã hủy chọn thư mục.",
 "Could not open the folder picker: ": "Lỗi khi mở hộp thoại chọn thư mục: ",
 "Select the project folder to audit.": "Vui lòng chọn thư mục dự án cần kiểm tra.",
 "Auditing...": "Đang thẩm định...",
 "Measuring source architecture...": "Đang đo kiểm kiến trúc mã nguồn...",
 "Starting the Universal Project Auditor engine...": "Khởi động bộ máy đo kiểm Universal Project Auditor...",
 "Scanning configuration files at: {dir}": "Khảo sát tệp tin cấu hình tại: {dir}",
 "Audit error: {msg}": "Lỗi đo kiểm: {msg}",
 "Failed: {msg}": "Thất bại: {msg}",
 "ERROR": "LỖI",
 "Analytics error: ": "Lỗi Analytics: ",
 "Health Check error: ": "Lỗi Health Check: ",
 "Audit failed.": "Đo kiểm thất bại.",
 "Backend connection error: {msg}": "Lỗi kết nối Backend: {msg}",
 "Connection error: {msg}": "Lỗi kết nối: {msg}",
 "Connection error.": "Lỗi kết nối.",
 "Checking...": "Đang kiểm tra...",
 "Scan session lost.": "Mất phiên quét.",
 "✓ Audit complete! Total score: {score}/100": "✓ Hoàn tất đo kiểm toàn diện! Tổng điểm: {score}/100",
 "DONE 100%": "XONG 100%",
 "Architecture audit finished ({score}/100)": "Đã hoàn tất đo kiểm kiến trúc ({score}/100)",
 "Done": "Hoàn tất",
 "Audit complete! Total score: {score}/100 [Grade {grade}]": "Hoàn tất đo kiểm toàn diện! Tổng điểm: {score}/100 [Hạng {grade}]",
 "Analytics complete! Score: {score}/100.": "Hoàn tất Analytics! Điểm: {score}/100.",
 "Health Check complete! Score: {score}/100.": "Hoàn tất Health Check! Điểm: {score}/100.",
 "Source code standard violation": "Vi phạm quy chuẩn mã nguồn",
 "No source violations or Anti-Crash issues found.": "Không phát hiện vi phạm mã nguồn hoặc lỗi Anti-Crash.",
 "Found": "Phát hiện",
 "across": "thuộc",
 "{n} violating locations": "{n} vị trí vi phạm",
 "{n} standard architecture issue types": "{n} loại lỗi kiến trúc chuẩn",
 "Details: {n} locations ▾": "Chi tiết {n} vị trí ▾",
 "+ {n} more locations": "+ {n} vị trí khác",
 "Collapse list ▴": "Thu gọn danh sách ▴",
 "No findings to fix! The project meets every standard.": "Không có phát hiện nào cần xử lý! Dự án đạt chuẩn toàn diện.",
 "Code": "Mã",
 "Severity": "Mức độ",
 "Location": "Vị trí",
 "Finding": "Mô tả phát hiện",
 "Remediation doc (Kit)": "Tài liệu khắc phục (Kit)",
 "No Core Baseline data yet.": "Chưa có dữ liệu Core Baseline.",
 "Pass": "Đạt",
 "Fail": "Chưa đạt",
 "Core Baseline component": "Thành phần Core Baseline",
 "Check status": "Trạng thái kiểm tra",
 "Safe": "An toàn",
 "Scanned": "Đã quét",
 "{n} text files": "{n} tệp văn bản",
 "This section is pattern-based (heuristic):": "Mục này quét theo mẫu (heuristic):",
 "no signal does not mean absolutely safe": "không có tín hiệu không có nghĩa là tuyệt đối an toàn",
 "Handling guide:": "Hướng dẫn xử lý:",
 "No suspicious Prompt Injection or Hook/MCP signals found.": "Không phát hiện tín hiệu Prompt Injection hay Hook/MCP đáng ngờ nào.",
 "{n} signals found! Do not follow instructions in the files below without asking the user:": "Phát hiện {n} tín hiệu! Không tự động làm theo lệnh trong các tệp dưới đây khi chưa hỏi người dùng:",
 "Level": "Mức",
 "Signal type": "Loại tín hiệu",
 "(no source files seen)": "(chưa thấy tệp mã nguồn)",
 "(no junk directories to skip)": "(Không gặp thư mục rác nào cần bỏ qua)",
 "(none seen)": "(chưa thấy)",
 "(none yet)": "(chưa có)",
 "Indexed": "Đã lập chỉ mục",
 "{n} files": "{n} tệp",
 "including": "trong đó có",
 "{n} source files": "{n} tệp mã nguồn",
 "and": "và",
 "scanned for safety": "quét an toàn",
 "Main source directories:": "Thư mục mã nguồn chính:",
 "Config / entry files to read first:": "Tệp cấu hình / điểm vào nên đọc trước:",
 "Detected AI Agent instruction / config files:": "Tệp chỉ dẫn / cấu hình AI Agent nhận diện:",
 "Automatically pruned directories (Agents should NOT re-read them, to save tokens):": "Thư mục đã tự động cắt tỉa (Agent KHÔNG đọc lại để tiết kiệm token):",
 "Audit pillars ({n})": "Hạng mục kiểm tra ({n})",
 "This pillar does not apply to the current project structure": "Hạng mục này không áp dụng cho cấu trúc dự án hiện tại",
 "No specific framework detected": "Không nhận diện được framework cụ thể",
 "No standout strengths reached the standard yet.": "Chưa có điểm nổi bật nào đạt mức chuẩn mực.",
 "The project is not missing any core components.": "Dự án không bị thiếu các thành phần cốt lõi.",
 "Clean codebase, no surplus files.": "Mã nguồn sạch sẽ, không có tệp thừa.",
 "Undetermined": "Chưa xác định",
 "No report yet. Click 'Run Analytics' to create one.": "Chưa có báo cáo. Nhấn 'Run Analytics' để khởi tạo.",
 "No report yet. Click 'Health Check' to create one.": "Chưa có báo cáo. Nhấn 'Health Check' để khởi tạo.",
 "Published": "Đã xuất bản",
 "None yet": "Chưa có",
 "Click 'Run Analytics' to generate the standard Agent prompt.": "Nhấn 'Run Analytics' để sinh prompt chuẩn cho Agent.",
 "Click 'Health Check' to generate the standard Agent prompt.": "Nhấn 'Health Check' để sinh prompt chuẩn cho Agent.",
 "There is no report file path to copy yet.": "Chưa có tệp báo cáo để sao chép đường dẫn.",
 "Copied!": "Đã sao chép!",
 "Copy path": "Sao chép đường dẫn",
 "Security & Supply Chain": "Bảo Mật & Chuỗi Cung Ứng",
 "Cloud Infrastructure & DevOps": "Hạ Tầng Cloud & DevOps",
 "Distributed Systems & Gateway": "Hệ Thống Phân Tán & Gateway",
 "Data Engineering & Cache": "Kỹ Thuật Dữ Liệu & Cache",
 "Monitoring & Operations": "Giám Sát & Vận Hành",
 "AI Agent Ecosystem (Rules, Skills & Workflows)": "Hệ Sinh Thái AI Agent (Rules, Skills & Workflows)",
 "Architecture Records & API Contracts": "Hồ Sơ Kiến Trúc & Hợp Đồng API",
 "Detailed audit against the Project-Builder-4-Agents standards": "Thẩm định chi tiết theo chuẩn mực Project-Builder-4-Agents",
 "No audit data yet.": "Chưa có dữ liệu đo kiểm.",
 "N/A (Not applicable)": "N/A (Không áp dụng)",
 "No mandatory requirements or failed criteria.": "Không có yêu cầu bắt buộc hay tiêu chí chưa đạt.",
 "No criteria recorded as met yet.": "Chưa có tiêu chí nào được ghi nhận hoàn tất.",
 "All criteria of this pillar are met.": "Đã đáp ứng đầy đủ tất cả tiêu chí của hạng mục này.",
 "Copy Prompt": "Sao chép Prompt",
 "Run Analytics before asking the AI to analyze.": "Vui lòng chạy Analytics trước khi yêu cầu AI phân tích.",
 "Run Health Check before asking the AI to analyze.": "Vui lòng chạy Health Check trước khi yêu cầu AI phân tích.",
 "⏳ Connecting to AI...": "⏳ Đang kết nối AI...",
 "Sending audit data to Senior Architect AI for analysis...": "Đang gửi dữ liệu đo kiểm và yêu cầu Senior Architect AI phân tích...",
 "Saved:": "Đã lưu:",
 "Error:": "Lỗi:",
 "AI connection error:": "Lỗi kết nối AI:",
 "✨ Analyze With AI": "✨ Phân Tích Bằng AI",
 "Checking GitHub for a new version...": "Đang kiểm tra phiên bản mới từ GitHub...",
 "New version available:": "Đã có phiên bản mới:",
 "Your current version:": "Phiên bản hiện tại của bạn:",
 "View Release on GitHub": "Xem Bản Phát Hành Trên GitHub",
 "You are on the latest version!": "Bạn đang sử dụng phiên bản mới nhất!",
 "Current version:": "Phiên bản hiện tại:",
 "Could not check for updates:": "Không thể kiểm tra cập nhật:",
 "No analysis data for this scan.": "Không có dữ liệu phân tích cho lượt quét này.",
 "None.": "Không có.",
 "pass": "đạt",
 "violated": "vi phạm",
 "needs confirmation": "cần xác nhận",
 "Summary": "Tóm tắt",
 "Languages": "Ngôn ngữ",
 "Language": "Ngôn ngữ",
 "Lines of code": "Dòng mã",
 "Files": "Tệp",
 "Share": "Tỷ lệ",
 "Components & dependencies": "Thành phần & phụ thuộc",
 "Component": "Thành phần",
 "Depends on": "Phụ thuộc vào",
 "Used by": "Được dùng bởi",
 "Comparison with the kit architecture profile": "Đối chiếu profile kiến trúc của kit",
 "Fits when:": "Phù hợp khi:",
 "Does not fit when:": "Không phù hợp khi:",
 "Strengths": "Điểm mạnh",
 "Bottlenecks": "Điểm nghẽn",
 "Prioritized recommendations": "Đề xuất theo ưu tiên",
 "Profile constraint check": "Đối chiếu ràng buộc của profile",
 "Source": "Nguồn",
 "Constraint": "Ràng buộc",
 "Result": "Kết quả",
 "Evidence": "Bằng chứng",
 "Kit knowledge:": "Tri thức kit:",
 "build": "bản",
 "{n} docs": "{n} tài liệu",
 "Could not reach the local server: ": "Không kết nối được máy chủ nội bộ: ",
 "Downloading...": "Đang tải...",
 "Select or paste the project folder path...": "Chọn hoặc nhập đường dẫn thư mục dự án...",
 "Choose a folder on this computer": "Chọn thư mục từ máy tính",
 "Browse": "Duyệt",
 "Run the full standards audit (zero-token, offline)": "Chạy thẩm định tiêu chuẩn toàn diện (Zero-Token, Offline)",
 "Configure an API Key in Settings to enable AI Review": "Cần cấu hình API Key trong Cài đặt để kích hoạt AI Review",
 "Switch Light / Dark theme": "Đổi giao diện Sáng / Tối",
 "Check for updates": "Kiểm tra cập nhật",
 "Settings": "Cài đặt",
 "Overview report": "Báo cáo tổng quan",
 "Audit pillars (12)": "Hạng mục kiểm tra (12)",
 "AI Agent Ecosystem": "Hệ Sinh Thái AI Agent",
 "Report & AI Prompt": "Báo cáo & Prompt AI",
 "Scan history": "Lịch sử quét",
 "Project: --": "Dự án: --",
 "audit-runtime.log — Scan activity log": "audit-runtime.log — Nhật ký quá trình quét",
 "[00:00:00] Ready to scan.": "[00:00:00] Sẵn sàng quét mã nguồn.",
 "Audit complete! Total score: --/100": "Hoàn tất đo kiểm toàn diện! Tổng điểm: --/100",
 "View Overview Results": "Xem Kết Quả Tổng Quan",
 "PROJECT TOTAL SCORE": "TỔNG ĐIỂM DỰ ÁN",
 "Project type:": "Loại hình:",
 "Architecture & Profile:": "Kiến trúc & Profile:",
 "Overview": "Tổng quan",
 "Project analysis": "Phân tích dự án",
 "Findings & Fixes (<span": "Phát hiện & Khắc phục (<span",
 "Core Baseline (<span": "Core Baseline (<span",
 "Safety & Scope (<span": "An toàn & Phạm vi (<span",
 "Gaps & Clutter (<span": "Thiếu sót & Rác (<span",
 "Source violations (<span": "Vi phạm mã nguồn (<span",
 "Tech profile & Kit configuration": "Hồ sơ công nghệ & Cấu hình Kit",
 "Auto-detected from configs, dependencies and `.builder/kit.json`:": "Tự động nhận diện qua cấu hình, dependencies và `.builder/kit.json`:",
 "No data yet": "Chưa có dữ liệu",
 "Architecture strengths": "Điểm mạnh kiến trúc",
 "Standards and good practices already met:": "Các tiêu chuẩn và điểm sáng tạo đã đạt chuẩn mực:",
 "Findings to fix (Section 2 — Actionable Findings)": "Danh sách phát hiện cần xử lý (Mục 2 — Actionable Findings)",
 "Sorted by priority High → Medium → Low, with direct links to the remediation docs in Project-Builder-4-Agents:": "Sắp xếp theo thứ tự ưu tiên Cao → Trung bình → Thấp kèm liên kết trực tiếp tới tài liệu khắc phục trong Project-Builder-4-Agents:",
 "Core Baseline B1–B9 (Section 4 — Mandatory for every Agent repo)": "Core Baseline B1–B9 (Mục 4 — Chuẩn bắt buộc cho mọi repo dùng Agent)",
 "0. Safety warnings (Prompt Injection)": "0. Cảnh báo an toàn (Prompt Injection)",
 "No safety scan data yet.": "Chưa có dữ liệu quét an toàn.",
 "7. Audit Scope": "7. Phạm vi quét (Audit Scope)",
 "Tells AI Agents the main directories, the generated directories to skip and the entry points to read first:": "Giúp AI Agent biết thư mục chính, các thư mục sinh tự động cần bỏ qua và điểm vào nên đọc trước:",
 "No audit scope data yet.": "Chưa có dữ liệu phạm vi quét.",
 "Criteria met": "Tiêu chí đã đạt",
 "No data yet.": "Chưa có dữ liệu.",
 "Criteria not met": "Tiêu chí chưa đạt",
 "Specific source violations": "Vi phạm mã nguồn cụ thể",
 "Architecture standards not met": "Tiêu chuẩn kiến trúc chưa đạt",
 "Surplus files & Security risks": "Tệp tin thừa & Rủi ro bảo mật",
 "No analysis data yet. Run Analytics.": "Chưa có dữ liệu phân tích. Hãy chạy Analytics.",
 "No analysis data yet. Run Health Check.": "Chưa có dữ liệu phân tích. Hãy chạy Health Check.",
 "No violation data yet.": "Chưa có dữ liệu vi phạm.",
 "Report Files & AI Agent Prompt": "Hồ Sơ Báo Cáo & Prompt AI Agent",
 "Manage the project-review.md technical report and the standard refactoring prompt for AI.": "Quản lý tệp báo cáo kỹ thuật project-review.md và bộ prompt tái cấu trúc chuẩn hóa cho AI.",
 "Ready": "Sẵn sàng",
 "File path:": "Đường dẫn tệp:",
 "No report yet": "Chưa có báo cáo",
 "Technical report with safety warnings (Section 0), findings with remediation docs (Section 2), 12-pillar scores (Section 3), Core Baseline B1–B9 (Section 4) and audit scope (Section 7).": "Bản báo cáo kỹ thuật độc quyền gồm Cảnh báo an toàn (Mục 0), Phát hiện kèm tài liệu khắc phục (Mục 2), Điểm 12 hạng mục (Mục 3), Core Baseline B1–B9 (Mục 4) và Phạm vi quét (Mục 7).",
 "Open Markdown report": "Mở báo cáo Markdown",
 "Open report folder": "Mở thư mục báo cáo",
 "Project Refactoring Prompt (Architect Refactor)": "Prompt Tái Cấu Trúc Dự Án (Architect Refactor)",
 "Deep Review From a Senior Architect AI": "Đánh Giá Chuyên Sâu Từ Senior Architect AI",
 "Overall architecture analysis, refactoring options and an optimization roadmap from an LLM.": "Phân tích kiến trúc tổng thể, chỉ ra giải pháp refactor và lộ trình tối ưu hoá với LLM.",
 "Re-analyze with AI": "Phân tích lại bằng AI",
 "Enter an API Key in Settings > API Keys (top right), then click '✨ AI Deep Review' in the title bar.": "Nhập API Key trong Cài đặt (góc trên bên phải), sau đó nhấn '✨ AI Deep Review' trên thanh tiêu đề.",
 "Checking GitHub...": "Đang kiểm tra từ GitHub...",
 "Close": "Đóng",
 "Ready. Click <strong>Run Analytics</strong> to scan the source code.": "Sẵn sàng kiểm tra. Nhấn <strong>Run Analytics</strong> để quét mã nguồn.",
 "Ready. Click <strong>Health Check</strong> to scan the source code.": "Sẵn sàng kiểm tra. Nhấn <strong>Health Check</strong> để quét mã nguồn.",
 "9 foundation components independent of language or architecture style, per <code>core/README.md</code> (K-003):": "9 thành phần nền tảng không phụ thuộc ngôn ngữ hay kiểu kiến trúc theo tài liệu <code>core/README.md</code> (K-003):",
 "Scans text files (md, json, html, txt, yaml...) for hidden directives, zero-width characters and command-running hooks/MCP (<code>SAFE-001</code>..<code>SAFE-005</code>):": "Quét tệp văn bản (md, json, html, txt, yaml...) tìm lệnh ẩn, ký tự zero-width và hook/MCP thực thi lệnh (<code>SAFE-001</code>..<code>SAFE-005</code>):",
 "Use this prompt with <strong>Claude Code, Antigravity, Cursor or Codex</strong> so the Agent reads <code>project-review.md</code> and fixes issues using the remediation docs in <strong>Project-Builder-4-Agents</strong>:": "Sử dụng prompt này cho <strong>Claude Code, Antigravity, Cursor hoặc Codex</strong> để chỉ dẫn Agent đọc <code>project-review.md</code> và tự sửa lỗi theo tài liệu khắc phục trong <strong>Project-Builder-4-Agents</strong>:",
 "Appearance": "Giao diện",
 "API Keys": "API Key",
 "User Guide": "Hướng dẫn sử dụng",
 "About & Version": "Thông tin & Phiên bản",
 "Choose how the interface looks. The change previews instantly and is stored when you press Save.": "Chọn giao diện hiển thị. Thay đổi được xem trước ngay và chỉ lưu khi bạn bấm Lưu.",
 "Run Analytics": "Chạy Analytics",
 "Theme": "Giao diện (Theme)",
 "Dark (Slate)": "Tối (Dark Slate)",
 "Light (Studio)": "Sáng (Studio Light)",
 "Midnight (OLED)": "Đen sâu (Midnight OLED)",
 "Dracula Purple": "Tím Dracula (Synthwave)",
 "Tokyo Night": "Đêm Tokyo (Tokyo Night)",
 "Nord Frost": "Băng Bắc Cực (Nord Frost)",
 "Emerald Matrix": "Xanh Ma Trận (Emerald Pine)",
 "Warm Sepia": "Giấy Ấm (Warm Sepia)",
 "Antigravity default": "Mặc định Antigravity",
 "Clean studio light": "Sáng hiện đại, tối giản",
 "Pitch black high contrast": "Đen tuyền OLED, siêu nét",
 "Cyberpunk violet tone": "Tông tím than cá tính",
 "Modern deep indigo": "Xanh chàm phong cách Tokyo",
 "Soothing arctic slate": "Xám xanh dịu mắt, êm ái",
 "Deep forest hacker pine": "Xanh rừng thông hacker",
 "Eye-comfort reading tone": "Màu giấy ngà dịu mắt",
 "Interface language. English is the default. Report content produced by the audit engine may still appear in its original language.": "Ngôn ngữ giao diện. Mặc định là tiếng Anh. Nội dung báo cáo do bộ máy đo kiểm sinh ra có thể vẫn hiển thị bằng ngôn ngữ gốc.",
 "Interface language": "Ngôn ngữ giao diện",
 "Only needed for the optional AI Deep Review. Health Check itself runs fully offline. Keys are stored encrypted for your Windows account and are never sent back to this page.": "Chỉ cần cho AI Deep Review (tùy chọn). Health Check tự chạy hoàn toàn offline. Khóa được mã hóa theo tài khoản Windows của bạn và không bao giờ gửi ngược lại trang này.",
 "AI provider (LLM Provider)": "Nhà cung cấp AI (LLM Provider)",
 "API Key": "API Key",
 "Model name": "Tên Model",
 "Test connection": "Kiểm tra kết nối",
 "Send snippets of the largest files to the AI (secrets masked)": "Gửi kèm đoạn mã của các tệp lớn nhất cho AI (đã che bí mật)",
 "By default only the analysis model (structure, dependencies) is sent, never source code. AI Deep Review needs the Internet; Health Check normally runs fully offline.": "Mặc định chỉ gửi mô hình phân tích (cấu trúc, phụ thuộc), không gửi mã. AI Deep Review cần Internet; Health Check thường chạy hoàn toàn offline.",
 "<strong>Pick a project.</strong> Click <em>Browse</em> or paste the project folder path in the top bar.": "<strong>Chọn dự án.</strong> Bấm <em>Duyệt</em> hoặc dán đường dẫn thư mục dự án vào thanh phía trên.",
 "<strong>Run Analytics.</strong> It scans files locally and offline, with no model calls. Large repositories can take up to a minute.": "<strong>Chạy Analytics.</strong> Công cụ quét tệp ngay trên máy, offline, không gọi mô hình AI. Repo lớn có thể mất tới một phút.",
 "<strong>Run Health Check.</strong> It scans files locally and offline, with no model calls. Large repositories can take up to a minute.": "<strong>Chạy Health Check.</strong> Công cụ quét tệp ngay trên máy, offline, không gọi mô hình AI. Repo lớn có thể mất tới một phút.",
 "<strong>Read the Overview.</strong> The total score, project type and the tabs (Findings & Fixes, Core Baseline, Safety & Scope, Gaps & Clutter, Source violations) explain what is wrong.": "<strong>Đọc phần Tổng quan.</strong> Tổng điểm, loại dự án và các tab (Phát hiện & Khắc phục, Core Baseline, An toàn & Phạm vi, Thiếu sót & Rác, Vi phạm mã nguồn) cho biết dự án đang có vấn đề gì.",
 "<strong>Fix by priority.</strong> Each finding links to a remediation document in the kit; the documents are read online, nothing else is downloaded.": "<strong>Sửa theo mức ưu tiên.</strong> Mỗi phát hiện có liên kết tới tài liệu khắc phục trong kit; tài liệu được đọc trực tuyến, không tải thêm gì khác.",
 "<strong>Hand it to your Agent.</strong> Open <em>Report & AI Prompt</em>, then copy the prompt into Claude Code, Antigravity, Cursor or Codex together with <code>project-review.md</code>.": "<strong>Giao cho Agent của bạn.</strong> Mở <em>Báo cáo & Prompt AI</em>, rồi sao chép prompt vào Claude Code, Antigravity, Cursor hoặc Codex cùng với <code>project-review.md</code>.",
 "<strong>Optional AI Deep Review.</strong> Add an API key under <em>Settings > API Keys</em>, then click <em>AI Deep Review</em> in the top bar.": "<strong>AI Deep Review (tùy chọn).</strong> Thêm API key tại <em>Cài đặt > API Key</em>, sau đó bấm <em>AI Deep Review</em> trên thanh phía trên.",
 "<strong>Command line.</strong> The same single file works headless: <code>Project-Builder-Analytics.exe audit C:\\path\\to\\project</code>.": "<strong>Dòng lệnh.</strong> Chính file duy nhất này chạy được không giao diện: <code>Project-Builder-Analytics.exe audit C:\\path\\to\\project</code>.",
 "Tip: a heuristic scan can miss issues and can flag false positives, so treat the score as a guide, not a verdict.": "Lưu ý: quét theo mẫu (heuristic) có thể bỏ sót hoặc báo nhầm, hãy xem điểm số như gợi ý chứ không phải phán quyết.",
 "Product": "Sản phẩm",
 "Version": "Phiên bản",
 "Mode": "Chế độ",
 "Static audit, offline, no model calls": "Quét tĩnh, offline, không gọi mô hình AI",
 "Settings file": "Tệp cấu hình",
 "Project": "Dự án",
 "Update kit knowledge (needs Internet)": "Cập nhật tri thức kit (cần Internet)",
 "Cancel": "Hủy",
 "Save settings": "Lưu cài đặt",
 "Updating...": "Đang cập nhật...",
 "Connection OK": "Kết nối thành công",
 "Unknown": "Không rõ"
} };

  const VI_TO_EN = {
    // Project Types & Archetypes
    "Kho tài liệu / tri thức": "Documentation / Knowledge base",
    "Kho tài liệu / tri thức kèm công cụ": "Documentation / Knowledge base with tools",
    "Ứng dụng web full-stack": "Full-stack web application",
    "Dịch vụ backend / API": "Backend / API service",
    "Ứng dụng giao diện web": "Web frontend application",
    "Ứng dụng desktop": "Desktop application",
    "Dự án dữ liệu / AI": "Data / AI project",
    "Công cụ dòng lệnh / script": "Command-line tool / script",
    "Thư viện / mã chưa rõ điểm vào": "Library / unspecified entrypoint",
    "Chưa xác định": "Undetermined",

    // Architectures & Styles
    "Kiến trúc phân tầng kiểu Clean / Hexagonal": "Clean / Hexagonal Layered Architecture",
    "Monolith theo module": "Modular Monolith",
    "Vertical slice (theo tính năng)": "Vertical Slice (Feature-driven)",
    "Phân tầng đơn giản (presentation → service → data)": "Simple Layered (presentation → service → data)",
    "Cấu trúc phẳng (ít thành phần)": "Flat structure (minimal components)",
    "Các thành phần theo thư mục, chưa có tầng rõ ràng": "Component-based without explicit layering",

    // Core Baseline Components (B1-B9)
    "AGENTS.md (chỉ dẫn Agent)": "AGENTS.md (Agent instructions)",
    "Lớp tương thích Agent (CLAUDE.md + skills)": "Agent compatibility layer (CLAUDE.md + skills)",
    "docs/project-brief.md": "docs/project-brief.md",
    "Nhật ký quyết định (adrs/ có ADR thật)": "Decision records (adrs/ with real ADRs)",
    "Chuẩn làm việc (docs/standards/)": "Working standards (docs/standards/)",
    "Lệnh kiểm chứng đã điền + CI chạy được": "Verification commands filled + CI operational",
    "Vệ sinh repo (.gitignore, .env.example)": "Repo hygiene (.gitignore, .env.example)",
    "Hồ sơ kit (.builder/kit.json)": "Kit profile (.builder/kit.json)",
    "Quy trình PR (PULL_REQUEST_TEMPLATE)": "PR workflow (PULL_REQUEST_TEMPLATE)",

    // Core Baseline Details / Failures
    "Thiếu AGENTS.md": "Missing AGENTS.md",
    "Thiếu CLAUDE.md": "Missing CLAUDE.md",
    "Thiếu skills (.agents/skills hoặc .claude/skills có */SKILL.md)": "Missing skills (.agents/skills or .claude/skills with */SKILL.md)",
    "Thiếu docs/project-brief.md": "Missing docs/project-brief.md",
    "Chưa có ADR nào ngoài mẫu": "No real ADRs beyond templates",
    "Thiếu docs/standards/coding-conventions.md hoặc definition-of-done.md": "Missing docs/standards/coding-conventions.md or definition-of-done.md",
    "AGENTS.md còn {{PLACEHOLDER}}": "AGENTS.md still contains {{PLACEHOLDER}}",
    "Thiếu workflow CI trong .github/workflows/": "Missing CI workflow in .github/workflows/",
    "Thiếu .gitignore hoặc .env.example": "Missing .gitignore or .env.example",
    "Thiếu .builder/kit.json": "Missing .builder/kit.json",
    "Thiếu .github/PULL_REQUEST_TEMPLATE.md": "Missing .github/PULL_REQUEST_TEMPLATE.md",

    // Strengths (Innovations)
    "Trang bị hạ tầng VECTOR DATABASE sẵn sàng cho AI RAG & SEMANTIC SEARCH.": "Equipped with VECTOR DATABASE infrastructure ready for AI RAG & SEMANTIC SEARCH.",
    "Cấu hình DISTRIBUTED CACHE với REDIS tối ưu tốc độ phản hồi.": "Configured DISTRIBUTED CACHE with REDIS for low latency.",
    "Tự động hóa QUALITY GATE & CI/CD PIPELINE với GITHUB ACTIONS.": "Automated QUALITY GATE & CI/CD PIPELINE with GITHUB ACTIONS.",
    "Chuẩn hóa môi trường phát triển nhất quán với DOCKER COMPOSE.": "Standardized consistent dev environment with DOCKER COMPOSE.",
    "Hệ thống DESIGN SYSTEM & UI TOKENS độc quyền được thiết kế bài bản.": "Structured DESIGN SYSTEM & UI TOKENS architecture implemented.",
    "Bảo vệ chuỗi cung ứng mã nguồn chặt chẽ qua DEPENDENCY LOCKFILE.": "Supply chain security protected via DEPENDENCY LOCKFILE.",
    "Chuẩn hóa hệ sinh thái AI AGENT (HIẾN PHÁP AGENTS.MD, SKILLS & WORKFLOWS) đón đầu kỷ nguyên Agentic AI.": "Standardized AI AGENT ecosystem (AGENTS.MD, SKILLS & WORKFLOWS).",
    "Tự động hóa đồng bộ TÀI LIỆU SỐNG (4-LAYER LIVING DOCUMENTATION & DRIFT-CONTROL PIPELINE).": "Automated LIVING DOCUMENTATION (4-Layer Drift-Control Pipeline).",

    // Gaps & Bloat
    "Dự án chưa có tệp `.gitignore` để loại trừ các tệp tạm và artifacts BUILD.": "Project lacks a `.gitignore` file to exclude temporary files and build artifacts.",
    "Sạch sẽ, không phát hiện tệp rác hay rủi ro bảo mật tệp cấu hình.": "Clean codebase, no surplus files or sensitive config risks.",
    "Clean codebase, no surplus files.": "Sạch sẽ, không phát hiện tệp rác hay rủi ro bảo mật tệp cấu hình.",

    // Pillar Criteria Met / Unmet
    "Phân định ranh giới rõ ràng giữa DOMAIN, APPLICATION và INFRASTRUCTURE": "Clear separation of DOMAIN, APPLICATION and INFRASTRUCTURE boundaries",
    "Cấu trúc module độc lập theo FEATURE-DRIVEN ARCHITECTURE": "Independent module structure following FEATURE-DRIVEN ARCHITECTURE",
    "Phân tách cơ bản giữa tầng PRESENTATION và BUSINESS LOGIC": "Basic separation between PRESENTATION and BUSINESS LOGIC layers",
    "Đã xác minh tổ chức mã nguồn theo từng Feature/Module độc lập cô lập.": "Verified independent isolated Feature/Module code organization.",
    "Đã xác minh phân định giữa tầng hiển thị/API và tầng xử lý nghiệp vụ.": "Verified separation between presentation/API and business logic layers.",
    "Toàn bộ mã nguồn nằm lẫn lộn trong cùng thư mục hoặc thiếu phân tầng rõ rệt giữa nghiệp vụ cốt lõi và hạ tầng.": "Source files mixed in same directories or lacking clear layering between core business and infrastructure.",
    "Tổ chức lại thư mục theo chuẩn phân tầng (domain/core, services, controllers/routes).": "Reorganize folders by architectural layers (domain/core, services, controllers/routes).",
    "Độ thuần khiết của DOMAIN và ranh giới CONTROLLER được bảo vệ hoàn hảo (0 LAYER LEAKS)": "DOMAIN purity and CONTROLLER boundaries protected (0 Layer Leaks)",
    "Không phát hiện bất kỳ controller nào gọi truy vấn SQL trực tiếp hoặc domain bị dính framework.": "No controllers execute direct SQL queries or bind domain to frameworks.",
    "Áp dụng DEPENDENCY INJECTION (DI) tiêm phụ thuộc tường minh": "Explicit DEPENDENCY INJECTION (DI) applied",
    "Đã phát hiện áp dụng kỹ thuật tiêm phụ thuộc (DI / IoC) giúp mã nguồn module hóa và dễ viết Unit Test.": "Detected Dependency Injection (DI/IoC) usage for modularity and testability.",
    "Xác thực dữ liệu đầu vào DTO tự động (ZOD / PYDANTIC / CLASS-VALIDATOR)": "Automated DTO input validation (Zod / Pydantic / Class-Validator)",
    "100% dữ liệu đầu vào từ API Request được kiểm tra tính hợp lệ qua schema DTO trước khi xử lý.": "100% API request input data validated via DTO schemas prior to processing.",
    "Cơ chế giải phóng kết nối và tài nguyên khi tắt SERVER (GRACEFUL SHUTDOWN)": "Graceful resource release and cleanup on SERVER shutdown (GRACEFUL SHUTDOWN)",
    "Chưa có cơ chế xử lý tín hiệu SIGTERM/SIGINT để giải phóng kết nối DB và dừng server mà không làm rớt request đang dở dang.": "Lacks SIGTERM/SIGINT signal handling to release DB connections and stop server without dropping in-flight requests.",
    "Bổ sung hàm lắng nghe SIGTERM/SIGINT đóng gracefully các pool kết nối cơ sở dữ liệu và server.": "Add SIGTERM/SIGINT signal listeners to gracefully close database connection pools and server instances.",
    "Thiếu cấu trúc DTO validation cho API requests": "Missing DTO validation structure for API requests",
    "Tất cả request payload cần được validate qua schema trước khi vào controller": "All request payloads should be validated against schemas before reaching controllers",
    "Thiếu Dependency Injection (DI)": "Missing Dependency Injection (DI)",
    "Khởi tạo trực tiếp dependencies trong class gây khó khăn cho Unit Test": "Directly instantiating dependencies inside classes makes unit testing difficult",

    // Anti-Crash & Database & Security
    "Kiểm soát ngoại lệ: Không có Silent Exception Eater (Bare Except / Pass)": "Exception control: No Silent Exception Eaters (Bare Except / Pass)",
    "Không nuốt chửng ngoại lệ hệ thống bằng except: pass, toàn bộ lỗi được ghi log tường minh.": "No silent swallowing of exceptions with except: pass; all errors logged explicitly.",
    "Bắt lỗi dạng `except:` hoặc `except Exception: pass` làm ẩn đi các lỗi nghiêm trọng không thể debug.": "Catching errors with `except:` or `except Exception: pass` obscures critical errors from debugging.",
    "Chỉ định chính xác ngoại lệ cần bắt (vd: except ValueError) và ghi log lỗi đầy đủ.": "Specify exact exceptions (e.g. except ValueError) and log errors comprehensively.",
    "An toàn bí mật mã nguồn: Không phát hiện Hardcoded Secret / API Key": "Secret safety: No Hardcoded Secrets / API Keys detected",
    "Không phát hiện chuỗi khóa bí mật, API key hoặc password nào bị gán cứng vào mã nguồn.": "No secret keys, API keys or passwords statically hardcoded in source.",
    "Chuỗi bí mật hoặc API key được gán tĩnh trực tiếp vào mã nguồn, có nguy cơ lộ khi commit lên Git.": "Secret keys or API keys hardcoded in source code; risk of leaking upon git commit.",
    "Di chuyển toàn bộ khóa bảo mật vào biến môi trường (.env) và đọc qua process.env hoặc os.environ.": "Move all secrets into environment variables (.env) and read via process.env or os.environ.",
    "An toàn phân tích cú pháp JSON: 0 Naked JSON.parse rủi ro sập runtime": "JSON Parsing Safety: 0 Naked JSON.parse runtime crash risks",
    "100% các lời gọi parse JSON đều được bọc trong try-catch hoặc schema validation an toàn.": "100% of JSON parsing calls wrapped in try-catch or safe schema validation.",
    "Gọi JSON.parse trực tiếp mà không có try-catch sẽ làm sập server hoặc ứng dụng nếu chuỗi JSON không hợp lệ.": "Directly calling JSON.parse without try-catch crashes the application if JSON is malformed.",
    "Bọc toàn bộ JSON.parse trong khối `try { ... } catch (e) { ... }` hoặc dùng hàm parse an toàn.": "Wrap all JSON.parse in `try { ... } catch (e) { ... }` blocks or use safe parse utilities.",
    "An toàn tài nguyên: Không phát hiện Timer / Event Listener rò rỉ bộ nhớ": "Resource safety: No Timer / Event Listener memory leak risks detected",
    "Toàn bộ các tác vụ định thời và đăng ký sự kiện đều có hàm hủy cleanup giải phóng tài nguyên.": "All timers and event subscriptions provide cleanup cancellation handlers.",
    "Khởi tạo setInterval hoặc addEventListener trong useEffect nhưng thiếu hàm cleanup giải phóng khi unmount.": "setInterval or addEventListener initiated in useEffect lacking cleanup on unmount.",
    "Trả về hàm dọn dẹp trong useEffect: `return () => clearInterval(id);`.": "Return cleanup handler in useEffect: `return () => clearInterval(id);`.",
    "An toàn truy vấn SQL: Không phát hiện Raw SQL Concatenation": "SQL Query Safety: No Raw SQL Concatenation detected",
    "100% câu lệnh truy vấn dữ liệu sử dụng ORM an toàn hoặc tham số hóa (parameterized queries).": "100% of database queries use safe ORMs or parameterized queries.",
    "Chuyển đổi các câu lệnh nối chuỗi sang sử dụng query parameter (ví dụ: $1, :val hoặc ?).": "Convert string concatenation queries to parameterized placeholders (e.g. $1, :val, or ?).",

    // Violations
    "Bắt lỗi im lặng (BARE EXCEPT hoặc EXCEPT EXCEPTION: PASS) làm nuốt chửng lỗi hệ thống.": "Silent exception handling (bare except or except Exception: pass) swallows system errors.",
    "Gọi JSON.PARSE không bọc trong khối TRY-CATCH an toàn (Nguy cơ sập RUNTIME khi dữ liệu JSON hỏng).": "JSON.parse called outside try-catch block (runtime crash risk on malformed JSON).",
    "Sử dụng kiểu dữ liệu \": any\" vi phạm quy chuẩn STRICT TYPING của TYPESCRIPT.": "Using \": any\" type violates TypeScript strict typing standards.",
    "Phát hiện CHUỖI KHÓA BẢO MẬT (SECRET/API KEY) được gán tĩnh trực tiếp vào mã nguồn.": "Hardcoded secret / API key statically assigned directly in source code.",
    "Phát hiện nối chuỗi trực tiếp vào câu lệnh SQL thay vì dùng tham số hóa (Nguy cơ SQL INJECTION nghiêm trọng).": "Direct string concatenation into SQL statements without parameterization (Critical SQL Injection risk).",
    "Controller trực tiếp truy vấn dữ liệu/gọi SQL vi phạm phân tầng Clean Architecture.": "Controller queries database directly, violating Clean Architecture layering.",
    "setInterval hoặc addEventListener trong useEffect thiếu hàm cleanup giải phóng tài nguyên.": "setInterval or addEventListener in useEffect lacks cleanup function (memory leak risk).",

    // Common labels
    "Hạng mục này không áp dụng cho cấu trúc dự án hiện tại": "This category does not apply to the current project structure",
    "Không có vi phạm nào thuộc nhóm này": "No violations recorded in this group",
    "Chưa có phát hiện nào cần xử lý. Dự án đạt chuẩn!": "No actionable findings. The project meets all standards!",
    "Chưa có dữ liệu kiểm tra": "No audit data yet",
    "Chưa có dữ liệu": "No data yet",
    "Quét Regex nhạy cảm": "Sensitive Regex Scan",
    "Quét Lifecycle Hooks": "Lifecycle Hooks Scan",
    "Cấu trúc thư mục": "Directory Structure",
    "Tệp README.md chuẩn xác tại thư mục gốc": "Accurate README.md in root directory",
    "Mô tả bài toán, mục tiêu và định vị giá trị sản phẩm rõ ràng": "Clear product vision, problem description and value proposition",
    "Đoạn giới thiệu mục tiêu bài toán và giá trị sản phẩm (PRODUCT VISION)": "Product vision and problem value proposition section",
    "Khối lệnh QUICK START hướng dẫn cài đặt và khởi chạy dự án cục bộ": "QUICK START command block guiding local setup and startup",
    "Khối lệnh QUICK START hướng dẫn thiết lập môi trường và chạy mã nguồn": "QUICK START block for environment setup and running code",
    "Tài liệu hướng dẫn cấu hình biến môi trường (.ENV)": "Environment variables configuration documentation (.ENV)",
    "Mô tả cấu trúc thư mục và sơ đồ ARCHITECTURE tổng quan": "Directory structure description and ARCHITECTURE overview diagram",
    "Sơ đồ hoặc tài liệu mô tả cấu trúc thư mục ARCHITECTURE": "Diagram or document describing ARCHITECTURE directory layout",
    "Cơ chế Tài liệu sống & Đồng bộ tự động 4 lớp (LIVING DOCUMENTATION AUTO-SYNC PIPELINE)": "4-Layer Living Documentation auto-sync pipeline",
    "Dự án chưa có tệp README.md giới thiệu": "Project is missing introductory README.md file",
    "Tệp quy chuẩn chỉ dẫn cho AI AGENT (AGENTS.md hoặc .CURSORRULES)": "AI Agent directive specification (AGENTS.md or .cursorrules)",
    "Hồ sơ ARCHITECTURE DECISION RECORDS (ADRS)": "Architecture Decision Records (ADRs)",
    "Tài liệu đặc tả hợp đồng API CONTRACT (OPENAPI / SWAGGER)": "API contract specification (OpenAPI / Swagger)",
    "Quy tắc ràng buộc phủ định (NEGATIVE CONSTRAINTS) ngăn chặn Agent tự ý sửa đổi bừa bãi": "Negative constraints preventing unintended modifications by Agent",
    "Quy tắc điều khoản cấm (NEGATIVE CONSTRAINTS: hành động nào Agent tuyệt đối KHÔNG được làm)": "Prohibited actions (Negative constraints: what Agent must NEVER do)",
    "Cơ chế ngắt mạch dừng lại hỏi (STOP & ASK / 2-ATTEMPT CIRCUIT BREAKER) chống vòng lặp Doom Loop": "Stop & Ask / 2-Attempt Circuit Breaker preventing Doom Loops",
    "Cơ chế chốt chặn STOP & ASK / CIRCUIT BREAKER (buộc Agent dừng lại xin ý kiến khi chạm rủi ro kiến trúc)": "Stop & Ask / Circuit Breaker gate (forces Agent to seek confirmation on architectural risks)",
    "Điều khoản ràng buộc bắt buộc lập trình phòng thủ (ANTI-CRASH DEFENSIVE STANDARD)": "Mandatory defensive programming clause (Anti-Crash standard)",
    "Quy chuẩn chống đổ vỡ ANTI-CRASH bắt buộc trong hiến pháp Agent": "Mandatory anti-crash defensive rules in Agent constitution",
    "Thiếu tệp hiến pháp định hướng hành vi cho AI Agent (AGENTS.md, .cursorrules hoặc .mdc)": "Missing behavioral constitution for AI Agents (AGENTS.md, .cursorrules or .mdc)",
    "Cấu trúc SKILL.md chuẩn hóa với YAML FRONTMATTER (name, description, instructions)": "Standardized SKILL.md structure with YAML frontmatter (name, description, instructions)",
    "Chuẩn hóa YAML FRONTMATTER (name, description) cho các tệp SKILL.md": "Standardized YAML frontmatter (name, description) for SKILL.md files",
    "Thư mục đóng gói kỹ năng AGENT SKILLS (.agents/skills/*/SKILL.md) để mở rộng năng lực tự động": "Packaged Agent skills directory (.agents/skills/*/SKILL.md) for automated capability expansion",
    "Quy trình tác vụ tích hợp chặng tự kiểm chứng (SELF-VERIFICATION / TDD FIRST)": "Task workflow with integrated self-verification stage (Self-Verification / TDD first)",
    "Chặng tự kiểm thử và nghiệm thu (SELF-VERIFICATION) trong kịch bản Workflow": "Self-testing and acceptance verification stage in Agent workflow",
    "Quy trình kịch bản tác vụ nhiều bước (AGENT WORKFLOWS) hỗ trợ cộng tác tự động": "Multi-step task workflow scripts (Agent Workflows) for autonomous collaboration",
    "Hạ tầng chỉ mục máy đọc ZERO-CLONE REMOTE HUB (MANIFEST.json / llms.txt)": "Zero-Clone machine-readable index infrastructure (MANIFEST.json / llms.txt)",
    "Mô hình tiêm phụ thuộc DEPENDENCY INJECTION (DI) để hỗ trợ Unit Testing": "Dependency Injection (DI) pattern supporting Unit Testing",
    "Xác thực tự động cho dữ liệu DTO đầu vào (Zod, Pydantic hoặc Schema Validator)": "Automated input DTO validation (Zod, Pydantic, or Schema Validator)",
    "Cơ chế giải phóng tài nguyên an toàn khi tắt SERVER (GRACEFUL SHUTDOWN)": "Safe resource cleanup on shutdown (Graceful Shutdown)",
    "Hệ thống DESIGN TOKENS độc quyền (CUSTOM TAILWIND CONFIG / CSS VARIABLES / THEME TOKENS)": "Design tokens system (Custom Tailwind config / CSS variables / Theme tokens)",
    "Hệ thống quản lý biến thiết kế giao diện tập trung (DESIGN TOKENS / THEME VARIABLES)": "Centralized design tokens and theme variables system",
    "API CLIENT phòng thủ tập trung (INTERCEPTORS, BASEURL, ERROR NORMALIZATION)": "Centralized defensive API client (Interceptors, baseURL, error normalization)",
    "Tệp bọc API CLIENT tập trung (tránh gọi FETCH / AXIOS rải rác trong COMPONENT)": "Centralized API client wrapper (avoids scattered fetch/axios calls in components)",
    "Trang bị ERROR BOUNDARY bắt lỗi runtime chống crash trắng toàn bộ màn hình": "Error Boundary catching runtime errors preventing white-screen crash",
    "Thành phần ERROR BOUNDARY bao bọc route để xử lý lỗi sập giao diện an toàn": "Error Boundary component wrapping routes for safe UI crash recovery",
    "Kỹ thuật CODE-SPLITTING / LAZY LOADING tối ưu tốc độ tải trang ban đầu": "Code-splitting / lazy loading optimizing initial page load speed",
    "Áp dụng React.lazy hoặc Dynamic Import tải chậm các module nặng": "Applied React.lazy or dynamic imports for heavy module lazy loading",
    "Quản lý DATABASE MIGRATION có kiểm soát phiên bản theo thời gian": "Version-controlled database migration management",
    "Công cụ quản lý LƯỢC ĐỒ CƠ SỞ DỮ LIỆU có phiên bản (Prisma, Alembic, Drizzle, TypeORM, Flyway)": "Database schema migration tooling with versioning (Prisma, Alembic, Drizzle, TypeORM, Flyway)",
    "Cấu hình CONNECTION POOL & TIMEOUT bảo vệ giới hạn kết nối DATABASE": "Connection pool & timeout configuration protecting database connection limits",
    "Cơ chế bọc TRANSACTION tường minh cho các tác vụ thay đổi nhiều thực thể": "Explicit transaction wrapping for multi-entity mutation operations",
    "An toàn câu lệnh QUERY: Sử dụng PARAMETERIZED QUERIES hoặc TYPE-SAFE ORM": "Query safety: Parameterized queries or type-safe ORM usage",
    "An toàn xử lý JSON: 0 Naked JSON.parse rủi ro sập runtime": "JSON handling safety: 0 naked JSON.parse risks of runtime crash",
    "Xác minh chính xác phiên bản phụ thuộc qua DEPENDENCY LOCKFILE (chống Supply Chain Attack)": "Dependency lockfile pinning exact versions (preventing supply chain attacks)",
    "Tệp DEPENDENCY LOCKFILE (package-lock.json, poetry.lock, go.sum)": "Dependency lockfile (package-lock.json, poetry.lock, go.sum)",
    "Cấu hình HTTP SECURITY HEADERS (CORS strict, HELMET, Content-Security-Policy)": "HTTP security headers configuration (Strict CORS, Helmet, Content-Security-Policy)",
    "Thiết lập HTTP SECURITY HEADERS bảo vệ giao thức (CORS, Helmet, CSP)": "Configured HTTP security headers protocol protection (CORS, Helmet, CSP)",
    "Cơ chế RATE LIMITING giới hạn tần suất yêu cầu chống Brute-force & DDoS": "Rate limiting mechanism protecting against brute-force and DDoS",
    "Cơ chế RATE LIMITING bảo vệ API trước các đợt tấn công vét cạn (Brute-force)": "Rate limiting protecting APIs from brute-force scanning attacks",
    "Cô lập biến môi trường nhạy cảm: .ENV được loại trừ 100% khỏi kho Git": "Sensitive environment isolation: .env 100% excluded from Git repository",
    "Chính sách cô lập SECRET nghiêm ngặt (đưa .ENV vào .gitignore và dùng KMS/Vault)": "Strict secret isolation policy (.env in .gitignore and KMS/Vault usage)",
    "Dockerfile chuẩn mực MULTI-STAGE BUILD tối ưu dung lượng và tính bảo mật": "Standard multi-stage build Dockerfile optimizing size and security",
    "Dockerfile tối ưu MULTI-STAGE BUILD (tách biệt môi trường build và runtime)": "Optimized multi-stage Dockerfile (separating build from minimal runtime)",
    "Chạy CONTAINER với quyền hạn tối thiểu (USER NON-ROOT)": "Container running with minimal privileges (non-root user)",
    "Khai báo USER NON-ROOT trong Dockerfile để ngăn chặn Container Escape": "Non-root user declaration in Dockerfile preventing container escapes",
    "Endpoint thăm dò trạng thái sức khỏe: LIVENESS & READINESS PROBES (/healthz, /readyz)": "Health check probe endpoints: Liveness & Readiness probes (/healthz, /readyz)",
    "Cung cấp endpoint LIVENESS & READINESS PROBES (/healthz, /readyz) cho bộ điều phối Cloud": "Liveness & Readiness probe endpoints (/healthz, /readyz) for cloud orchestrator",
    "Khai báo hạ tầng dưới dạng mã INFRASTRUCTURE AS CODE (DOCKER COMPOSE / KUBERNETES MANIFESTS)": "Infrastructure as Code declaration (Docker Compose / Kubernetes manifests)",
    "Tệp quản lý hạ tầng INFRASTRUCTURE AS CODE (docker-compose.yml hoặc K8s Helm)": "Infrastructure as Code management file (docker-compose.yml or K8s Helm)",
    "API GATEWAY / REVERSE PROXY làm cổng điều phối lưu lượng tập trung": "API Gateway / Reverse Proxy as centralized ingress traffic router",
    "Cấu hình API GATEWAY tập trung (Kong, Traefik, Ocelot hoặc Nginx)": "Centralized API Gateway configuration (Kong, Traefik, Ocelot, or Nginx)",
    "Cơ chế ngắt mạch CIRCUIT BREAKER & RETRY WITH JITTER chống sập dây chuyền (Cascading Failure)": "Circuit Breaker & retry with jitter preventing cascading failures",
    "Cơ chế CIRCUIT BREAKER bảo vệ các lời gọi liên dịch vụ phân tán": "Circuit breaker mechanism protecting distributed inter-service calls",
    "Hợp đồng liên dịch vụ chặt chẽ qua gRPC PROTOBUF hoặc EVENT-DRIVEN MESSAGING (KAFKA/RABBITMQ)": "Inter-service contract enforcement via gRPC Protobuf or Event-driven messaging",
    "Đặc tả hợp đồng giao tiếp liên dịch vụ (gRPC Protobuf hoặc Event Broker)": "Inter-service communication contract specification (gRPC Protobuf or Event Broker)",
    "Đính kèm CORRELATION ID (x-request-id) xuyên suốt hành trình của request": "Correlation ID (x-request-id) propagation throughout request lifecycle",
    "Middleware gán CORRELATION ID (x-request-id) phục vụ truy vết phân tán": "Middleware attaching Correlation ID (x-request-id) for distributed tracing",
    "Chiến lược CACHING chuẩn mực: Bắt buộc cài đặt thời gian sống (TTL) cho mọi Redis Key": "Standard caching strategy: Mandatory TTL for all cache keys",
    "Thiết lập TTL (Time-To-Live) bắt buộc cho Cache Key để chống cạn kiệt RAM Redis": "Mandatory TTL configuration for cache keys preventing RAM exhaustion",
    "Dự án áp dụng bộ nhớ đệm cục bộ (In-Memory Cache) đơn giản": "Project applies basic local in-memory caching",
    "Giới hạn CONNECTION POOLING rõ ràng bảo vệ hạ tầng cơ sở dữ liệu": "Explicit connection pooling limit protecting database infrastructure",
    "Giới hạn CONNECTION POOLING tối đa để chống nghẽn đường truyền (Connection Exhaustion)": "Maximum connection pooling limit preventing connection exhaustion",
    "Kiểm soát chặt chẽ hợp đồng dữ liệu qua DATA CONTRACTS / SCHEMA VALIDATION": "Strict data contract control via Data Contracts / Schema Validation",
    "Đặc tả SCHEMA tường minh cho các đối tượng luồng dữ liệu (Data Contracts)": "Explicit schema specification for data transfer objects (Data Contracts)",
    "Ghi nhật ký có cấu trúc chuẩn mực (STRUCTURED JSON LOGGING) sẵn sàng cho ELK / Loki": "Standardized structured JSON logging ready for ELK / Loki",
    "Thư viện ghi nhật ký có cấu trúc STRUCTURED LOGGING (thay thế console.log / print thô)": "Structured logging library (replacing raw console.log / print)",
    "Tích hợp OPENTELEMETRY phục vụ thu thập dấu vết và phân tích độ trễ xuyên suốt": "OpenTelemetry integration for end-to-end tracing and latency analysis",
    "Công cụ truy vết OPENTELEMETRY để theo dõi độ trễ hệ thống": "OpenTelemetry tracing instrumentation for latency observation",
    "Cung cấp endpoint chỉ số PROMETHEUS METRICS (/metrics) phục vụ giám sát": "Prometheus metrics endpoint (/metrics) for operational monitoring",
    "Endpoint xuất chỉ số hiệu năng PROMETHEUS METRICS (/metrics) phục vụ giám sát": "Prometheus metrics export endpoint (/metrics) for monitoring",
    "Bổ sung mục Defensive Programming Guidelines vào AGENTS.md.": "Add Defensive Programming Guidelines section to AGENTS.md.",
    "Chưa trang bị công cụ APM Tracing phân tán để quan sát độ trễ của các lệnh gọi CSDL và API bên ngoài.": "Missing distributed APM tracing tool to monitor database and external API call latencies.",
    "Chưa tìm thấy khối bọc Transaction cho các nghiệp vụ cập nhật nhiều bảng cùng lúc.": "No transaction block found for multi-table update operations.",
    "Cài đặt `@opentelemetry/sdk-node` hoặc `opentelemetry-sdk` Python để theo dõi hiệu năng hệ thống.": "Install `@opentelemetry/sdk-node` or `opentelemetry-sdk` Python to track performance.",
    "Thiếu yêu cầu bắt buộc Agent phải bọc try-catch, kiểm tra null safety và validate kiểu dữ liệu đầu vào.": "Missing mandatory rule requiring Agent to wrap try-catch, check null safety, and validate input types.",
    "Tệp .env chứa biến nhạy cảm đã được loại trừ an toàn trong .gitignore và không bị theo dõi bởi Git.": ".env file containing secrets is safely excluded in .gitignore and not tracked by Git.",
    "Đã phát hiện component Error Boundary bắt các ngoại lệ React rendering, bảo vệ trải nghiệm người dùng.": "Detected Error Boundary component catching React rendering exceptions, protecting user experience.",
    "Đã phát hiện khối mã lệnh hướng dẫn khởi chạy dự án môi trường phát triển cục bộ.": "Detected command block instructing how to run the project in local development.",
    "Đã xác minh Dockerfile sử dụng multi-stage build tách biệt giai đoạn biên dịch và môi trường chạy tối giản.": "Verified Dockerfile utilizes multi-stage build separating compilation from minimal runtime.",
    "Đã xác minh bộ giới hạn tần suất yêu cầu chống tấn công dò quét vét cạn và quá tải tài nguyên.": "Verified rate limiter protecting against brute-force attacks and resource exhaustion.",
    "Đã xác minh cấu hình Gateway/Reverse Proxy điều phối và định tuyến lưu lượng vào hệ thống.": "Verified Gateway/Reverse Proxy routing and ingress configuration.",
    "Đã xác minh tham số giới hạn connection pooling tối đa chống cạn kiệt tài nguyên kết nối.": "Verified maximum connection pooling limits preventing connection exhaustion.",
    "Đã xác minh tích hợp SDK OpenTelemetry hỗ trợ APM và đo lường độ trễ chi tiết từng span.": "Verified OpenTelemetry SDK integration supporting APM and span latency measurement.",
    "Đã xác minh đối tượng truyền tải dữ liệu có schema validation chặt chẽ bảo vệ tính toàn vẹn dữ liệu.": "Verified data transfer objects have strict schema validation protecting integrity.",
  };

  // Two-way synchronization: populate DICT.vi with any missing English -> Vietnamese pairs
  Object.keys(VI_TO_EN).forEach(viKey => {
    const enVal = VI_TO_EN[viKey];
    if (!DICT.vi[enVal]) {
      DICT.vi[enVal] = viKey;
    }
  });

  function translateDynamicViToEn(text) {
    if (!text || typeof text !== "string") return text;
    // Grade with red alarm
    let m = text.match(/^F\s*\(BÁO ĐỘNG ĐỎ:\s*PHÁT HIỆN\s*(\d+)\s*LỖI MỨC CAO\)/i);
    if (m) return `F (RED ALARM: ${m[1]} HIGH-SEVERITY RISKS DETECTED)`;
    if (text === "F (CẦN TÁI CẤU TRÚC KIẾN TRÚC TOÀN DIỆN)") return "F (NEEDS ARCHITECTURAL REFACTORING)";
    if (text === "A+ (XUẤT SẮC - SẴN SÀNG PRODUCTION)") return "A+ (EXCELLENT - PRODUCTION READY)";
    if (text === "A (RẤT TỐT - SẴN SÀNG STAGING)") return "A (VERY GOOD - STAGING READY)";
    if (text === "B+ (TỐT - CÒN MỘT SỐ TECHNICAL DEBT NHỎ)") return "B+ (GOOD - MINOR TECH DEBT)";
    if (text === "B (CHẤP NHẬN ĐƯỢC - CẦN REFACTOR)") return "B (ACCEPTABLE - NEEDS REFACTOR)";
    if (text === "C (DƯỚI CHUẨN TIÊU CHÍ)") return "C (BELOW CRITERIA BASELINE)";

    // Secret count
    m = text.match(/^CẢNH BÁO:\s*Phát hiện\s*(\d+)\s*chuỗi HARDCODED SECRET trong mã/i);
    if (m) return `WARNING: Detected ${m[1]} HARDCODED SECRET strings in code`;

    // Bare except count
    m = text.match(/^Phát hiện\s*(\d+)\s*vị trí BARE EXCEPT nuốt chửng lỗi hệ thống/i);
    if (m) return `Detected ${m[1]} BARE EXCEPT locations silently swallowing system errors`;

    // Naked JSON parse count
    m = text.match(/^Phát hiện\s*(\d+)\s*vị trí NAKED JSON\.PARSE không bọc try-catch/i);
    if (m) return `Detected ${m[1]} NAKED JSON.PARSE locations without try-catch`;

    // React leak count
    m = text.match(/^Cảnh báo MEMORY LEAK:\s*Phát hiện\s*(\d+)\s*Timer\/Listener thiếu hàm cleanup/i);
    if (m) return `MEMORY LEAK WARNING: Detected ${m[1]} Timer/Listeners lacking cleanup handler`;

    // SQL injection count
    m = text.match(/^Cảnh báo SQL INJECTION:\s*Phát hiện\s*(\d+)\s*vị trí nối chuỗi trực tiếp/i);
    if (m) return `SQL INJECTION WARNING: Detected ${m[1]} direct string concatenation locations`;

    // Scanned files
    m = text.match(/^(\d+)\s*tệp mã nguồn/i);
    if (m) return `${m[1]} source files`;
    m = text.match(/^Đã quét\s*(\d+)\s*tệp mã nguồn/i);
    if (m) return `Scanned ${m[1]} source files`;

    // Bloat env
    m = text.match(/^Có tệp cấu hình nhạy cảm `([^`]+)` trong dự án/i);
    if (m) return `Sensitive configuration file \`${m[1]}\` present in project: ensure it is in .gitignore and not tracked by Git.`;

    // Build cache bloat
    m = text.match(/^Thư mục cache BUILD `([^`]+)` có nguy cơ bị đưa lên remote git\./i);
    if (m) return `Build cache directory \`${m[1]}\` risks being committed to remote Git.`;

    // Layered arch template
    m = text.match(/^Cấu trúc phân tầng chuẩn mực theo (.*)$/i);
    if (m) {
      const arch = VI_TO_EN[m[1]] || m[1];
      return `Standard layered structure following ${arch}`;
    }
    m = text.match(/^Đã xác minh cấu trúc phân tầng với các tầng chức năng rõ rệt:\s*(.*)$/i);
    if (m) return `Verified layered architecture with distinct functional layers: ${m[1]}`;

    // Scan activity log translations
    m = text.match(/^\s*->\s*đã quét\s*(\d+)\s*tệp văn bản\.\.\./i);
    if (m) return `  -> scanned ${m[1]} text files...`;

    m = text.match(/^Quét an toàn nội dung:\s*(\d+)\s*tệp văn bản,\s*(\d+)\s*tín hiệu\./i);
    if (m) return `Content safety scan: ${m[1]} text files, ${m[2]} signals.`;

    if (/^Quét an toàn nội dung\s*\(tệp văn bản/i.test(text)) {
      return "Scanning content safety (text files, agent directives)...";
    }

    m = text.match(/^✓\s*HOÀN THÀNH ĐO KIỂM TOÀN DIỆN!\s*TỔNG ĐIỂM:\s*(\d+)\/100\s*\[HẠNG:\s*(.*)\]/i);
    if (m) return `✓ COMPREHENSIVE AUDIT COMPLETE! TOTAL SCORE: ${m[1]}/100 [GRADE: ${translateDynamicViToEn(m[2])}]`;

    m = text.match(/^Tệp báo cáo lưu tại:\s*(.*)$/i);
    if (m) return `Audit report saved to: ${m[1]}`;

    if (/^✓\s*Quá trình quét hoàn tất thành công/i.test(text)) {
      return "✓ Scan completed successfully. Click 'View Overview Results' or select any pillar on the left for details.";
    }

    m = text.match(/^Tech Stack nhận diện:\s*Ngôn ngữ\s*\[(.*?)\]\s*\|\s*Frameworks\s*\[(.*?)\]/i);
    if (m) return `Detected Tech Stack: Languages [${m[1]}] | Frameworks [${m[2]}]`;

    m = text.match(/^\[(\d+)\/(\d+)\]\s*(.*?)\.\.\.$/i);
    if (m) return `[${m[1]}/${m[2]}] ${lookup(m[3])}...`;

    m = text.match(/^Đang thẩm định\s*\[(\d+)\/(\d+)\]:\s*(.*?)\.\.\.$/i);
    if (m) return `Auditing [${m[1]}/${m[2]}]: ${lookup(m[3])}...`;

    m = text.match(/^Đang quét an toàn nội dung:\s*(\d+)\s*tệp\.\.\.$/i);
    if (m) return `Scanning content safety: ${m[1]} files...`;

    m = text.match(/^Đã hoàn thành thẩm định!\s*Báo cáo:\s*(.*)$/i);
    if (m) return `Audit complete! Report: ${m[1]}`;

    m = text.match(/^->\s*Đã tìm thấy\s*(.*?)\s*\((\d+)\s*dòng\)\./i);
    if (m) return `  -> Found ${m[1]} (${m[2]} lines).`;

    m = text.match(/^Đã phát hiện tệp tài liệu khởi đầu chính của dự án tại `(.*?)` với (\d+) dòng nội dung\./i);
    if (m) return `Detected main starter documentation file at \`${m[1]}\` with ${m[2]} lines of content.`;

    m = text.match(/^Phát hiện tiêu đề và định vị sản phẩm:\s*(.*)$/i);
    if (m) return `Detected title and product vision: ${m[1]}`;

    // Architecture & Pillar details
    if (/^Chưa có cơ chế xử lý tín hiệu SIGTERM\/SIGINT/i.test(text)) {
      return "No SIGTERM/SIGINT signal handling to release DB connections and stop server without dropping in-flight requests.";
    }
    if (/^Remediation:\s*Bổ sung hàm lắng nghe SIGTERM\/SIGINT/i.test(text)) {
      return "Remediation: Add SIGTERM/SIGINT listener to gracefully close database connection pools and server.";
    }
    if (/^Độ thuần khiết của DOMAIN và ranh giới CONTROLLER/i.test(text)) {
      return "Domain purity & controller boundary perfectly protected (0 layer leaks)";
    }
    if (/^Không phát hiện bất kỳ controller nào gọi truy vấn SQL/i.test(text)) {
      return "No controllers directly query SQL or domain tainted by framework.";
    }
    if (/^Áp dụng DEPENDENCY INJECTION/i.test(text)) {
      return "Explicit Dependency Injection (DI) applied";
    }
    if (/^Đã phát hiện áp dụng kỹ thuật tiêm phụ thuộc/i.test(text)) {
      return "Detected Dependency Injection (DI / IoC) pattern making code modular and unit-testable.";
    }
    if (/^Cơ chế giải phóng kết nối và tài nguyên khi tắt SERVER/i.test(text)) {
      return "Resource and connection release on server shutdown (Graceful Shutdown)";
    }
    if (/^Xác thực dữ liệu đầu vào DTO tự động/i.test(text)) {
      return "Automated DTO input validation (Zod / Pydantic / class-validator)";
    }
    if (/^Đã phát hiện schema validation tự động cho các đối tượng/i.test(text)) {
      return "Detected automated schema validation for Data Transfer Objects (DTO).";
    }
    if (/^Thiếu schema validation tự động cho các request đầu vào/i.test(text)) {
      return "Missing automated schema validation for input requests (DTO).";
    }
    m = text.match(/^Remediation:\s*(.*)$/i);
    if (m) return `Remediation: ${lookup(m[1])}`;

    // Specific audit runtime logs translations
    if (/^Khởi động bộ máy đo kiểm/i.test(text)) {
      return "Initializing Universal Project Auditor engine...";
    }
    m = text.match(/^Khảo sát thư mục dự án:\s*(.*)$/i);
    if (m) return `Scanning target directory: ${m[1]}`;

    m = text.match(/^\s*->\s*Phân tích import:\s*(\d+)\/(\d+)\s*tệp Python\.\.\./i);
    if (m) return `  -> Analyzing imports: ${m[1]}/${m[2]} Python files...`;

    m = text.match(/^Phân tích dự án:\s*(.*?);\s*ngôn ngữ chính\s*(.*?);\s*(\d+)\s*thành phần\./i);
    if (m) return `Project analysis: ${lookup(m[1])}; primary language ${m[2]}; ${m[3]} components.`;

    m = text.match(/^Project analysis:\s*(.*?);\s*primary language\s*(.*?);\s*(\d+)\s*components\./i);
    if (m) return `Project analysis: ${lookup(m[1])}; primary language ${m[2]}; ${m[3]} components.`;

    m = text.match(/^(?:Nhận diện|Detected|Identified)\s*Archetype:\s*(.*)$/i);
    if (m) return `Detected Archetype: ${lookup(m[1])}`;

    m = text.match(/^Lập chỉ mục ProjectTree siêu tốc:\s*Đã duyệt\s*(\d+)\s*tệp tin\s*\((\d+)\s*tệp mã nguồn\)\./i);
    if (m) return `ProjectTree indexing: Scanned ${m[1]} files (${m[2]} source files).`;

    m = text.match(/^\s*->\s*Phân tầng kiến trúc:\s*(.*)$/i);
    if (m) return `  -> Layered architecture: ${m[1]}`;

    m = text.match(/^\s*->\s*Khảo sát giao diện:\s*tìm thấy\s*(\d+)\s*tệp UI components & styling\./i);
    if (m) return `  -> UI audit: found ${m[1]} UI components & styling files.`;

    m = text.match(/^\s*->\s*Cơ sở dữ liệu:\s*(.*?)\.\s*Đã rà soát migration và query safety\./i);
    if (m) return `  -> Database: ${m[1]}. Audited migrations and query safety.`;

    m = text.match(/^\s*->\s*Đã quét AST trên\s*(\d+)\s*tệp mã nguồn:\s*kiểm tra\s*(.*)$/i);
    if (m) return `  -> AST scan completed on ${m[1]} source files: checked ${m[2]}`;

    return text;
  }

  let lang = "en";
  const ATTRS = ["title", "placeholder"];

  function fmt(s, vars) {
    if (!vars) return s;
    return s.replace(/\{(\w+)\}/g, (m, k) => {
      if (k in vars) {
        let val = vars[k];
        if (typeof val === "string") {
          val = lookup(val);
        }
        return val;
      }
      return m;
    });
  }
  function lookup(key) {
    if (!key || typeof key !== "string") return key;
    if (lang === "en") {
      if (VI_TO_EN[key]) return VI_TO_EN[key];
      return translateDynamicViToEn(key);
    } else {
      if (DICT[lang] && DICT[lang][key]) return DICT[lang][key];
      return key;
    }
  }
  window.t = (key, vars) => fmt(lookup(key), vars);
  window.currentLang = () => lang;
  window.supportedLanguages = () => ["en"].concat(Object.keys(DICT));

  window.applyI18n = function (root) {
    root = root || document;
    root.querySelectorAll("[data-i18n-html]").forEach((el) => {
      const key = el.getAttribute("data-i18n-html");
      el.innerHTML = lookup(key);
    });
    root.querySelectorAll("*").forEach((el) => {
      if (el.children.length === 0 && !el.closest("[data-i18n-html]")) {
        if (!el.dataset.i18nKey) {
          const key = (el.textContent || "").trim();
          if (key && DICT.vi[key]) { el.dataset.i18nKey = key; el.dataset.i18nCur = el.textContent; }
        }
        const k = el.dataset.i18nKey;
        // Skip text that JS replaced with dynamic content since we last wrote it.
        if (k && el.textContent === el.dataset.i18nCur) {
          const next = lookup(k);
          el.textContent = next;
          el.dataset.i18nCur = next;
        }
      }
      ATTRS.forEach((a) => {
        const dk = "i18nA" + a;
        if (!el.hasAttribute(a)) return;
        if (!el.dataset[dk]) {
          const key = el.getAttribute(a);
          if (DICT.vi[key]) { el.dataset[dk] = key; el.dataset[dk + "Cur"] = key; }
        }
        const k = el.dataset[dk];
        if (k && el.getAttribute(a) === el.dataset[dk + "Cur"]) {
          const next = lookup(k);
          el.setAttribute(a, next);
          el.dataset[dk + "Cur"] = next;
        }
      });
    });
    document.documentElement.setAttribute("lang", lang);
  };

  window.setLanguage = function (next) {
    lang = next === "vi" ? "vi" : "en";
    window.applyI18n(document);
  };
})();
