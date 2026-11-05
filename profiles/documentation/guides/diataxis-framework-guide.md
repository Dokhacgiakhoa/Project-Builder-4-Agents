# 📚 THE DIÁTAXIS DOCUMENTATION FRAMEWORK

> **Tiêu chuẩn Quốc tế về Cấu trúc Tài liệu Kỹ thuật**  
> Diátaxis (tiếng Hy Lạp: *sự sắp xếp, tổ chức*) là bộ khung kiến trúc tài liệu được áp dụng chính thức bởi các tổ chức công nghệ hàng đầu thế giới như **Python Official Docs, Canonical (Ubuntu), Cloudflare, NumPy, Django, và Gatsby**.

---

## 🧭 1. TẠI SAO PHẢI DÙNG DIÁTAXIS?

Vấn đề lớn nhất của tài liệu dự án phần mềm là **"nội dung bị trộn lẫn"**: Trong một bài hướng dẫn cài đặt lại giải thích triết lý kiến trúc, trong một bảng tra cứu API lại có các bước thực hành dài dòng. Điều này khiến cả lập trình viên lẫn người dùng bị quá tải và không tìm được thông tin mình cần.

Diátaxis giải quyết triệt để vấn đề này bằng cách chia tài liệu thành **4 Góc Phần Tư (4 Quadrants)** dựa trên 2 trục tọa độ:
* **Trục Ngang**: Phục vụ cho việc **Học tập (Learning-oriented)** ⟷ Phục vụ cho **Công việc thực tế (Work-oriented)**.
* **Trục Dọc**: Tập trung vào **Lý thuyết / Nguyên lý (Theoretical)** ⟷ Tập trung vào **Hành động thực tế (Practical)**.

```
                   THỰC HÀNH (Practical)
                           ▲
                           │
       TUTORIALS           │         HOW-TO GUIDES
     (Học việc/Nhập môn)   │    (Giải quyết bài toán cụ thể)
                           │
HỌC TẬP ───────────────────┼─────────────────── LÀM VIỆC
(Learning-oriented)        │              (Work-oriented)
                           │
       EXPLANATION         │          REFERENCE
  (Lý giải nguyên lý/Tại sao) │    (Tra cứu thông số kỹ thuật)
                           │
                           ▼
                   LÝ THUYẾT (Theoretical)
```

---

## 🧩 2. CHI TIẾT 4 GÓC PHẦN TƯ TÀI LIỆU

### Góc 1: TUTORIALS (Hướng dẫn Nhập môn / Học việc)
* **Mục tiêu**: Giúp người mới bắt đầu đạt được thành công đầu tiên (First Win) ngay lập tức và xây dựng sự tự tin.
* **Đặc điểm**:
  - Giống như **dạy một đứa trẻ tập nấu ăn**: Từng bước cầm tay chỉ việc từ A đến Z.
  - Không giải thích lan man về lý thuyết; không đưa ra quá nhiều lựa chọn (không nói "bạn có thể chọn Option A hoặc Option B"). Chỉ đưa ra DUY NHẤT 1 con đường chạy được ngay.
  - Kết quả cuối cùng là một sản phẩm chạy được thực tế.
* **Ví dụ trong dự án**:
  - *"Xây dựng tính năng Todo List đầu tiên trong 10 phút với AI Agent"*.
  - *"Chạy thử nghiệm hệ thống Fullstack cục bộ lần đầu tiên"*.

---

### Góc 2: HOW-TO GUIDES (Hướng dẫn Giải quyết Tình huống Cụ thể)
* **Mục tiêu**: Giúp người đã có kinh nghiệm giải quyết một vấn đề hoặc ca sử dụng cụ thể trong công việc thực tế.
* **Đặc điểm**:
  - Giống như **sổ tay công thức nấu ăn (Recipe Book)**: "Làm thế nào để làm món bánh pizza?".
  - Bắt đầu bằng một mục tiêu rõ ràng của người dùng: *"Làm thế nào để..."*.
  - Giả định người đọc đã nắm được các khái niệm cơ bản (không cần giải thích lại biến môi trường là gì hay Git là gì).
  - Tập trung vào chuỗi các bước hành động cụ thể để đạt kết quả.
* **Ví dụ trong dự án**:
  - *"Làm thế nào để tích hợp một mô hình LLM mới vào hệ thống Multi-Agent?"*.
  - *"Làm thế nào để đổi phong cách giao diện sang Cyberpunk HUD?"*.
  - *"Làm thế nào để rollback một phiên bản release bị lỗi trên production?"*.

