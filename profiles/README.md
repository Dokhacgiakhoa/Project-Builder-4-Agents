---
id: K-004
type: router
when: "Cần **chọn kiểu kiến trúc / profile** phù hợp dự án"
---
# CHỌN KIỂU DỰ ÁN → KIẾN TRÚC, PATTERN, MỨC RÀO CHẮN

> Dành cho Agent. `core/` là phần bắt buộc cho mọi repo. Tệp này giúp bạn **chọn phần tùy biến** từ tín hiệu trong `docs/project-brief.md` hoặc cuộc trò chuyện. **Đừng hỏi người dùng thuật ngữ** ("bạn muốn Clean Architecture không?"); hãy suy ra từ tín hiệu, đề xuất một phương án kèm lý do một câu, rồi xin xác nhận.

## 1. Chọn kiến trúc từ tín hiệu
Đi từ trên xuống, dừng ở dòng đầu tiên khớp.

| Tín hiệu trong yêu cầu | Chọn | Tài liệu | Tín hiệu ngược (đừng chọn) |
| :-- | :-- | :-- | :-- |
| Demo, đồ án, MVP, một người làm, chủ yếu CRUD | **Layered đơn giản** | [architecture/simple-layered.md](architecture/simple-layered.md) | Nghiệp vụ có nhiều quy tắc, sống nhiều năm |
| Nhiều tính năng độc lập, nhiều người/Agent làm song song | **Vertical Slice** | [architecture/vertical-slice.md](architecture/vertical-slice.md) | Các tính năng dùng chung nhiều quy tắc lõi |
| Nhiều miền nghiệp vụ, sẽ lớn dần, cần ranh giới module | **Modular Monolith** | [architecture/modular-monolith.md](architecture/modular-monolith.md) | Dự án nhỏ; hoặc đã cần triển khai riêng từng phần |
| Nghiệp vụ phức tạp, test độc lập framework, có thể đổi hạ tầng | **Clean Architecture** (+DDD khi nghiệp vụ phong phú) | [architecture/clean-architecture.md](architecture/clean-architecture.md) | Demo/CRUD nhỏ |

Không khớp dòng nào hoặc mơ hồ: **chọn phương án đơn giản hơn** (Layered cho dự án nhỏ, Clean cho dự án có nghiệp vụ thật), ghi giả định vào ADR. Nâng cấp sau bằng ADR mới tốt hơn là over-engineering ngay từ đầu.

## 2. Chọn mức rào chắn
Rào chắn là thứ **Agent phải cài** để kiến trúc không bị phá khi dự án lớn dần (Agent hay "đi đường tắt"). Health Check kiểm tra sự có mặt của nó.

| Mức | Gồm | Dùng cho |
| :-- | :-- | :-- |
| **M1** | Lệnh lint + test + build chạy được, CI chạy đúng các lệnh đó | Layered đơn giản |
| **M2** | M1 + luật ép ranh giới import (tách project/package, hoặc luật lint cấm import chéo) | Vertical Slice, Clean Architecture |
| **M3** | M2 + ADR bắt buộc cho mọi thay đổi ranh giới, test kiến trúc trong CI | Modular Monolith, dự án nhiều người/Agent |

## 3. Thêm profile bổ sung (chỉ khi dự án có)
| Khi dự án có... | Thêm | Tài liệu |
| :-- | :-- | :-- |
| Giao diện web React | Frontend | [frontend/bulletproof-react.md](frontend/bulletproof-react.md), mã khởi đầu [frontend/starter](frontend/starter/README.md) |
| Cần diện mạo UI rõ ràng, theme sáng/tối | Design system | [design/ui-ux-archetypes-and-presets.md](design/ui-ux-archetypes-and-presets.md) |
| LLM, Agent, RAG trong sản phẩm | Ứng dụng AI | [ai-apps/agentic-patterns-and-evals.md](ai-apps/agentic-patterns-and-evals.md) |
| Ngân sách bằng 0 | Stack free tier | [stacks/cloud-free-tier-stack.md](stacks/cloud-free-tier-stack.md) |
| Cần tài liệu người dùng, runbook, onboarding | Tài liệu | [documentation/documentation-and-pitch-standards.md](documentation/documentation-and-pitch-standards.md) |

**Design pattern**: không chọn trước. Chỉ tra [patterns/design-patterns-catalog.md](patterns/design-patterns-catalog.md) khi gặp vấn đề cụ thể (nhiều biến thể cần chọn lúc chạy, tạo đối tượng phức tạp...). Pattern thêm vào mà không có vấn đề thật là over-engineering.

**Ngôn ngữ và framework**: kit không quy định. Dùng Technology Selection Gate trong `AGENTS.md` của dự án; Agent đã biết cú pháp và công cụ, kit chỉ cần quyết định và ràng buộc.

## 4. Ghi lại quyết định (bắt buộc)
1. ADR kiến trúc: tín hiệu đã thấy, phương án chọn, phương án đã loại, mức rào chắn.
2. `.builder/kit.json`: `profiles.architecture` (một trong `simple-layered`, `clean-architecture`, `vertical-slice`, `modular-monolith`), `stack`, `extras`. Health Check đối chiếu mục này với cấu trúc thư mục (`ARCH-007`).
3. Người dùng xác nhận trước khi dựng khung.

## 5. Dấu hiệu đã chọn sai (nâng/hạ cấp bằng ADR mới)
| Dấu hiệu | Hướng |
| :-- | :-- |
| Test logic phải dựng DB mới viết được; service phình to | Layered → Clean |
| Thêm một tính năng mà phải sửa nhiều chỗ ở nhiều tầng | Tầng → Vertical Slice |
| Tính năng import chéo nhau, `shared/` phình to | Vertical Slice → Modular Monolith |
| Toàn là lớp trung gian, mỗi thay đổi nhỏ phải sửa 5 tệp | Clean → hạ xuống Layered/Vertical Slice |

## 6. Khuôn cho profile mới (dành cho người bảo trì kit)
Profile kiến trúc thuộc loại `decision` và phải có đủ frontmatter (`id`, `type`, `when`, `not_when`) và các mục: *Khi nào chọn*, *Không chọn khi*, *Thư mục mục tiêu*, *Ràng buộc*, *Thêm một tính năng*, *Lỗi thường gặp*. Mỗi tài liệu có dòng trong `../INDEX.md`. `python scripts/check_links.py` kiểm tra tự động.
