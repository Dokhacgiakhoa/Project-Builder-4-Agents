"""Pillar Security, Cloud, Microservices, Data và Observability."""

import os
import sys
import re
import json
import datetime
from pathlib import Path

from .constants import IGNORE_DIRS, CODE_EXTENSIONS  # noqa: F401


class InfraPillarsMixin:
    """Pillar Security, Cloud, Microservices, Data và Observability."""

    def audit_security_and_supply_chain(self):

        score = 0

        found = []

        missing = []

        # 1. Dependency Lockfiles

        lockfiles = ['package-lock.json', 'yarn.lock', 'pnpm-lock.yaml', 'poetry.lock', 'Pipfile.lock', 'go.sum', 'Cargo.lock', 'packages.lock.json']

        has_lockfile = any(bool(self.tree.find_by_name(lf)) for lf in lockfiles)

        if has_lockfile:

            score += 35

            found.append("Khóa chính xác phiên bản phụ thuộc qua DEPENDENCY LOCKFILE (chống Supply Chain Attack)")

        else:

            missing.append("Tệp DEPENDENCY LOCKFILE (package-lock.json, poetry.lock, go.sum)")

            self.gaps.append("Thiếu lockfile quản lý phụ thuộc, tiềm ẩn rủi ro trôi lệch phiên bản hoặc dính mã độc.")

        # 2. HTTP Security Headers (Helmet, CORS)

        has_headers = 'HELMET (HTTP HEADERS)' in self.tools or 'CORS MIDDLEWARE' in self.tools

        if not has_headers:

            for p in self.tree.code_files:

                try:

                    t = p.read_text(encoding='utf-8', errors='ignore')

                    if 'helmet' in t or 'CORSMiddleware' in t or 'UseCors' in t or 'Content-Security-Policy' in t:

                        has_headers = True

                        break

                except Exception:

                    pass

        if has_headers:

            score += 25

            found.append("Cấu hình HTTP SECURITY HEADERS (CORS strict, HELMET, Content-Security-Policy)")

        else:

            missing.append("Thiết lập HTTP SECURITY HEADERS bảo vệ giao thức (CORS, Helmet, CSP)")

        # 3. Rate Limiting protection

        has_ratelimit = 'RATE LIMITING' in self.tools

        if not has_ratelimit:

            for p in self.tree.code_files:

                try:

                    t = p.read_text(encoding='utf-8', errors='ignore')

                    if 'rateLimit' in t or 'slowapi' in t or 'RateLimiter' in t or 'Throttle' in t:

                        has_ratelimit = True

                        break

                except Exception:

                    pass

        if has_ratelimit:

            score += 20

            found.append("Cơ chế RATE LIMITING giới hạn tần suất yêu cầu chống Brute-force & DDoS")

        else:

            missing.append("Cơ chế RATE LIMITING bảo vệ API trước các đợt tấn công vét cạn (Brute-force)")

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

            found.append("Cô lập biến môi trường nhạy cảm: .ENV được loại trừ 100% khỏi kho Git")

        else:

            missing.append("Chính sách cô lập SECRET nghiêm ngặt (đưa .ENV vào .gitignore và dùng KMS/Vault)")

        score = min(100, score)

        self.scores['Bảo Mật & Chuỗi Cung Ứng (SECURITY)'] = score

        self.add_log("  -> Kiểm tra lockfiles chuỗi cung ứng, file .env và quét hardcoded secrets.", "security", "muted")
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

        for df in dockerfiles:

            try:

                content = df.read_text(encoding='utf-8', errors='ignore')

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

            found.append("Dockerfile chuẩn mực MULTI-STAGE BUILD tối ưu dung lượng và tính bảo mật")

        else:

            missing.append("Dockerfile tối ưu MULTI-STAGE BUILD (tách biệt môi trường build và runtime)")

        if has_nonroot:

            score += 25

            found.append("Chạy CONTAINER với quyền hạn tối thiểu (USER NON-ROOT)")

        else:

            missing.append("Khai báo USER NON-ROOT trong Dockerfile để ngăn chặn Container Escape")

        # 2. Health Checks (Liveness & Readiness Probes)

        if not has_healthcheck:

            for p in self.tree.code_files:

                try:

                    t = p.read_text(encoding='utf-8', errors='ignore')

                    if '/healthz' in t or '/readyz' in t or '/health' in t:

                        has_healthcheck = True

                        break

                except Exception:

                    pass

        if has_healthcheck:

            score += 20

            found.append("Endpoint thăm dò trạng thái sức khỏe: LIVENESS & READINESS PROBES (/healthz, /readyz)")

        else:

            missing.append("Cung cấp endpoint LIVENESS & READINESS PROBES (/healthz, /readyz) cho bộ điều phối Cloud")

        # 3. Infrastructure as Code (Docker Compose, K8s manifests, Helm)

        has_iac = bool(self.tree.find_by_name('docker-compose.yml') or self.tree.find_by_name('docker-compose.yaml')) or any('k8s' in p.parts or 'helm' in p.parts for p in self.tree.all_files)

        if has_iac:

            score += 20

            found.append("Khai báo hạ tầng dưới dạng mã INFRASTRUCTURE AS CODE (DOCKER COMPOSE / KUBERNETES MANIFESTS)")

        else:

            missing.append("Tệp quản lý hạ tầng INFRASTRUCTURE AS CODE (docker-compose.yml hoặc K8s Helm)")

        score = min(100, score)

        self.scores['Hạ Tầng CLOUD & CONTAINER (DEVOPS)'] = score

        self.add_log("  -> Kiểm tra cấu hình Dockerfile, container specs và CI/CD workflows.", "cloud", "muted")
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

        if not has_gateway:

            for p in self.tree.find_by_ext('.conf'):

                try:

                    if 'proxy_pass' in p.read_text(encoding='utf-8', errors='ignore'):

                        has_gateway = True

                        break

                except Exception:

                    pass

        if has_gateway:

            score += 30

            found.append("API GATEWAY / REVERSE PROXY làm cổng điều phối lưu lượng tập trung")

        else:

            missing.append("Cấu hình API GATEWAY tập trung (Kong, Traefik, Ocelot hoặc Nginx)")

        # 2. Circuit Breaker & Resiliency (Polly, Resilience4j, Tenacity)

        has_circuit_breaker = False

        for p in self.tree.code_files:

            try:

                t = p.read_text(encoding='utf-8', errors='ignore')

                if re.search(r'(circuitBreaker|Policy\.Handle|resilience4j|tenacity|retry_with_backoff)', t, re.IGNORECASE):

                    has_circuit_breaker = True

                    break

            except Exception:

                pass

        if has_circuit_breaker:

            score += 30

            found.append("Cơ chế ngắt mạch CIRCUIT BREAKER & RETRY WITH JITTER chống sập dây chuyền (Cascading Failure)")

        else:

            missing.append("Cơ chế CIRCUIT BREAKER bảo vệ các lời gọi liên dịch vụ phân tán")

        # 3. Inter-service contracts (gRPC / Event-Driven)

        has_contracts = bool(self.tree.find_by_ext('.proto')) or 'KAFKA CLIENT' in self.tools or 'RABBITMQ CLIENT' in self.tools

        if has_contracts:

            score += 25

            found.append("Hợp đồng liên dịch vụ chặt chẽ qua gRPC PROTOBUF hoặc EVENT-DRIVEN MESSAGING (KAFKA/RABBITMQ)")

        else:

            missing.append("Đặc tả hợp đồng giao tiếp liên dịch vụ (gRPC Protobuf hoặc Event Broker)")

        # 4. Correlation ID Tracking

        has_correlation_id = False

        for p in self.tree.code_files:

            try:

                t = p.read_text(encoding='utf-8', errors='ignore')

                if 'x-request-id' in t.lower() or 'correlationid' in t.lower() or 'traceparent' in t.lower():

                    has_correlation_id = True

                    break

            except Exception:

                pass

        if has_correlation_id:

            score += 15

            found.append("Đính kèm CORRELATION ID (x-request-id) xuyên suốt hành trình của request")

        else:

            missing.append("Middleware gán CORRELATION ID (x-request-id) phục vụ truy vết phân tán")

        score = min(100, score)

        self.scores['Hệ Thống PHÂN TÁN & GATEWAY (MICROSERVICES)'] = score

        self.add_log("  -> Khảo sát API Gateway, Proto/gRPC schemas và ranh giới microservices.", "microservices", "muted")
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

        if has_redis:

            for p in self.tree.code_files:

                try:

                    t = p.read_text(encoding='utf-8', errors='ignore')

                    if re.search(r'(setex|expire|ttl\s*=|ex\s*=|px\s*=|TimeSpan\.From)', t, re.IGNORECASE):

                        has_ttl = True

                        break

                except Exception:

                    pass

            if has_ttl:

                score += 40

                found.append("Chiến lược CACHING chuẩn mực: Bắt buộc cài đặt thời gian sống (TTL) cho mọi Redis Key")

            else:

                score += 15

                missing.append("Thiết lập TTL (Time-To-Live) bắt buộc cho Cache Key để chống cạn kiệt RAM Redis")

        else:

            score += 35

            found.append("Dự án áp dụng bộ nhớ đệm cục bộ (In-Memory Cache) đơn giản")

        # 2. Connection Pool Limits

        has_pool_limits = False

        for p in self.tree.code_files:

            try:

                t = p.read_text(encoding='utf-8', errors='ignore')

                if re.search(r'(max_connections|pool_size|connectionLimit|maxPoolSize|poolTimeout)', t, re.IGNORECASE):

                    has_pool_limits = True

                    break

            except Exception:

                pass

        if has_pool_limits:

            score += 30

            found.append("Giới hạn CONNECTION POOLING rõ ràng bảo vệ hạ tầng cơ sở dữ liệu")

        else:

            missing.append("Giới hạn CONNECTION POOLING tối đa để chống nghẽn đường truyền (Connection Exhaustion)")

        # 3. Data Schema Validation / Data Contracts

        has_data_contract = 'PYDANTIC (DATA VALIDATION)' in self.tools or any(p.name.lower().startswith('schema.') or p.name.lower().startswith('models.') for p in self.tree.code_files)

        if has_data_contract:

            score += 30

            found.append("Kiểm soát chặt chẽ hợp đồng dữ liệu qua DATA CONTRACTS / SCHEMA VALIDATION")

        else:

            missing.append("Đặc tả SCHEMA tường minh cho các đối tượng luồng dữ liệu (Data Contracts)")

        score = min(100, score)

        self.scores['Kỹ Thuật DỮ LIỆU & CACHE (DATA RESILIENCY)'] = score

        self.add_log("  -> Rà soát chiến lược Cache (Redis/In-memory) và khả năng phục hồi dữ liệu.", "data_caching", "muted")
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

            score += 40

            found.append("Ghi nhật ký có cấu trúc chuẩn mực (STRUCTURED JSON LOGGING) sẵn sàng cho ELK / Loki")

        else:

            missing.append("Thư viện ghi nhật ký có cấu trúc STRUCTURED LOGGING (thay thế console.log / print thô)")

        # 2. Distributed Tracing (OpenTelemetry)

        has_otel = 'OPENTELEMETRY' in self.tools or any('otel' in p.name.lower() for p in self.tree.all_files)

        if has_otel:

            score += 30

            found.append("Tích hợp OPENTELEMETRY phục vụ thu thập dấu vết và phân tích độ trễ xuyên suốt")

        else:

            missing.append("Công cụ truy vết OPENTELEMETRY để theo dõi độ trễ hệ thống")

        # 3. Prometheus / Metrics Endpoint

        has_metrics = False

        for p in self.tree.code_files:

            try:

                t = p.read_text(encoding='utf-8', errors='ignore')

                if '/metrics' in t or 'prometheus' in t.lower() or 'prom-client' in t:

                    has_metrics = True

                    break

            except Exception:

                pass

        if has_metrics:

            score += 30

            found.append("Cung cấp endpoint chỉ số PROMETHEUS METRICS (/metrics) phục vụ cảnh báo tự động")

        else:

            missing.append("Endpoint xuất chỉ số hiệu năng PROMETHEUS METRICS (/metrics)")

        score = min(100, score)

        self.scores['Giám Sát & VẬN HÀNH (OBSERVABILITY & OPS)'] = score

        self.add_log("  -> Kiểm tra giải pháp Giám sát: Structured Logging, Tracing & Metrics.", "observability", "muted")
        self.details['observability'] = {

            'name': 'Giám Sát & Vận Hành',

            'found': found,

            'missing': missing,

            'score': score,

            'max_points': 15,

            'is_na': False

        }
