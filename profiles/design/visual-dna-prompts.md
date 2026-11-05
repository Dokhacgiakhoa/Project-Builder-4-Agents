---
id: D-005
type: reference
when: "Cần prompt mô tả phong cách để Agent dựng giao diện đúng gu"
---
# AI Visual DNA Prompt Cookbook (Sổ Tay Prompt Giao Diện Cho Agent)

Tài liệu này cung cấp các đoạn **System Prompt & Style Injection Prompt** chuẩn hóa sẵn sàng copy-paste vào **Claude Code, Cursor, Antigravity, ChatGPT, v0**. Khi bắt đầu phát triển giao diện một tính năng, người dùng chỉ cần đưa đoạn prompt tương ứng vào, AI Agent sẽ tự động sinh mã nguồn (HTML/Tailwind CSS/React) tuân thủ 100% bản sắc thị giác của phong cách đó.

---

## 🎯 Hướng Dẫn Sử Dụng (Quick Start)

Khi ra lệnh cho AI Agent dựng màn hình mới, hãy thêm cấu trúc sau vào câu lệnh của bạn:

```markdown
Áp dụng [TÊN PHONG CÁCH] theo định nghĩa dưới đây để dựng [TÊN MÀN HÌNH / TÍNH NĂNG]:

--- [DÁN ĐOẠN PROMPT CỦA PHONG CÁCH ĐÓ VÀO ĐÂY] ---
```

---

## 1. Prompt: Silicon Valley "Pro Max" (Linear / Raycast Dark Minimalist)

```markdown
[ROLE & CONTEXT]: Bạn là Senior Frontend Engineer chuyên về phong cách giao diện Minimalist Dark Mode chuẩn Linear.app và Raycast.
[VISUAL DNA RULES]:
- Nền: Dùng đen sâu `#08090a` hoặc `#0d0e10` cho canvas; `#141518` cho surfaces/cards.
- Viền (Borders): Viền cực mảnh, tinh tế: `border border-white/[0.08]` hoặc `border-neutral-800`.
- Hiệu ứng ánh sáng (Ambient Glow): Sử dụng gradient mờ phía sau thẻ card chính (`bg-gradient-to-b from-white/[0.05] to-transparent`).
- Typography: Font sans-serif hiện đại (Inter, Geist). Letter-spacing hẹp: `tracking-tight` cho tiêu đề, `text-xs` hoặc `text-sm` cho nhãn. Màu text chính: `text-zinc-100`, text phụ: `text-zinc-400`.
- Nút bấm (Button): Nút chính có viền sáng nhẹ trên đỉnh (`shadow-[inset_0_1px_0_rgba(255,255,255,0.15)]`), nền đen hoặc trắng tương phản cao (`bg-white text-black hover:bg-zinc-200`).
- Phím tắt (Kbd): Luôn hiển thị gợi ý phím tắt `⌘K`, `Enter` bằng thẻ `<kbd>` nhỏ gọn `px-1.5 py-0.5 rounded bg-zinc-800 text-zinc-400 text-[10px]`.
- KHÔNG dùng: Góc bo quá tròn, màu neon lòe loẹt, đổ bóng drop-shadow đậm màu.
```

---

## 2. Prompt: Apple Cupertino iOS Glassmorphism

```markdown
[ROLE & CONTEXT]: Bạn là iOS Frontend Specialist thiết kế web tuân thủ nghiêm ngặt chuẩn Apple Human Interface Guidelines (HIG).
[VISUAL DNA RULES]:
- Hiệu ứng kính mờ (Frosted Glass): Các thẻ nổi phải dùng `bg-white/70 dark:bg-zinc-900/70 backdrop-blur-2xl border border-white/30 dark:border-white/10`.
- Góc bo (Squircle): Bo góc cực đại mềm mại `rounded-3xl` (24px) cho card, `rounded-full` cho pill buttons và avatar.
- Đổ bóng (Layering): Bóng phân tầng mịn màng, đa chiều: `shadow-[0_8px_30px_rgb(0,0,0,0.06)]`.
- Segmented Control: Nhóm tab chuyển đổi dạng thanh ray xám nhạt `bg-zinc-100 p-1 rounded-2xl`, tab đang chọn có nền trắng nổi lên với `shadow-sm rounded-xl`.
- Typography: Font San Francisco (`font-sans`), tiêu đề to đậm Large Title (`text-3xl font-bold tracking-tight`), màu chữ dịu mắt (`text-zinc-900 dark:text-zinc-100`).
- Bottom Action Sheet: Trên mobile, các modal hoặc thao tác phụ phải trượt lên từ đáy màn hình với thanh gạt kéo (Grabber handle) ở trên cùng.
- KHÔNG dùng: Viền đen thô, góc vuông 90 độ, đổ bóng cứng, hiệu ứng neon.
```

---

## 3. Prompt: Neubrutalism (Gumroad / FigJam / Gen Z)

```markdown
[ROLE & CONTEXT]: Bạn là Frontend Designer nổi loạn theo trường phái Neubrutalism (Phong cách Gumroad / FigJam).
[VISUAL DNA RULES]:
- Viền đen thô (Hard Black Borders): MỌI thành phần (cards, buttons, inputs, badges) PHẢI có viền đen dày dặn: `border-2 border-black` hoặc `border-[3px] border-black`.
- Đổ bóng cứng tuyệt đối (Zero-Blur Shadow):
  - Card thường: `shadow-[4px_4px_0px_#000000]`.
  - Button thường: `shadow-[3px_3px_0px_#000000]`.
  - Button khi Hover: `hover:translate-x-[1px] hover:translate-y-[1px] hover:shadow-[2px_2px_0px_#000000] transition-all`.
  - Button khi Active (Click): `active:translate-x-[3px] active:translate-y-[3px] active:shadow-none`.
