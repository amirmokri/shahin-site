# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV DJANGO_SETTINGS_MODULE=shahin_auto.settings_production

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        default-libmysqlclient-dev \
        pkg-config \
        gcc \
        g++ \
        curl \
        wget \
        git \
        vim \
        default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Create directories for static and media files
RUN mkdir -p /app/staticfiles /app/media /app/logs

# Collect static files (skip if no database)
RUN python manage.py collectstatic --noinput --clear || true

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Create startup script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Wait for database\n\
echo "Waiting for database..."\n\
while ! python manage.py dbshell --command="SELECT 1;" > /dev/null 2>&1; do\n\
  echo "Database is unavailable - sleeping"\n\
  sleep 1\n\
done\n\
echo "Database is up - continuing"\n\
\n\
# Run migrations\n\
python manage.py migrate\n\
\n\
# Collect static files\n\
python manage.py collectstatic --noinput\n\
\n\
# Start server\n\
exec gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 120 shahin_auto.wsgi:application\n\
' > /app/start.sh && chmod +x /app/start.sh

# Run the application
CMD ["/app/start.sh"]
