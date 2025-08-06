FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    ANONYMIZED_TELEMETRY=False \
    # Force pip to fail if package not found locally (no internet)
    PIP_NO_INDEX=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 appuser

# Copy wheels directory - THIS IS YOUR PACKAGE CACHE
COPY --chown=appuser:appuser wheels /tmp/wheels

# Create a local pip repository index
RUN cd /tmp/wheels && \
    python3 -m pip install --user pip-tools && \
    ls -1 *.whl > index.txt

# Copy requirements file
COPY --chown=appuser:appuser requirements.txt .

# Switch to non-root user
USER appuser

# Install ONLY from local wheels (completely offline)
# --no-index: Don't use PyPI at all
# --find-links: Use /tmp/wheels as package source
RUN pip install --user \
    --no-index \
    --find-links /tmp/wheels \
    --no-cache-dir \
    "numpy<2.0" && \
    pip install --user \
    --no-index \
    --find-links /tmp/wheels \
    --no-cache-dir \
    -r requirements.txt

# Clean up wheels after installation to reduce image size
USER root
RUN rm -rf /tmp/wheels

# Copy application code
COPY --chown=appuser:appuser . .

# Copy and set permissions for entrypoint script
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh && \
    chown -R appuser:appuser /app

# Switch back to non-root user
USER appuser

# Add user's pip install location to PATH
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# Run the application
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]