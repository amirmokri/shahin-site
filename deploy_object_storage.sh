#!/bin/bash

# Object Storage Deployment Script for Shahin Auto Service
# This script deploys the application with MinIO object storage

set -e

echo "🚀 Deploying Shahin Auto Service with Object Storage..."

# Set default environment variables
export STORAGE_TYPE=${STORAGE_TYPE:-minio}
export MINIO_ACCESS_KEY=${MINIO_ACCESS_KEY:-minioadmin}
export MINIO_SECRET_KEY=${MINIO_SECRET_KEY:-minioadmin}
export MINIO_BUCKET_NAME=${MINIO_BUCKET_NAME:-shahin-media}
export MINIO_STATIC_BUCKET_NAME=${MINIO_STATIC_BUCKET_NAME:-shahin-static}
export MINIO_ENDPOINT_URL=${MINIO_ENDPOINT_URL:-http://minio:9000}

echo "📋 Configuration:"
echo "  Storage Type: $STORAGE_TYPE"
echo "  MinIO Endpoint: $MINIO_ENDPOINT_URL"
echo "  Media Bucket: $MINIO_BUCKET_NAME"
echo "  Static Bucket: $MINIO_STATIC_BUCKET_NAME"

# Stop existing containers
echo "⏹️ Stopping existing containers..."
docker-compose -f docker-compose.prod.yml down

# Remove old volumes if needed (uncomment if you want to start fresh)
# echo "🗑️ Removing old volumes..."
# docker volume rm shahin_minio_data || true

# Build and start containers
echo "🔨 Building and starting containers..."
docker-compose -f docker-compose.prod.yml up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 60

# Check container status
echo "📊 Checking container status..."
docker-compose -f docker-compose.prod.yml ps

# Wait for MinIO to be ready
echo "⏳ Waiting for MinIO to be ready..."
until docker-compose -f docker-compose.prod.yml exec -T minio curl -f http://localhost:9000/minio/health/live >/dev/null 2>&1; do
    echo "Waiting for MinIO..."
    sleep 5
done

echo "✅ MinIO is ready!"

# Set up storage and migrate files
echo "🗄️ Setting up object storage..."
docker-compose -f docker-compose.prod.yml exec web python manage.py setup_storage --storage-type=minio --create-buckets --migrate-files

# Collect static files
echo "🎨 Collecting static files..."
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# Test storage connection
echo "🧪 Testing storage connection..."
docker-compose -f docker-compose.prod.yml exec web python manage.py shell -c "
from main.storage import get_storage_backend
storage = get_storage_backend()
print('Storage backend:', type(storage).__name__)
print('Storage test: SUCCESS' if storage else 'Storage test: FAILED')
"

# Create admin user if it doesn't exist
echo "👤 Creating admin user..."
docker-compose -f docker-compose.prod.yml exec web python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@shahinautoservice.ir', 'admin123')
    print('Admin user created: admin/admin123')
else:
    print('Admin user already exists')
"

# Test application health
echo "🏥 Testing application health..."
sleep 10
if curl -f http://localhost/health/ >/dev/null 2>&1; then
    echo "✅ Application is healthy!"
else
    echo "❌ Application health check failed"
    echo "📋 Checking logs..."
    docker-compose -f docker-compose.prod.yml logs --tail=50 web
fi

echo ""
echo "🎉 Deployment completed successfully!"
echo ""
echo "🌐 Access your application:"
echo "  Main Site: https://shahinautoservice.ir"
echo "  Admin Panel: https://shahinautoservice.ir/admin/"
echo "  MinIO Console: https://minio.shahinautoservice.ir"
echo ""
echo "🔑 Default Credentials:"
echo "  Django Admin: admin / admin123"
echo "  MinIO Console: $MINIO_ACCESS_KEY / $MINIO_SECRET_KEY"
echo ""
echo "📋 Next Steps:"
echo "  1. Change admin password immediately"
echo "  2. Configure MinIO console access"
echo "  3. Upload your media files"
echo "  4. Test file uploads and downloads"
echo ""
echo "📚 For troubleshooting, check:"
echo "  docker-compose -f docker-compose.prod.yml logs web"
echo "  docker-compose -f docker-compose.prod.yml logs minio"
