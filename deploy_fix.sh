#!/bin/bash

# Quick deployment script to apply media files fixes
echo "🚀 Deploying Media Files Fix..."

# Stop existing containers
echo "⏹️ Stopping existing containers..."
docker-compose -f docker-compose.prod.yml down

# Rebuild and start containers
echo "🔨 Building and starting containers..."
docker-compose -f docker-compose.prod.yml up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check container status
echo "📊 Checking container status..."
docker-compose -f docker-compose.prod.yml ps

# Test media file serving
echo "🧪 Testing media file serving..."
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

echo "✅ Deployment completed!"
echo "🌐 Your site should now be accessible at: https://shahinautoservice.ir"
echo "📋 Check the troubleshooting guide if you encounter any issues: MEDIA_FILES_TROUBLESHOOTING.md"
