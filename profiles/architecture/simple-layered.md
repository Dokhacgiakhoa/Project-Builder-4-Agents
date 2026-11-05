---
id: A-001
type: decision
when: "Demo, đồ án, MVP nhỏ, CRUD đơn giản"
not_when: "Nghiệp vụ phức tạp, sống nhiều năm, cần test sâu logic độc lập framework"
---
# PROFILE: LAYERED ĐƠN GIẢN

## Khi nào chọn
* Một người hoặc nhóm rất nhỏ, ít nghiệp vụ, cần ra sản phẩm nhanh.
* Dữ liệu chủ yếu là CRUD; chưa cần thay thế database hay framework.

## Không chọn khi
* Nghiệp vụ phức tạp hoặc sống nhiều năm, cần test sâu logic độc lập framework: dùng [clean-architecture.md](clean-architecture.md).
* Nhiều tính năng độc lập cần làm song song: dùng [vertical-slice.md](vertical-slice.md).

## Thư mục mục tiêu
```text
src/
├── routes/ (hoặc controllers/, pages/)  # nhận request, gọi service. KHÔNG chứa nghiệp vụ
├── services/                            # nghiệp vụ của ứng dụng
├── data/ (hoặc repositories/, models/)  # truy cập database/API ngoài
├── lib/                                 # tiện ích dùng chung (log, validate)
└── config/                              # đọc biến môi trường một chỗ duy nhất
tests/                                   # phản chiếu cấu trúc src/
```

## Ràng buộc
* `routes → services → data`. Chiều ngược lại **cấm**; `routes` không truy vấn DB trực tiếp.
* `lib/` và `config/` ai cũng dùng được nhưng không phụ thuộc ngược vào ba tầng trên.
* Rào chắn tối thiểu (mức M1, xem [../README.md](../README.md)): lint + test + CI chạy được.

## Thêm một tính năng
1. Ghi mục tiêu và tiêu chí chấp nhận (`tasks/task-spec.md`).
2. Viết test cho `services` (thành công + 2 trường hợp biên/lỗi).
3. Thêm hàm ở `services`, truy cập dữ liệu qua `data`.
4. Thêm route mỏng gọi service; kiểm tra dữ liệu vào ở route.
5. Chạy test/lint/build; cập nhật `docs/project-brief.md` nếu luồng đổi.

## Lỗi thường gặp (Health Check bắt)
* Route chứa truy vấn DB hoặc logic dài (rò rỉ tầng).
* Tệp "thần thánh" > 350 dòng gom UI + state + truy vấn.
* Secret trong code; thiếu `.env.example`.
* Nuốt lỗi im lặng, `JSON.parse` không bọc xử lý lỗi.

## Dấu hiệu cần nâng cấp
`services` phình to và test phải dựng DB/framework mới viết được: chuyển dần sang Clean Architecture bằng một ADR mới (tách `domain` khỏi `data`).
