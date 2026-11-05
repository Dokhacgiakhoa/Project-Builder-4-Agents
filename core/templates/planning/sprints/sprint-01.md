# KẾ HOẠCH SPRINT 01: KHỞI TẠO NỀN TẢNG & KIẾN TRÚC

* **Thời gian**: Tuần 1 - Tuần 2
* **Mục tiêu Sprint (Sprint Goal)**: Thiết lập hoàn chỉnh không gian ngữ cảnh (Context Workspace), ban hành toàn bộ ADRs nền tảng, thiết lập CI/CD và kết nối môi trường Cloud Free-Tier.

---

## 🎯 CÁC TASK CAM KẾT (COMMITTED TASKS)
- [x] **T-001**: Khởi tạo cấu trúc Repo chuẩn (`specs/`, `adrs/`, `AGENTS.md`).
- [ ] **T-002**: Thiết lập quy trình CI Pipeline trên GitHub Actions.
- [ ] **T-003**: Soạn thảo API Contracts đầu tiên cho hệ thống.
- [ ] **T-004**: Thiết lập kết nối Database & Vector DB trên Supabase.

---

## ⚠️ RỦI RO & PHƯƠNG ÁN PHÒNG NGỪA
* **Rủi ro**: Lệch pha giữa Frontend và Backend khi phát triển song song.
* **Giải pháp**: Đóng băng API Contract trong `specs/contracts/` trước khi bắt đầu viết code.
