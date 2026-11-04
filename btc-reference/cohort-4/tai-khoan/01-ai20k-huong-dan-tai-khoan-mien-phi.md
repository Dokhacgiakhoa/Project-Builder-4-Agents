VINUNI AI20KCHƯƠNG TRÌNH TÌM KIẾM NHÂN TÀI THỰC CHIẾN A.I

HƯỚNG DẪN ĐĂNG KÝ TÀI KHOẢN MIỄN PHÍĐỂ BẮT ĐẦU BUILD ỨNG DỤNG AI

Tài liệu dành cho các đội tham gia chương trình AK20KCập nhật: Tháng 6/2026



# MỤC LỤC



### 1. Giới thiệu — Tại sao cần tài khoản này?



### 2. Tổng quan Technology Stack AI20K



### 3. Nhóm 1: AI/LLM APIs (xử lý ngôn ngữ &amp; trí tuệ nhân tạo)



### 4. Nhóm 2: Cloud Hosting (triển khai backend &amp; frontend)



### 5. Nhóm 3: Database &amp; Vector Store (lưu trữ dữ liệu)



### 6. Nhóm 4: DevOps &amp; CI/CD (tự động hóa)



### 7. Nhóm 5: Monitoring &amp; Logging (giám sát ứng dụng)



### 8. Nhóm 6: Frontend Hosting (giao diện người dùng)



### 9. Nhóm 7: Domain &amp; DNS (tên miền)



### 10. Nhóm 8: Công cụ hỗ trợ khác



### 11. Bảng tổng hợp — Tài khoản nên đăng ký theo thứ tự ưu tiên



### 12. Checklist đăng ký — In ra &amp; đánh dấu



### 13. Cấu trúc file .env mẫu



### 14. FAQ — Câu hỏi thường gặp



# 1. Giới thiệu — Tại sao cần tài khoản này?

Trong chương trình VinUni AI20K, các đội sẽ phải build một ứng dụng AI Agent hoàn chỉnh — từ backend (FastAPI + LangGraph), frontend (Next.js/Streamlit), database, đến deployment lên cloud.

Tất cả các dịch vụ dưới đây đều có gói miễn phí (free tier) đủ dùng cho việc phát triển và demo trong thời gian chương trình (6 tuần). Bạn KHÔNG cần thẻ tín dụng cho hầu hết các dịch vụ.

⚠️ Lưu ý: Một số dịch vụ yêu cầu thẻ tín dụng để xác minh (nhưng sẽ không tính phí nếu bạn dùng trong free tier). Sẽ được ghi rõ bên cạnh mỗi dịch vụ.

💡 Mẹo: Đăng ký tài khoản là việc ĐẦU TIÊN đội nên làm trong Tuần 1. Càng sớm đăng ký, càng sớm bắt đầu code!



# 2. Tổng quan Technology Stack AI20K

Trước khi đăng ký tài khoản, hãy hiểu bạn sẽ cần gì:


