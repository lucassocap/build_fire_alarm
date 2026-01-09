FROM python:3.9-slim
WORKDIR /app

# Install system dependencies
# poppler-utils is required for pdf2image
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Main command logic
ENV PORT 8080
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT}
