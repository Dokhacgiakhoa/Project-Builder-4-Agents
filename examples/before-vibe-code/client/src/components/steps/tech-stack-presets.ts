import { 
  ShieldCheck, Zap, Globe, Sparkles, 
  Rocket, Building2, BrainCircuit, Smartphone,
  FileText, Database
} from 'lucide-react';

export interface SolutionPack {
  id: string;
  icon: any;
  tag: string;
  title: string;
  desc: string;
  backend: string;
  database: string;
  frontend: string;
  nfrs: string[];
}

export const SOLUTION_PACKS: SolutionPack[] = [
  {
    id: 'startup',
    icon: Rocket,
    tag: 'Phổ biến nhất cho Startup',
    title: 'Gói 1: Web Khởi Nghiệp & MVP Nhanh',
    desc: 'Phù hợp làm nhanh sản phẩm để thử nghiệm thị trường, giao diện đẹp mắt, dễ vận hành.',
    backend: 'Node.js / Express.js (Lightweight REST API)',
    database: 'PostgreSQL + Prisma / Dapper / Hibernate',
    frontend: 'React 19 + TypeScript + Tailwind CSS (SPA Client)',
    nfrs: [
      'Tốc độ phản hồi tức thì (< 250ms)',
      'Giao diện tương thích mượt mà trên cả Điện thoại & Máy tính',
      'Có tài liệu hướng dẫn chạy code từ A-Z'
    ]
  },
  {
    id: 'enterprise',
    icon: Building2,
    tag: 'Chuẩn Doanh Nghiệp',
    title: 'Gói 2: Hệ Thống Doanh Nghiệp Ổn Định',
    desc: 'Phù hợp quản lý nội bộ, bán hàng, phòng khám, trường học cần bảo mật cao và bền bỉ.',
    backend: 'ASP.NET Core 10 Web API (Clean Architecture / Repository)',
    database: 'SQL Server + Entity Framework Core 10',
    frontend: 'React 19 + TypeScript + Tailwind CSS (SPA Client)',
    nfrs: [
      'Bảo mật đăng nhập đa lớp & Mã hóa dữ liệu an toàn',
      'Kiến trúc phân tầng chuẩn doanh nghiệp (Dễ bảo trì)',
      'Tối ưu hóa cơ sở dữ liệu & Không lo mất mát thông tin'
    ]
  },
  {
    id: 'ai_data',
    icon: BrainCircuit,
    tag: 'Công Nghệ AI & Dữ Liệu',
    title: 'Gói 3: Nền Tảng AI & Tự Động Hóa',
    desc: 'Phù hợp ứng dụng tích hợp Chatbot AI, phân tích số liệu, xử lý hình ảnh và tài liệu thông minh.',
    backend: 'Python FastAPI (High Performance Async + Pydantic)',
    database: 'PostgreSQL + Prisma / Dapper / Hibernate',
    frontend: 'Next.js 15 (Fullstack SSR / App Router / RSC)',
    nfrs: [
      'Tốc độ xử lý tính toán cực nhanh',
      'Tích hợp sẵn cổng kết nối API trí tuệ nhân tạo',
      'Có tài liệu hướng dẫn chạy code từ A-Z'
    ]
  },
  {
    id: 'mobile_first',
    icon: Smartphone,
    tag: 'Đa Nền Tảng Di Động',
    title: 'Gói 4: Ứng Dụng App Di Động & Web',
    desc: 'Phù hợp ứng dụng muốn người dùng cài đặt lên cả điện thoại iOS, Android và dùng trên Web.',
    backend: 'Node.js / NestJS (TypeScript + Enterprise Modular)',
    database: 'MongoDB + Mongoose (NoSQL Document Store)',
    frontend: 'Flutter (Dart Cross-Platform Mobile / Web)',
    nfrs: [
      'Trải nghiệm mượt mà 60 FPS trên cả iPhone & Android',
      'Bảo mật đăng nhập an toàn',
      'Giao diện tương thích mượt mà trên cả Điện thoại & Máy tính'
    ]
  }
];

export const QUALITY_STANDARDS = [
  {
    id: "std_sec",
    icon: ShieldCheck,
    title: "Bảo mật tài khoản & Chống hack",
    desc: "Mã hóa mật khẩu an toàn, chống người lạ xâm nhập trái phép vào hệ thống."
  },
  {
    id: "std_speed",
    icon: Zap,
    title: "Tốc độ tải trang cực nhanh",
    desc: "Bấm là mở ngay tức thì, không bị đơ lag kể cả khi có nhiều người cùng truy cập."
  },
  {
    id: "std_mobile",
    icon: Globe,
    title: "Hiển thị đẹp trên Điện thoại & PC",
    desc: "Giao diện tự động co giãn vừa vặn trên mọi kích thước màn hình từ điện thoại đến laptop."
  },
  {
    id: "std_clean",
    icon: Sparkles,
    title: "Code sạch đẹp, dễ mở rộng sau này",
    desc: "Cấu trúc mã nguồn chuẩn mực, giúp bạn dễ dàng thuê dev hoặc bảo AI code thêm tính năng mới."
  },
  {
    id: "std_db",
    icon: Database,
    title: "Tự động lưu & Bảo vệ dữ liệu",
    desc: "Dữ liệu được lưu trữ an toàn, không bị mất mát khi người dùng vô tình tắt trình duyệt."
  },
  {
    id: "std_readme",
    icon: FileText,
    title: "Có sẵn hướng dẫn chạy code A-Z",
    desc: "AI sẽ viết sẵn 1 file hướng dẫn chi tiết cách mở và chạy dự án lên màn hình."
  }
];
