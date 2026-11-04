# ADR 0005: DEFINITION OF DONE (DOD) & QUALITY GATE

* **Trạng thái**: Đã phê duyệt (Accepted)
* **Ngày quyết định**: 2026-11-04

---

## 1. ĐỊNH NGHĨA "HOÀN THÀNH" (WHAT IS DONE?)
Một Task hoặc Pull Request chỉ được coi là **HOÀN THÀNH (DONE)** khi và chỉ khi thỏa mãn đầy đủ các điều kiện sau:

1. [x] **Logic & Specs**: Mã nguồn cài đặt đúng và đầy đủ theo `specs/features/`.
2. [x] **Zero Regressions**: Không phá vỡ bất kỳ tính năng hoặc test case nào đang chạy.
3. [x] **Anti-Crash Compliance**: Tuân thủ chuẩn lập trình phòng vệ trong `adrs/0003-coding-conventions.md`.
4. [x] **Automated Tests**: Bổ sung đầy đủ Unit/Integration Tests và vượt qua 100% tests trên local.
5. [x] **Lint & Static Check**: Không có lỗi linting, không có warning bảo mật nghiêm trọng.
6. [x] **Clean Git PR**: Pull Request dưới 400 dòng thay đổi, có mô tả rõ ràng theo mẫu PR template.
7. [x] **Human Review**: Được ít nhất 1 Human Tech Lead hoặc Peer Reviewer phê duyệt.
