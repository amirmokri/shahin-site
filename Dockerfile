# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV DJANGO_SETTINGS_MODULE=shahin_auto.settings_production

# Set work directory
WORKDIR /app

# Install system dependencies for mysqlclient
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        default-libmysqlclient-dev \
        build-essential \
        pkg-config \
        wget \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install Python dependencies first (for better caching)
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Create directories and set permissions
RUN mkdir -p /app/staticfiles /app/media /app/logs \
    && chmod -R 755 /app

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Create startup script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Wait for database using Python MySQL connection\n\
echo "Waiting for database..."\n\
python - <<"PYCODE"\n\
import os, time, sys\n\
import MySQLdb as mysql\n\
host = os.environ.get("DB_HOST", "db")\n\
port = int(os.environ.get("DB_PORT", "3306"))\n\
user = os.environ.get("DB_USER", "root")\n\
password = os.environ.get("DB_PASSWORD", "")\n\
name = os.environ.get("DB_NAME", "")\n\
for i in range(60):\n\
    try:\n\
        conn = mysql.connect(host=host, port=port, user=user, passwd=password, db=name)\n\
        conn.close()\n\
        print("Database is up")\n\
        break\n\
    except Exception as e:\n\
        print(f"DB not ready ({e}); retry {i+1}/60")\n\
        time.sleep(2)\n\
else:\n\
    print("Database not reachable after retries", file=sys.stderr)\n\
    sys.exit(1)\n\
PYCODE\n\
\n\
# Run migrations\n\
echo "Running migrations..."\n\
python manage.py migrate --noinput\n\
\n\
# Wait for MinIO to be ready if using MinIO\n\
if [ "$STORAGE_TYPE" = "minio" ]; then\n\
    echo "Waiting for MinIO to be ready..."\n\
    for i in {1..30}; do\n\
        if curl -f http://minio:9000/minio/health/live >/dev/null 2>&1; then\n\
            echo "MinIO is ready!"\n\
            break\n\
        fi\n\
        echo "Waiting for MinIO... ($i/30)"\n\
        sleep 2\n\
    done\n\
    \n\
    echo "Setting up MinIO storage..."\n\
    python manage.py setup_storage --storage-type=minio --create-buckets || echo "Storage setup failed, continuing..."\n\
elif [ "$STORAGE_TYPE" = "aws" ]; then\n\
    echo "Setting up AWS S3 storage..."\n\
    python manage.py setup_storage --storage-type=aws --create-buckets || echo "Storage setup failed, continuing..."\n\
fi\n\
\n\
# Collect static files\n\
echo "Collecting static files..."\n\
python manage.py collectstatic --noinput\n\
\n\
# Start server\n\
echo "Starting Gunicorn server..."\n\
exec gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 120 --access-logfile - --error-logfile - shahin_auto.wsgi:application\n\
' > /app/start.sh && chmod +x /app/start.sh

# Run the application
CMD ["/app/start.sh"]