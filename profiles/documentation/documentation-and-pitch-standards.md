---
id: O-001
type: reference
when: "Viết tài liệu người dùng/vận hành theo khung Diátaxis, runbook sự cố"
---
# ADR 0010: DOCUMENTATION FRAMEWORK (DIÁTAXIS) AND PITCH DECK STANDARDS

* **Trạng thái**: Đã phê duyệt (Accepted)
* **Ngày quyết định**: 2026-11-04
* **Người quyết định**: Principal Architect & Documentation Lead

---

## 1. BỐI CẢNH (CONTEXT)

Trong hầu hết các dự án công nghệ, hai cấu phần sau thường bị xem nhẹ hoặc thực hiện một cách chắp vá:
1. **Pitch Deck (Thuyết trình & Bảo vệ dự án)**: Đội ngũ kỹ thuật thường chỉ tập trung vào việc code mà thiếu một bộ tài liệu kinh doanh và thuyết trình chuẩn mực (Problem, TAM/SAM/SOM, Unit Economics, GTM) khiến dự án gặp khó khăn lớn khi gọi vốn, thi đấu hackathon hoặc bảo vệ trước ban lãnh đạo.
2. **Hệ thống Tài liệu (Documentation)**: Tài liệu dự án thường bị viết lộn xộn, trộn lẫn giữa hướng dẫn cho người mới học (Tutorials), cách giải quyết bài toán cụ thể (How-To), thông số kỹ thuật (Reference) và triết lý kiến trúc (Explanation), dẫn đến việc tài liệu nhanh chóng bị lỗi thời (Stale documentation) và không thể áp dụng trong thực tế.

---

## 2. QUYẾT ĐỊNH (DECISION)

Chúng ta quyết định chuẩn hóa toàn diện hai cấu phần này vào `Project-Starter-Kit`:

1. **Chuẩn Hóa Pitch Deck Theo Y Combinator & Sequoia Capital**:
   - Lưu trữ tại `templates/pitch-deck/pitch-deck-template.md`.
   - Hỗ trợ định dạng **Slides-as-Code** qua Marp (`templates/pitch-deck/marp-presentation.md`) giúp đội ngũ có thể quản lý slide bằng Git và xuất ra PDF/HTML tự động.
   - Trang bị kịch bản thuyết trình 3 phút / 5 phút và cẩm nang trả lời **20 câu hỏi phản biện hiểm hóc** của Nhà đầu tư / Giám khảo (`templates/pitch-deck/pitch-scripts-and-qa-guide.md`).
   - Cung cấp **AI Pitch Generator Prompts** (`templates/pitch-deck/ai-pitch-generator-prompts.md`) để AI Agent tự động phân tích codebase và điền nội dung slide.

2. **Áp Dụng Diátaxis Documentation Framework**:
   - Toàn bộ tài liệu hướng dẫn kỹ thuật được cấu trúc theo 4 góc phần tư của Diátaxis (`profiles/documentation/guides/diataxis-framework-guide.md`):
     - **Tutorials**: Khởi đầu cho người mới trong 10-15 phút.
     - **How-To Guides**: Giải quyết tình huống thực tế cụ thể.
     - **Reference**: Tra cứu thông số kỹ thuật và API contracts.
     - **Explanation**: Lý giải kiến trúc và các quyết định ADR.
   - Cung cấp sẵn:
     - `profiles/documentation/guides/developer-onboarding-guide.md`: Hướng dẫn kỹ sư mới có first commit trong 30 phút.
     - `profiles/documentation/guides/user-guide-template.md`: Mẫu hướng dẫn người dùng cuối không dùng thuật ngữ kỹ thuật.
     - `profiles/documentation/guides/incident-runbook-template.md`: Sổ tay trực ca và quy trình phản ứng sự cố P1/P2 lúc 2h sáng.

---

## 3. HỆ QUẢ (CONSEQUENCES)

* **Ưu điểm [Pros]**:
  - Tăng tỷ lệ thành công của dự án từ khâu thuyết phục hội đồng (Pitching) đến khâu vận hành thực tế (Production Operations).
  - Giảm thời gian onboarding lập trình viên mới từ vài ngày xuống dưới 30 phút.
  - Xử lý sự cố production có quy trình chuẩn xác, giảm thiểu thời gian gián đoạn hệ thống (MTTR).
* **Nhược điểm [Cons]**:
  - Đòi hỏi các thành viên trong nhóm phải duy trì kỷ luật cập nhật tài liệu và slide khi có thay đổi lớn về sản phẩm.
* **Tác động hệ thống [System Impact]**:
  - Không gây ảnh hưởng đến hiệu năng hay runtime của mã nguồn ứng dụng.