| <w:tcW w:w="1842" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="1B4F72"/></w:tcPr><w:p w14:paraId="4C7B2049" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:jc w:val="center"/><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="21"/><w:szCs w:val="24"/></w:rPr><w:t>Thành phần | <w:tcW w:w="2751" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="1B4F72"/></w:tcPr><w:p w14:paraId="2A9264E4" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:jc w:val="center"/><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="21"/><w:szCs w:val="24"/></w:rPr><w:t>Công nghệ | <w:tcW w:w="2460" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="1B4F72"/></w:tcPr><w:p w14:paraId="4D354689" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:jc w:val="center"/><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="21"/><w:szCs w:val="24"/></w:rPr><w:t>Nền tảng | <w:tcW w:w="2351" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="1B4F72"/></w:tcPr><w:p w14:paraId="0FDFC918" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:jc w:val="center"/><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="21"/><w:szCs w:val="24"/></w:rPr><w:t>Mục đích |
| --- | --- | --- | --- |
| <w:tcW w:w="1842" w:type="dxa"/></w:tcPr><w:p w14:paraId="004ABDE0" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Backend | <w:tcW w:w="2751" w:type="dxa"/></w:tcPr><w:p w14:paraId="4E62E801" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>FastAPI + Python 3.11 | <w:tcW w:w="2460" w:type="dxa"/></w:tcPr><w:p w14:paraId="436B5FF5" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Render / Railway | <w:tcW w:w="2351" w:type="dxa"/></w:tcPr><w:p w14:paraId="094D09F5" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>API server cho AI Agent |
| <w:tcW w:w="1842" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="34D8FFE7" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>AI Agent | <w:tcW w:w="2751" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="03DE0422" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>LangGraph + LangChain | <w:tcW w:w="2460" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="77513D34" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>— | <w:tcW w:w="2351" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="02A5DE38" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Xử lý logic &amp; workflow của agent |
| <w:tcW w:w="1842" w:type="dxa"/></w:tcPr><w:p w14:paraId="3CF10384" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>LLM | <w:tcW w:w="2751" w:type="dxa"/></w:tcPr><w:p w14:paraId="0520C5C2" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>GPT-4o-mini / Gemini / Mistral | <w:tcW w:w="2460" w:type="dxa"/></w:tcPr><w:p w14:paraId="554F5F0B" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>OpenAI / Google / Mistral API | <w:tcW w:w="2351" w:type="dxa"/></w:tcPr><w:p w14:paraId="60FE1258" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Bộ não AI — xử lý ngôn ngữ |
| <w:tcW w:w="1842" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="7BF66443" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Database | <w:tcW w:w="2751" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="367153C1" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>PostgreSQL + pgvector | <w:tcW w:w="2460" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="34A6DEDE" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Supabase | <w:tcW w:w="2351" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="00C0B6A1" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Lưu trữ dữ liệu &amp; vector |
| <w:tcW w:w="1842" w:type="dxa"/></w:tcPr><w:p w14:paraId="179F9640" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Vector Store | <w:tcW w:w="2751" w:type="dxa"/></w:tcPr><w:p w14:paraId="6053D011" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>ChromaDB / Pinecone / Qdrant | <w:tcW w:w="2460" w:type="dxa"/></w:tcPr><w:p w14:paraId="0A620C92" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Self-host / Cloud | <w:tcW w:w="2351" w:type="dxa"/></w:tcPr><w:p w14:paraId="6E890232" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Lưu trữ embedding để tìm kiếm ngữ nghĩa |
| <w:tcW w:w="1842" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="685076B5" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Frontend | <w:tcW w:w="2751" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="71E6FE07" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Next.js / Streamlit | <w:tcW w:w="2460" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="45AC518C" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Vercel / Streamlit Cloud | <w:tcW w:w="2351" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="7EC13D33" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Giao diện người dùng |
| <w:tcW w:w="1842" w:type="dxa"/></w:tcPr><w:p w14:paraId="341E77FA" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>DevOps | <w:tcW w:w="2751" w:type="dxa"/></w:tcPr><w:p w14:paraId="0FED8FEF" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Docker + GitHub Actions | <w:tcW w:w="2460" w:type="dxa"/></w:tcPr><w:p w14:paraId="27B77CB2" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>GitHub | <w:tcW w:w="2351" w:type="dxa"/></w:tcPr><w:p w14:paraId="45378D55" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Đóng gói &amp; tự động deploy |
| <w:tcW w:w="1842" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="4FE446B4" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Monitoring | <w:tcW w:w="2751" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="03794222" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Langfuse / LangSmith | <w:tcW w:w="2460" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="5DEAC48D" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Cloud / Self-host | <w:tcW w:w="2351" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="128349E4" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Theo dõi hoạt động của AI Agent |

💡 Mẹo: Template dự án (ai20k-agent-template) đã được setup sẵn cho stack này. Bạn chỉ cần fork về và bắt đầu code!



# 3. Nhóm 1: AI/LLM APIs — Xử lý ngôn ngữ &amp; trí tuệ nhân tạo

Đây là nhóm quan trọng nhất — LLM (Large Language Model) là "bộ não" của ứng dụng AI. Mỗi đội nên đăng ký ít nhất 2-3 provider để có lựa chọn dự phòng.



