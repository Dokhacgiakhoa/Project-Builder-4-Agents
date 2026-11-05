# PROFILE: VERTICAL SLICE (THEO TÍNH NĂNG)

## 1. Khi nào chọn
* Nhiều tính năng tương đối độc lập; muốn thêm/sửa tính năng mà không đụng tính năng khác.
* Nhóm nhỏ làm song song, hoặc nhiều Agent làm song song trên các tính năng khác nhau.
* **Không chọn** khi các tính năng chia sẻ nhiều quy tắc nghiệp vụ lõi phải nhất quán → cân nhắc [clean-architecture.md](clean-architecture.md) hoặc [modular-monolith.md](modular-monolith.md).

## 2. Sơ đồ thư mục mục tiêu
```text
src/
├── features/
│   ├── create-order/        # MỘT lát cắt: request → xử lý → dữ liệu → phản hồi
│   │   ├── handler.*        # điểm vào của tính năng
│   │   ├── validator.*      # kiểm tra dữ liệu vào
│   │   ├── logic.*          # nghiệp vụ riêng của tính năng
│   │   ├── data.*           # truy cập dữ liệu riêng
│   │   └── create-order.test.*
│   └── list-orders/
├── shared/                  # CHỈ những thứ thật sự dùng chung (auth, log, config, kiểu cơ bản)
└── app.*                    # lắp ráp (routing, DI)
```

## 3. Quy tắc phụ thuộc
* Tính năng **không import** tính năng khác. Cần dùng chung → rút phần chung vào `shared/` khi có **từ 2–3 nơi dùng thật** (đừng trừu tượng hóa sớm).
* `shared/` không phụ thuộc `features/`.

## 4. Thêm một tính năng
1. Tạo thư mục `features/<tên-động-từ>/` (đặt tên theo hành động người dùng).
2. Viết test của lát cắt trước (đi từ handler đến dữ liệu thật hoặc giả lập).
3. Cài `validator` → `logic` → `data` → `handler`.
4. Đăng ký handler ở `app.*`.

## 5. Lỗi thường gặp (Health Check bắt)
* Tính năng này import trực tiếp tính năng kia.
* `shared/` phình thành "bãi rác", chứa logic nghiệp vụ của một tính năng.
* Mỗi tính năng tự viết lại validate/log khác nhau (thiếu chuẩn chung ở `shared/`).