---

### Góc 3: REFERENCE (Tài liệu Tra cứu Kỹ thuật)
* **Mục tiêu**: Cung cấp thông tin mô tả kỹ thuật chính xác, ngắn gọn và khách quan để người dùng tra cứu khi đang làm việc.
* **Đặc điểm**:
  - Giống như **cuốn từ điển bách khoa hoặc bản đồ chỉ dẫn kỹ thuật**.
  - Không chứa lời khuyên, không có các bước làm việc, không có câu chuyện dẫn dắt.
  - Chỉ thuần túy là sự thật kỹ thuật: Tên hàm, tham số đầu vào (arguments), kiểu dữ liệu (types), mã lỗi trả về (HTTP status codes), biến cấu hình.
  - Cấu trúc phải nhất quán và có thể tự động sinh ra từ mã nguồn (như Swagger/OpenAPI, TypeDoc).
* **Ví dụ trong dự án**:
  - `specs/contracts/api-contract-template.yaml` (Đặc tả API endpoints).
  - Bảng danh mục biến môi trường `.env.example`.
  - Danh mục lệnh của `Makefile`.

---

### Góc 4: EXPLANATION (Tài liệu Lý giải & Phân tích Chuyên sâu)
* **Mục tiêu**: Giúp người đọc hiểu sâu sắc bức tranh tổng thể, lý do đằng sau các quyết định thiết kế và triết lý kiến trúc.
* **Đặc điểm**:
  - Giống như **một bài giảng hay một bài tiểu luận phân tích lịch sử/khoa học**.
  - Trả lời cho câu hỏi: *"Tại sao lại làm như vậy?" (Why)*, *"Bối cảnh lịch sử ra sao?"*, *"Các giải pháp thay thế đã bị loại bỏ vì lý do gì?"*.
  - Không chứa các bước thực hành từng dòng lệnh.
* **Ví dụ trong dự án**:
  - Toàn bộ thư mục `adrs/` (Architecture Decision Records).
  - `profiles/documentation/system-architecture.md` (Giải thích vì sao chọn Modular Monolith thay vì Microservices).
  - Triết lý The Anti-Crash Standard trong `README.md`.

---

## 📋 3. MA TRẬN PHÂN LOẠI & QUY TẮC VIẾT TÀI LIỆU NHANH

| Câu Hỏi Cốt Lõi | Loại Tài Liệu | Phong Cách Hành Văn | Đối Tượng Đọc |
| :--- | :---: | :--- | :--- |
| **"Hãy chỉ cho tôi cách bắt đầu"** | **Tutorial** | Cầm tay chỉ việc, từng bước tuần tự, không giải thích dài | Người mới bắt đầu (Beginner) |
| **"Làm thế nào để giải quyết vấn đề X?"** | **How-To Guide** | Hướng đến mục tiêu, tập trung vào hành động thực tế | Kỹ sư đang làm việc (Practitioner) |
| **"Cái này gồm những thuộc tính gì?"** | **Reference** | Khách quan, súc tích, chính xác từng thông số kỹ thuật | Kỹ sư cần tra cứu nhanh (Lookup) |
| **"Tại sao hệ thống lại thiết kế thế này?"** | **Explanation** | Tư duy phản biện, phân tích bối cảnh và sự đánh đổi | Tech Lead, Architect, Reviewer |

---

## 🚫 4 CẠM BẪY CẦN TRÁNH TUYỆT ĐỐI (DOCUMENTATION ANTI-PATTERNS)
1. **Trộn lẫn Tutorial vào How-To Guide**: Đưa quá nhiều lựa chọn phức tạp vào bài học cho người mới khiến họ bối rối và bỏ cuộc.
2. **Trộn lẫn Explanation vào Reference**: Chèn những đoạn triết lý dông dài vào bảng tra cứu thông số API khiến lập trình viên mất thời gian tìm kiếm.
3. **Tài liệu không được phiên bản hóa (Out-of-date Docs)**: Docs nằm ở trang wiki rời rạc bên ngoài thay vì nằm trực tiếp trong Git repo bên cạnh mã nguồn.
4. **Viết docs mà không có code mẫu chạy được**: Mọi hướng dẫn phải kèm theo snippet có thể copy-paste và kiểm thử tự động trong CI.