## 3.1 Mistral AI — KHUYÊN DÙNG (Hào phóng nhất)

Gói miễn phí: Cấp 1 TỶ token/tháng miễn phí — không cần thẻ tín dụng!

Models: Truy cập TẤT CẢ model: Mistral Large, Mistral Small, Codestral, Pixtral

Giới hạn: 1 request/giây, 2 request/phút, 500,000 token/phút

Lưu ý: Có thể dùng data để train (có thể tắt trong Admin Console)

Đăng ký: https://console.mistral.ai

💡 Mẹo: Đây là gói LLM API miễn phí HÀO PHÓNG NHẤT hiện có. 1 tỷ token/tháng đủ để phát triển và demo nhiều lần. Ưu tiên đăng ký tài khoản này ĐẦU TIÊN!



## 3.2 Google Gemini API — KHUYÊN DÙNG (Dễ đăng ký)

Gói miễn phí: Không cần thẻ tín dụng. Lấy API key ngay trên Google AI Studio.

Model khuyên dùng: Gemini 2.5 Flash: 10 RPM, ~250 request/ngày — nhanh &amp; mạnh

Model cao cấp: Gemini 2.5 Pro: 5 RPM, ~25-100 request/ngày — giới hạn thấp hơn

Lưu ý: Giới hạn rate đã giảm đáng kể từ cuối 2025. Nên dùng Flash thay vì Pro.

Đăng ký: https://aistudio.google.com/apikey

💡 Mẹo: Chỉ cần tài khoản Google (Gmail). Lấy API key trong 30 giây. Flash model đủ mạnh cho hầu hết use case AI Agent.



## 3.3 Groq API — Tốc độ cực nhanh (Dùng cho demo)

Gói miễn phí: Không cần thẻ tín dụng. Truy cập tất cả model miễn phí.

Giới hạn: 30 request/phút, 6,000 token/phút

Models: Llama 3.x, Mixtral, Gemma, DeepSeek, Whisper (speech-to-text)

Mẹo: Nếu thêm thẻ tín dụng (không cần nạp tiền) → giới hạn tăng 10x + giảm 25% giá.

Đăng ký: https://console.groq.com

💡 Mẹo: Groq có tốc độ inference nhanh nhất hiện nay (LPU chip chuyên dụng). Tuyệt vời cho demo ngày — response gần như tức thì!



## 3.6 Cohere API — Tốt cho RAG &amp; Search

Gói miễn phí: 1,000 API calls/tháng, reset đầu mỗi tháng.

Giới hạn: 20 RPM (Chat), 100 RPM (Embed), 10 RPM (Rerank)

Đặc biệt: Command R+, Embed v3/v4, Rerank v3/3.5 — cực kỳ phù hợp cho ứng dụng RAG.

Đăng ký: https://cohere.com



# 4. Nhóm 2: Cloud Hosting — Triển khai Backend &amp; Frontend

Bạn cần cloud hosting để deploy ứng dụng lên internet, để ban giám khảo và người dùng có thể truy cập demo.



## 4.1 Render.com — KHUYÊN DÙNG CHO BACKEND

Gói miễn phí: 750 giờ instance miễn phí/tháng (chia cho các service)

Tài nguyên: 512 MB RAM, 0.1 CPU cho mỗi web service

Database: 1 GB PostgreSQL (hết hạn sau 30 ngày, rồi xóa sau 14 ngày grace)

Cold start: Service tự sleep sau 15 phút không hoạt động → mất 30-60 giây để wake up

Bandwidth: 5 GB bandwidth/tháng

Đăng ký: https://render.com

💡 Mẹo: Deploy FastAPI backend lên Render rất đơn giản — chỉ cần kết nối GitHub repo, chọn Docker, và Render tự build + deploy. Template ai20k-agent-template đã có sẵn Dockerfile!

⚠️ Lưu ý: Database miễn phí trên Render sẽ bị XÓA sau 30 ngày. Dùng Supabase (mục 5.1) thay thế cho database lâu dài.



## 4.2 Vercel — KHUYÊN DÙNG CHO FRONTEND (Next.js)

Gói miễn phí: 100 GB bandwidth/tháng

