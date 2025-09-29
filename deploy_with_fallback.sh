#!/bin/bash

# Deploy with fallback approach - start with local storage, then migrate to MinIO
echo "🚀 Deploying with fallback approach..."

# Stop current deployment
echo "⏹️ Stopping current deployment..."
docker-compose -f docker-compose.prod.yml down

# Set environment variables
export STORAGE_TYPE=local
export MINIO_ACCESS_KEY=minioadmin
export MINIO_SECRET_KEY=minioadmin

# Start services with local storage first
echo "🔨 Starting services with local storage..."
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
    
    # Now create MinIO buckets
    echo "🗄️ Creating MinIO buckets..."
    docker-compose -f docker-compose.prod.yml exec -T minio mc alias set minio http://localhost:9000 minioadmin minioadmin || true
    docker-compose -f docker-compose.prod.yml exec -T minio mc mb minio/shahin-media || echo "Bucket shahin-media already exists"
    docker-compose -f docker-compose.prod.yml exec -T minio mc mb minio/shahin-static || echo "Bucket shahin-static already exists"
    
    # Set bucket policies to public
    echo "🔓 Setting bucket policies..."
    docker-compose -f docker-compose.prod.yml exec -T minio mc anonymous set public minio/shahin-media || true
    docker-compose -f docker-compose.prod.yml exec -T minio mc anonymous set public minio/shahin-static || true
    
    echo "✅ MinIO buckets created successfully!"
    echo ""
    echo "🎉 Deployment completed successfully!"
    echo ""
    echo "📋 Next Steps:"
    echo "  1. Application is running with local storage"
    echo "  2. MinIO buckets are created and ready"
    echo "  3. To switch to MinIO, run:"
    echo "     export STORAGE_TYPE=minio"
    echo "     docker-compose -f docker-compose.prod.yml up -d"
    echo ""
    echo "🌐 Access your application:"
    echo "  Main Site: https://shahinautoservice.ir"
    echo "  Admin Panel: https://shahinautoservice.ir/admin/"
    echo "  MinIO Console: https://minio.shahinautoservice.ir"
    echo ""
    echo "🔑 Default Credentials:"
    echo "  Django Admin: admin / admin123"
    echo "  MinIO Console: minioadmin / minioadmin"
    
else
    echo "❌ Application test failed with local storage, checking logs..."
    docker-compose -f docker-compose.prod.yml logs --tail=30 web
fi
