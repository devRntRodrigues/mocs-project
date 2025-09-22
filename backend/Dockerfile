# Use Python 3.13 image
FROM python:3.13

# Set working directory
WORKDIR /app

# Install system dependencies for OCR
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-por \
    tesseract-ocr-eng \
    libtesseract-dev \
    poppler-utils \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set UV to install packages in the global Python environment
ENV UV_SYSTEM_PYTHON=1

# Copy project files for dependency installation
COPY pyproject.toml ./
COPY uv.lock ./
COPY README.md ./

# Install dependencies globally to avoid venv conflicts with volume mounts
RUN uv sync --frozen

# Create uploads directory
RUN mkdir -p uploads

# Copy all source code (this will be overridden by volume mount in dev)
COPY app/ app/
COPY main.py .

# Expose port
EXPOSE 8000

# Run the application with hot reload
CMD ["uv", "run", "uvicorn", "app.core.app:get_application", "--host", "0.0.0.0", "--port", "8000", "--reload", "--factory"]


