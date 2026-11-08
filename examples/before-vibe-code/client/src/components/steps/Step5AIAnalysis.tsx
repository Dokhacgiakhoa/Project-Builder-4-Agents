import React, { useEffect, useState } from 'react';
import { Sparkles, Terminal, CheckCircle2, Loader2 } from 'lucide-react';

interface Step5Props {
  projectName: string;
  onComplete: () => void;
}

const ANALYSIS_LOGS = [
  "Đang tải ngữ cảnh dự án và trích xuất Functional Requirements...",
  "Khởi tạo cấu trúc Database Schema (Relational / NoSQL Entities)...",
  "Thiết lập mối quan hệ giữa các Models, Foreign Keys và Transactions...",
  "Xây dựng biểu đồ kiến trúc hệ thống bằng cú pháp Mermaid.js...",
  "Tổng hợp Master System Prompt tối ưu cho AI Coding Agents (Cursor / Copilot / Claude)...",
  "Hoàn tất đóng gói toàn bộ tài liệu (REQUIREMENTS.md, ARCHITECTURE.md, MASTER_PROMPT.md)!"
];

export const Step5AIAnalysis: React.FC<Step5Props> = ({ projectName, onComplete }) => {
  const [currentLogIndex, setCurrentLogIndex] = useState(0);
  const [progress, setProgress] = useState(10);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentLogIndex((prev) => {
        if (prev < ANALYSIS_LOGS.length - 1) {
          return prev + 1;
        }
        return prev;
      });

      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(timer);
          setTimeout(() => {
            onComplete();
          }, 800);
          return 100;
        }
        return prev + 18;
      });
    }, 850);

    return () => clearInterval(timer);
  }, [onComplete]);

  return (
    <div className="py-8 px-4 text-center max-w-2xl mx-auto space-y-6">
      <div className="relative w-22 h-22 mx-auto">
        <div className="octa-card-lg floating-shadow-blue relative w-22 h-22 bg-blue-700 flex items-center justify-center">
          <Sparkles className="w-11 h-11 text-orange-400" />
        </div>
      </div>

      <div className="space-y-2">
        <h2 className="text-2xl sm:text-3xl font-black text-slate-950 tracking-tight">
          AI đang phân tích kiến trúc cho <span className="text-blue-700">"{projectName}"</span>
        </h2>
        <p className="text-base text-slate-700 font-semibold">
          Hệ thống đang chuẩn bị tài liệu kỹ thuật và Master Prompt hoàn chỉnh theo đúng bộ Tech Stack bạn đã chọn.
        </p>
      </div>

      {/* Progress Bar */}
      <div className="space-y-2">
        <div className="octa-card-sm w-full bg-slate-200 h-5 overflow-hidden p-0.5 shadow-inner">
          <div
            className="octa-card-sm bg-blue-700 h-full transition-all duration-500 shadow-sm"
            style={{ width: `${Math.min(progress, 100)}%` }}
          />
        </div>
        <div className="flex justify-between text-sm font-black text-slate-700">
          <span>Tiến trình hoàn tất</span>
          <span className="text-blue-700 font-black">{Math.min(progress, 100)}%</span>
        </div>
      </div>

      {/* Terminal logs */}
      <div className="octa-card floating-shadow bg-slate-950 p-6 text-left font-mono text-sm space-y-3 max-h-60 overflow-y-auto">
        <div className="flex items-center gap-2.5 text-slate-400 pb-3">
          <Terminal className="w-5 h-5 text-orange-500" />
          <span className="font-bold text-slate-200">System Architecture Orchestrator Log:</span>
        </div>
        {ANALYSIS_LOGS.slice(0, currentLogIndex + 1).map((log, idx) => (
          <div key={idx} className="flex items-start gap-3 text-slate-200">
            {idx === currentLogIndex && progress < 100 ? (
              <Loader2 className="w-4.5 h-4.5 text-orange-500 animate-spin shrink-0 mt-0.5" />
            ) : (
              <CheckCircle2 className="w-4.5 h-4.5 text-emerald-400 shrink-0 mt-0.5" />
            )}
            <span className={idx === currentLogIndex ? 'text-orange-400 font-bold' : 'text-slate-300'}>
              {log}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
