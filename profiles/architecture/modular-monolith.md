# ADR 0001: ARCHITECTURE STYLE SELECTION

* **Trạng thái**: Đã phê duyệt (Accepted)
* **Ngày quyết định**: 2026-11-04
* **Người quyết định**: Human Tech Lead / Software Architect

---

## 1. BỐI CẢNH (CONTEXT)
Chúng ta cần lựa chọn phong cách kiến trúc phần mềm phù hợp cho dự án để đảm bảo tốc độ phát triển nhanh chóng, khả năng mở rộng trong tương lai, đồng thời tối ưu hóa việc phân chia ranh giới cho nhiều kỹ sư và AI Coding Agents làm việc song song.

## 2. QUYẾT ĐỊNH (DECISION)
Chúng ta lựa chọn kiến trúc **Modular Monolith (Monolith theo mô-đun hóa cao)** cho giai đoạn khởi đầu:
* Tất cả mã nguồn nằm trong cùng một repository (Single Repo).
* Hệ thống được phân chia thành các Domain Modules tách biệt hoàn toàn (`/domains/{domain-name}`).
* Các Modules chỉ giao tiếp với nhau thông qua Service Interfaces hoặc DTOs công khai, cấm truy cập chéo cấu trúc nội bộ.

## 3. HỆ QUẢ (CONSEQUENCES)
* **Tích cực [Pros]**:
  - Dễ dàng deploy, debug và theo dõi trên một môi trường duy nhất.
  - Tránh chi phí vận hành mạng và latency phức tạp của Microservices trong giai đoạn đầu.
  - AI Coding Agent dễ dàng đọc hiểu context module mà không bị quá tải token.
* **Hạn chế [Cons]**:
  - Cần kỷ luật nghiêm ngặt trong Code Review để ngăn ngừa việc import lậu giữa các modules.

---

## HƯỚNG DẪN CHO AGENT (PROFILE: MODULAR MONOLITH)

1. **Khi nào chọn**: hệ thống sẽ lớn dần, cần ranh giới module rõ để chia việc, nhưng chưa cần tách dịch vụ/triển khai riêng. Có thể kết hợp với Clean Architecture **bên trong** từng module.
2. **Sơ đồ thư mục**: `src/modules/<tên-miền>/` (mỗi module có API công khai nhỏ + phần nội bộ), `src/shared/` (kernel dùng chung rất mỏng), `src/app.*` (lắp ráp).
3. **Quy tắc phụ thuộc**: module chỉ gọi module khác qua **API công khai** (interface/DTO), không import phần nội bộ; không chia sẻ bảng dữ liệu giữa module (hoặc chỉ qua view/API được khai báo).
4. **Thêm tính năng**: xác định module sở hữu (nếu chưa có → tạo module + ghi vào bản đồ miền `specs/domains.md`); thêm vào module đó; nếu cần dữ liệu module khác → thêm hàm vào API công khai của module đó.
5. **Lỗi thường gặp (Health Check bắt)**: import chéo vào thư mục nội bộ của module khác; `shared/` chứa nghiệp vụ; module "thần thánh" ôm nhiều miền.
