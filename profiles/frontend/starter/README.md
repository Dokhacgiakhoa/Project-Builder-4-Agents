# 🎨 UNIVERSAL FRONTEND STARTER KIT (BULLETPROOF REACT)

Bộ khung giao diện Frontend chuẩn hóa theo kiến trúc **Feature-Driven (Bulletproof React)**, tối ưu cho sự phối hợp nhịp nhàng giữa Kỹ sư công nghệ và AI Coding Agents.

---

## 🏛️ 1. CẤU TRÚC THƯ MỤC CHUẨN

```text
frontend/src/
├── app/                  # Application Layer (AppProviders, Global Router)
├── assets/               # Global static assets (Images, SVG, Icons)
├── components/           # Shared UI Components (Button, Card, Layouts)
│   ├── layouts/          # MainLayout, Sidebar, Navbar
│   └── ui/               # Nguyên tử UI dùng chung (Buttons, Cards, Inputs)
├── config/               # Biến môi trường & cấu hình validate qua Zod
├── features/             # CÁC MODULE NGHIỆP VỤ ĐỘC LẬP (Feature-Driven)
│   ├── auth/             # Xác thực người dùng (Login, Register, Session)
│   ├── dashboard/        # Bảng điều khiển & thống kê
│   └── ai-chat/          # Module tương tác AI Agent
│       ├── api/          # Lời gọi API & React Query hooks của feature
│       ├── components/   # UI components nội bộ của feature
│       ├── types/        # TypeScript types của feature
│       └── index.ts      # Public API Export (Cổng giao tiếp duy nhất)
├── hooks/                # Custom React Hooks dùng chung
├── lib/                  # Cấu hình thư viện (Axios api-client, TanStack Query)
├── stores/               # Quản lý Global Client State qua Zustand
└── types/                # Generic API response & common types
```

---

## ⚡ 2. CÁC NGUYÊN TẮC BẤT BIẾN

1. **Feature Isolation**: Mọi component, hook hay type chỉ phục vụ cho một tính năng cụ thể thì PHẢI nằm trong thư mục của feature đó.
2. **Public API Pattern (`index.ts`)**: Mỗi feature chỉ xuất khẩu những gì bên ngoài cần dùng thông qua `index.ts`. Không import trực tiếp vào các file nội bộ của feature khác.
3. **The Anti-Crash Standard**:
   - Dữ liệu từ API luôn được kiểm tra bằng Optional Chaining (`?.`) và Safe Fallbacks (`?? []`).
   - Mọi form submission và async fetch đều bọc trong `try...catch` hoặc React Query Error Boundaries.

---

## 🚀 3. HƯỚNG DẪN BẮT ĐẦU

1. Cài đặt dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Cấu hình file môi trường:
   ```bash
   cp .env.example .env
   ```
3. Khởi chạy dev server:
   ```bash
   npm run dev
   ```
   Ứng dụng sẽ khả dụng tại: `http://localhost:3000`.
