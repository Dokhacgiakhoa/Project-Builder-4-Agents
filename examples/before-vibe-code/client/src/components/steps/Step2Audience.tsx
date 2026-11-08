import React from 'react';
import { Users, ArrowLeft, ArrowRight, Check } from 'lucide-react';

interface Step2Props {
  targetAudience: string;
  setTargetAudience: (val: string) => void;
  onNext: () => void;
  onBack: () => void;
}

const AUDIENCE_PRESETS = [
  {
    title: "Học sinh / Sinh viên",
    desc: "Cần giao diện trực quan, vui nhộn, dễ tiếp cận, tương thích tối đa trên Mobile.",
    value: "Học sinh, sinh viên độ tuổi từ 15-24, ưu tiên trải nghiệm mobile-first, giao diện trực quan, thao tác nhanh."
  },
  {
    title: "Nhân viên Văn phòng / Doanh nghiệp",
    desc: "Cần tính năng quản trị dữ liệu chặt chẽ, bảo mật cao, xuất file Excel/PDF báo cáo.",
    value: "Nhân viên văn phòng, quản lý doanh nghiệp, cần tính chính xác, phân quyền bảo mật, dashboard báo cáo."
  },
  {
    title: "Khách hàng Đại chúng (B2C)",
    desc: "Cần quy trình mua sắm / sử dụng dịch vụ đơn giản nhất, thanh toán 1-chạm.",
    value: "Người tiêu dùng đại chúng mọi độ tuổi, cần thao tác đơn giản, không rườm rà, hỗ trợ thanh toán online."
  },
  {
    title: "Lập trình viên & Tech Team (B2B)",
    desc: "Cần hệ thống có API mở, CLI, cấu hình thông qua file Json/Yaml.",
    value: "Lập trình viên và các nhóm kỹ thuật, yêu cầu tài liệu API đầy đủ, khả năng tự động hóa và tích hợp CI/CD."
  }
];

export const Step2Audience: React.FC<Step2Props> = ({
  targetAudience,
  setTargetAudience,
  onNext,
  onBack
}) => {
  const handleSelect = (val: string) => {
    setTargetAudience(val);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!targetAudience.trim()) return;
    onNext();
  };

  return (
    <div className="space-y-6">
      <div>
        <div className="octa-card-sm inline-flex items-center gap-2 px-4 py-2 bg-blue-100 text-blue-950 text-sm font-black mb-3">
          <Users className="w-4 h-4 text-orange-600" /> Bước 2 / 6: Chân dung Người Dùng
        </div>
        <h2 className="text-2xl sm:text-3xl font-black text-slate-950 tracking-tight">Ai sẽ là người sử dụng chính sản phẩm này?</h2>
        <p className="text-slate-700 text-base mt-1 font-semibold">
          Xác định đối tượng giúp AI tối ưu hóa ngôn ngữ thiết kế, UX và luồng trải nghiệm người dùng phù hợp nhất.
        </p>
      </div>

      {/* Preset Audience Cards (Không Viền) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {AUDIENCE_PRESETS.map((item, idx) => {
          const isSelected = targetAudience === item.value;
          return (
            <div key={idx} className={isSelected ? 'floating-shadow-blue' : 'floating-shadow-sm'}>
              <button
                type="button"
                onClick={() => handleSelect(item.value)}
                className={`octa-card w-full text-left p-5 sm:p-6 transition-all relative cursor-pointer ${
                  isSelected
                    ? 'bg-blue-700 text-white'
                    : 'bg-white hover:bg-blue-50 text-slate-900'
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className={`font-black text-base sm:text-lg ${isSelected ? 'text-white' : 'text-slate-950'}`}>{item.title}</div>
                  {isSelected && (
                    <div className="octa-card-sm w-6 h-6 bg-orange-500 text-white flex items-center justify-center shadow-xs">
                      <Check className="w-4 h-4 stroke-[3]" />
                    </div>
                  )}
                </div>
                <p className={`text-sm mt-2 leading-relaxed font-medium ${isSelected ? 'text-blue-100' : 'text-slate-700'}`}>{item.desc}</p>
              </button>
            </div>
          );
        })}
      </div>

      <form onSubmit={handleSubmit} className="space-y-5">
        <div className="space-y-2">
          <label className="block text-base font-black text-slate-950">
            Hoặc tự điều chỉnh chi tiết chân dung khách hàng:
          </label>
          <textarea
            rows={3}
            value={targetAudience}
            onChange={(e) => setTargetAudience(e.target.value)}
            placeholder="Ví dụ: Bác sĩ và bệnh nhân tại các phòng khám tư, cần đặt lịch khám online và tra cứu bệnh án..."
            required
            className="w-full px-5 py-3.5 bg-slate-100 text-base text-slate-950 placeholder:text-slate-400 resize-none font-bold rounded-lg focus:bg-white focus:shadow-md transition-all leading-relaxed"
          />
        </div>

        <div className="flex justify-between items-center pt-2">
          <button
            type="button"
            onClick={onBack}
            className="octa-btn inline-flex items-center gap-2 px-6 py-3 bg-blue-100 hover:bg-blue-200 text-blue-950 font-black text-base shadow-xs transition-all cursor-pointer"
          >
            <ArrowLeft className="w-4.5 h-4.5" /> Quay lại
          </button>
          <button
            type="submit"
            disabled={!targetAudience.trim()}
            className="octa-btn floating-shadow-blue inline-flex items-center gap-2 px-8 py-4 bg-blue-700 hover:bg-blue-800 disabled:opacity-50 disabled:cursor-not-allowed text-white font-black text-base transition-all cursor-pointer hover:-translate-y-0.5"
          >
            Tiếp tục: Yêu Cầu Tính Năng
            <ArrowRight className="w-5 h-5" />
          </button>
        </div>
      </form>
    </div>
  );
};
