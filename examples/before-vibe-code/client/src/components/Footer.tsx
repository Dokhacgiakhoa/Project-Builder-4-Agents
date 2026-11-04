import React from 'react';
import { Link } from 'react-router-dom';
import { Sparkles, Heart, ChevronRight, Server, FileCode, CheckCircle2, Github, Cpu } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="w-full bg-slate-900 text-slate-300 mt-auto relative z-10 shadow-2xl">
      {/* 100% Full Width Container (Hoàn Toàn Không Viền) */}
      <div className="w-full px-6 sm:px-10 lg:px-14 py-12 sm:py-16">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-12 gap-8 lg:gap-12">
          {/* Col 1: Brand Info & Status (5 cols) */}
          <div className="lg:col-span-5 space-y-4">
            <div className="flex items-center gap-3">
              <div className="octa-card-sm w-10 h-10 bg-blue-600 flex items-center justify-center shadow-md shadow-blue-600/30">
                <Sparkles className="w-5 h-5 text-white font-bold" />
              </div>
              <div className="flex items-center gap-2">
                <span className="font-black text-white text-xl tracking-tight">Before Vibe Code</span>
                <span className="octa-card-sm text-[10px] uppercase font-black px-2 py-0.5 bg-blue-900 text-blue-300">.NET 10 Core</span>
              </div>
            </div>

            <p className="text-sm text-slate-400 leading-relaxed font-normal max-w-md">
              Nền tảng kiến trúc hỗ trợ chuẩn hóa yêu cầu (SRS), mô hình hóa Database EF Core và sinh Master System Prompt cho cộng đồng lập trình viên cùng AI.
            </p>

            {/* System Status Pill */}
            <div className="octa-card-sm inline-flex items-center gap-2 px-3.5 py-1.5 bg-slate-800 text-slate-300 text-xs font-semibold">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              <span>ASP.NET Core Engine: <strong className="text-white">Online (Port 7292)</strong></span>
            </div>
          </div>

          {/* Col 2: Navigation Links (2 cols) */}
          <div className="lg:col-span-2 space-y-3.5">
            <h4 className="text-xs font-black uppercase tracking-wider text-slate-100">
              Trang Chính
            </h4>
            <ul className="space-y-2.5 text-sm text-slate-400 font-medium">
              <li>
                <Link to="/" className="hover:text-blue-400 transition-colors flex items-center gap-1.5 group">
                  <ChevronRight className="w-3.5 h-3.5 text-slate-600 group-hover:text-blue-400 transition-colors" />
                  <span>Trang Chủ</span>
                </Link>
              </li>
              <li>
                <Link to="/studio" className="hover:text-orange-400 transition-colors flex items-center gap-1.5 group">
                  <ChevronRight className="w-3.5 h-3.5 text-slate-600 group-hover:text-orange-400 transition-colors" />
                  <span>Setup Prompt</span>
                </Link>
              </li>
              <li>
                <Link to="/contact" className="hover:text-blue-400 transition-colors flex items-center gap-1.5 group">
                  <ChevronRight className="w-3.5 h-3.5 text-slate-600 group-hover:text-blue-400 transition-colors" />
                  <span>Liên Hệ & FAQ</span>
                </Link>
              </li>
              <li>
                <Link to="/login" className="hover:text-blue-400 transition-colors flex items-center gap-1.5 group">
                  <ChevronRight className="w-3.5 h-3.5 text-slate-600 group-hover:text-blue-400 transition-colors" />
                  <span>Đăng Nhập</span>
                </Link>
              </li>
            </ul>
          </div>

          {/* Col 3: Tech & Support (2 cols) */}
          <div className="lg:col-span-2 space-y-3.5">
            <h4 className="text-xs font-black uppercase tracking-wider text-slate-100">
              Tài Liệu .NET
            </h4>
            <ul className="space-y-2.5 text-sm text-slate-400 font-medium">
              <li>
                <a href="/swagger" target="_blank" rel="noreferrer" className="hover:text-blue-400 transition-colors flex items-center gap-1.5 group">
                  <Server className="w-3.5 h-3.5 text-blue-400" />
                  <span>Swagger API</span>
                </a>
              </li>
              <li>
                <Link to="/contact" className="hover:text-blue-400 transition-colors flex items-center gap-1.5 group">
                  <FileCode className="w-3.5 h-3.5 text-orange-400" />
                  <span>Hướng dẫn Vibe Code</span>
                </Link>
              </li>
              <li>
                <a href="https://github.com" target="_blank" rel="noreferrer" className="hover:text-blue-400 transition-colors flex items-center gap-1.5 group">
                  <Github className="w-3.5 h-3.5 text-slate-400" />
                  <span>Mã Nguồn GitHub</span>
                </a>
              </li>
            </ul>
          </div>

          {/* Col 4: Highlight Mini Card (3 cols) */}
          <div className="lg:col-span-3">
            <div className="octa-card p-5 bg-slate-800 space-y-2.5">
              <div className="flex items-center gap-2 text-white font-black text-sm">
                <Cpu className="w-4 h-4 text-orange-400" />
                <span>Kiến Trúc Đồ Án</span>
              </div>
              <p className="text-xs text-slate-400 leading-relaxed font-normal">
                ASP.NET Core (.NET 10) Web API + Entity Framework Core & SQL Server (Single Page Application React Client).
              </p>
              <div className="flex items-center gap-1 text-[11px] font-bold text-emerald-400">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                <span>Single Server Architecture</span>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Copyright Bar */}
        <div className="mt-10 pt-6 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-500 font-medium">
          <p>© {new Date().getFullYear()} Before Vibe Code Studio (ASP.NET Core .NET 10 Engine). All rights reserved.</p>
          <div className="flex items-center gap-1.5">
            <span>Made with</span>
            <Heart className="w-3.5 h-3.5 text-rose-500 fill-rose-500" />
            <span>for the .NET & Vibe Code Community</span>
          </div>
        </div>
      </div>
    </footer>
  );
};