Requests: 1 triệu edge requests/tháng

Build: 6,000 build minutes/tháng

Tích hợp: Deploy tự động khi push lên GitHub

Đăng ký: https://vercel.com/signup

💡 Mẹo: Vercel là lựa chọn TỐT NHẤT cho Next.js frontend. Deploy chỉ mất 2 phút — kết nối GitHub repo → tự nhận Next.js → deploy xong!



## 4.3 Hugging Face Spaces — FREE GPU cho AI Demo!

Gói miễn phí: CPU Basic: 2 vCPU, 16 GB RAM, 50 GB disk — ngủ sau 48h không dùng

GPU miễn phí: ZeroGPU: ~3.5 phút/ngày GPU compute trên NVIDIA H200!

Phù hợp: Tốt nhất cho AI demo, gradio apps, streamlit apps

Đăng ký: https://huggingface.co/new-space

💡 Mẹo: Nếu đội cần chạy model AI nặng ( Whisper, LLM local, image generation), Hugging Face Spaces là lựa chọn duy nhất có GPU miễn phí!



## 4.5 Streamlit Community Cloud — Deploy Streamlit nhanh chóng

Gói miễn phí: Unlimited public apps (từ public GitHub repos)

Tài nguyên: 1 GB RAM (burst lên 3 GB), 2 CPU cores

URL: URL dạng your-app.streamlit.app

Đăng ký: https://streamlit.io/cloud



# 5. Nhóm 3: Database &amp; Vector Store — Lưu trữ dữ liệu

Ứng dụng AI Agent cần 2 loại lưu trữ: (1) Database truyền thống cho dữ liệu người dùng, và (2) Vector Store cho tìm kiếm ngữ nghĩa (RAG).



## 5.1 Supabase — KHUYÊN DÙNG (PostgreSQL + pgvector)

Gói miễn phí: 500 MB database, 500 MB RAM, 5 GB egress/tháng

Projects: Tối đa 2 active projects

Vector Search: Có pgvector extension — tìm kiếm vector ngay trong PostgreSQL!

Tính năng: Bao gồm: Auth (50K MAU), Storage (1 GB), Edge Functions (500K/tháng)

Lưu ý: Tự động pause sau 7 ngày không dùng

Đăng ký: https://supabase.com

💡 Mẹo: Supabase là lựa chọn TỐT NHẤT cho AI20K vì: (1) PostgreSQL tương thích với template, (2) pgvector thay thế Vector Store riêng, (3) Auth sẵn có, (4) 2 projects đủ cho dev + demo.



## 5.2 Pinecone — Vector Database chuyên dụng

Gói miễn phí: 2 GB vector storage, 5 serverless indexes

Operations: 2 triệu write units/tháng, 1 triệu read units/tháng

Embedding: 5 triệu token/tháng cho embedding inference

Đăng ký: https://www.pinecone.io



## 5.3 ChromaDB — Self-hosted, KHÔNG GIỚI HẠN

Gói miễn phí: Hoàn toàn miễn phí, open-source (Apache 2.0). Chạy local hoặc trong Docker.

Cài đặt: pip install chromadb — chạy ngay trong Python

Tương thích: Template ai20k-agent-template đã tích hợp sẵn ChromaDB.

💡 Mẹo: ChromaDB self-hosted là lựa chọn ĐƠN GIẢN NHẤT — không cần tài khoản cloud, chạy trực tiếp trong FastAPI server. Kết hợp với Supabase để có cả database truyền thống + vector search.



## 5.4 Qdrant Cloud — Vector DB miễn phí trên cloud

Gói miễn phí: 1 GB RAM, 0.5 vCPU, 4 GB disk — ~250K vectors

Features: Đầy đủ API (REST + gRPC), hybrid search, quantization

Thẻ CC: Không cần thẻ tín dụng

Đăng ký: https://cloud.qdrant.io



## 5.5 MongoDB Atlas — NoSQL miễn phí

Gói miễn phí: 512 MB storage, 100 ops/sec, 500 connections (MIỄN PHÍ mãi mãi)

Vector Search: Atlas Vector Search khả dụng trên gói M0

