# Multi-stage build for Project-Builder-4-Agents Auditor & Reviewer Server
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt || true

FROM python:3.12-slim AS runner
WORKDIR /app

# Least privilege: Run as non-root user
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /bin/sh appuser

COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appgroup . .

USER appuser
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Liveness probe endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/api/status')" || exit 1

EXPOSE 5000
CMD ["python", "scripts/project_auditor.py", "."]
