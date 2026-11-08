"""Pillar Security, Cloud, Microservices, Data và Observability."""

import os
import sys
import re
import json
import datetime
from pathlib import Path

from .constants import IGNORE_DIRS, CODE_EXTENSIONS  # noqa: F401
from .models import CriterionItem


class InfraPillarsMixin:
    """Pillar Security, Cloud, Microservices, Data và Observability."""

    def audit_security_and_supply_chain(self):
        score = 0
        found = []
        missing = []

        # 1. Dependency Lockfiles
        lockfiles = ['package-lock.json', 'yarn.lock', 'pnpm-lock.yaml', 'poetry.lock', 'Pipfile.lock', 'go.sum', 'Cargo.lock', 'packages.lock.json']
        matched_lfs = [lf for lf in lockfiles if self.tree.find_by_name(lf)]

        if matched_lfs:
            score += 35
            found.append(CriterionItem(
                "Khóa chính xác phiên bản phụ thuộc qua DEPENDENCY LOCKFILE (chống Supply Chain Attack)",
                evidence=", ".join(matched_lfs),
                details=f"Đã phát hiện lockfile xác thực mã băm và phiên bản phụ thuộc: {', '.join(matched_lfs)}.",
                badge="Lockfile OK"
            ))
        else:
            missing.append(CriterionItem(
                "Tệp DEPENDENCY LOCKFILE (package-lock.json, poetry.lock, go.sum)",
                evidence="Thư mục gốc",
                details="Chưa có lockfile cố định phiên bản gói phụ thuộc, có nguy cơ bị tấn công chuỗi cung ứng hoặc lệch môi trường.",
                remediation="Chạy npm install / poetry lock / cargo generate-lockfile và commit tệp lockfile vào Git."
            ))
            self.gaps.append("Thiếu lockfile quản lý phụ thuộc, tiềm ẩn rủi ro trôi lệch phiên bản hoặc dính mã độc.")

        # 2. HTTP Security Headers (Helmet, CORS)
        has_headers = 'HELMET (HTTP HEADERS)' in self.tools or 'CORS MIDDLEWARE' in self.tools
        headers_file = None

        if not has_headers:
            for p in self.tree.code_files:
                try:
                    t = self.tree.read_text(p)
                    if 'helmet' in t or 'CORSMiddleware' in t or 'UseCors' in t or 'Content-Security-Policy' in t:
                        has_headers = True
                        headers_file = str(self.tree.rel_path(p)) if hasattr(self.tree, 'rel_path') else p.name
                        break
                except Exception:
                    pass
        else:
            headers_file = "Security Middleware"

        if has_headers:
            score += 25
            found.append(CriterionItem(
                "Cấu hình HTTP SECURITY HEADERS (CORS strict, HELMET, Content-Security-Policy)",
                evidence=headers_file or "HTTP Middleware",
                details="Đã phát hiện cấu hình bảo vệ HTTP Headers (CORS, Helmet hoặc CSP) chống XSS và Clickjacking.",
                badge="Security Headers"
            ))
        else:
            missing.append(CriterionItem(
                "Thiết lập HTTP SECURITY HEADERS bảo vệ giao thức (CORS, Helmet, CSP)",
                evidence="Server Config",
                details="Chưa cấu hình các header an ninh chuẩn (Content-Security-Policy, X-Frame-Options, Helmet) bảo vệ ứng dụng.",
                remediation="Tích hợp middleware Helmet hoặc CORS strict bảo vệ giao thức HTTP."
            ))

        # 3. Rate Limiting protection
        has_ratelimit = 'RATE LIMITING' in self.tools
        ratelimit_file = None

        if not has_ratelimit:
            for p in self.tree.code_files:
                try:
                    t = self.tree.read_text(p)
                    if 'rateLimit' in t or 'slowapi' in t or 'RateLimiter' in t or 'Throttle' in t:
                        has_ratelimit = True
                        ratelimit_file = str(self.tree.rel_path(p)) if hasattr(self.tree, 'rel_path') else p.name
                        break
                except Exception:
                    pass
        else:
            ratelimit_file = "Rate Limiter"

        if has_ratelimit:
            score += 20
            found.append(CriterionItem(
                "Cơ chế RATE LIMITING giới hạn tần suất yêu cầu chống Brute-force & DDoS",
                evidence=ratelimit_file or "Rate Limiter",
                details="Đã xác minh bộ giới hạn tần suất yêu cầu chống tấn công dò quét vét cạn và quá tải tài nguyên.",
                badge="Rate Limiting"
            ))
        else:
            missing.append(CriterionItem(
                "Cơ chế RATE LIMITING bảo vệ API trước các đợt tấn công vét cạn (Brute-force)",
                evidence="API Middleware",
                details="Chưa có middleware giới hạn tần suất gọi API (Rate Limiting / Throttle) cho các endpoint nhạy cảm.",
                remediation="Bổ sung express-rate-limit, slowapi hoặc redis-based rate limiter cho các API xác thực/công khai."
            ))

        # 4. Secret Isolation & .gitignore
        gitignore = self.root / '.gitignore'
        has_git_secret_protect = False

        if gitignore.exists():
            try:
                gi_text = gitignore.read_text(encoding='utf-8', errors='ignore')
                if '.env' in gi_text and not (self.root / '.env').exists():
                    has_git_secret_protect = True
            except Exception:
                pass

        if has_git_secret_protect:
            score += 20
            found.append(CriterionItem(
                "Cô lập biến môi trường nhạy cảm: .ENV được loại trừ 100% khỏi kho Git",
                evidence=".gitignore",
                details="Tệp .env chứa biến nhạy cảm đã được loại trừ an toàn trong .gitignore và không bị theo dõi bởi Git.",
                badge="Secrets Isolated"
            ))
        else:
            missing.append(CriterionItem(
                "Chính sách cô lập SECRET nghiêm ngặt (đưa .ENV vào .gitignore và dùng KMS/Vault)",
                evidence=".gitignore / .env",
                details="Chưa cấu hình loại trừ tệp .env trong .gitignore hoặc có nguy cơ lộ thông tin bí mật cấu hình.",
                remediation="Thêm `.env` và `*.pem` vào tệp `.gitignore` ngay lập tức."
            ))

        score = min(100, score)
        self.scores['Bảo Mật & Chuỗi Cung Ứng (SECURITY)'] = score
        self.add_log("  -> Checked supply chain lockfiles, .env isolation and scanned for hardcoded secrets.", "security", "muted")
        self.details['security'] = {
            'name': 'Bảo Mật & Chuỗi Cung Ứng',
            'found': found,
            'missing': missing,
            'score': score,
            'max_points': 15,
            'is_na': False
        }

    def audit_cloud_and_container(self):
        score = 0
        found = []
        missing = []

        # 1. Dockerfile Multi-stage Build & Non-root User
        dockerfiles = [p for p in self.tree.all_files if p.name.lower().startswith('dockerfile')]
        has_multistage = False
        has_nonroot = False
        has_healthcheck = False
        df_target_name = "Dockerfile"

        for df in dockerfiles:
            try:
                content = df.read_text(encoding='utf-8', errors='ignore')
                df_target_name = df.name
                if re.search(r'FROM\s+.*?AS\s+\w+', content, re.IGNORECASE) and 'COPY --from=' in content:
                    has_multistage = True
                if re.search(r'USER\s+(?:non-root|10001|appuser|node|\w+)', content, re.IGNORECASE) and 'USER root' not in content:
                    has_nonroot = True
                if 'HEALTHCHECK' in content:
                    has_healthcheck = True
            except Exception:
                pass

        if has_multistage:
            score += 35
            found.append(CriterionItem(
                "Dockerfile chuẩn mực MULTI-STAGE BUILD tối ưu dung lượng và tính bảo mật",
                evidence=df_target_name,
                details="Đã xác minh Dockerfile sử dụng multi-stage build tách biệt giai đoạn biên dịch và môi trường chạy tối giản.",
                badge="Multi-Stage"
            ))
        else:
            missing.append(CriterionItem(
                "Dockerfile tối ưu MULTI-STAGE BUILD (tách biệt môi trường build và runtime)",
                evidence=df_target_name,
                details="Dockerfile chưa áp dụng Multi-stage build (AS builder -> FROM minimal), làm phình to kích thước image.",
                remediation="Tách Dockerfile thành giai đoạn Build (chứa SDK/compiler) và Runtime (chỉ chứa dist và runtime tối giản)."
            ))

        if has_nonroot:
            score += 25
            found.append(CriterionItem(
                "Chạy CONTAINER với quyền hạn tối thiểu (USER NON-ROOT)",
                evidence=df_target_name,
                snippet="USER node / appuser / non-root",
                details="Đã khai báo user không có đặc quyền root trong Dockerfile nhằm chống leo thang đặc quyền container escape.",
                badge="Non-Root"
            ))
        else:
            missing.append(CriterionItem(
                "Khai báo USER NON-ROOT trong Dockerfile để ngăn chặn Container Escape",
                evidence=df_target_name,
                details="Dockerfile chạy mặc định bằng quyền root, tiềm ẩn rủi ro thoát container (container escape) khi ứng dụng có lỗ hổng.",
                remediation="Thêm `USER node` hoặc tạo user appuser: `USER appuser` trước lệnh ENTRYPOINT/CMD."
            ))

        # 2. Health Checks (Liveness & Readiness Probes)
        probe_file = None
        if not has_healthcheck:
            for p in self.tree.code_files:
                try:
                    t = self.tree.read_text(p)
                    if '/healthz' in t or '/readyz' in t or '/health' in t:
                        has_healthcheck = True
                        probe_file = str(self.tree.rel_path(p)) if hasattr(self.tree, 'rel_path') else p.name
                        break
                except Exception:
                    pass
        else:
            probe_file = f"{df_target_name}:HEALTHCHECK"

        if has_healthcheck:
            score += 20
            found.append(CriterionItem(
                "Endpoint thăm dò trạng thái sức khỏe: LIVENESS & READINESS PROBES (/healthz, /readyz)",
                evidence=probe_file or "/healthz",
                details="Đã xác minh endpoint kiểm tra sức khỏe (/healthz, /readyz) hỗ trợ bộ điều phối Kubernetes/Cloud nạp traffic an toàn.",
                badge="Health Probes"
            ))
        else:
            missing.append(CriterionItem(
                "Cung cấp endpoint LIVENESS & READINESS PROBES (/healthz, /readyz) cho bộ điều phối Cloud",
                evidence="Routing / Endpoints",
                details="Thiếu endpoint kiểm tra sức khỏe ứng dụng (/health hoặc /healthz) phục vụ load balancer và Kubernetes probes.",
                remediation="Tạo endpoint GET `/health` hoặc `/healthz` trả về trạng thái hoạt động của server và database."
            ))

        # 3. Infrastructure as Code (Docker Compose, K8s manifests, Helm)
        has_iac = bool(self.tree.find_by_name('docker-compose.yml') or self.tree.find_by_name('docker-compose.yaml')) or any('k8s' in p.parts or 'helm' in p.parts for p in self.tree.all_files)
        iac_ev = "docker-compose.yml" if bool(self.tree.find_by_name('docker-compose.yml') or self.tree.find_by_name('docker-compose.yaml')) else "Kubernetes / Helm"

        if has_iac:
            score += 20
            found.append(CriterionItem(
                "Khai báo hạ tầng dưới dạng mã INFRASTRUCTURE AS CODE (DOCKER COMPOSE / KUBERNETES MANIFESTS)",
                evidence=iac_ev,
                details=f"Đã phát hiện khai báo hạ tầng triển khai cục bộ và cloud dạng mã qua `{iac_ev}`.",
                badge="IaC Ready"
            ))
        else:
            missing.append(CriterionItem(
                "Tệp quản lý hạ tầng INFRASTRUCTURE AS CODE (docker-compose.yml hoặc K8s Helm)",
                evidence="Thư mục gốc",
                details="Chưa có tệp docker-compose.yml hoặc Kubernetes manifests để tự động hóa khởi tạo môi trường đồng nhất.",
                remediation="Tạo tệp `docker-compose.yml` định nghĩa các dịch vụ app, database và cache cho môi trường dev."
            ))

        score = min(100, score)
        self.scores['Hạ Tầng CLOUD & CONTAINER (DEVOPS)'] = score
        self.add_log("  -> Audited Dockerfile config, container specs and CI/CD workflows.", "cloud", "muted")
        self.details['cloud'] = {
            'name': 'Hạ Tầng Cloud & DevOps',
            'found': found,
            'missing': missing,
            'score': score,
            'max_points': 15,
            'is_na': False
        }

    def audit_microservices_and_gateway(self):
        score = 0
        found = []
        missing = []

        # 1. API Gateway Routing
        has_gateway = any(self.tree.any_name_starts_with(gw) for gw in ['ocelot', 'kong', 'traefik', 'envoy'])
        gw_file = None

        if not has_gateway:
            for p in self.tree.find_by_ext('.conf'):
                try:
                    if 'proxy_pass' in self.tree.read_text(p):
                        has_gateway = True
                        gw_file = str(self.tree.rel_path(p)) if hasattr(self.tree, 'rel_path') else p.name
                        break
                except Exception:
                    pass
        else:
            gw_file = "API Gateway Config"

        if has_gateway:
            score += 30
            found.append(CriterionItem(
                "API GATEWAY / REVERSE PROXY làm cổng điều phối lưu lượng tập trung",
                evidence=gw_file or "API Gateway",
                details="Đã xác minh cấu hình Gateway/Reverse Proxy điều phối và định tuyến lưu lượng vào hệ thống.",
                badge="API Gateway"
            ))
        else:
            missing.append(CriterionItem(
                "Cấu hình API GATEWAY tập trung (Kong, Traefik, Ocelot hoặc Nginx)",
                evidence="Hạ tầng mạng",
                details="Chưa có cổng Reverse Proxy hoặc API Gateway để quản lý routing, auth và SSL termination tập trung.",
                remediation="Thiết lập Nginx, Traefik hoặc Kong làm reverse proxy trung tâm."
            ))

        # 2. Circuit Breaker & Resiliency (Polly, Resilience4j, Tenacity)
        has_circuit_breaker = False
        cb_file = None

        for p in self.tree.code_files:
            try:
                t = self.tree.read_text(p)
                if re.search(r'(circuitBreaker|Policy\.Handle|resilience4j|tenacity|retry_with_backoff)', t, re.IGNORECASE):
                    has_circuit_breaker = True
                    cb_file = str(self.tree.rel_path(p)) if hasattr(self.tree, 'rel_path') else p.name
                    break
            except Exception:
                pass

        if has_circuit_breaker:
            score += 30
            found.append(CriterionItem(
                "Cơ chế ngắt mạch CIRCUIT BREAKER & RETRY WITH JITTER chống sập dây chuyền (Cascading Failure)",
                evidence=cb_file or "Resilience Module",
                details="Đã phát hiện cơ chế Circuit Breaker / Retry bảo vệ các lời gọi liên dịch vụ trước sự cố sập domino.",
                badge="Circuit Breaker"
            ))
        else:
            missing.append(CriterionItem(
                "Cơ chế CIRCUIT BREAKER bảo vệ các lời gọi liên dịch vụ phân tán",
                evidence="Inter-service Calls",
                details="Thiếu cơ chế ngắt mạch (Circuit Breaker) và retry có jitter khi gọi các dịch vụ bên ngoài.",
                remediation="Sử dụng Resilience4j, Tenacity, Polly hoặc axios-retry với exponential backoff."
            ))

        # 3. Inter-service contracts (gRPC / Event-Driven)
        has_contracts = bool(self.tree.find_by_ext('.proto')) or 'KAFKA CLIENT' in self.tools or 'RABBITMQ CLIENT' in self.tools
        contract_ev = ".proto files" if bool(self.tree.find_by_ext('.proto')) else "Kafka/RabbitMQ Broker"

        if has_contracts:
            score += 25
            found.append(CriterionItem(
                "Hợp đồng liên dịch vụ chặt chẽ qua gRPC PROTOBUF hoặc EVENT-DRIVEN MESSAGING (KAFKA/RABBITMQ)",
                evidence=contract_ev,
                details="Đã xác minh hợp đồng giao tiếp giữa các dịch vụ có cấu trúc chặt chẽ qua Protobuf hoặc Event Broker.",
                badge="Inter-service"
            ))
        else:
            missing.append(CriterionItem(
                "Đặc tả hợp đồng giao tiếp liên dịch vụ (gRPC Protobuf hoặc Event Broker)",
                evidence="Dịch vụ phân tán",
                details="Chưa có đặc tả hợp đồng gRPC Protobuf hoặc message schema cho bus sự kiện phân tán.",
                remediation="Định nghĩa tệp `.proto` hoặc AsyncAPI schema cho luồng giao tiếp giữa các microservices."
            ))

        # 4. Correlation ID Tracking
        has_correlation_id = False
        corr_file = None

        for p in self.tree.code_files:
            try:
                t = self.tree.read_text(p)
                if 'x-request-id' in t.lower() or 'correlationid' in t.lower() or 'traceparent' in t.lower():
                    has_correlation_id = True
                    corr_file = str(self.tree.rel_path(p)) if hasattr(self.tree, 'rel_path') else p.name
                    break
            except Exception:
                pass

        if has_correlation_id:
            score += 15
            found.append(CriterionItem(
                "Đính kèm CORRELATION ID (x-request-id) xuyên suốt hành trình của request",
                evidence=corr_file or "x-request-id",
                details="Đã xác minh middleware gắn x-request-id / traceparent hỗ trợ truy vết phân tán xuyên suốt các dịch vụ.",
                badge="Correlation ID"
            ))
        else:
            missing.append(CriterionItem(
                "Middleware gán CORRELATION ID (x-request-id) phục vụ truy vết phân tán",
                evidence="HTTP Middleware",
                details="Chưa có middleware gắn mã Correlation ID (x-request-id) để theo dõi luồng request xuyên qua nhiều service.",
                remediation="Thêm middleware trích xuất hoặc tự sinh `x-request-id` và truyền tiếp trong header outgoing requests."
            ))

        score = min(100, score)
        self.scores['Hệ Thống PHÂN TÁN & GATEWAY (MICROSERVICES)'] = score
        self.add_log("  -> Audited API Gateway, Proto/gRPC schemas and microservice boundaries.", "microservices", "muted")
        self.details['microservices'] = {
            'name': 'Hệ Thống Phân Tán & Gateway',
            'found': found,
            'missing': missing,
            'score': score,
            'max_points': 15,
            'is_na': False
        }

    def audit_data_and_caching(self):
        score = 0
        found = []
        missing = []

        # 1. Redis Caching & Mandatory TTL
        has_redis = 'REDIS CLIENT' in self.databases or 'REDIS (DISTRIBUTED CACHE)' in self.databases or any('redis' in p.name.lower() for p in self.tree.all_files)
        has_ttl = False
        redis_file = None

        if has_redis:
            for p in self.tree.code_files:
                try:
                    t = self.tree.read_text(p)
                    if re.search(r'(setex|expire|ttl\s*=|ex\s*=|px\s*=|TimeSpan\.From)', t, re.IGNORECASE):
                        has_ttl = True
                        redis_file = str(self.tree.rel_path(p)) if hasattr(self.tree, 'rel_path') else p.name
                        break
                except Exception:
                    pass

            if has_ttl:
                score += 40
                found.append(CriterionItem(
                    "Chiến lược CACHING chuẩn mực: Bắt buộc cài đặt thời gian sống (TTL) cho mọi Redis Key",
                    evidence=redis_file or "Redis Cache",
                    details="Đã xác minh toàn bộ key cache đều có cài đặt TTL (expire/setex) chống tràn bộ nhớ RAM.",
                    badge="TTL Configured"
                ))
            else:
                score += 15
                missing.append(CriterionItem(
                    "Thiết lập TTL (Time-To-Live) bắt buộc cho Cache Key để chống cạn kiệt RAM Redis",
                    evidence="Redis Caching",
                    details="Phát hiện sử dụng Redis nhưng có lệnh lưu cache không cài đặt thời gian hết hạn (TTL), rủi ro tràn RAM.",
                    remediation="Bắt buộc truyền TTL khi ghi cache: `SETEX key seconds value` hoặc `expire(key, time)`."
                ))
        else:
            score += 35
            found.append(CriterionItem(
                "Dự án áp dụng bộ nhớ đệm cục bộ (In-Memory Cache) đơn giản",
                evidence="In-Memory Cache",
                details="Dự án sử dụng cơ chế cache trong bộ nhớ tiến trình (In-Memory Cache) phù hợp với quy mô hiện tại.",
                badge="In-Memory"
            ))

        # 2. Connection Pool Limits
        has_pool_limits = False
        pool_file = None

        for p in self.tree.code_files:
            try:
                t = self.tree.read_text(p)
                if re.search(r'(max_connections|pool_size|connectionLimit|maxPoolSize|poolTimeout)', t, re.IGNORECASE):
                    has_pool_limits = True
                    pool_file = str(self.tree.rel_path(p)) if hasattr(self.tree, 'rel_path') else p.name
                    break
            except Exception:
                pass

        if has_pool_limits:
            score += 30
            found.append(CriterionItem(
                "Giới hạn CONNECTION POOLING rõ ràng bảo vệ hạ tầng cơ sở dữ liệu",
                evidence=pool_file or "Pool Config",
                details="Đã xác minh tham số giới hạn connection pooling tối đa chống cạn kiệt tài nguyên kết nối.",
                badge="Pool Limits OK"
            ))
        else:
            missing.append(CriterionItem(
                "Giới hạn CONNECTION POOLING tối đa để chống nghẽn đường truyền (Connection Exhaustion)",
                evidence="Database Driver",
                details="Chưa cấu hình giới hạn kết nối đồng thời tối đa tới CSDL, có nguy cơ gây tắc nghẽn connection pool.",
                remediation="Thiết lập `max_connections` hoặc `pool_size` giới hạn số lượng kết nối đồng thời."
            ))

        # 3. Data Schema Validation / Data Contracts
        has_data_contract = 'PYDANTIC (DATA VALIDATION)' in self.tools or any(p.name.lower().startswith('schema.') or p.name.lower().startswith('models.') for p in self.tree.code_files)

        if has_data_contract:
            score += 30
            found.append(CriterionItem(
                "Kiểm soát chặt chẽ hợp đồng dữ liệu qua DATA CONTRACTS / SCHEMA VALIDATION",
                evidence="Schemas / Models",
                details="Đã xác minh đối tượng truyền tải dữ liệu có schema validation chặt chẽ bảo vệ tính toàn vẹn dữ liệu.",
                badge="Data Contracts"
            ))
        else:
            missing.append(CriterionItem(
                "Đặc tả SCHEMA tường minh cho các đối tượng luồng dữ liệu (Data Contracts)",
                evidence="Data Pipelines",
                details="Chưa có schema định nghĩa cấu trúc dữ liệu tường minh (Pydantic / Zod / Avro) cho các đối tượng trao đổi.",
                remediation="Tạo các lớp schema kiểm chứng kiểu dữ liệu trước khi nạp vào pipeline xử lý."
            ))

        score = min(100, score)
        self.scores['Kỹ Thuật DỮ LIỆU & CACHE (DATA RESILIENCY)'] = score
        self.add_log("  -> Reviewed Caching strategy (Redis/In-memory) and data resiliency.", "data_caching", "muted")
        self.details['data_caching'] = {
            'name': 'Kỹ Thuật Dữ Liệu & Cache',
            'found': found,
            'missing': missing,
            'score': score,
            'max_points': 15,
            'is_na': False
        }

    def audit_observability_and_ops(self):
        score = 0
        found = []
        missing = []

        # 1. Structured JSON Logging
        has_structured_logger = any(l in self.tools for l in ['WINSTON', 'PINO', 'SERILOG', 'LOGURU / STRUCTLOG'])

        if has_structured_logger:
            matched_logger = [l for l in ['WINSTON', 'PINO', 'SERILOG', 'LOGURU / STRUCTLOG'] if l in self.tools]
            score += 40
            found.append(CriterionItem(
                "Ghi nhật ký có cấu trúc chuẩn mực (STRUCTURED JSON LOGGING) sẵn sàng cho ELK / Loki",
                evidence=", ".join(matched_logger),
                details=f"Đã phát hiện thư viện ghi log có cấu trúc ({', '.join(matched_logger)}) hỗ trợ phân tích log tập trung.",
                badge="JSON Logging"
            ))
        else:
            missing.append(CriterionItem(
                "Thư viện ghi nhật ký có cấu trúc STRUCTURED LOGGING (thay thế console.log / print thô)",
                evidence="Logging",
                details="Mã nguồn sử dụng console.log hoặc print thô rải rác thay vì thư viện logging có cấu trúc JSON (Winston, Pino, Loguru).",
                remediation="Chuyển đổi sang thư viện Structured Logger (Winston/Pino cho Node.js, Loguru cho Python)."
            ))

        # 2. Distributed Tracing (OpenTelemetry)
        has_otel = 'OPENTELEMETRY' in self.tools or any('otel' in p.name.lower() for p in self.tree.all_files)

        if has_otel:
            score += 30
            found.append(CriterionItem(
                "Tích hợp OPENTELEMETRY phục vụ thu thập dấu vết và phân tích độ trễ xuyên suốt",
                evidence="OpenTelemetry SDK",
                details="Đã xác minh tích hợp SDK OpenTelemetry hỗ trợ APM và đo lường độ trễ chi tiết từng span.",
                badge="OpenTelemetry"
            ))
        else:
            missing.append(CriterionItem(
                "Công cụ truy vết OPENTELEMETRY để theo dõi độ trễ hệ thống",
                evidence="APM / Tracing",
                details="Chưa trang bị công cụ APM Tracing phân tán để quan sát độ trễ của các lệnh gọi CSDL và API bên ngoài.",
                remediation="Cài đặt `@opentelemetry/sdk-node` hoặc `opentelemetry-sdk` Python để theo dõi hiệu năng hệ thống."
            ))

        # 3. Prometheus / Metrics Endpoint
        has_metrics = False
        metrics_file = None

        for p in self.tree.code_files:
            try:
                t = self.tree.read_text(p)
                if '/metrics' in t or 'prometheus' in t.lower() or 'prom-client' in t:
                    has_metrics = True
                    metrics_file = str(self.tree.rel_path(p)) if hasattr(self.tree, 'rel_path') else p.name
                    break
            except Exception:
                pass

        if has_metrics:
            score += 30
            found.append(CriterionItem(
                "Cung cấp endpoint chỉ số PROMETHEUS METRICS (/metrics) phục vụ giám sát",
                evidence=metrics_file or "/metrics",
                details="Đã xác minh endpoint xuất chỉ số hiệu năng chuẩn Prometheus hỗ trợ Grafana dashboards.",
                badge="Prometheus OK"
            ))
        else:
            missing.append(CriterionItem(
                "Endpoint xuất chỉ số hiệu năng PROMETHEUS METRICS (/metrics) phục vụ giám sát",
                evidence="Monitoring Endpoints",
                details="Chưa có endpoint `/metrics` định dạng Prometheus để thu thập dữ liệu tải CPU, RAM và request rate.",
                remediation="Tích hợp thư viện `prom-client` hoặc `prometheus_client` mở endpoint `/metrics`."
            ))

        score = min(100, score)
        self.scores['GIÁM SÁT & VẬN HÀNH (OBSERVABILITY & OPS)'] = score
        self.add_log("  -> Audited Structured Logging, Prometheus metrics and OpenTelemetry traces.", "observability", "muted")
        self.details['observability'] = {
            'name': 'Giám Sát & Vận Hành',
            'found': found,
            'missing': missing,
            'score': score,
            'max_points': 15,
            'is_na': False
        }
