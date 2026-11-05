---
id: A-002
type: decision
when: "Nghiệp vụ phức tạp, test độc lập framework, đổi hạ tầng"
not_when: "Demo, CRUD nhỏ, một người làm, ít nghiệp vụ"
---
# PROFILE: CLEAN ARCHITECTURE (+ DDD KHI CẦN)

## Khi nào chọn
* Nghiệp vụ phức tạp, sống lâu, nhiều quy tắc phải nhất quán.
* Cần test logic nghiệp vụ mà không dựng DB/framework.
* Có khả năng đổi hạ tầng (database, nhà cung cấp, framework).

## Không chọn khi
* Demo, đồ án, CRUD nhỏ: dùng [simple-layered.md](simple-layered.md); chi phí DTO/interface sẽ lớn hơn lợi ích.
* Chỉ cần tách theo tính năng độc lập: [vertical-slice.md](vertical-slice.md).

## Thư mục mục tiêu
Bốn tầng đồng tâm `Domain → Application → Infrastructure → Presentation`. Bản đồ chi tiết theo .NET / Python / TypeScript: [clean-architecture-layout.md](clean-architecture-layout.md). Dùng **tên thư mục theo thông lệ ngôn ngữ**, miễn giữ đúng ranh giới tầng.

## Ràng buộc
* **Phụ thuộc chỉ hướng vào trong.** `Domain` không import gì từ tầng khác hay framework; `Application` chỉ biết `Domain` và interface do chính nó định nghĩa.
* `Domain` định nghĩa interface lưu trữ; `Infrastructure` cài đặt. Ghép nối (DI) ở **một** nơi (composition root).
* Đặt kiểm tra hợp lệ và biến đổi trạng thái **trong entity** (không để entity là túi dữ liệu).
* CQRS (tách Command/Query) chỉ áp dụng khi đọc và ghi thật sự khác nhau; không bắt buộc.
* Rào chắn: **mức M2** trở lên ([../README.md](../README.md)): cài công cụ ép ranh giới import (tách project/package hoặc luật lint) để Agent không "đi đường tắt".

## Thêm một tính năng
1. Domain: entity / value object / quy tắc.
2. Application: use case và interface cần thêm.
3. Infrastructure: cài interface.
4. Presentation: endpoint mỏng, chỉ gọi use case.
5. Viết test từ Domain/Application trước (không cần DB thật).

## Lỗi thường gặp (Health Check bắt)
* Controller chứa truy vấn DB (`ARCH-001`).
* `Domain` import ORM/HTTP; use case phụ thuộc lớp cụ thể của hạ tầng.
* Entity chỉ có getter/setter, nghiệp vụ nằm ở service thủ tục.
* Thiếu composition root; DI rải rác khắp nơi.
