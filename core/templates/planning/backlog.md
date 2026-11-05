# SPRINT BACKLOG & USER STORIES

---

## 📋 1. DANH SÁCH USER STORIES (US-CATALOG)

| Mã US | Tên Câu Chuyện | Với vai trò | Tôi muốn | Để đạt được | Mức ưu tiên | Sprint |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| `US-001` | Thiết lập nền tảng dự án | Developer / AI | Có đầy đủ Specs, ADRs, AGENTS.md | Làm việc nhất quán không bị xung đột | P0 | Sprint 1 |
| `US-002` | Quản lý xác thực người dùng | User | Đăng nhập an toàn qua JWT/OAuth | Truy cập tài nguyên bảo mật | P0 | Sprint 1 |
| `US-003` | Thực thi nghiệp vụ AI cốt lõi | User | Nhận phản hồi chính xác từ AI Agent | Giải quyết bài toán chuyên môn | P0 | Sprint 2 |

---

## 🔨 2. DANH MỤC NHIỆM VỤ THỰC THI (TASKS)

| Mã Task | Liên kết US | Tên Nhiệm Vụ | Phụ trách | Dự kiến (h) | Trạng thái | Link Spec / PR |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| `T-001` | `US-001` | Khởi tạo cấu trúc Repo chuẩn | Tech Lead | 4 | DONE | `adrs/`, `specs/` |
| `T-002` | `US-001` | Cấu hình GitHub Actions CI | DevOps | 2 | TODO | `.github/workflows/` |
| `T-003` | `US-002` | Tạo API Contract cho Auth | Backend | 3 | TODO | `specs/contracts/` |
| `T-004` | `US-003` | Xây dựng AI Agent Prompt Pipeline | AI Engineer | 6 | TODO | `specs/features/` |
