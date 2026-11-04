import React, { useState } from 'react';
import { Mail, MessageSquare, Send, HelpCircle, CheckCircle2, MapPin, Github } from 'lucide-react';

const FAQS = [
  {
    q: "Vibe Code là gì?",
    a: "Vibe Code là thuật ngữ chỉ việc bạn chỉ cần tập trung vào ý tưởng, kiến trúc và điều hướng để AI (như Cursor, GitHub Copilot, Claude) viết 90-95% mã nguồn thực tế."
  },
  {
    q: "Tại sao người non-tech lại cần 'Before Vibe Code'?",
    a: "Nếu bạn không chuẩn bị kỹ yêu cầu (SRS) và kiến trúc hệ thống trước, AI sẽ tự đoán mò logic, dẫn đến code bị lỗi xung đột, không thể chạy hoặc khó mở rộng sau này."
  },
  {
    q: "Sau khi xuất Master Prompt thì làm gì tiếp theo?",
    a: "Bạn chỉ cần copy chuỗi Master Prompt, dán vào khung chat của Cursor hoặc Visual Studio và bảo AI: 'Hãy tạo dự án theo đúng bản thiết kế này!'."
  }
];

export const ContactPage: React.FC = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [isSent, setIsSent] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name || !email || !message) return;
    setIsSent(true);
    setName('');
    setEmail('');
    setMessage('');
    setTimeout(() => setIsSent(false), 4000);
  };

  return (
    <div className="w-full max-w-[85%] mx-auto px-4 py-10 sm:py-16 space-y-16 relative z-10">
      {/* Header */}
      <div className="text-center space-y-3">
        <div className="octa-card-sm inline-flex items-center gap-2 px-4 py-2 bg-blue-100 text-blue-950 text-sm font-black">
          <Mail className="w-4 h-4 text-orange-600" /> Hỗ Trợ & Góp Ý
        </div>
        <h1 className="text-3xl sm:text-5xl font-black text-slate-950">Liên Hệ Với Đội Ngũ Phát Triển</h1>
        <p className="text-base sm:text-lg text-slate-700 max-w-xl mx-auto font-semibold">
          Bạn có thắc mắc về quy trình Vibe Code hoặc muốn đóng góp ý tưởng phát triển tính năng mới? Hãy để lại tin nhắn!
        </p>
      </div>

      {/* Main Grid: Form + Contact Info */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-start">
        {/* Contact Form */}
        <div className="md:col-span-7 floating-shadow-lg">
          <div className="octa-card-lg bg-white/95 p-8 sm:p-10 space-y-6 border border-slate-200/80 shadow-md">
            <div className="flex items-center gap-2.5 text-slate-950 font-black text-xl">
              <MessageSquare className="w-6 h-6 text-orange-600" />
              <span>Gửi Tin Nhắn Cho Chúng Tôi</span>
            </div>

            {isSent && (
              <div className="octa-card-sm p-4.5 bg-blue-100 text-blue-950 text-sm flex items-center gap-3 font-bold">
                <CheckCircle2 className="w-5 h-5 text-orange-600 shrink-0" />
                Cảm ơn bạn! Tin nhắn đã được gửi thành công. Chúng tôi sẽ phản hồi sớm nhất.
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-5">
              <div className="space-y-2">
                <label className="block text-base font-black text-slate-900">Họ và Tên</label>
                <input
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Nguyễn Văn A..."
                  className="w-full px-5 py-3.5 bg-slate-100 text-base text-slate-950 placeholder:text-slate-400 font-bold rounded-lg border border-slate-200/80 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-transparent transition-all"
                />
              </div>

              <div className="space-y-2">
                <label className="block text-base font-black text-slate-900">Email Liên Hệ</label>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="your.email@example.com..."
                  className="w-full px-5 py-3.5 bg-slate-100 text-base text-slate-950 placeholder:text-slate-400 font-bold rounded-lg border border-slate-200/80 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-transparent transition-all"
                />
              </div>

              <div className="space-y-2">
                <label className="block text-base font-black text-slate-900">Nội Dung Tin Nhắn</label>
                <textarea
                  rows={4}
                  required
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  placeholder="Chia sẻ câu hỏi hoặc ý kiến đóng góp của bạn..."
                  className="w-full px-5 py-3.5 bg-slate-100 text-base text-slate-950 placeholder:text-slate-400 resize-none font-bold rounded-lg border border-slate-200/80 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-transparent transition-all leading-relaxed"
                />
              </div>

              <div className="floating-shadow-orange pt-1">
                <button
                  type="submit"
                  className="octa-btn inline-flex items-center gap-2 px-8 py-4 bg-orange-600 hover:bg-orange-700 text-white font-black text-base transition-transform cursor-pointer hover:-translate-y-0.5"
                >
                  <Send className="w-5 h-5" /> Gửi Tin Nhắn Ngay
                </button>
              </div>
            </form>
          </div>
        </div>

        {/* Contact Info & Channels */}
        <div className="md:col-span-5 space-y-7">
          <div className="floating-shadow">
            <div className="octa-card bg-white/95 p-7 sm:p-8 space-y-5 text-sm sm:text-base text-slate-700 border border-slate-200/80 shadow-md">
              <h3 className="font-black text-slate-950 text-lg">Kênh Hỗ Trực Tiếp</h3>
              <div className="space-y-4">
                <div className="flex items-center gap-3.5">
                  <div className="octa-card-sm w-11 h-11 bg-blue-100 flex items-center justify-center text-blue-800 shrink-0">
                    <Mail className="w-5 h-5" />
                  </div>
                  <div>
                    <div className="text-slate-500 text-xs font-bold">Email Hỗ Trợ</div>
                    <div className="font-black text-slate-950 text-sm sm:text-base">support@beforevibecode.dev</div>
                  </div>
                </div>

                <div className="flex items-center gap-3.5">
                  <div className="octa-card-sm w-11 h-11 bg-blue-100 flex items-center justify-center text-blue-800 shrink-0">
                    <Github className="w-5 h-5" />
                  </div>
                  <div>
                    <div className="text-slate-500 text-xs font-bold">Mã Nguồn Mở</div>
                    <div className="font-black text-slate-950 text-sm sm:text-base">github.com/Before-Vibe-Code</div>
                  </div>
                </div>

                <div className="flex items-center gap-3.5">
                  <div className="octa-card-sm w-11 h-11 bg-blue-100 flex items-center justify-center text-blue-800 shrink-0">
                    <MapPin className="w-5 h-5" />
                  </div>
                  <div>
                    <div className="text-slate-500 text-xs font-bold">Trụ Sở</div>
                    <div className="font-black text-slate-950 text-sm sm:text-base">Hà Nội & TP. Hồ Chí Minh, Việt Nam</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Quick FAQ Box */}
          <div className="floating-shadow">
            <div className="octa-card bg-white/95 p-7 sm:p-8 space-y-4 border border-slate-200/80 shadow-md">
              <h3 className="font-black text-slate-950 text-lg flex items-center gap-2">
                <HelpCircle className="w-5 h-5 text-orange-600" /> Câu Hỏi Thường Gặp (FAQ)
              </h3>
              <div className="space-y-4">
                {FAQS.map((faq, i) => (
                  <div key={i} className="space-y-1.5 text-sm sm:text-base">
                    <div className="font-black text-blue-900 text-base">{faq.q}</div>
                    <p className="text-slate-700 leading-relaxed font-semibold">{faq.a}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
