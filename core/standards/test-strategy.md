# ADR 0004: AUTOMATED TESTING STRATEGY (TDD)

* **Trạng thái**: Đã phê duyệt (Accepted)
* **Ngày quyết định**: 2026-11-04

---

## 1. KIM TỰ THÁP KIỂM THỬ (TEST PYRAMID)
* **Unit Tests (70%)**: Kiểm thử các hàm xử lý logic nghiệp vụ độc lập, hàm tính toán, helper functions. Mocking toàn bộ I/O bên ngoài.
* **Integration Tests (20%)**: Kiểm thử luồng tích hợp giữa Controller -> Service -> Repository / Database.
* **Contract Tests / E2E (10%)**: Kiểm thử tính tương thích giữa API Request/Response so với file OpenAPI Spec.

## 2. NGUYÊN TẮC TDD CHO AI AGENT
* *"Test là hợp đồng hành vi của hệ thống"*.
* Khi nhận task, Agent phải viết test case cho Happy Path và ít nhất 2 Failure Cases trước.
* Mã code hoàn thành chỉ khi toàn bộ test suite chạy XANH (PASS 100%).
