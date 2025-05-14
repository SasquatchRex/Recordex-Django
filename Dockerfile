FROM python:3.11-slim

WORKDIR /app

# Install system dependencies first
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]