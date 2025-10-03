FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project
COPY . /app

# Install Python deps
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r Eyes-of-an-Addict/requirements.txt
# Add runtime helpers used in deployment and background workers
RUN pip install --no-cache-dir gunicorn rq redis

EXPOSE 8000

CMD ["gunicorn", "Eyes-of-an-Addict.app:create_app()", "--workers", "3", "--bind", "0.0.0.0:8000"]
