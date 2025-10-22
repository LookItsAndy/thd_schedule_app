# Dockerfile
FROM python:3.11-slim

# Prevent .pyc, and ensure output flushes
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Cloud Run provides $PORT; default to 8080 locally
ENV PORT=8080

# Use gunicorn to serve Flask in production
CMD ["gunicorn", "-b", ":8080", "app:app"]
