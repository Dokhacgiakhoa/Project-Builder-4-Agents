---
name: kit-consult
description: Dùng khi cần hướng dẫn kiến trúc, pattern, design system, test, CI hoặc cách sửa phát hiện trong project-review.md mà repo chưa có hướng dẫn. Tự tra Project-Builder-4-Agents theo ý định thay vì bịa quy ước.
---

# Tra cứu Project-Builder-4-Agents

1. Đọc `.builder/kit.json` để biết địa chỉ kit (`kit_repo`, `kit_ref`) và profile đã chọn.
2. Tải `INDEX.md` của kit (raw URL: `https://raw.githubusercontent.com/<owner>/<repo>/<kit_ref>/INDEX.md`).
3. Chọn các dòng có cột "Khi nào dùng" khớp với việc đang làm (tối đa 2–3 tài liệu). Ưu tiên tài liệu thuộc profile đã chọn.
4. Đọc tài liệu đó, áp dụng, và ghi lại quyết định đáng nhớ vào `adrs/` (nếu đổi kiến trúc/hợp đồng).
5. Không tải cả kho. Không áp quy ước của profile khác với profile dự án đã chọn trừ khi có ADR đổi profile.
