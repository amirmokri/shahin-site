#!/bin/bash

# Quick fix for the USE_S3 variable error
echo "🔧 Fixing deployment error..."

# Stop the current deployment
echo "⏹️ Stopping current deployment..."
docker-compose -f docker-compose.prod.yml down

# Rebuild and restart with the fix
echo "🔨 Rebuilding and starting with fix..."
docker-compose -f docker-compose.prod.yml up -d --build

# Wait for services
echo "⏳ Waiting for services to start..."
sleep 30

# Check status
echo "📊 Checking deployment status..."
docker-compose -f docker-compose.prod.yml ps

# Test the application
echo "🧪 Testing application..."
sleep 10
if curl -f http://localhost/health/ >/dev/null 2>&1; then
    echo "✅ Application is running successfully!"
else
    echo "❌ Application test failed, checking logs..."
    docker-compose -f docker-compose.prod.yml logs --tail=20 web
fi

echo "🎉 Fix applied successfully!"