Đăng ký: https://www.mongodb.com/cloud/atlas/register



# 6. Nhóm 4: DevOps &amp; CI/CD — Tự động hóa



## 6.1 GitHub — BẮT BUỘC (Quản lý code &amp; CI/CD)

Gói miễn phí: Unlimited public repos, unlimited private repos

GitHub Actions: Public repos: UNLIMITED minutes. Private repos: 2,000 phút/tháng.

CI/CD sẵn: Template ai20k-agent-template đã có sẵn file .github/workflows/ci.yml

Các bước đăng ký:

Bước 1: Vào https://github.com/signup → tạo tài khoản (dùng email trường)

Bước 2: Fork repo ai20k-agent-template về tài khoản của đội

Bước 3: Invite các thành viên trong đội vào repo (Settings → Collaborators)

Bước 4: Kiểm tra GitHub Actions đã chạy (tab Actions) — CI pipeline tự test code



## 6.2 Docker Hub — Lưu trữ container images

Gói miễn phí: 100 pulls/giờ (đã login), unlimited public repos, 1 private repo

Template: Template đã có Dockerfile + docker-compose.yml

Đăng ký: https://hub.docker.com



## 6.3 GitLab CI — Thay thế GitHub (nếu muốn)

Gói miễn phí: 400 CI/CD phút/tháng trên shared runners, 5 GB storage

Self-hosted: Self-managed runners không giới hạn minutes

Đăng ký: https://gitlab.com



# 7. Nhóm 5: Monitoring &amp; Logging — Giám sát ứng dụng AI

Monitoring giúp bạn biết AI Agent đang hoạt động ra sao, có lỗi gì, và chất lượng response thế nào. Đây cũng là tiêu chí đánh giá DevOps trong Demo Day.



## 7.1 Langfuse — KHUYÊN DÙNG (Open-source, unlimited)

Cloud miễn phí: Cloud: 50,000 traces/tháng, 2 users, 30 ngày retention

Self-hosted: Self-hosted: UNLIMITED traces, UNLIMITED users — MIT license

Tương thích: Hoạt động với mọi LLM framework (LangChain, LangGraph, OpenAI SDK...)

Đăng ký: Cloud: https://cloud.langfuse.com | Self-hosted: https://github.com/langfuse/langfuse

💡 Mẹo: Langfuse self-hosted là lựa chọn TỐT NHẤT — không giới hạn, chạy trong Docker cùng FastAPI. 10x nhiều traces hơn LangSmith trên cloud!



## 7.2 LangSmith — Chính thức từ LangChain

Gói miễn phí: 5,000 traces/tháng, 1 user, 14 ngày retention

Ưu điểm: Tích hợp sâu với LangChain/LangGraph (dùng trong template)

Đăng ký: https://smith.langchain.com



## 7.3 Phoenix by Arize — Open-source AI Observability

Gói miễn phí: Hoàn toàn miễn phí, open-source. Không giới hạn.

Cài đặt: pip install arize-phoenix — chạy local

Features: Embedding visualization, drift detection, token monitoring

GitHub: https://github.com/arize-ai/phoenix



## 7.4 Grafana Cloud — Monitoring hạ tầng tổng quát

Gói miễn phí: 3 users, 10K metrics, 50 GB logs/tháng, 50 GB traces/tháng

Phù hợp: Tốt cho monitoring hạ tầng (CPU, RAM, network) — không chuyên AI

Đăng ký: https://grafana.com/cloud



# 8. Nhóm 6: Frontend Hosting — Giao diện người dùng

Tùy vào framework frontend đội chọn:


