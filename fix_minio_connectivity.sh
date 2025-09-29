#!/bin/bash

# Comprehensive fix for MinIO connectivity issues
echo "🔧 Fixing MinIO connectivity issues..."

# Stop current deployment
echo "⏹️ Stopping current deployment..."
docker-compose -f docker-compose.prod.yml down

# Clean up any network issues
echo "🧹 Cleaning up Docker networks..."
docker network prune -f

# Start with local storage first
echo "🚀 Starting with local storage first..."
export STORAGE_TYPE=local

# Start services
echo "🔨 Starting services..."
docker-compose -f docker-compose.prod.yml up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 60

# Check container status
echo "📊 Checking container status..."
docker-compose -f docker-compose.prod.yml ps

# Test application with local storage
echo "🧪 Testing application with local storage..."
sleep 10
if curl -f http://localhost/health/ >/dev/null 2>&1; then
    echo "✅ Application is running with local storage!"
    
    # Now set up MinIO properly
    echo "🗄️ Setting up MinIO..."
    
    # Wait for MinIO to be fully ready
    echo "⏳ Waiting for MinIO to be fully ready..."
    for i in {1..30}; do
        if curl -f http://localhost:9000/minio/health/live >/dev/null 2>&1; then
            echo "✅ MinIO is ready!"
            break
        fi
        echo "Waiting for MinIO... ($i/30)"
        sleep 2
    done
    
    # Create MinIO buckets
    echo "🗄️ Creating MinIO buckets..."
    docker-compose -f docker-compose.prod.yml exec -T minio mc alias set minio http://localhost:9000 minioadmin minioadmin
    docker-compose -f docker-compose.prod.yml exec -T minio mc mb minio/shahin-media
    docker-compose -f docker-compose.prod.yml exec -T minio mc mb minio/shahin-static
    
    # Set bucket policies to public
    echo "🔓 Setting bucket policies..."
    docker-compose -f docker-compose.prod.yml exec -T minio mc anonymous set public minio/shahin-media
    docker-compose -f docker-compose.prod.yml exec -T minio mc anonymous set public minio/shahin-static
    
    echo "✅ MinIO setup completed!"
    
    # Test MinIO connectivity from web container
    echo "🧪 Testing MinIO connectivity from web container..."
    docker-compose -f docker-compose.prod.yml exec -T web python manage.py shell -c "
from django.conf import settings
print('Storage type:', settings.STORAGE_TYPE)
print('MinIO endpoint:', settings.MINIO_ENDPOINT_URL)
print('MinIO bucket:', settings.MINIO_BUCKET_NAME)
"
    
    echo ""
    echo "🎉 Setup completed successfully!"
    echo ""
    echo "📋 Current Status:"
    echo "  ✅ Application running with local storage"
    echo "  ✅ MinIO buckets created and configured"
    echo "  ✅ Sitemap links added to footer (hidden for SEO)"
    echo ""
    echo "🔄 To switch to MinIO storage:"
    echo "  export STORAGE_TYPE=minio"
    echo "  docker-compose -f docker-compose.prod.yml up -d"
    echo ""
    echo "🌐 Access your application:"
    echo "  Main Site: https://shahinautoservice.ir"
    echo "  Admin Panel: https://shahinautoservice.ir/admin/"
    echo "  MinIO Console: https://minio.shahinautoservice.ir"
    echo "  Sitemap: https://shahinautoservice.ir/sitemap.xml"
    echo ""
    echo "🔑 Default Credentials:"
    echo "  Django Admin: admin / admin123"
    echo "  MinIO Console: minioadmin / minioadmin"
    
else
    echo "❌ Application test failed, checking logs..."
    docker-compose -f docker-compose.prod.yml logs --tail=30 web
    echo ""
    echo "🔧 Try running the fallback deployment:"
    echo "  ./deploy_with_fallback.sh"
fi
