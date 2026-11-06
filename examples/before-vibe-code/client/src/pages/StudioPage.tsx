import React, { useState, useEffect, useRef } from 'react';
import { WizardHeader } from '../components/WizardHeader';
import { Step1ProjectInfo } from '../components/steps/Step1ProjectInfo';
import { Step2Audience } from '../components/steps/Step2Audience';
import { Step3Features } from '../components/steps/Step3Features';
import { Step4TechStack } from '../components/steps/Step4TechStack';
import { Step5AIAnalysis } from '../components/steps/Step5AIAnalysis';
import { Step6Export } from '../components/steps/Step6Export';
import { StudioContextSummary } from '../components/studio/StudioContextSummary';
import { api } from '../services/api';
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

  useEffect(() => {
    if (stepContainerRef.current) {
      gsap.fromTo(
        stepContainerRef.current,
        { opacity: 0, y: 15, scale: 0.99 },
        { opacity: 1, y: 0, scale: 1, duration: 0.45, ease: 'power2.out', clearProps: 'transform' }
      );
    }
  }, [currentStep]);

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
      <WizardHeader
        currentStep={currentStep}
        totalSteps={6}
        stepTitles={STEP_TITLES}
      />

      <div className="w-full max-w-[85%] mx-auto px-2 sm:px-4">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          <StudioContextSummary
            currentStep={currentStep}
            onNavigateStep={(step) => setCurrentStep(step)}
            projectName={projectName}
            targetAudience={targetAudience}
            features={features}
            frontendStack={frontendStack}
            backendStack={backendStack}
            databaseStack={databaseStack}
            nonFunctionalReqs={nonFunctionalReqs}
          />

          <div className="lg:col-span-9" ref={stepContainerRef}>
            <div className="floating-shadow">
              <div className="octa-card bg-white p-6 sm:p-8 lg:p-10 border-2 border-slate-900 shadow-xl">
                {currentStep === 1 && (
                  <Step1ProjectInfo
                    projectName={projectName}
                    setProjectName={setProjectName}
                    description={description}
                    setDescription={setDescription}
                    onNext={() => setCurrentStep(2)}
                  />
                )}
                {currentStep === 2 && (
                  <Step2Audience
                    targetAudience={targetAudience}
                    setTargetAudience={setTargetAudience}
                    onNext={() => setCurrentStep(3)}
                    onBack={() => setCurrentStep(1)}
                  />
                )}
                {currentStep === 3 && (
                  <Step3Features
                    features={features}
                    setFeatures={setFeatures}
                    onNext={() => setCurrentStep(4)}
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
                    onNext={() => setCurrentStep(5)}
                    onBack={() => setCurrentStep(3)}
                  />
                )}
                {currentStep === 5 && (
                  <Step5AIAnalysis
                    projectName={projectName}
                    description={description}
                    targetAudience={targetAudience}
                    features={features}
                    backendStack={backendStack}
                    databaseStack={databaseStack}
                    frontendStack={frontendStack}
                    nonFunctionalReqs={nonFunctionalReqs}
                    onComplete={handleStep5Complete}
                    onBack={() => setCurrentStep(4)}
                  />
                )}
                {currentStep === 6 && (
                  <Step6Export
                    projectName={projectName}
                    description={description}
                    targetAudience={targetAudience}
                    features={features}
                    backendStack={backendStack}
                    databaseStack={databaseStack}
                    frontendStack={frontendStack}
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
