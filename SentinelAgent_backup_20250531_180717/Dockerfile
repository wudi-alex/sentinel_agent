# SentinelAgent Dockerfile
# Multi-stage build for optimized production image

# Build stage
FROM python:3.11-slim AS builder

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set work directory
WORKDIR /app

# Copy Python dependencies from builder stage to a location accessible by appuser
COPY --from=builder /root/.local /usr/local

# Set PATH to include installed packages
ENV PATH=/usr/local/bin:$PATH

# Copy application code
COPY . .

# Create necessary directories and set permissions
RUN mkdir -p data/{output,uploads,demo} logs && \
    chown -R appuser:appuser /app

# Make scripts executable
RUN chmod +x scripts/*.py scripts/*.sh sentinel_agent.py

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5002

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5002/health || exit 1

# Default command
CMD ["python", "scripts/start_web_ui.py"]
