#!/bin/bash

# Deploy with local static files first, then migrate to object storage
echo "🚀 Deploying with local static files first..."

# Stop current deployment
echo "⏹️ Stopping current deployment..."
docker-compose -f docker-compose.prod.yml down

# Set environment to use local storage for static files temporarily
export STORAGE_TYPE=minio
export MINIO_ACCESS_KEY=minioadmin
export MINIO_SECRET_KEY=minioadmin

# Create a temporary docker-compose override
cat > docker-compose.override.yml << EOF
services:
  web:
    environment:
      - STATICFILES_STORAGE=whitenoise.storage.CompressedStaticFilesStorage
EOF

# Start services
echo "🔨 Starting services with local static storage..."
docker-compose -f docker-compose.prod.yml up -d

# Wait for services
echo "⏳ Waiting for services to start..."
sleep 60

# Check status
echo "📊 Checking container status..."
docker-compose -f docker-compose.prod.yml ps

# Create MinIO buckets
echo "🗄️ Creating MinIO buckets..."
docker-compose -f docker-compose.prod.yml exec -T web python manage.py setup_storage --storage-type=minio --create-buckets || echo "Storage setup failed"

# Test MinIO connection
echo "🧪 Testing MinIO connection..."
docker-compose -f docker-compose.prod.yml exec -T web python manage.py shell -c "
from main.storage import get_storage_backend
storage = get_storage_backend()
print('Storage backend:', type(storage).__name__)
"

# Now switch to MinIO for static files
echo "🔄 Switching to MinIO for static files..."
rm docker-compose.override.yml

# Restart with MinIO static storage
docker-compose -f docker-compose.prod.yml up -d

# Wait and test
sleep 30
echo "📊 Final status check..."
docker-compose -f docker-compose.prod.yml ps

# Test application
echo "🧪 Testing application..."
sleep 10
if curl -f http://localhost/health/ >/dev/null 2>&1; then
    echo "✅ Application is running successfully!"
    echo "🎉 Deployment completed with object storage!"
else
    echo "❌ Application test failed, checking logs..."
    docker-compose -f docker-compose.prod.yml logs --tail=20 web
fi

echo ""
echo "🌐 Access your application:"
echo "  Main Site: https://shahinautoservice.ir"
echo "  Admin Panel: https://shahinautoservice.ir/admin/"
echo "  MinIO Console: https://minio.shahinautoservice.ir"
