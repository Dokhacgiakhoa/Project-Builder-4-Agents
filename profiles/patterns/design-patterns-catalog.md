# CẨM NANG TRA CỨU DESIGN PATTERNS TRONG PHẦN MỀM & AI
*(Software & AI Agentic Design Patterns Catalog)*

---

## 🏛️ PHẦN 1: GOF CLASSIC DESIGN PATTERNS

### 1. Creational Patterns (Mẫu Khởi Tạo)
* **Factory Method**: Đóng gói việc khởi tạo đối tượng, cho phép lớp con quyết định loại đối tượng cần tạo.
  - *Use Case*: Khởi tạo các LLM Provider (`get_llm(provider="mistral" | "gemini" | "groq")`).
* **Builder**: Tách rời việc xây dựng một đối tượng phức tạp khỏi biểu diễn của nó.
  - *Use Case*: Xây dựng Prompt Templates hoặc Agent State Configuration.

### 2. Structural Patterns (Mẫu Cấu Trúc)
* **Adapter (Wrapper)**: Chuyển đổi giao diện của một lớp thành giao diện khác mà client mong đợi.
  - *Use Case*: Bọc API của các bên thứ ba (Stripe, SendGrid) thành các Interface chuẩn của Domain.
* **Decorator**: Gắn thêm trách nhiệm mới cho đối tượng một cách linh hoạt mà không cần kế thừa.
  - *Use Case*: Gắn thêm Logging, Caching, hoặc Rate Limiting vào API Service.
* **Facade**: Cung cấp một giao diện đơn giản cho một hệ thống con phức tạp.

### 3. Behavioral Patterns (Mẫu Hành Vi)
* **Mediator**: Định nghĩa một đối tượng đóng gói cách thức một tập hợp các đối tượng tương tác với nhau.
  - *Use Case*: Thư viện MediatR trong CQRS để gửi Command/Query đến Handler tương ứng.
* **Strategy**: Định nghĩa một họ thuật toán, đóng gói từng thuật toán và làm cho chúng có thể hoán đổi cho nhau.
  - *Use Case*: Chiến lược Chunking văn bản trong RAG (Fixed-size, Recursive, Semantic chunking).
* **Observer / Domain Events**: Khi một đối tượng thay đổi trạng thái, tất cả các thành phần phụ thuộc sẽ được thông báo tự động.

---

## 🏢 PHẦN 2: ENTERPRISE & ARCHITECTURAL PATTERNS

### 1. Repository & Unit of Work Pattern
* **Repository**: Đóng vai trò như một bộ sưu tập các thực thể trong bộ nhớ, che giấu chi tiết của cơ sở dữ liệu.
* **Unit of Work**: Duy trì danh sách các nghiệp vụ thay đổi trong một transaction và commit đồng thời.

### 2. Outbox Pattern
* Đảm bảo tính nhất quán dữ liệu (Guaranteed Delivery) giữa việc lưu DB và gửi Event ra Message Broker (Kafka/RabbitMQ) mà không bị mất dữ liệu khi mất kết nối mạng.

### 3. Circuit Breaker Pattern
* Tự động ngắt kết nối tạm thời tới một dịch vụ bên ngoài khi dịch vụ đó liên tục bị lỗi hoặc timeout, tránh làm cạn kiệt tài nguyên của hệ thống chính.

---

## 🤖 PHẦN 3: AI-NATIVE & AGENTIC DESIGN PATTERNS

| Mẫu Thiết Kế | Mô Tả & Bản Chất | Use Case Thực Tế |
| :--- | :--- | :--- |
| **ReAct Loop** | Kết hợp giữa Reasoning (Suy luận) và Action (Thực thi Tool) | Agent tra cứu dữ liệu web hoặc truy vấn SQL từng bước |
| **Semantic Router** | Định tuyến yêu cầu dựa trên độ tương đồng vector embedding | Phân luồng câu hỏi của user về đúng domain chuyên môn |
| **Supervisor Swarm** | Một tác tử chủ điều phối các tác tử con độc lập | Điều phối luồng làm việc giữa Coder Agent và Reviewer Agent |
| **RAG Triad Eval** | Bộ 3 tiêu chí đo lường: Faithfulness, Relevance, Precision | Đánh giá chất lượng pipeline tìm kiếm ngữ nghĩa tự động |
| **Model Context Protocol (MCP)** | Chuẩn giao tiếp mở kết nối LLM với Tools và Data Sources | Cho phép Agent truy xuất database, terminal, APIs đồng nhất |
| **Human-in-the-Loop (HITL)** | Chốt chặn an toàn yêu cầu xác nhận từ con người | Phê duyệt giao dịch thanh toán hoặc deploy code production |
