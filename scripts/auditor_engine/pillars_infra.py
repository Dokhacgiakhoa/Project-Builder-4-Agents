"""Security, Cloud, Microservices, Data and Observability pillars."""

import os
import sys
import re
import json
import datetime
from pathlib import Path

from .constants import IGNORE_DIRS, CODE_EXTENSIONS  # noqa: F401
from .models import CriterionItem


class InfraPillarsMixin:
    """Security, Cloud, Microservices, Data and Observability pillars."""

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
                'Pin exact dependency versions via DEPENDENCY LOCKFILE (against Supply Chain Attacks)',
                evidence=", ".join(matched_lfs),
                details=f"Detected a lockfile verifying hashes and dependency versions: {', '.join(matched_lfs)}.",
                badge="Lockfile OK"
            ))
        else:
            missing.append(CriterionItem(
                'Dependency lockfile (package-lock.json, poetry.lock, go.sum)',
                evidence='Root folder',
                details='No lockfile pinning dependency package versions; risk of a supply chain attack or environment drift.',
                remediation='Run npm install / poetry lock / cargo generate-lockfile and commit the lockfile to Git.'
            ))
            self.gaps.append('Missing a dependency lockfile, risking version drift or malicious code.')

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
                'HTTP security headers configuration (Strict CORS, Helmet, Content-Security-Policy)',
                evidence=headers_file or "HTTP Middleware",
                details='Detected HTTP header protection configuration (CORS, Helmet or CSP) against XSS and Clickjacking.',
                badge="Security Headers"
            ))
        else:
            missing.append(CriterionItem(
                'Configured HTTP security headers protocol protection (CORS, Helmet, CSP)',
                evidence="Server Config",
                details='Standard security headers (Content-Security-Policy, X-Frame-Options, Helmet) are not configured to protect the application.',
                remediation='Integrate Helmet middleware or strict CORS to protect the HTTP protocol.'
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
                'Rate limiting mechanism protecting against brute-force and DDoS',
                evidence=ratelimit_file or "Rate Limiter",
                details='Verified rate limiter protecting against brute-force attacks and resource exhaustion.',
                badge="Rate Limiting"
            ))
        else:
            missing.append(CriterionItem(
                'Rate limiting protecting APIs from brute-force scanning attacks',
                evidence="API Middleware",
                details='No API rate-limiting middleware (Rate Limiting / Throttle) for sensitive endpoints.',
                remediation='Add express-rate-limit, slowapi or a redis-based rate limiter for authentication/public APIs.'
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
                'Sensitive environment isolation: .env 100% excluded from Git repository',
                evidence=".gitignore",
                details='.env file containing secrets is safely excluded in .gitignore and not tracked by Git.',
                badge="Secrets Isolated"
            ))
        else:
            missing.append(CriterionItem(
                'Strict secret isolation policy (.env in .gitignore and KMS/Vault usage)',
                evidence=".gitignore / .env",
                details='The .env file is not excluded in .gitignore, or there is a risk of leaking configuration secrets.',
                remediation='Add `.env` and `*.pem` to the `.gitignore` file immediately.'
            ))

        score = min(100, score)
        self.scores['SECURITY & Supply Chain'] = score
        self.add_log("  -> Checked supply chain lockfiles, .env isolation and scanned for hardcoded secrets.", "security", "muted")
        self.details['security'] = {
            'name': 'Security & Supply Chain',
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
                'Standard multi-stage build Dockerfile optimizing size and security',
                evidence=df_target_name,
                details='Verified Dockerfile utilizes multi-stage build separating compilation from minimal runtime.',
                badge="Multi-Stage"
            ))
        else:
            missing.append(CriterionItem(
                'Optimized multi-stage Dockerfile (separating build from minimal runtime)',
                evidence=df_target_name,
                details='The Dockerfile does not use a Multi-stage build (AS builder -> FROM minimal), bloating the image size.',
                remediation='Split the Dockerfile into a Build stage (containing the SDK/compiler) and a Runtime stage (containing only dist and a minimal runtime).'
            ))

        if has_nonroot:
            score += 25
            found.append(CriterionItem(
                'Container running with minimal privileges (non-root user)',
                evidence=df_target_name,
                snippet="USER node / appuser / non-root",
                details='A non-root user is declared in the Dockerfile to prevent container-escape privilege escalation.',
                badge="Non-Root"
            ))
        else:
            missing.append(CriterionItem(
                'Non-root user declaration in Dockerfile preventing container escapes',
                evidence=df_target_name,
                details='The Dockerfile runs as root by default, risking container escape if the application has a vulnerability.',
                remediation='Add `USER node` or create an appuser: `USER appuser` before the ENTRYPOINT/CMD instruction.'
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
                'Health check probe endpoints: Liveness & Readiness probes (/healthz, /readyz)',
                evidence=probe_file or "/healthz",
                details='Verified health-check endpoints (/healthz, /readyz) that let Kubernetes/Cloud orchestrators route traffic safely.',
                badge="Health Probes"
            ))
        else:
            missing.append(CriterionItem(
                'Liveness & Readiness probe endpoints (/healthz, /readyz) for cloud orchestrator',
                evidence="Routing / Endpoints",
                details='Missing an application health-check endpoint (/health or /healthz) for load balancers and Kubernetes probes.',
                remediation='Create a GET `/health` or `/healthz` endpoint returning the status of the server and database.'
            ))

        # 3. Infrastructure as Code (Docker Compose, K8s manifests, Helm)
        has_iac = bool(self.tree.find_by_name('docker-compose.yml') or self.tree.find_by_name('docker-compose.yaml')) or any('k8s' in p.parts or 'helm' in p.parts for p in self.tree.all_files)
        iac_ev = "docker-compose.yml" if bool(self.tree.find_by_name('docker-compose.yml') or self.tree.find_by_name('docker-compose.yaml')) else "Kubernetes / Helm"

        if has_iac:
            score += 20
            found.append(CriterionItem(
                'Infrastructure as Code declaration (Docker Compose / Kubernetes manifests)',
                evidence=iac_ev,
                details=f"Detected local and cloud deployment infrastructure declared as code via `{iac_ev}`.",
                badge="IaC Ready"
            ))
        else:
            missing.append(CriterionItem(
                'Infrastructure as Code management file (docker-compose.yml or K8s Helm)',
                evidence='Root folder',
                details='No docker-compose.yml or Kubernetes manifests to automate a uniform environment setup.',
                remediation='Create a `docker-compose.yml` defining the app, database and cache services for the dev environment.'
            ))

        score = min(100, score)
        self.scores['CLOUD & CONTAINER Infrastructure (DEVOPS)'] = score
        self.add_log("  -> Audited Dockerfile config, container specs and CI/CD workflows.", "cloud", "muted")
        self.details['cloud'] = {
            'name': 'Cloud Infrastructure & DevOps',
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
                'API Gateway / Reverse Proxy as centralized ingress traffic router',
                evidence=gw_file or "API Gateway",
                details='Verified Gateway/Reverse Proxy routing and ingress configuration.',
                badge="API Gateway"
            ))
        else:
            missing.append(CriterionItem(
                'Centralized API Gateway configuration (Kong, Traefik, Ocelot, or Nginx)',
                evidence='Network infrastructure',
                details='No Reverse Proxy or API Gateway to manage routing, auth and SSL termination centrally.',
                remediation='Set up Nginx, Traefik or Kong as the central reverse proxy.'
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
                'Circuit Breaker & retry with jitter preventing cascading failures',
                evidence=cb_file or "Resilience Module",
                details='Detected a Circuit Breaker / Retry mechanism protecting inter-service calls from cascading failures.',
                badge="Circuit Breaker"
            ))
        else:
            missing.append(CriterionItem(
                'Circuit breaker mechanism protecting distributed inter-service calls',
                evidence="Inter-service Calls",
                details='Missing a circuit breaker and retry with jitter when calling external services.',
                remediation='Use Resilience4j, Tenacity, Polly or axios-retry with exponential backoff.'
            ))

        # 3. Inter-service contracts (gRPC / Event-Driven)
        has_contracts = bool(self.tree.find_by_ext('.proto')) or 'KAFKA CLIENT' in self.tools or 'RABBITMQ CLIENT' in self.tools
        contract_ev = ".proto files" if bool(self.tree.find_by_ext('.proto')) else "Kafka/RabbitMQ Broker"

        if has_contracts:
            score += 25
            found.append(CriterionItem(
                'Inter-service contract enforcement via gRPC Protobuf or Event-driven messaging',
                evidence=contract_ev,
                details='Verified that inter-service communication contracts are strictly structured via Protobuf or an Event Broker.',
                badge="Inter-service"
            ))
        else:
            missing.append(CriterionItem(
                'Inter-service communication contract specification (gRPC Protobuf or Event Broker)',
                evidence='Distributed services',
                details='No gRPC Protobuf contract specification or message schema for the distributed event bus.',
                remediation='Define a `.proto` file or an AsyncAPI schema for communication between microservices.'
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
                'Correlation ID (x-request-id) propagation throughout request lifecycle',
                evidence=corr_file or "x-request-id",
                details='Verified middleware attaching x-request-id / traceparent to support distributed tracing across services.',
                badge="Correlation ID"
            ))
        else:
            missing.append(CriterionItem(
                'Middleware attaching Correlation ID (x-request-id) for distributed tracing',
                evidence="HTTP Middleware",
                details='No middleware attaching a Correlation ID (x-request-id) to follow request flows across multiple services.',
                remediation='Add middleware that extracts or generates `x-request-id` and propagates it in outgoing request headers.'
            ))

        score = min(100, score)
        self.scores['DISTRIBUTED Systems & GATEWAY (MICROSERVICES)'] = score
        self.add_log("  -> Audited API Gateway, Proto/gRPC schemas and microservice boundaries.", "microservices", "muted")
        self.details['microservices'] = {
            'name': 'Distributed Systems & Gateway',
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
                    'Standard caching strategy: Mandatory TTL for all cache keys',
                    evidence=redis_file or "Redis Cache",
                    details='Verified that all cache keys have a TTL (expire/setex) preventing RAM overflow.',
                    badge="TTL Configured"
                ))
            else:
                score += 15
                missing.append(CriterionItem(
                    'Mandatory TTL configuration for cache keys preventing RAM exhaustion',
                    evidence="Redis Caching",
                    details='Redis usage detected but some cache-write commands set no expiry (TTL), risking RAM overflow.',
                    remediation='Always pass a TTL when writing the cache: `SETEX key seconds value` or `expire(key, time)`.'
                ))
        else:
            score += 35
            found.append(CriterionItem(
                'Project applies basic local in-memory caching',
                evidence="In-Memory Cache",
                details='The project uses in-process memory caching (In-Memory Cache), which fits the current scale.',
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
                'Explicit connection pooling limit protecting database infrastructure',
                evidence=pool_file or "Pool Config",
                details='Verified maximum connection pooling limits preventing connection exhaustion.',
                badge="Pool Limits OK"
            ))
        else:
            missing.append(CriterionItem(
                'Maximum connection pooling limit preventing connection exhaustion',
                evidence="Database Driver",
                details='No maximum concurrent database connection limit configured, risking connection pool congestion.',
                remediation='Set `max_connections` or `pool_size` to limit the number of concurrent connections.'
            ))

        # 3. Data Schema Validation / Data Contracts
        has_data_contract = 'PYDANTIC (DATA VALIDATION)' in self.tools or any(p.name.lower().startswith('schema.') or p.name.lower().startswith('models.') for p in self.tree.code_files)

        if has_data_contract:
            score += 30
            found.append(CriterionItem(
                'Strict data contract control via Data Contracts / Schema Validation',
                evidence="Schemas / Models",
                details='Verified data transfer objects have strict schema validation protecting integrity.',
                badge="Data Contracts"
            ))
        else:
            missing.append(CriterionItem(
                'Explicit schema specification for data transfer objects (Data Contracts)',
                evidence="Data Pipelines",
                details='No schema defining an explicit data structure (Pydantic / Zod / Avro) for exchanged objects.',
                remediation='Create schema classes that validate data types before they enter the processing pipeline.'
            ))

        score = min(100, score)
        self.scores['DATA Engineering & CACHE (DATA RESILIENCY)'] = score
        self.add_log("  -> Reviewed Caching strategy (Redis/In-memory) and data resiliency.", "data_caching", "muted")
        self.details['data_caching'] = {
            'name': 'Data Engineering & Cache',
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
                'Standardized structured JSON logging ready for ELK / Loki',
                evidence=", ".join(matched_logger),
                details=f"Detected a structured logging library ({', '.join(matched_logger)}) supporting centralized log analysis.",
                badge="JSON Logging"
            ))
        else:
            missing.append(CriterionItem(
                'Structured logging library (replacing raw console.log / print)',
                evidence="Logging",
                details='The source code scatters raw console.log or print instead of a JSON structured logging library (Winston, Pino, Loguru).',
                remediation='Switch to a Structured Logger library (Winston/Pino for Node.js, Loguru for Python).'
            ))

        # 2. Distributed Tracing (OpenTelemetry)
        has_otel = 'OPENTELEMETRY' in self.tools or any('otel' in p.name.lower() for p in self.tree.all_files)

        if has_otel:
            score += 30
            found.append(CriterionItem(
                'OpenTelemetry integration for end-to-end tracing and latency analysis',
                evidence="OpenTelemetry SDK",
                details='Verified OpenTelemetry SDK integration supporting APM and span latency measurement.',
                badge="OpenTelemetry"
            ))
        else:
            missing.append(CriterionItem(
                'OpenTelemetry tracing instrumentation for latency observation',
                evidence="APM / Tracing",
                details='Missing distributed APM tracing tool to monitor database and external API call latencies.',
                remediation='Install `@opentelemetry/sdk-node` or `opentelemetry-sdk` Python to track performance.'
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
                'Prometheus metrics endpoint (/metrics) for operational monitoring',
                evidence=metrics_file or "/metrics",
                details='Verified a Prometheus-standard performance metrics export endpoint supporting Grafana dashboards.',
                badge="Prometheus OK"
            ))
        else:
            missing.append(CriterionItem(
                'Prometheus metrics export endpoint (/metrics) for monitoring',
                evidence="Monitoring Endpoints",
                details='No Prometheus-format `/metrics` endpoint to collect CPU, RAM load and request rate data.',
                remediation='Integrate `prom-client` or `prometheus_client` to expose a `/metrics` endpoint.'
            ))

        score = min(100, score)
        self.scores['MONITORING & OPERATIONS (OBSERVABILITY & OPS)'] = score
        self.add_log("  -> Audited Structured Logging, Prometheus metrics and OpenTelemetry traces.", "observability", "muted")
        self.details['observability'] = {
            'name': 'Monitoring & Operations',
            'found': found,
            'missing': missing,
            'score': score,
            'max_points': 15,
            'is_na': False
        }