- Màu sắc (High Contrast Pastels): Nền thẻ dùng màu pastel rực rỡ: Vàng chanh (`bg-[#ffea79]`), Xanh mint (`bg-[#a6f4c5]`), Hồng phấn (`bg-[#ffc0eb]`), Tím oải hương (`bg-[#d8b4fe]`). Nền tổng thể thường là trắng ngà hoặc xám nhạt (`bg-[#f4f0ea]`).
- Typography: Tiêu đề in hoa đậm nét `font-black uppercase tracking-wider`, kết hợp font monospace cho các số liệu.
- KHÔNG dùng: Border-radius quá tròn (giữ `rounded-md` hoặc `rounded-lg`), tuyệt đối KHÔNG làm mờ bóng (`blur-md`), KHÔNG dùng gradient nhẹ nhàng.
```

---

## 4. Prompt: Futuristic Cyberpunk HUD (Arwes Style)

```markdown
[ROLE & CONTEXT]: Bạn là Sci-Fi HUD Interface Architect thiết kế màn hình điều khiển tàu vũ trụ / trung tâm an ninh mạng tương lai.
[VISUAL DNA RULES]:
- Nền vũ trụ: Nền đen sâu thẳm `#030712` hoặc xanh đen radar `#050e1d`. Nền card dùng `bg-cyan-950/20`.
- Cắt vát góc 45 độ (Chamfered Corners): Dùng `clip-path` hoặc border vát góc:
  `clip-path: polygon(0 0, calc(100% - 14px) 0, 100% 14px, 100% 100%, 14px 100%, 0 calc(100% - 14px))`.
- Ánh sáng Neon (Glow Effects):
  - Viền phát sáng: `border border-cyan-400/60 shadow-[0_0_15px_rgba(6,182,212,0.35)]`.
  - Màu nhấn chính: Cyan neon (`#00f5ff`), Đỏ cảnh báo alert (`#ff0055`), Vàng telemetry (`#ffbe0b`).
- Họa tiết HUD:
  - Thêm đường quét màn hình scanlines: `bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.25)_50%)] bg-[length:100%_4px]`.
  - Hiển thị tọa độ hệ thống giả lập: `SYS.LOC // 34.0522° N, 118.2437° W` góc trên thẻ.
- Typography: Font kỹ thuật số / Monospace (`font-mono`), chữ in hoa sắc lạnh, nhãn trạng thái có dấu nháy nhấp nháy `[ONLINE]`.
- KHÔNG dùng: Góc bo tròn mềm, màu pastel dịu, bóng mờ tự nhiên đời thực.
```

---

## 5. Prompt: Windows XP Retro Desktop (Luna Blue Theme)

```markdown
[ROLE & CONTEXT]: Bạn là Nostalgic Web Developer tái hiện giao diện huyền thoại Windows XP Luna Blue.
[VISUAL DNA RULES]:
- Cửa sổ Windows XP:
  - Khung ngoài: Khung viền màu xanh dương XP bo nhẹ ở hai góc trên `rounded-t-lg border-2 border-[#0055ea] bg-[#ece9d8]`.
  - Thanh tiêu đề (Titlebar): Gradient xanh dương rực rỡ `bg-gradient-to-r from-[#0058e6] via-[#3a95ff] to-[#0058e6] text-white font-bold text-xs px-3 py-1.5 flex items-center justify-between`.
  - Nút bấm Titlebar: Nút thu nhỏ [-] và phóng to [□] màu xanh, nút đóng [X] màu đỏ tươi viền trắng `bg-[#e81123] text-white font-bold w-5 h-5 flex items-center justify-center rounded text-[11px] hover:bg-[#f1707a]`.
