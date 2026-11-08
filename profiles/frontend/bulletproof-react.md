---
id: D-001
type: reference
when: "Làm giao diện web React theo cấu trúc tính năng"
---
# ADR 0008: FRONTEND FEATURE-DRIVEN ARCHITECTURE (BULLETPROOF REACT)

* **Trạng thái**: Đã phê duyệt (Accepted)
* **Ngày quyết định**: 2026-11-04
* **Người quyết định**: Frontend Architect & Tech Lead

---

## 1. BỐI CẢNH (CONTEXT)
Trong các dự án phần mềm có giao diện người dùng phức tạp, cách tổ chức thư mục theo kiểu phân loại kỹ thuật truyền thống (tất cả components vào một thư mục, tất cả hooks vào một thư mục) nhanh chóng dẫn đến cấu trúc "spaghetti", khó bảo trì và dễ gây xung đột git khi nhiều lập trình viên hoặc AI Coding Agents làm việc cùng lúc.

---

## 2. QUYẾT ĐỊNH (DECISION)
Chúng ta áp dụng kiến trúc **Feature-Driven Architecture** (dựa trên mô hình **Bulletproof React**):

1. **Tech Stack**:
   - **Framework**: React 18+ kết hợp Vite (Build tool tốc độ cao).
   - **Language**: TypeScript ở chế độ kiểm tra nghiêm ngặt (`strict: true`).
   - **Styling**: Tailwind CSS.
   - **Server State**: TanStack React Query (Xử lý cache, đồng bộ hóa API).
   - **Client State**: Zustand (Quản lý trạng thái gọn nhẹ, không boilerplate).
   - **Schema Validation**: Zod (Kiểm tra kiểu dữ liệu thời gian thực).

2. **Quy Tắc Ranh Giới (Module Boundaries)**:
   - Toàn bộ nghiệp vụ được chia thành các Feature Modules độc lập bên trong `src/features/{feature-name}/`.
   - Một Feature **KHÔNG ĐƯỢC PHÉP** import trực tiếp tệp tin nội bộ của một Feature khác. Nếu cần chia sẻ, phải thông qua file `index.ts` công khai hoặc đưa lên tầng `src/components/` chung.
   - Luồng phụ thuộc một chiều (Unidirectional Dependency Flow): `Features` phụ thuộc vào `Shared Layers` (`components/`, `lib/`, `stores/`), không có chiều ngược lại.

---

## 3. HỆ QUẢ (CONSEQUENCES)
* **Ưu điểm [Pros]**:
  - Module hóa cao, dễ dàng xóa bỏ hoặc thay thế một tính năng mà không gây ảnh hưởng đến phần còn lại của ứng dụng.
  - Cực kỳ thân thiện với AI Coding Agents: Agent chỉ cần tập trung context vào đúng 1 thư mục feature để hoàn thành task.
  - Tách bạch hoàn toàn khỏi Backend: Kết nối qua API Contract độc lập.
* **Nhược điểm [Cons]**:
  - Yêu cầu đội ngũ tuân thủ kỷ luật export qua `index.ts`.
