---
id: T-004
type: reference
when: "Hướng dẫn triển khai"
---
# HƯỚNG DẪN TRIỂN KHAI HỆ THỐNG (DEPLOYMENT GUIDE)

---

## 🚀 1. MÔI TRƯỜNG PHÁT TRIỂN LOCAL
1. Clone repository về máy:
   ```bash
   git clone https://github.com/<your-org>/<your-repo>.git
   cd Project-Builder-4-Agents
   ```
2. Tạo file `.env` từ file mẫu:
   ```bash
   cp .env.example .env
   ```
3. Cài đặt dependencies và khởi chạy theo stack tương ứng.

---

## 🌐 2. TRIỂN KHAI CLOUD FREE TIER
* **Frontend**: Kết nối repository với **Vercel**, cấu hình biến môi trường và deploy tự động.
* **Backend**: Triển khai trên **Render.com** (sử dụng Dockerfile hoặc Web Service).
* **Database**: Khởi tạo project miễn phí trên **Supabase**, lấy PostgreSQL Connection String gắn vào `.env`.