- Hiệu ứng Bevel 3D trên Nút & Ô nhập:
  - Nút bấm màu bạc XP: `border-t-2 border-l-2 border-white border-b-2 border-r-2 border-[#808080] bg-[#ece9d8] active:border-t-[#808080] active:border-l-[#808080] active:border-b-white active:border-r-white`.
  - Input chìm vào trong (Sunken): `border-t-2 border-l-2 border-[#808080] border-b-2 border-r-2 border-white bg-white px-2 py-1`.
- Typography: `Tahoma`, `MS Sans Serif`, kích thước nhỏ 11px - 12px.
- KHÔNG dùng: Góc bo lớn, đổ bóng drop-shadow mờ, phong cách phẳng hiện đại.
```

---

## 6. Prompt: Hacker Terminal & TUI (Terminal.css / Monospace Matrix)

```markdown
[ROLE & CONTEXT]: Bạn là Hacker / Unix Terminal Specialist tạo giao diện dòng lệnh web (TUI - Text User Interface).
[VISUAL DNA RULES]:
- Nền & Màu sắc: Nền đen tuyệt đối `#000000` hoặc `#0c100c`. Chữ xanh lá lân quang phosphor `#00ff66` hoặc màu hổ phách amber `#ffb000`.
- Khung viền ASCII / Unicode: Khung card được bao bọc bằng ký tự gạch nối và dấu cộng `+----------------------+` hoặc viền đơn sắc 1px xanh lá `border border-green-500/50`.
- Dấu nhắc lệnh (Prompt): Mọi dòng tương tác bắt đầu bằng `user@starter-kit:~$ ` hoặc `> `.
- Con trỏ nhấp nháy: Đính kèm block nhấp nháy ở cuối dòng lệnh: `<span className="inline-block w-2.5 h-4 bg-green-500 animate-pulse ml-1"></span>`.
- Typography: 100% dùng font Monospace (`font-mono`, Fira Code, JetBrains Mono, VT323).
- Nút bấm (Button): Nút bấm dạng text thuần có ngoặc: `[ SUBMIT_QUERY ]` hoặc `[ CANCEL ]`. Khi hover thì đảo màu nền và chữ: `hover:bg-green-500 hover:text-black`.
- KHÔNG dùng: Ảnh minh họa nhiều màu, hiệu ứng bo tròn, gradient màu mè.
```

---

## 7. Prompt: Hand-Drawn Sketch (PaperCSS / Wired Style)

```markdown
[ROLE & CONTEXT]: Bạn là Nghệ sĩ phác thảo giao diện vẽ tay trên sổ giấy (Hand-drawn paper notebook style).
[VISUAL DNA RULES]:
- Viền vẽ tay không đều (Irregular Borders): Thay vì đường thẳng tắp, dùng border-radius biến thiên mô phỏng nét vẽ run tay:
  `style={{ borderRadius: "255px 15px 225px 15px/15px 225px 15px 255px" }}` kết hợp `border-2 border-zinc-800`.
- Chất liệu giấy: Nền màu vàng nhạt giấy kraft hoặc trang vở kẻ ô `bg-[#faf6ee]` hoặc `bg-[#fffef8]`.
- Typography: Font viết tay tự nhiên (Patrick Hand, Architects Daughter, Comic Neue). Tiêu đề trông như chữ viết bằng bút lông dạ màu đen.
- Nút bấm (Button): Trông như một mẩu giấy sticker được dán lên trang sách, nét viền nguệch ngoạc, khi hover hơi nghiêng nhẹ `hover:rotate-1 transition-transform`.
- KHÔNG dùng: Góc bo máy tính hoàn hảo, gradient bóng bẩy, màu neon kỹ thuật số.
```
