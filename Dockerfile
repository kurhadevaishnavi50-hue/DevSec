# --- Stage 1: Build & Dependency Gathering ---
FROM python:3.12-slim AS builder

WORKDIR /usr/src/app

# System build dependencies install karne ke liye (psutil ke compilation ke liye zaroori hai)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Cache optimization ke liye requirements pehle copy kar rahe hain
COPY requirements.txt ./

# Global path settings ke bina standard local directory mein wheels build karna
RUN pip install --no-cache-dir --user -r requirements.txt


# --- Stage 2: Final Secure Runtime Image ---
FROM python:3.12-slim AS runner

# Python optimization parameters setting
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH=/home/appuser/.local/bin:$PATH

WORKDIR /usr/src/app

# 🛡️ Trivy Compliance: Secure Non-Root User & Group Generation
RUN groupadd -g 10001 appuser && \
    useradd -u 10001 -g appuser -m -s /bin/bash appuser

# Stage 1 se built python packages ko user directory mein copy karna
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local
# Main application code script copy karna root privileges ke bina
COPY --chown=appuser:appuser app.py ./

# Port 80 open karna (Flask internal mapping matching deployment specs)
EXPOSE 80

# Non-root user par context switch karna
USER appuser

# Bufferless tracking mode execute karne ke liye cmd parameter mapping
CMD [ "python", "-u", "app.py" ]
