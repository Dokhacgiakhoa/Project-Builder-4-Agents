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