| <w:tcW w:w="1417" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="1B4F72"/></w:tcPr><w:p w14:paraId="0CB420D2" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:jc w:val="center"/><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="21"/><w:szCs w:val="24"/></w:rPr><w:t>Framework | <w:tcW w:w="1701" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="1B4F72"/></w:tcPr><w:p w14:paraId="755BDE6B" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:jc w:val="center"/><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="21"/><w:szCs w:val="24"/></w:rPr><w:t>Nền tảng | <w:tcW w:w="1984" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="1B4F72"/></w:tcPr><w:p w14:paraId="6070AFAC" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:jc w:val="center"/><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="21"/><w:szCs w:val="24"/></w:rPr><w:t>Gói miễn phí | <w:tcW w:w="1417" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="1B4F72"/></w:tcPr><w:p w14:paraId="5E103C9D" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:jc w:val="center"/><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="21"/><w:szCs w:val="24"/></w:rPr><w:t>Đánh giá | <w:tcW w:w="2551" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="1B4F72"/></w:tcPr><w:p w14:paraId="2FF238CA" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:jc w:val="center"/><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="21"/><w:szCs w:val="24"/></w:rPr><w:t>Ghi chú |
| --- | --- | --- | --- | --- |
| <w:tcW w:w="1417" w:type="dxa"/></w:tcPr><w:p w14:paraId="1EF6ED5E" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Next.js | <w:tcW w:w="1701" w:type="dxa"/></w:tcPr><w:p w14:paraId="01FCEC38" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Vercel | <w:tcW w:w="1984" w:type="dxa"/></w:tcPr><w:p w14:paraId="5EFED53E" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>100 GB BW, 1M requests | <w:tcW w:w="1417" w:type="dxa"/></w:tcPr><w:p w14:paraId="71478E81" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>⭐⭐⭐⭐⭐ | <w:tcW w:w="2551" w:type="dxa"/></w:tcPr><w:p w14:paraId="6132D9AE" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Deploy 2 phút |
| <w:tcW w:w="1417" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="053C9376" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Next.js | <w:tcW w:w="1701" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="7FF1D5C7" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Cloudflare Pages | <w:tcW w:w="1984" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="7BA3312B" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Unlimited BW, 100 projects | <w:tcW w:w="1417" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="3EA244D1" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>⭐⭐⭐⭐⭐ | <w:tcW w:w="2551" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="7236EC0D" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>BW không giới hạn |
| <w:tcW w:w="1417" w:type="dxa"/></w:tcPr><w:p w14:paraId="7275C7D5" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Streamlit | <w:tcW w:w="1701" w:type="dxa"/></w:tcPr><w:p w14:paraId="2B801BAF" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Streamlit Cloud | <w:tcW w:w="1984" w:type="dxa"/></w:tcPr><w:p w14:paraId="6CB2D23A" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Unlimited public apps | <w:tcW w:w="1417" w:type="dxa"/></w:tcPr><w:p w14:paraId="2337EA1E" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>⭐⭐⭐⭐ | <w:tcW w:w="2551" w:type="dxa"/></w:tcPr><w:p w14:paraId="331D3BB8" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Chỉ cần GitHub repo |
| <w:tcW w:w="1417" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="32021589" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Static HTML | <w:tcW w:w="1701" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="1500F559" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>GitHub Pages | <w:tcW w:w="1984" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="60D1233C" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>1 GB, 100 GB BW | <w:tcW w:w="1417" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="52418EB6" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>⭐⭐⭐⭐ | <w:tcW w:w="2551" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="380CB4C2" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Miễn phí, đơn giản |
| <w:tcW w:w="1417" w:type="dxa"/></w:tcPr><w:p w14:paraId="6089ACFC" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Bất kỳ framework | <w:tcW w:w="1701" w:type="dxa"/></w:tcPr><w:p w14:paraId="1CBE2E25" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Netlify | <w:tcW w:w="1984" w:type="dxa"/></w:tcPr><w:p w14:paraId="46FCF8D0" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>300 credits/tháng | <w:tcW w:w="1417" w:type="dxa"/></w:tcPr><w:p w14:paraId="71E22651" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>⭐⭐⭐ | <w:tcW w:w="2551" w:type="dxa"/></w:tcPr><w:p w14:paraId="0BE4DAB4" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Giới hạn mới (2025) |



# 9. Nhóm 7: Domain &amp; DNS — Tên miền

Tên miền riêng KHÔNG BẮT BUỘC cho Demo Day — bạn hoàn toàn có thể dùng URL miễn phí từ các cloud platform (yourapp.vercel.app, yourapp.onrender.com, yourapp.streamlit.app).

