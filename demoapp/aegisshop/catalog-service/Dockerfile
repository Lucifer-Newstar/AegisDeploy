# syntax=docker/dockerfile:1
# ─────────────────────────────────────────────────────────────────────────────
# AegisShop catalog-service — vertical slice image (base-layer sprint).
# Multi-stage build: builder installs deps, runtime image is small and slim.
# Pinned base + explicit requirements = reproducible images (working rules).
# ─────────────────────────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
    SERVICE_NAME=catalog-service \
    SERVICE_PORT=9001
WORKDIR /app
# Copy the installed site-packages from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
# Copy the service package (renamed from 'app' → 'catalog_service', monorepo rule)
COPY catalog_service ./catalog_service
EXPOSE 9001
HEALTHCHECK --interval=10s --timeout=3s --retries=5 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:9001/health', timeout=3).status==200 else 1)"
CMD ["uvicorn", "catalog_service.main:app", "--host", "0.0.0.0", "--port", "9001"]
