# PROFILE: LAYERED ĐƠN GIẢN (DEMO / ĐỒ ÁN / MVP)

## 1. Khi nào chọn
* Một người hoặc nhóm rất nhỏ, ít nghiệp vụ, cần ra sản phẩm nhanh.
* Dữ liệu chủ yếu là CRUD; chưa cần thay thế database hay framework.
* **Không chọn** khi nghiệp vụ phức tạp, sống nhiều năm, hoặc cần test sâu logic nghiệp vụ độc lập framework → dùng [clean-architecture.md](clean-architecture.md).

## 2. Sơ đồ thư mục mục tiêu
```text
src/
├── routes/ (hoặc controllers/, pages/)  # nhận request, gọi service, trả kết quả. KHÔNG chứa nghiệp vụ.
├── services/                            # nghiệp vụ của ứng dụng
├── data/ (hoặc repositories/, models/)  # truy cập database/API ngoài
├── lib/                                 # tiện ích dùng chung (log, config, validate)
└── config/                              # đọc biến môi trường một chỗ duy nhất
tests/                                   # phản chiếu cấu trúc src/
```

## 3. Quy tắc phụ thuộc
`routes → services → data`. Chiều ngược lại **cấm**. `routes` không truy vấn DB trực tiếp. `lib/` và `config/` ai cũng dùng được nhưng không phụ thuộc ngược vào ba tầng trên.

## 4. Thêm một tính năng
1. Ghi mục tiêu và tiêu chí chấp nhận (`tasks/task-spec.md`).
2. Viết test cho `services` (thành công + 2 trường hợp biên/lỗi).
3. Thêm hàm ở `services`, truy cập dữ liệu qua `data`.
4. Thêm route mỏng gọi service; kiểm tra dữ liệu vào ở route.
5. Chạy test/lint/build, cập nhật `docs/project-brief.md` nếu luồng đổi.

## 5. Lỗi thường gặp (Health Check bắt)
* Route chứa truy vấn DB hoặc logic dài (tầng bị rò rỉ).
* Tệp "thần thánh" > 350 dòng gom UI + state + truy vấn.
* Secret nằm trong code; thiếu `.env.example`.
* Nuốt lỗi im lặng (`catch` rỗng), `JSON.parse` không bọc xử lý lỗi.

## 6. Khi nào nâng cấp
Khi `services` phình to và test phụ thuộc DB/framework khó viết → chuyển dần sang Clean Architecture bằng một ADR mới (tách `domain` khỏi `data`).
