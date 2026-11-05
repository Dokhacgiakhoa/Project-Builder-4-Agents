---
id: A-005
type: decision
when: "Hệ thống lớn dần, cần ranh giới module"
not_when: "Dự án nhỏ chưa có nhiều miền nghiệp vụ; hoặc đã cần triển khai/mở rộng từng phần độc lập"
---
# PROFILE: MODULAR MONOLITH

## Khi nào chọn
* Hệ thống sẽ lớn dần, cần ranh giới module rõ để chia việc (người hoặc Agent), nhưng chưa cần tách dịch vụ/triển khai riêng.
* Có thể dùng Clean Architecture **bên trong** từng module.

## Không chọn khi
* Dự án nhỏ, ít miền nghiệp vụ: [simple-layered.md](simple-layered.md) hoặc [vertical-slice.md](vertical-slice.md).
* Đã có yêu cầu triển khai/mở rộng độc lập theo từng phần: đây là bài toán dịch vụ riêng, cần ADR và hỏi người dùng, không tự quyết.

## Thư mục mục tiêu
```text
src/
├── modules/<tên-miền>/   # mỗi module: API công khai nhỏ + phần nội bộ
├── shared/               # kernel dùng chung rất mỏng
└── app.*                 # lắp ráp
```
Bản đồ miền ghi ở `specs/domains.md` của dự án.

## Ràng buộc
* Module chỉ gọi module khác qua **API công khai** (interface/DTO), không import phần nội bộ.
* Không chia sẻ bảng dữ liệu giữa module (hoặc chỉ qua view/API được khai báo).
* `shared/` không chứa nghiệp vụ.
* Rào chắn: **mức M3** ([../README.md](../README.md)): luật cấm import vào thư mục nội bộ của module khác, ADR cho mọi thay đổi ranh giới.

## Thêm một tính năng
1. Xác định module sở hữu; chưa có thì tạo module và ghi vào `specs/domains.md`.
2. Thêm vào module đó.
3. Cần dữ liệu của module khác: thêm hàm vào **API công khai** của module đó, không import trực tiếp.

## Lỗi thường gặp (Health Check bắt)
* Import chéo vào thư mục nội bộ của module khác.
* `shared/` chứa nghiệp vụ.
* Module "thần thánh" ôm nhiều miền.