Tuy nhiên, nếu muốn tên miền riêng cho chuyên nghiệp:



## 9.1 Subdomain miễn phí (Không cần đăng ký)


| <w:tcW w:w="1701" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="1B4F72"/></w:tcPr><w:p w14:paraId="5620BC4C" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:jc w:val="center"/><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="21"/><w:szCs w:val="24"/></w:rPr><w:t>Nền tảng | <w:tcW w:w="2551" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="1B4F72"/></w:tcPr><w:p w14:paraId="40E49177" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:jc w:val="center"/><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="21"/><w:szCs w:val="24"/></w:rPr><w:t>Subdomain mẫu | <w:tcW w:w="3969" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="1B4F72"/></w:tcPr><w:p w14:paraId="1BAD649D" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:jc w:val="center"/><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="21"/><w:szCs w:val="24"/></w:rPr><w:t>Cách lấy |
| --- | --- | --- |
| <w:tcW w:w="1701" w:type="dxa"/></w:tcPr><w:p w14:paraId="34B4488B" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Vercel | <w:tcW w:w="2551" w:type="dxa"/></w:tcPr><w:p w14:paraId="034FCF12" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>your-team.vercel.app | <w:tcW w:w="3969" w:type="dxa"/></w:tcPr><w:p w14:paraId="27C79F76" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Tự động khi deploy Next.js |
| <w:tcW w:w="1701" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="37274E9E" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Render | <w:tcW w:w="2551" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="79FFC269" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>your-team.onrender.com | <w:tcW w:w="3969" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="63D22D21" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Tự động khi deploy FastAPI |
| <w:tcW w:w="1701" w:type="dxa"/></w:tcPr><w:p w14:paraId="35930D34" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Streamlit | <w:tcW w:w="2551" w:type="dxa"/></w:tcPr><w:p w14:paraId="656E4A65" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>your-team.streamlit.app | <w:tcW w:w="3969" w:type="dxa"/></w:tcPr><w:p w14:paraId="532901F8" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Tự động khi deploy Streamlit |
| <w:tcW w:w="1701" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="3CC753F0" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>GitHub Pages | <w:tcW w:w="2551" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="45EC042A" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>your-team.github.io | <w:tcW w:w="3969" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="0A68A145" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Tự động khi tạo GitHub Pages |
| <w:tcW w:w="1701" w:type="dxa"/></w:tcPr><w:p w14:paraId="659E4C95" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Cloudflare Pages | <w:tcW w:w="2551" w:type="dxa"/></w:tcPr><w:p w14:paraId="04ECE732" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>your-team.pages.dev | <w:tcW w:w="3969" w:type="dxa"/></w:tcPr><w:p w14:paraId="0F6E0E55" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Tự động khi deploy |
| <w:tcW w:w="1701" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="0A411C87" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>DuckDNS | <w:tcW w:w="2551" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="7EF01412" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>your-team.duckdns.org | <w:tcW w:w="3969" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="EBF5FB"/></w:tcPr><w:p w14:paraId="5B3EFD1C" w14:textId="77777777" w:rsidR="0026410A" w:rsidRPr="00FA0412" w:rsidRDefault="00000000"><w:pPr><w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:pPr><w:r w:rsidRPr="00FA0412"><w:rPr><w:sz w:val="20"/><w:szCs w:val="24"/></w:rPr><w:t>Dynamic DNS, cần cập nhật |



## 9.2 Tên miền trả phí

Giá rẻ: Porkbun.com — tên miền .xyz, .top từ $1-2/năm

Phổ biến: Namecheap.com — nhiều lựa chọn, ~$2-5/năm cho TLD rẻ

Minh bạch: Cloudflare Registrar — giá at-cost (không markup)

💡 Mẹo: Tên miền riêng là "nice to have" — KHÔNG ảnh hưởng điểm đánh giá. Ưu tiên thời gian cho việc build app hơn!



# 10. Nhóm 8: Công cụ hỗ trợ khác



## 10.1 ngrok — Chia sẻ localhost cho người khác test

Gói miễn phí: 1 tunnel, URL random (đổi mỗi 2 giờ), 1 GB bandwidth/tháng

