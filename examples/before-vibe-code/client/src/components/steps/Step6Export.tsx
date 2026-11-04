import React, { useState } from 'react';
import { Download, Copy, Check, FileText, Code2, Sparkles, RefreshCw, Layers } from 'lucide-react';
import confetti from 'canvas-confetti';

interface Step6Props {
  projectName: string;
  description: string;
  targetAudience: string;
  features: { title: string; priority: string }[];
  frontendStack: string;
  backendStack: string;
  databaseStack: string;
  nonFunctionalReqs: string[];
  onRestart: () => void;
}

export const Step6Export: React.FC<Step6Props> = ({
  projectName,
  description,
  targetAudience,
  features,
  frontendStack,
  backendStack,
  databaseStack,
  nonFunctionalReqs,
  onRestart
}) => {
  const [activeTab, setActiveTab] = useState<'prompt' | 'srs' | 'arch'>('prompt');
  const [isCopied, setIsCopied] = useState(false);

  // Trigger confetti on mount
  React.useEffect(() => {
    try {
      confetti({
        particleCount: 90,
        spread: 80,
        origin: { y: 0.6 }
      });
    } catch {
      // ignore
    }
  }, []);

  // 1. Generate Master Prompt (Adaptive to any selected Tech Stack)
  const masterPrompt = `# SYSTEM PROMPT FOR AI CODING AGENT (VIBE CODE - MULTI-STACK ARCHITECTURE)
**Role:** Bạn là Senior Fullstack Software Engineer & Solution Architect.
**Task:** Xây dựng hoàn chỉnh mã nguồn dự án: "${projectName}" với Backend là **${backendStack.split('(')[0].trim()}**, Database là **${databaseStack.split('(')[0].trim()}** và Frontend là **${frontendStack.split('(')[0].trim()}**.

## 1. TỔNG QUAN DỰ ÁN & MỤC TIÊU
- **Tên dự án:** ${projectName}
- **Mô tả nghiệp vụ:** ${description}
- **Chân dung người dùng mục tiêu:** ${targetAudience}

## 2. BỘ CÔNG NGHỆ CHUẨN (TECH STACK)
- **Backend Core:** ${backendStack}
- **Database & ORM:** ${databaseStack}
- **Frontend Client:** ${frontendStack}

## 3. DANH SÁCH TÍNH NĂNG CỐT LÕI (FUNCTIONAL REQUIREMENTS)
${features.map((f, i) => `${i + 1}. **${f.title}** (Mức độ ưu tiên: ${f.priority})`).join('\n')}

## 4. TIÊU CHUẨN CHẤT LƯỢNG & PHI CHỨC NĂNG (NON-FUNCTIONAL REQUIREMENTS)
${nonFunctionalReqs.map(n => `- ${n}`).join('\n')}

## 5. HƯỚNG DẪN THỰC HIỆN TỪNG BƯỚC (ENGINEERING BEST PRACTICES)
1. **Cấu trúc thư mục chuẩn (Clean Architecture):** Tách biệt rõ ràng tầng Controllers/Routers, Business Services/Use Cases, Repositories/Data Access và Models/Entities.
2. **Xử lý Bất đồng bộ & Hiệu năng:** Sử dụng triệt để \`async/await\`, phân trang (Pagination), validation dữ liệu đầu vào (DTOs/Schemas).
3. **Bảo mật & Phòng chống lỗi (Anti-Crash):** Bọc \`try...catch\` cho các xử lý nhạy cảm, mã hóa mật khẩu an toàn, áp dụng Global Error Handling Middleware.
4. **Clean Code & Chú thích:** Viết code tuân thủ SOLID principles, đặt tên biến chuẩn xác, comment giải thích lý do xử lý logic nghiệp vụ.
`;

  // 2. Generate SRS Markdown
  const srsMarkdown = `# Software Requirements Specification (SRS)
**Project Name:** ${projectName}
**Tech Stack:** ${backendStack.split('(')[0].trim()} + ${databaseStack.split('(')[0].trim()} + ${frontendStack.split('(')[0].trim()}
**Date:** ${new Date().toLocaleDateString('vi-VN')}

## 1. Mục Tiêu Sản Phẩm
${description}

## 2. Đối Tượng Người Dùng
${targetAudience}

## 3. Yêu Cầu Chức Năng (Functional Requirements)
${features.map((f, i) => `### FR-${(i + 1).toString().padStart(2, '0')}: ${f.title}
- **Mức độ ưu tiên:** ${f.priority}
- **Mô tả:** Người dùng có thể thực hiện tính năng ${f.title.toLowerCase()} dễ dàng, an toàn và trực quan.
`).join('\n')}

## 4. Yêu Cầu Phi Chức Năng & Tiêu Chuẩn Kỹ Thuật (NFR)
${nonFunctionalReqs.map(n => `- ${n}`).join('\n')}
`;

  // 3. Generate Architecture Markdown
  const archMarkdown = `# System Architecture & Design
**Project Name:** ${projectName}

## 1. Cấu Trúc Công Nghệ
- **Server:** ${backendStack}
- **Database:** ${databaseStack}
- **Client:** ${frontendStack}

## 2. Sơ Đồ Kiến Trúc Hệ Thống (Mermaid Diagram)

\`\`\`mermaid
graph TD
    Client["${frontendStack.split('(')[0].trim()}"] -->|RESTful API / JSON / GraphQL| API["${backendStack.split('(')[0].trim()}"]
    
    subgraph Application Server Architecture
        API --> Controllers["API Endpoints / Routers"]
        Controllers --> Services["Services Layer (Business Logic)"]
        Services --> Repositories["Repositories / Data Access Layer"]
        Repositories --> DBContext["Database Engine / ORM"]
    end

    DBContext --> DB[("${databaseStack.split('(')[0].trim()}")]
\`\`\`
`;

  const handleCopyPrompt = () => {
    navigator.clipboard.writeText(masterPrompt);
    setIsCopied(true);
    setTimeout(() => setIsCopied(false), 2000);
  };

  const handleDownloadFile = (filename: string, content: string) => {
    const blob = new Blob([content], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const handleDownloadAll = () => {
    handleDownloadFile('MASTER_PROMPT.md', masterPrompt);
    setTimeout(() => handleDownloadFile('REQUIREMENTS.md', srsMarkdown), 200);
    setTimeout(() => handleDownloadFile('ARCHITECTURE.md', archMarkdown), 400);
  };

  return (
    <div className="space-y-6">
      {/* Header Banner (Không Viền) */}
      <div className="octa-card floating-shadow-sm p-6 sm:p-8 bg-blue-50 flex flex-col md:flex-row items-start md:items-center justify-between gap-5">
        <div className="space-y-1.5">
          <div className="inline-flex items-center gap-2 text-blue-900 text-sm font-black uppercase tracking-wider">
            <Sparkles className="w-4.5 h-4.5 text-orange-600" /> Hoàn thành chuẩn bị Context Kiến Trúc!
          </div>
          <h2 className="text-2xl sm:text-3xl font-black text-slate-950">Bộ Tài Liệu & Master System Prompt Đã Sẵn Sàng</h2>
          <p className="text-base text-slate-700 font-semibold">
            Đã tùy biến chính xác theo bộ Tech Stack bạn chọn ({backendStack.split('(')[0].trim()} + {frontendStack.split('(')[0].trim()})!
          </p>
        </div>
        <div className="flex flex-wrap gap-3">
          <button
            type="button"
            onClick={handleCopyPrompt}
            className="octa-btn floating-shadow-orange inline-flex items-center gap-2 px-7 py-3.5 bg-orange-600 hover:bg-orange-700 text-white font-black text-sm sm:text-base transition-transform cursor-pointer hover:-translate-y-0.5"
          >
            {isCopied ? <Check className="w-5 h-5" /> : <Copy className="w-5 h-5" />}
            {isCopied ? 'Đã Copy Master Prompt!' : 'Copy Master Prompt (1-Click)'}
          </button>
          <button
            type="button"
            onClick={handleDownloadAll}
            className="octa-btn inline-flex items-center gap-2 px-6 py-3.5 bg-blue-100 hover:bg-blue-200 text-blue-950 font-black text-sm sm:text-base shadow-xs transition-colors cursor-pointer"
          >
            <Download className="w-5 h-5 text-blue-800" /> Tải về tất cả (.md)
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex flex-wrap gap-3">
        <button
          type="button"
          onClick={() => setActiveTab('prompt')}
          className={`octa-btn py-3 px-5 text-sm sm:text-base transition-all cursor-pointer flex items-center gap-2 ${
            activeTab === 'prompt'
              ? 'floating-shadow-blue bg-blue-700 text-white font-black'
              : 'bg-blue-100 text-blue-950 font-bold hover:bg-blue-200'
          }`}
        >
          <Sparkles className="w-4 h-4" /> MASTER_PROMPT.md
        </button>
        <button
          type="button"
          onClick={() => setActiveTab('srs')}
          className={`octa-btn py-3 px-5 text-sm sm:text-base transition-all cursor-pointer flex items-center gap-2 ${
            activeTab === 'srs'
              ? 'floating-shadow-blue bg-blue-700 text-white font-black'
              : 'bg-blue-100 text-blue-950 font-bold hover:bg-blue-200'
          }`}
        >
          <FileText className="w-4 h-4" /> REQUIREMENTS.md (SRS)
        </button>
        <button
          type="button"
          onClick={() => setActiveTab('arch')}
          className={`octa-btn py-3 px-5 text-sm sm:text-base transition-all cursor-pointer flex items-center gap-2 ${
            activeTab === 'arch'
              ? 'floating-shadow-blue bg-blue-700 text-white font-black'
              : 'bg-blue-100 text-blue-950 font-bold hover:bg-blue-200'
          }`}
        >
          <Code2 className="w-4 h-4" /> ARCHITECTURE.md (Diagram)
        </button>
      </div>

      {/* Preview Content (Không Viền) */}
      <div className="octa-card floating-shadow relative bg-slate-950 p-6 font-mono text-sm sm:text-base text-slate-100 max-h-96 overflow-y-auto leading-relaxed">
        <pre className="whitespace-pre-wrap font-mono">
          {activeTab === 'prompt' && masterPrompt}
          {activeTab === 'srs' && srsMarkdown}
          {activeTab === 'arch' && archMarkdown}
        </pre>
      </div>

      {/* Instructions */}
      <div className="octa-card floating-shadow-sm p-5 sm:p-6 bg-blue-50 flex items-start gap-4">
        <Layers className="w-6 h-6 text-blue-700 shrink-0 mt-0.5" />
        <div className="text-sm sm:text-base text-slate-800 space-y-1.5">
          <div className="font-black text-slate-950 text-base sm:text-lg">Làm thế nào để bắt đầu Vibe Code cùng AI?</div>
          <p className="text-slate-700 leading-relaxed font-semibold">
            1. Bấm nút <strong>Copy Master Prompt</strong> ở trên. <br />
            2. Mở <strong>Cursor IDE / VS Code / Claude / ChatGPT</strong> trong thư mục dự án của bạn. <br />
            3. Dán prompt này vào khung chat và yêu cầu: <em>"Hãy bắt đầu khởi tạo dự án và code theo đúng bản thiết kế kiến trúc này!"</em>.
          </p>
        </div>
      </div>

      <div className="flex justify-between items-center pt-2">
        <button
          type="button"
          onClick={onRestart}
          className="octa-btn inline-flex items-center gap-2 px-6 py-3 bg-blue-100 hover:bg-blue-200 text-blue-950 font-black text-sm sm:text-base shadow-xs transition-colors cursor-pointer"
        >
          <RefreshCw className="w-4 h-4" /> Tạo dự án mới khác
        </button>
      </div>
    </div>
  );
};
