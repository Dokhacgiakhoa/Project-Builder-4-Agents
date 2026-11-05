# Bảng Tổng Hợp UI/UX Design Archetypes & Thư Viện Mã Nguồn Mở

Tài liệu này định nghĩa chi tiết **7 Vũ trụ thẩm mỹ (Aesthetic Universes)** và **14 Phong cách thiết kế (Design Archetypes)** phổ biến nhất trong phát triển phần mềm và thiết kế số. Bộ tài liệu đóng vai trò là "Sổ tay bản thể thị giác" (Visual DNA Specification) giúp Product Manager, Designer, Human Developer và AI Agent (Claude Code, Cursor, Antigravity, v0) dễ dàng lựa chọn và hiện thực hóa giao diện đồng nhất.

---

## 📑 Mục lục 7 Vũ trụ Thẩm mỹ

1. [Vũ trụ 1: Nền tảng & Hệ điều hành (Platform & OS Emulation)](#1-vũ-trụ-nền-tảng--hệ-điều-hành-platform--os-emulation)
   - 1.1. Windows XP / 98 / 7 Retro Desktop
   - 1.2. Apple Cupertino iOS Glassmorphism
   - 1.3. Google Material You (Material Design 3)
2. [Vũ trụ 2: Siêu công nghệ & Viễn tưởng (Futuristic & Sci-Fi)](#2-vũ-trụ-siêu-công-nghệ--viễn-tưởng-futuristic--sci-fi)
   - 2.1. Cyberpunk / Sci-Fi HUD (Arwes Style)
   - 2.2. Frutiger Aero (Glossy Skeuomorphic Optimism)
   - 2.3. Synthwave / Outrun 80s Neon
3. [Vũ trụ 3: Silicon Valley "Pro Max" & Modern SaaS](#3-vũ-trụ-silicon-valley-pro-max--modern-saas)
   - 3.1. Linear / Raycast Dark Minimalist
   - 3.2. Apple Bento Grid Layout
   - 3.3. High-Motion SaaS (Magic UI & Aceternity)
4. [Vũ trụ 4: Nổi loạn & Phá cách (Anti-Design & Gen Z)](#4-vũ-trụ-nổi-loạn--phá-cách-anti-design--gen-z)
   - 4.1. Neubrutalism (Gumroad / Figma FigJam Style)
   - 4.2. Y2K Cyber Glitch & Hologram
5. [Vũ trụ 5: Trò chơi Hoài niệm & Văn hóa Geek (Retro Gaming & Geek)](#5-vũ-trụ-trò-chơi-hoài-niệm--văn-hóa-geek-retro-gaming--geek)
   - 5.1. 8-bit Console Pixel Art (NES.css)
   - 5.2. 16-bit RPG Video Game (RPGUI)
   - 5.3. Hacker Terminal & TUI (Terminal.css)
6. [Vũ trụ 6: Thủ công & Xúc giác Hữu cơ (Tactile & Handcrafted)](#6-vũ-trụ-thủ-công--xúc-giác-hữu-cơ-tactile--handcrafted)
   - 6.1. Hand-Drawn Sketch (PaperCSS & Wired-Elements)
   - 6.2. Claymorphism (3D Soft Puffy Clay)
   - 6.3. Skeuomorphism Cổ điển (Wood, Leather & Brass)
7. [Vũ trụ 7: Hàn lâm, Báo chí & Tạp chí (Editorial & Bauhaus)](#7-vũ-trụ-hàn-lâm-báo-chí--tạp-chí-editorial--bauhaus)
   - 7.1. Swiss / Bauhaus International Style
   - 7.2. Luxury Editorial & Newspaper

---

## 1. Vũ trụ Nền tảng & Hệ điều hành (Platform & OS Emulation)

### 1.1. Windows XP / 98 / 7 Retro Desktop

- **Cảm xúc & Ngữ cảnh**: Hoài niệm kỷ nguyên PC cá nhân thập niên 90-2000, tạo sự thích thú, độc lạ và phá vỡ sự rập khuôn của web hiện đại.
- **Thư viện mã nguồn mở tiêu biểu**:
  - [98.css](https://github.com/jdan/98.css) — CSS framework thuần không phụ thuộc JS tái hiện Windows 98.
  - [XP.css](https://github.com/botoxparty/XP.css) — Tái hiện theme Luna đặc trưng của Windows XP.
  - [7.css](https://github.com/khang-nd/7.css) — Tái hiện hiệu ứng kính mờ Aero của Windows 7.
- **Visual DNA & Design Tokens**:
  - *Color Palette*: Thanh tiêu đề xanh gradient `#0055ea` sang `#3a93ff`, nền xám bạc `#ece9d8`, nút đóng đỏ rực `#d93c2c`.
  - *Borders & Shadows*: Hiệu ứng dập nổi 3D Bevel kinh điển: `border-top: 2px solid #ffffff`, `border-left: 2px solid #ffffff`, `border-right: 2px solid #808080`, `border-bottom: 2px solid #808080`.
  - *Typography*: `Tahoma`, `MS Sans Serif`, `Segoe UI`, kích thước nhỏ gọn 11px - 12px.
- **Trường hợp sử dụng tốt nhất**: Web3 portfolio, ứng dụng mô phỏng hệ điều hành trên web, Easter egg marketing campaigns.

### 1.2. Apple Cupertino iOS Glassmorphism

- **Cảm xúc & Ngữ cảnh**: Sang trọng, nhẹ nhàng, tập trung tối đa vào nội dung thị giác, chuẩn mực di động cao cấp.
- **Tài liệu tham chiếu**: [Apple Human Interface Guidelines (HIG)](https://developer.apple.com/design/human-interface-guidelines/).
- **Visual DNA & Design Tokens**:
  - *Color Palette*: Nền kính mờ `rgba(255, 255, 255, 0.7)` (light) hoặc `rgba(30, 30, 35, 0.75)` (dark), viền phát sáng nhẹ `rgba(255, 255, 255, 0.2)`.
  - *Blur & Filter*: `backdrop-blur-xl`, `backdrop-saturate-150`.
  - *Border Radius*: Góc bo siêu tròn (Squircle) `rounded-3xl` (24px - 32px).
  - *Shadows*: Đổ bóng phân tầng đa chiều, mềm mịn: `box-shadow: 0 20px 40px rgba(0,0,0,0.08)`.
  - *Typography*: `SF Pro Display`, `SF Pro Text`, `-apple-system`.
- **Trường hợp sử dụng tốt nhất**: Ứng dụng Lifestyle, Mobile-first Web App, FinTech cá nhân, Dashboard chăm sóc sức khỏe.

### 1.3. Google Material You (Material Design 3)

- **Cảm xúc & Ngữ cảnh**: Thân thiện, linh hoạt, cá nhân hóa sâu sắc, dễ sử dụng cho mọi lứa tuổi.
- **Thư viện mã nguồn mở**: [Material Web (@material/web)](https://github.com/material-components/material-web).
- **Visual DNA & Design Tokens**:
  - *Color Palette*: Tonal Palettes — màu chủ đạo tự động trích xuất các sắc độ (Primary, Secondary, Tertiary, Container, Surface Tint).
  - *Shape & Elements*: Nút dạng viên thuốc (Pill-shaped `rounded-full`), nút nổi Floating Action Button (FAB).
  - *State & Interaction*: Hiệu ứng gợn sóng xúc giác (Ink Ripple Effect) khi click chuột hoặc chạm.
  - *Typography*: `Roboto`, `Google Sans`.
- **Trường hợp sử dụng tốt nhất**: Enterprise SaaS, ứng dụng năng suất công việc (Docs, Spreadsheets, CRM), hệ sinh thái Android.

---

## 2. Vũ trụ Siêu công nghệ & Viễn tưởng (Futuristic & Sci-Fi)

### 2.1. Cyberpunk / Sci-Fi HUD (Arwes Style)

- **Cảm xúc & Ngữ cảnh**: Tương lai viễn tưởng, không gian tàu vũ trụ, phòng thí nghiệm trí tuệ nhân tạo, an ninh mạng quân sự.
- **Thư viện mã nguồn mở**: [Arwes Framework](https://github.com/arwes/arwes) (Futuristic Sci-Fi UI Web Framework).
- **Visual DNA & Design Tokens**:
  - *Color Palette*: Nền đen vũ trụ `#030712`, viền và ánh sáng Neon Cyan `#00f5ff`, Neon Magenta `#ff007f`, Amber Warning `#ffb703`.
  - *Edges & Borders*: Góc cắt vát 45 độ (Chamfered Clip-path `polygon(0 0, calc(100% - 12px) 0, 100% 12px, 100% 100%, 0 100%)`).
  - *Effects*: Viền phát sáng `box-shadow: 0 0 15px rgba(0, 245, 255, 0.5)`, lưới tọa độ Radar nền, đường kẻ quét màn hình (CRT Scanlines).
  - *Typography*: `Orbitron`, `Share Tech Mono`, `Chakra Petch`.
- **Trường hợp sử dụng tốt nhất**: Giám sát hệ thống máy chủ, SOC Dashboard, Web3 Crypto Exchange, Gaming telemetry.

### 2.2. Frutiger Aero (Kỷ nguyên 2005 - 2012)

- **Cảm xúc & Ngữ cảnh**: Lạc quan công nghệ, trong lành, thân thiện với thiên nhiên (sinh thái kết hợp kỹ thuật số).
- **Visual DNA & Design Tokens**:
  - *Color Palette*: Xanh da trời quang đãng, xanh lá mạ tươi mát, trắng ngọc trai, vàng chanh.
  - *Textures & Glass*: Bong bóng nước bóng loáng, mặt nước lăn tăn, thấu kính lồi 3D phản quang ánh sáng mặt trời.
  - *Lighting*: Highlight viền trên cực sáng, gradient bóng mượt từ nhạt sang đậm.
- **Trường hợp sử dụng tốt nhất**: Ứng dụng môi trường, giáo dục, tái hiện thẩm mỹ hoài niệm Web 2.0.

### 2.3. Synthwave / Outrun 80s Neon

- **Cảm xúc & Ngữ cảnh**: Hoài niệm thập niên 80, tốc độ, màn đêm neon Miami.
- **Visual DNA & Design Tokens**:
  - *Color Palette*: Tím than sâu thẳm `#12072b`, hồng dạ quang `#ff007f`, tím sen `#9d4edd`, vàng cam hoàng hôn `#ff9e00`.
  - *Visual Elements*: Mặt trời bán nguyệt với các đường sọc ngang cắt lát, lưới phối cảnh 3D Perspective Grid chạy về vô cực.
  - *Typography*: `Monoton`, `Press Start 2P`, chữ in nghiêng tốc độ (Italicized bold display fonts).

---

## 3. Vũ trụ Silicon Valley "Pro Max" & Modern SaaS

### 3.1. Linear / Raycast Dark Minimalist

- **Cảm xúc & Ngữ cảnh**: Đẳng cấp kỹ thuật cao nhất, tốc độ xử lý tức thì, chính xác đến từng pixel, công cụ cho kỹ sư phần mềm hàng đầu.
- **Điển hình thực tế**: [Linear.app](https://linear.app), [Raycast](https://raycast.com), [Supabase](https://supabase.com).
- **Visual DNA & Design Tokens**:
  - *Color Palette*: Nền tối sâu thẳm `#08090a` / `#0f1011`, viền mảnh siêu thực `border border-white/10`, màu nhấn tím nhạt `#5e6ad2` hoặc xanh cobalt.
  - *Ambient Glow*: Quầng sáng mờ ảo phía sau khối card: `background: radial-gradient(circle, rgba(94,106,210,0.15) 0%, transparent 70%)`.
  - *Typography*: `Geist`, `Inter`, kích thước hiển thị nhỏ gọn, khoảng cách chữ (letter-spacing) `-0.02em`.
  - *Interactions*: Phím tắt hiển thị khắp nơi (Keyboard first), tooltip tức thì, không có animation thừa thãi làm chậm thao tác.

### 3.2. Apple Bento Grid Layout

- **Cảm xúc & Ngữ cảnh**: Tổ chức thông tin gọn gàng, chia ngăn thông minh, thị giác cuốn hút, tôn vinh các tính năng sản phẩm.
- **Điển hình thực tế**: Trang giới thiệu iPhone/MacBook của Apple, GitHub Copilot landing page.
- **Visual DNA & Design Tokens**:
  - *Grid Layout*: Lưới bất đối xứng `grid grid-cols-1 md:grid-cols-3 gap-4`, một số card chiếm 2 cột hoặc 2 hàng (`col-span-2`, `row-span-2`).
  - *Card Styling*: Viền mờ bo tròn `rounded-2xl`, nền gradient tối, kết hợp hình minh họa hoặc biểu đồ trực tiếp bên trong từng ngăn Bento.

### 3.3. High-Motion SaaS (Magic UI & Aceternity)

- **Cảm xúc & Ngữ cảnh**: Đột phá ấn tượng, thu hút ánh nhìn ngay giây đầu tiên, chuyển đổi cao cho landing page.
- **Thư viện mã nguồn mở**:
  - [Magic UI](https://github.com/magicuidesign/magicui) — 150+ animated components tích hợp trực tiếp với shadcn/ui.
  - [Aceternity UI](https://github.com/aceternity/aceternity-ui) — Thẻ 3D parallax, Canvas reveal, Particle canvas.
- **Visual DNA & Design Tokens**:
  - *Effects*: Border Beam (Tia sáng lướt quanh viền), Spotlight Card (Card phản chiếu đèn theo vị trí con trỏ chuột), Meteor effect (Mưa sao băng nền).

---

## 4. Vũ trụ Nổi loạn & Phá cách (Anti-Design & Gen Z)

### 4.1. Neubrutalism (Gumroad / Figma FigJam Style)

- **Cảm xúc & Ngữ cảnh**: Táo bạo, nghịch ngợm, không sợ hãi, tràn đầy năng lượng của nhà sáng tạo độc lập (Indie Maker).
- **Thư viện mã nguồn mở**: [neobrutalism-components](https://github.com/ekmas/neobrutalism-components).
- **Visual DNA & Design Tokens**:
  - *Color Palette*: Vàng chanh rực `#ffda59`, tím mộng mơ `#e0aaff`, hồng phấn `#ff90e8`, xanh mint `#bbf7d0`.
  - *Borders*: Đường viền đen tuyền dầy đặc `border-3 border-black` (hoặc `border-[2.5px]`).
  - *Box Shadow*: Đổ bóng cứng tuyệt đối không có độ mờ (0 blur): `box-shadow: 4px 4px 0px #000000`. Khi nhấn (active state): biến mất bóng `translate-x-[2px] translate-y-[2px] shadow-none`.
  - *Typography*: `Lexend Mega`, `Space Grotesk`, `Public Sans` in hoa, đậm nét.

### 4.2. Y2K Cyber Glitch & Hologram

- **Cảm xúc & Ngữ cảnh**: Cuối thập niên 90 - đầu 2000, kỷ nguyên sợ lỗi Thiên niên kỷ (Y2K bug), văn hóa âm nhạc điện tử underground.
- **Visual DNA & Design Tokens**:
  - *Color Palette*: Bạc ánh kim loại Chrome, hồng fuchsia, xanh lơ huỳnh quang.
  - *Visual Elements*: Font chữ uốn lượn như bong bóng bơm căng, nhãn dán sticker ảo, dải màu cầu vồng đa hướng Hologram, hiệu ứng rung lắc văn bản (text glitch).

---

## 5. Vũ trụ Trò chơi Hoài niệm & Văn hóa Geek (Retro Gaming & Geek)

### 5.1. 8-bit Console Pixel Art (NES.css)

- **Cảm xúc & Ngữ cảnh**: Máy chơi game 4 nút Nintendo (NES), Game Boy cổ điển, vui nhộn và gợi lại tuổi thơ.
- **Thư viện mã nguồn mở**: [NES.css](https://github.com/nostalgic-css/NES.css) (Hơn 22.000 stars trên GitHub).
- **Visual DNA & Design Tokens**:
  - *Borders*: Viền tạo bằng shadow nhiều lớp để mô phỏng bậc thang pixel (không dùng border thông thường).
  - *Elements*: Khung bong bóng lời thoại (Speech balloons), thanh năng lượng HP/MP phân đoạn, icon trái tim 8-bit.
  - *Typography*: `Press Start 2P`, font chữ pixel tỷ lệ cố định.

### 5.2. 16-bit RPG Video Game (RPGUI)

- **Cảm xúc & Ngữ cảnh**: Các game nhập vai huyền thoại như Final Fantasy VI, Chrono Trigger, Diablo II.
- **Thư viện mã nguồn mở**: [RPGUI](https://github.com/RounArts/RPGUI).
- **Visual DNA & Design Tokens**:
  - *Borders & Frames*: Khung chạm khắc bằng đá xám cổ hoặc gỗ sồi thế kỷ 16.
  - *Elements*: Rương đồ lưới ô vuông (Inventory slots), thanh cuộn trang sách giả da cổ, con trỏ găng tay sắt hiệp sĩ.

### 5.3. Hacker Terminal & TUI (Terminal.css)

- **Cảm xúc & Ngữ cảnh**: Màn hình xanh của hacker phim ma trận, console quản trị Linux, tối giản tuyệt đối, tiết kiệm tài nguyên.
- **Thư viện mã nguồn mở**: [Terminal.css](https://github.com/panr/terminal-css).
- **Visual DNA & Design Tokens**:
  - *Color Palette*: Nền đen tuyền `#000000`, chữ xanh huỳnh quang phosphor `#00ff66` hoặc màu hổ phách amber `#ffb000`.
  - *Elements*: Con trỏ nhấp nháy liên tục `_` hoặc `█`, khung viền tạo từ ký tự ASCII/Unicode (`+---+`, `| |`).
  - *Typography*: `VT323`, `Fira Code`, `JetBrains Mono`.

---

## 6. Vũ trụ Thủ công & Xúc giác Hữu cơ (Tactile & Handcrafted)

### 6.1. Hand-Drawn Sketch (PaperCSS & Wired-Elements)

- **Cảm xúc & Ngữ cảnh**: Phác thảo sơ đồ trên giấy napkin quán café, thân thiện, như do chính con người vẽ tay bằng bút máy.
- **Thư viện mã nguồn mở**:
  - [PaperCSS](https://github.com/papercss/papercss) — Khung sườn thô ráp như trang giấy vẽ.
  - [Wired Elements](https://github.com/rough-stuff/wired-elements) — Web components sinh nét vẽ ngẫu nhiên theo thuật toán Rough.js.
- **Visual DNA & Design Tokens**:
  - *Borders*: Đường viền lồi lõm không đều: `border-radius: 255px 15px 225px 15px/15px 225px 15px 255px`.
  - *Typography*: `Patrick Hand`, `Architects Daughter`, `Kalam`.

### 6.2. Claymorphism (3D Soft Puffy Clay)

- **Cảm xúc & Ngữ cảnh**: Đồ chơi đất nặn bằng đất sét dẻo Play-Doh, mềm mại, an toàn, kích thích chạm vuốt.
- **Visual DNA & Design Tokens**:
  - *Shape*: Góc bo cực đại dạng bóng hơi `rounded-3xl`.
  - *Shadow*: Kết hợp 2 lớp shadow (đổ bóng ngoài mềm + đổ bóng trong phản chiếu sáng):
    `box-shadow: 16px 16px 32px #c8d0e7, -16px -16px 32px #ffffff, inset 4px 4px 8px rgba(255,255,255,0.6)`.

### 6.3. Skeuomorphism Cổ điển

- **Cảm xúc & Ngữ cảnh**: Mô phỏng vật lý đồ vật ngoài đời thực (bàn mixer phòng thu âm, đồng hồ cơ Thụy Sĩ).
- **Visual DNA & Design Tokens**: Mặt kim loại đánh xước (brushed aluminum), các nút gạt công tắc mạ chrome, núm vặn rotary encoder có vạch chia độ chính xác.

---

## 7. Vũ trụ Hàn lâm, Báo chí & Tạp chí (Editorial & Bauhaus)

### 7.1. Swiss / Bauhaus International Style

- **Cảm xúc & Ngữ cảnh**: Trật tự lý tính tuyệt đối, cấu trúc toán học chặt chẽ, nghệ thuật hiện đại châu Âu.
- **Visual DNA & Design Tokens**:
  - *Color Palette*: Nền trắng kem `#f7f7f5`, đen tuyền `#111111`, điểm nhấn bằng 3 màu gốc cơ bản: Đỏ cờ `#e63946`, Vàng nghệ `#ffb703`, Xanh dương `#1d3557`.
  - *Layout & Geometry*: Phân chia lưới bất đối xứng cứng nhắc, sử dụng các hình khối học cơ bản (tròn, vuông, tam giác) làm điểm nhấn kiến trúc.
  - *Typography*: `Helvetica Neue`, `Arial`, tiêu đề cỡ lớn canh lề trái tuyệt đối.

### 7.2. Luxury Editorial & Newspaper

- **Cảm xúc & Ngữ cảnh**: Đẳng cấp thương hiệu xa xỉ, tạp chí thời trang Vogue, trang báo The New York Times.
- **Visual DNA & Design Tokens**:
  - *Typography*: Font Serif danh giá: `Playfair Display`, `Cinzel`, `Merriweather`, tiêu đề có gạch chân siêu mảnh 1px.
  - *Layout*: Cột báo chia nhiều cột (Multi-column layout), chữ cái đầu tiên thụt lề to (Drop Cap), khoảng cách đệm (Padding) hào phóng tạo độ thoáng đãng.

---

## 8. Bảng So Sánh Quyết Định Lựa Chọn Nhanh (Decision Matrix)

| Phong cách Archetype | Khuyến nghị dùng cho (Best For) | Không nên dùng cho (Avoid For) | Độ khó triển khai CSS |
| :--- | :--- | :--- | :---: |
| **Linear Pro Max** | SaaS B2B, Devtools, AI Product | Sản phẩm thiếu nhi, cửa hàng thời trang vintage | Trung bình |
| **Cupertino iOS** | Ứng dụng di động, FinTech, Lifestyle | Web kỹ thuật phức tạp, ứng dụng gaming | Thấp |
| **Neubrutalism** | Landing page sáng tạo, Gen Z, Web3 | Bệnh viện, bảo hiểm truyền thống, ngân hàng lớn | Rất thấp |
| **Cyberpunk HUD** | SOC, Giám sát an ninh, Crypto, Game | Báo chí tin tức, ứng dụng y tế | Cao |
| **Windows XP / 98** | Portfolio cá nhân, Easter egg, Meme tools | Bán hàng thương mại điện tử đại chúng | Trung bình |
| **Hacker Terminal** | Developer tool, CLI docs, Blog cá nhân | Trang web công ty tài chính cho người lớn tuổi | Thấp |
| **Hand-Drawn Paper** | Giáo dục trẻ em, Tool vẽ mindmap, Khảo sát | Hệ thống thanh toán ngân hàng, dashboard ERP | Trung bình |
