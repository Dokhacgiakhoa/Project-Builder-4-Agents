# USER ROLES & PERMISSION MATRIX

---

## 👥 1. DANH SÁCH VAI TRÒ (ACTORS)

| Mã Role | Tên Vai Trò | Mô Tả & Thẩm Quyền |
| :--- | :--- | :--- |
| `ROLE_ADMIN` | Quản trị viên hệ thống | Toàn quyền cấu hình, quản lý người dùng, xem toàn bộ báo cáo và traces |
| `ROLE_USER` | Người dùng tiêu chuẩn | Sử dụng các tính năng nghiệp vụ cốt lõi, quản lý profile cá nhân |
| `ROLE_GUEST` | Khách vãng lai | Chỉ xem các thông tin công khai, giới hạn số lượt request dùng thử |

---

## 🔐 2. MA TRẬN PHÂN QUYỀN (PERMISSION MATRIX)

| Nghiệp Vụ / Tài Nguyên | Guest | Standard User | System Admin |
| :--- | :---: | :---: | :---: |
| Xem trang giới thiệu & tài liệu public | ✅ | ✅ | ✅ |
| Đăng nhập, quản lý phiên làm việc | ❌ | ✅ | ✅ |
| Thực thi tác vụ AI chính (AI Agent invocation) | Giới hạn | ✅ | ✅ |
| Quản lý tài khoản người dùng khác | ❌ | ❌ | ✅ |
| Xem cấu hình hệ thống & API Keys | ❌ | ❌ | ✅ |
