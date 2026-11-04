import React, { useState, useEffect, useRef } from 'react';
import { WizardHeader } from '../components/WizardHeader';
import { Step1ProjectInfo } from '../components/steps/Step1ProjectInfo';
import { Step2Audience } from '../components/steps/Step2Audience';
import { Step3Features } from '../components/steps/Step3Features';
import { Step4TechStack } from '../components/steps/Step4TechStack';
import { Step5AIAnalysis } from '../components/steps/Step5AIAnalysis';
import { Step6Export } from '../components/steps/Step6Export';
import { api } from '../services/api';
import { Sparkles, Edit3, Cpu, Users, Layers, Rocket, ShieldCheck } from 'lucide-react';
import gsap from 'gsap';

const STEP_TITLES = [
  'Ý tưởng',
  'Khách hàng',
  'Tính năng',
  'Định hướng',
  'AI Xử lý',
  'Xuất Prompt'
];

const DRAFT_STORAGE_KEY = 'bvc_studio_draft_session';

export const StudioPage: React.FC = () => {
  const [currentStep, setCurrentStep] = useState(1);
  const [, setProjectId] = useState<number | null>(null);
  const stepContainerRef = useRef<HTMLDivElement>(null);

  // Form State (Lưu bộ nhớ tạm thời)
  const [projectName, setProjectName] = useState(() => {
    try {
      const draft = sessionStorage.getItem(DRAFT_STORAGE_KEY);
      return draft ? JSON.parse(draft).projectName || '' : '';
    } catch {
      return '';
    }
  });

  const [description, setDescription] = useState(() => {
    try {
      const draft = sessionStorage.getItem(DRAFT_STORAGE_KEY);
      return draft ? JSON.parse(draft).description || '' : '';
    } catch {
      return '';
    }
  });

  const [targetAudience, setTargetAudience] = useState(() => {
    try {
      const draft = sessionStorage.getItem(DRAFT_STORAGE_KEY);
      return draft ? JSON.parse(draft).targetAudience || '' : '';
    } catch {
      return '';
    }
  });

  const [features, setFeatures] = useState<Array<{ id?: number; title: string; description: string; priority: string }>>(() => {
    try {
      const draft = sessionStorage.getItem(DRAFT_STORAGE_KEY);
      if (draft && JSON.parse(draft).features?.length > 0) {
        return JSON.parse(draft).features;
      }
    } catch {
      // ignore
    }
    return [
      { title: 'Đăng nhập & Đăng ký tài khoản (Google & Email)', description: '', priority: 'High' },
      { title: 'Quản lý thông tin & Hồ sơ cá nhân', description: '', priority: 'Medium' }
    ];
  });

  const [backendStack, setBackendStack] = useState(() => {
    try {
      const draft = sessionStorage.getItem(DRAFT_STORAGE_KEY);
      return draft ? JSON.parse(draft).backendStack || 'ASP.NET Core 10 Web API (Clean Architecture / Repository)' : 'ASP.NET Core 10 Web API (Clean Architecture / Repository)';
    } catch {
      return 'ASP.NET Core 10 Web API (Clean Architecture / Repository)';
    }
  });

  const [databaseStack, setDatabaseStack] = useState(() => {
    try {
      const draft = sessionStorage.getItem(DRAFT_STORAGE_KEY);
      return draft ? JSON.parse(draft).databaseStack || 'SQL Server + Entity Framework Core 10' : 'SQL Server + Entity Framework Core 10';
    } catch {
      return 'SQL Server + Entity Framework Core 10';
    }
  });

  const [frontendStack, setFrontendStack] = useState(() => {
    try {
      const draft = sessionStorage.getItem(DRAFT_STORAGE_KEY);
      return draft ? JSON.parse(draft).frontendStack || 'React 19 + TypeScript + Tailwind CSS' : 'React 19 + TypeScript + Tailwind CSS';
    } catch {
      return 'React 19 + TypeScript + Tailwind CSS';
    }
  });

  const [nonFunctionalReqs, setNonFunctionalReqs] = useState<string[]>([
    'Bảo mật tài khoản & Chống hack',
    'Tốc độ tải trang cực nhanh (< 250ms)',
    'Hiển thị đẹp trên Điện thoại & PC',
    'Code sạch đẹp, dễ mở rộng sau này'
  ]);

  // Tự động lưu bộ nhớ tạm thời vào sessionStorage khi state thay đổi
  useEffect(() => {
    try {
      sessionStorage.setItem(
        DRAFT_STORAGE_KEY,
        JSON.stringify({
          projectName,
          description,
          targetAudience,
          features,
          backendStack,
          databaseStack,
          frontendStack,
          nonFunctionalReqs
        })
      );
    } catch {
      // ignore
    }
  }, [projectName, description, targetAudience, features, backendStack, databaseStack, frontendStack, nonFunctionalReqs]);

  // GSAP animation on step change
  useEffect(() => {
    if (stepContainerRef.current) {
      gsap.fromTo(
        stepContainerRef.current,
        { opacity: 0, y: 15, scale: 0.99 },
        { opacity: 1, y: 0, scale: 1, duration: 0.45, ease: 'power2.out', clearProps: 'transform' }
      );
    }
  }, [currentStep]);

  // Handlers for steps (Lưu tạm thời trong bộ nhớ, chuyển bước tức thì)
  const handleStep1Next = () => {
    setCurrentStep(2);
  };

  const handleStep2Next = () => {
    setCurrentStep(3);
  };

  const handleStep3Next = () => {
    setCurrentStep(4);
  };

  const handleStep4Next = () => {
    setCurrentStep(5);
  };

  // Bước 5: Khi AI phân tích hoàn tất, tiến hành lưu chính thức 1 lần duy nhất vào Database
  const handleStep5Complete = async () => {
    try {
      const project = await api.createProject({
        name: projectName || 'Dự Án Mới',
        description: description || 'Mô tả dự án'
      });
      if (project?.id) {
        setProjectId(project.id);
        await api.updateAudience(project.id, { targetAudience });
        for (const feat of features) {
          await api.addRequirement(project.id, {
            type: 1,
            title: feat.title,
            description: feat.description || '',
            priority: feat.priority || 'Medium'
          });
        }
      }
    } catch (e) {
      console.warn('Lưu database nền hoàn tất:', e);
    }
    setCurrentStep(6);
  };

  const handleRestart = () => {
    try {
      sessionStorage.removeItem(DRAFT_STORAGE_KEY);
    } catch {
      // ignore
    }
    setProjectName('');
    setDescription('');
    setTargetAudience('');
    setProjectId(null);
    setFeatures([
      { title: 'Đăng nhập & Đăng ký tài khoản (Google & Email)', description: '', priority: 'High' },
      { title: 'Quản lý thông tin & Hồ sơ cá nhân', description: '', priority: 'Medium' }
    ]);
    setCurrentStep(1);
  };

  return (
    <div className="py-6 sm:py-8 space-y-6 relative z-10">
      {/* Wizard Progress Breadcrumb */}
      <WizardHeader
        currentStep={currentStep}
        totalSteps={6}
        stepTitles={STEP_TITLES}
      />

      {/* 1/4 and 3/4 Split Layout Container */}
      <div className="w-full max-w-[85%] mx-auto px-2 sm:px-4">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          {/* Left Column (1/4 - lg:col-span-3): Tóm Tắt Ngữ Cảnh Đã Chọn */}
          <div className="lg:col-span-3 space-y-4 lg:sticky lg:top-24">
            <div className="floating-shadow">
              <div className="octa-card bg-white p-5 sm:p-6 space-y-5">
                <div className="flex items-center justify-between pb-2">
                  <div className="flex items-center gap-2 text-slate-950 font-black text-sm">
                    <Sparkles className="w-4 h-4 text-orange-500" />
                    <span>Ngữ Cảnh Đã Chọn</span>
                  </div>
                  <span className="octa-card-sm text-[10px] uppercase font-black px-2.5 py-1 bg-blue-100 text-blue-950">
                    {currentStep > 1 ? `Bước 1-${currentStep - 1} OK` : 'Khởi tạo'}
                  </span>
                </div>

                {/* Step 1 Summary: Ý tưởng */}
                <div className={`space-y-1.5 p-3.5 octa-card-sm transition-all ${
                  currentStep > 1 ? 'bg-blue-100/70 text-slate-950' : 'bg-slate-100 text-slate-600'
                }`}>
                  <div className="flex items-center justify-between text-xs font-black">
                    <span className="flex items-center gap-1.5 text-blue-950">
                      <Rocket className="w-3.5 h-3.5 text-orange-600" /> 1. Ý Tưởng Dự Án
                    </span>
                    {currentStep > 1 && (
                      <button
                        type="button"
                        onClick={() => setCurrentStep(1)}
                        title="Sửa bước 1"
                        className="text-blue-700 hover:text-blue-900 p-0.5 cursor-pointer"
                      >
                        <Edit3 className="w-3.5 h-3.5" />
                      </button>
                    )}
                  </div>
                  <div className="text-xs font-black text-slate-950 truncate">
                    {projectName ? projectName : <span className="text-slate-400 font-normal">Chưa nhập tên...</span>}
                  </div>
                  {description && (
                    <p className="text-[11px] text-slate-700 line-clamp-2 leading-relaxed font-semibold">
                      {description}
                    </p>
                  )}
                </div>

                {/* Step 2 Summary: Khách hàng */}
                <div className={`space-y-1.5 p-3.5 octa-card-sm transition-all ${
                  currentStep > 2 ? 'bg-blue-100/70 text-slate-950' : 'bg-slate-100 text-slate-600'
                }`}>
                  <div className="flex items-center justify-between text-xs font-black">
                    <span className="flex items-center gap-1.5 text-blue-950">
                      <Users className="w-3.5 h-3.5 text-orange-600" /> 2. Khách Hàng
                    </span>
                    {currentStep > 2 && (
                      <button
                        type="button"
                        onClick={() => setCurrentStep(2)}
                        title="Sửa bước 2"
                        className="text-blue-700 hover:text-blue-900 p-0.5 cursor-pointer"
                      >
                        <Edit3 className="w-3.5 h-3.5" />
                      </button>
                    )}
                  </div>
                  <p className="text-[11px] text-slate-700 line-clamp-2 leading-relaxed font-semibold">
                    {targetAudience ? targetAudience : <span className="text-slate-400 font-normal">{currentStep === 2 ? 'Đang chọn ở bước này...' : 'Chưa thiết lập'}</span>}
                  </p>
                </div>

                {/* Step 3 Summary: Tính năng */}
                <div className={`space-y-1.5 p-3.5 octa-card-sm transition-all ${
                  currentStep > 3 ? 'bg-blue-100/70 text-slate-950' : 'bg-slate-100 text-slate-600'
                }`}>
                  <div className="flex items-center justify-between text-xs font-black">
                    <span className="flex items-center gap-1.5 text-blue-950">
                      <Layers className="w-3.5 h-3.5 text-orange-600" /> 3. Tính Năng
                    </span>
                    {currentStep > 3 && (
                      <button
                        type="button"
                        onClick={() => setCurrentStep(3)}
                        title="Sửa bước 3"
                        className="text-blue-700 hover:text-blue-900 p-0.5 cursor-pointer"
                      >
                        <Edit3 className="w-3.5 h-3.5" />
                      </button>
                    )}
                  </div>
                  <div className="text-xs font-black text-slate-950">
                    {features.length} tính năng đã chọn
                  </div>
                  <div className="space-y-1 max-h-20 overflow-hidden text-[11px] text-slate-700 font-medium">
                    {features.slice(0, 2).map((f, i) => (
                      <div key={i} className="truncate flex items-center gap-1.5">
                        <span className="w-1.5 h-1.5 rounded-full bg-blue-700 shrink-0" />
                        <span className="truncate">{f.title}</span>
                      </div>
                    ))}
                    {features.length > 2 && (
                      <div className="text-[10px] text-slate-500 font-bold pl-3">
                        +{features.length - 2} tính năng khác...
                      </div>
                    )}
                  </div>
                </div>

                {/* Step 4 Summary: Định hướng */}
                <div className={`space-y-1.5 p-3.5 octa-card-sm transition-all ${
                  currentStep > 4 ? 'bg-blue-100/70 text-slate-950' : 'bg-slate-100 text-slate-600'
                }`}>
                  <div className="flex items-center justify-between text-xs font-black">
                    <span className="flex items-center gap-1.5 text-blue-950">
                      <Cpu className="w-3.5 h-3.5 text-orange-600" /> 4. Định Hướng
                    </span>
                    {currentStep > 4 && (
                      <button
                        type="button"
                        onClick={() => setCurrentStep(4)}
                        title="Sửa bước 4"
                        className="text-blue-700 hover:text-blue-900 p-0.5 cursor-pointer"
                      >
                        <Edit3 className="w-3.5 h-3.5" />
                      </button>
                    )}
                  </div>
                  <div className="text-[11px] text-slate-800 space-y-0.5 font-bold">
                    <div className="truncate"><strong>Nền tảng:</strong> {frontendStack.split('(')[0].trim()}</div>
                    <div className="truncate"><strong>Máy chủ:</strong> {backendStack.split('(')[0].trim()}</div>
                    <div className="truncate"><strong>Lưu trữ:</strong> {databaseStack.split('(')[0].trim()}</div>
                  </div>
                </div>

                {/* Architecture Badge */}
                <div className="pt-2 flex items-center gap-1.5 text-[11px] font-black text-emerald-800 bg-emerald-50 p-2 octa-card-sm">
                  <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>Dành Riêng Cho Người Non-Tech</span>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column (3/4 - lg:col-span-9): Nội Dung Bước Hiện Tại */}
          <div className="lg:col-span-9">
            <div 
              ref={stepContainerRef}
              className="floating-shadow-lg transition-all"
            >
              <div className="octa-card-lg bg-white/95 p-6 sm:p-8 md:p-10">
                {currentStep === 1 && (
                  <Step1ProjectInfo
                    projectName={projectName}
                    setProjectName={setProjectName}
                    description={description}
                    setDescription={setDescription}
                    onNext={handleStep1Next}
                  />
                )}

                {currentStep === 2 && (
                  <Step2Audience
                    targetAudience={targetAudience}
                    setTargetAudience={setTargetAudience}
                    onNext={handleStep2Next}
                    onBack={() => setCurrentStep(1)}
                  />
                )}

                {currentStep === 3 && (
                  <Step3Features
                    features={features}
                    setFeatures={setFeatures}
                    onNext={handleStep3Next}
                    onBack={() => setCurrentStep(2)}
                  />
                )}

                {currentStep === 4 && (
                  <Step4TechStack
                    frontendStack={frontendStack}
                    setFrontendStack={setFrontendStack}
                    backendStack={backendStack}
                    setBackendStack={setBackendStack}
                    databaseStack={databaseStack}
                    setDatabaseStack={setDatabaseStack}
                    nonFunctionalReqs={nonFunctionalReqs}
                    setNonFunctionalReqs={setNonFunctionalReqs}
                    onNext={handleStep4Next}
                    onBack={() => setCurrentStep(3)}
                  />
                )}

                {currentStep === 5 && (
                  <Step5AIAnalysis
                    projectName={projectName || 'Dự Án Phần Mềm'}
                    onComplete={handleStep5Complete}
                  />
                )}

                {currentStep === 6 && (
                  <Step6Export
                    projectName={projectName || 'Before Vibe Code Studio'}
                    description={description}
                    targetAudience={targetAudience}
                    features={features}
                    frontendStack={frontendStack}
                    backendStack={backendStack}
                    databaseStack={databaseStack}
                    nonFunctionalReqs={nonFunctionalReqs}
                    onRestart={handleRestart}
                  />
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