Dùng khi: Tốt cho test nhanh — cho teammate hoặc mentor xem app đang chạy local

Đăng ký: https://ngrok.com



## 10.2 Postman — Test API

Gói miễn phí: Core API testing cho 1 user, 5,000 AI credits/tháng

Dùng cho: Test các endpoint FastAPI (/api/v1/chat, /api/v1/status)

Đăng ký: https://www.postman.com



## 10.3 Figma — Thiết kế giao diện

Gói miễn phí: 3 design files + 3 FigJam files, unlimited personal drafts

Dùng cho: Wireframe UI/UX cho ứng dụng AI Agent

Đăng ký: https://www.figma.com



## 10.4 Sentry — Error tracking

Gói miễn phí: 5,000 error events/tháng, unlimited projects

Dùng cho: Tự động bắt lỗi trong FastAPI app, gửi alert

Đăng ký: https://sentry.io



# 14. FAQ — Câu hỏi thường gặp

Q: Tôi có cần thẻ tín dụng không?

A: Hầu hết KHÔNG CẦN. Mistral, Google Gemini, Groq, Together AI, Cohere, Supabase, Qdrant, Langfuse, GitHub, Docker Hub đều không yêu cầu thẻ tín dụng. Chỉ Render (cho một số tính năng) và Railway có thể yêu cầu.

Q: Tôi nên dùng LLM nào?

A: Khuyến nghị: Mistral (1 tỷ token free) làm chính, Google Gemini Flash làm backup, Groq cho demo cần tốc độ. Nếu template yêu cầu OpenAI cụ thể → đăng ký OpenAI và dùng GPT-4o-mini (rẻ nhất).

Q: Free tier có đủ cho Demo Day không?

A: CÓ. Tất cả các dịch vụ trên đều đủ cho 6 tuần phát triển + Demo Day. Lưu ý: (1) Render database miễn phí hết hạn 30 ngày — dùng Supabase, (2) OpenAI credit $5 sẽ hết nhanh nếu dùng GPT-4o — ưu tiên GPT-4o-mini hoặc Mistral.

Q: Làm sao để tiết kiệm credit?

A: (1) Dùng Mistral/Gemini/Groq (free) thay vì OpenAI cho development. (2) Dùng GPT-4o-mini thay vì GPT-4o khi phải dùng OpenAI. (3) Tắt debug mode khi không cần. (4) Dùng ChromaDB local thay vì Pinecone cloud. (5) Giảm token output bằng prompt ngắn gọn.

Q: Render sleep sau 15 phút — sao cho app luôn sẵn sàng cho Demo?

A: (1) Dùng script ping mỗi 10 phút (cron job hoặc GitHub Actions). (2) Hoặc upgrade lên paid plan ($7/tháng). (3) Hoặc deploy trên Railway/UptimeRobot. (4) Wake up thủ công trước demo 1 phút.

Q: Nhiều người trong đội có dùng chung tài khoản được không?

A: GitHub: Mỗi người 1 tài khoản → collaborate trên repo. Vercel/Render: 1 tài khoản đội → share login hoặc invite members. API keys: Share qua file .env (KHÔNG commit lên GitHub).

Q: Template dùng OpenAI, nhưng tôi muốn dùng Mistral/Gemini — được không?

A: ĐƯỢC! Template dùng LangChain — hỗ trợ nhiều provider. Chỉ cần thay đổi get_llm() trong src/services/llm.py. Ví dụ: ChatMistralAI thay vì ChatOpenAI. Xem hướng dẫn trong docs/guide/chapter-04.md của template.

Q: Tôi có thể dùng ChatGPT Plus / Claude Pro subscription thay vì API không?

A: KHÔNG. ChatGPT Plus / Claude Pro là subscription cho chat interface, KHÔNG phải API access. Bạn cần đăng ký API riêng (platform.openai.com, console.anthropic.com). API tính phí theo token sử dụng.

───

Chúc các đội xây dựng thành công ứng dụng AI!VinUni AI20K — Tìm Kiếm Nhân Tài Thực Chiến A.I

