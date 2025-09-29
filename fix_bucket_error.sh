#!/bin/bash

# Fix for MinIO bucket error during deployment
echo "🔧 Fixing MinIO bucket error..."

# Stop current deployment
echo "⏹️ Stopping current deployment..."
docker-compose -f docker-compose.prod.yml down

# Rebuild with the fix
echo "🔨 Rebuilding with bucket creation fix..."
docker-compose -f docker-compose.prod.yml up -d --build

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 60

# Check if web container is running
echo "📊 Checking container status..."
docker-compose -f docker-compose.prod.yml ps

# Check web container logs
echo "📋 Checking web container logs..."
docker-compose -f docker-compose.prod.yml logs --tail=20 web

# If web container is still failing, let's manually create buckets
echo "🗄️ Manually creating MinIO buckets if needed..."
docker-compose -f docker-compose.prod.yml exec -T minio mc alias set minio http://localhost:9000 minioadmin minioadmin || true
docker-compose -f docker-compose.prod.yml exec -T minio mc mb minio/shahin-media || echo "Bucket shahin-media already exists"
docker-compose -f docker-compose.prod.yml exec -T minio mc mb minio/shahin-static || echo "Bucket shahin-static already exists"

# Try to restart web container
echo "🔄 Restarting web container..."
docker-compose -f docker-compose.prod.yml restart web

# Wait and check again
sleep 30
echo "📊 Final status check..."
docker-compose -f docker-compose.prod.yml ps

# Test application
echo "🧪 Testing application..."
sleep 10
if curl -f http://localhost/health/ >/dev/null 2>&1; then
    echo "✅ Application is running successfully!"
    echo "🎉 Bucket error fixed!"
else
    echo "❌ Application still not responding, checking logs..."
    docker-compose -f docker-compose.prod.yml logs --tail=30 web
    echo ""
    echo "🔧 Try running: docker-compose -f docker-compose.prod.yml exec web python manage.py setup_storage --storage-type=minio --create-buckets"
fi
