import React, { useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { Sparkles, ArrowRight, FileText, CheckCircle2, Layers, Terminal } from 'lucide-react';
import gsap from 'gsap';

export const HomePage: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const ctx = gsap.context(() => {
      // Hero entrance animation
      gsap.fromTo(
        '.gsap-hero-item',
        { opacity: 0, y: 20 },
        { opacity: 1, y: 0, stagger: 0.12, duration: 0.7, ease: 'power2.out', clearProps: 'transform' }
      );

      // Comparison cards
      gsap.fromTo(
        '.gsap-comp-card',
        { opacity: 0, y: 25 },
        { opacity: 1, y: 0, stagger: 0.15, duration: 0.7, ease: 'power2.out', delay: 0.2, clearProps: 'transform' }
      );

      // Pillars cards
      gsap.fromTo(
        '.gsap-pillar-card',
        { opacity: 0, y: 25 },
        { opacity: 1, y: 0, stagger: 0.12, duration: 0.7, ease: 'power2.out', delay: 0.35, clearProps: 'transform' }
      );
    }, containerRef);

    return () => ctx.revert();
  }, []);

  return (
    <div ref={containerRef} className="space-y-16 py-10 sm:py-16 relative z-10 w-full max-w-[85%] mx-auto px-2 sm:px-4">
      {/* 1. Hero Section */}
      <section className="max-w-5xl mx-auto text-center px-4 space-y-6">
        <div className="gsap-hero-item inline-block">
          <div className="octa-btn inline-flex items-center gap-2 px-5 py-2.5 bg-blue-100 text-blue-950 text-sm font-black shadow-xs">
            <Sparkles className="w-4 h-4 text-orange-500" />
            <span>Giải pháp số 1 cho người Non-Tech & Developer trước khi Vibe Code</span>
          </div>
        </div>

        <h1 className="gsap-hero-item text-4xl sm:text-5xl md:text-6xl font-black text-slate-950 tracking-tight leading-tight">
          Chuẩn Bị <span className="text-blue-600">Ngữ Cảnh</span> & <span className="text-orange-500">Kiến Trúc</span> Trước Khi Cho AI Sinh Code
        </h1>

        <p className="gsap-hero-item text-lg sm:text-xl text-slate-600 max-w-3xl mx-auto leading-relaxed font-medium">
          Đừng để AI tự do đoán mò cấu trúc dự án của bạn! <strong>Before Vibe Code</strong> giúp bạn từng bước tạo 
          file yêu cầu (SRS), sơ đồ kiến trúc hệ thống và sinh <strong>Master Prompt chuẩn chỉ</strong> chỉ sau vài phút.
        </p>

        <div className="gsap-hero-item flex flex-col sm:flex-row items-center justify-center gap-4 pt-2">
          <Link
            to="/studio"
            className="octa-btn w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-8 py-3.5 bg-blue-600 hover:bg-blue-700 text-white font-black text-base shadow-md shadow-blue-600/25 transition-all duration-200 hover:scale-105 cursor-pointer"
          >
            <Sparkles className="w-5 h-5 text-orange-300" /> Bắt Đầu Setup Prompt Ngay
            <ArrowRight className="w-5 h-5" />
          </Link>
          <Link
            to="/contact"
            className="octa-btn w-full sm:w-auto inline-flex items-center justify-center gap-2 px-7 py-3.5 bg-white hover:bg-slate-50 text-slate-800 font-bold text-base shadow-sm transition-all duration-200 cursor-pointer"
          >
            Tìm Hiểu Vibe Code Là Gì?
          </Link>
        </div>
      </section>

      {/* 2. Problem & Solution Comparison (Hoàn Toàn Không Viền) */}
      <section className="w-full">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Box 1: Without Before Vibe Code */}
          <div className="gsap-comp-card opacity-100 floating-shadow">
            <div className="octa-card p-8 sm:p-10 bg-rose-50 space-y-5">
              <div className="octa-card-sm inline-flex items-center gap-2 px-3.5 py-1.5 bg-rose-200 text-rose-950 text-xs sm:text-sm font-black uppercase tracking-wider">
                Vibe Code Không Có Chuẩn Bị ❌
              </div>
              <h3 className="text-2xl font-black text-rose-950">Dự án dễ sập, crash và lạc hướng</h3>
              <ul className="space-y-3.5 text-base text-slate-800 font-semibold">
                <li className="flex items-start gap-3">
                  <span className="text-rose-600 font-black text-lg leading-none">✕</span>
                  <span>AI tự đặt tên biến, cấu trúc thư mục lộn xộn, không có kiến trúc phân tầng.</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-rose-600 font-black text-lg leading-none">✕</span>
                  <span>Quên các tiêu chuẩn bảo mật cơ bản (chưa mã hóa mật khẩu, thiếu JWT).</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-rose-600 font-black text-lg leading-none">✕</span>
                  <span>Khi dự án lớn dần lên, sửa tính năng A thì tính năng B bị hỏng (Regression).</span>
                </li>
              </ul>
            </div>
          </div>

          {/* Box 2: With Before Vibe Code */}
          <div className="gsap-comp-card opacity-100 floating-shadow">
            <div className="octa-card p-8 sm:p-10 bg-blue-50 space-y-5">
              <div className="octa-card-sm inline-flex items-center gap-2 px-3.5 py-1.5 bg-orange-500 text-white text-xs sm:text-sm font-black uppercase tracking-wider">
                Có Before Vibe Code Chuẩn Bị ✅
              </div>
              <h3 className="text-2xl font-black text-blue-950">Kiến trúc vững chắc, AI code chuẩn 100%</h3>
              <ul className="space-y-3.5 text-base text-slate-900 font-bold">
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-blue-600 shrink-0 mt-0.5" />
                  <span>Có sẵn file <code className="text-blue-900 bg-blue-200 px-2 py-0.5 font-mono text-sm font-black">REQUIREMENTS.md</code> và <code className="text-blue-900 bg-blue-200 px-2 py-0.5 font-mono text-sm font-black">ARCHITECTURE.md</code>.</span>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-blue-600 shrink-0 mt-0.5" />
                  <span>Cung cấp <strong>Master Prompt .NET</strong> nạp thẳng vào Cursor, Copilot hoặc Claude.</span>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-blue-600 shrink-0 mt-0.5" />
                  <span>Tuân thủ các mẫu thiết kế chuẩn doanh nghiệp (Repository & Service Pattern).</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* 3. 3-Pillar Features (Không Viền) */}
      <section className="w-full space-y-8">
        <div className="text-center space-y-2">
          <h2 className="text-3xl sm:text-4xl font-black text-slate-950">3 Trụ Cột Bạn Nhận Được Sau 6 Bước</h2>
          <p className="text-base text-slate-600 font-bold">Được đóng gói tự động thành file Markdown và ZIP tải về máy</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-7">
          <div className="gsap-pillar-card hover:-translate-y-1.5 transition-transform duration-300 opacity-100 floating-shadow">
            <div className="octa-card bg-white p-8 space-y-4">
              <div className="octa-card-sm w-13 h-13 bg-blue-600 text-white flex items-center justify-center shadow-sm">
                <FileText className="w-6.5 h-6.5" />
              </div>
              <h3 className="font-black text-xl text-slate-950">1. Tài liệu Yêu cầu (SRS)</h3>
              <p className="text-base text-slate-600 leading-relaxed font-normal">
                Trích xuất toàn bộ yêu cầu chức năng (FR) và phi chức năng (NFR) kèm phân loại mức độ ưu tiên rõ ràng.
              </p>
            </div>
          </div>

          <div className="gsap-pillar-card hover:-translate-y-1.5 transition-transform duration-300 opacity-100 floating-shadow">
            <div className="octa-card bg-white p-8 space-y-4">
              <div className="octa-card-sm w-13 h-13 bg-orange-500 text-white flex items-center justify-center shadow-sm">
                <Layers className="w-6.5 h-6.5" />
              </div>
              <h3 className="font-black text-xl text-slate-950">2. Sơ đồ Kiến trúc Mermaid</h3>
              <p className="text-base text-slate-600 leading-relaxed font-normal">
                Tự động sinh mã nguồn biểu đồ kiến trúc hệ thống từ Client đến Server và Database để trực quan hóa luồng dữ liệu.
              </p>
            </div>
          </div>

          <div className="gsap-pillar-card hover:-translate-y-1.5 transition-transform duration-300 opacity-100 floating-shadow">
            <div className="octa-card bg-white p-8 space-y-4">
              <div className="octa-card-sm w-13 h-13 bg-slate-900 text-white flex items-center justify-center shadow-sm">
                <Terminal className="w-6.5 h-6.5" />
              </div>
              <h3 className="font-black text-xl text-slate-950">3. Master System Prompt</h3>
              <p className="text-base text-slate-600 leading-relaxed font-normal">
                Một chuỗi Prompt đầy đủ ngữ cảnh nhất để bạn dán vào AI Coding Assistant và bắt đầu code mà không sợ bị "ngáo".
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* 4. Bottom CTA Card */}
      <section className="w-full text-center">
        <div className="floating-shadow-lg">
          <div className="octa-card-lg bg-white p-10 sm:p-16 space-y-6">
            <h2 className="text-3xl sm:text-5xl font-black text-slate-950">Sẵn sàng để Vibe Code chuẩn chỉ?</h2>
            <p className="text-base sm:text-lg text-slate-600 max-w-xl mx-auto leading-relaxed font-medium">
              Không cần biết code trước, chỉ cần có ý tưởng. Hãy để Before Vibe Code lo phần kiến trúc cho bạn!
            </p>
            <div className="pt-2">
              <Link
                to="/studio"
                className="octa-btn inline-flex items-center gap-2 px-8 py-4 bg-orange-500 hover:bg-orange-600 text-white font-black text-base shadow-md shadow-orange-500/25 transition-all duration-200 hover:scale-105 cursor-pointer"
              >
                Mở Setup Prompt Ngay <ArrowRight className="w-5 h-5" />
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};
