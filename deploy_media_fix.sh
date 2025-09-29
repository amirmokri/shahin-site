#!/bin/bash

# Media Files Deployment Fix Script
# This script helps fix media file issues in Django deployment

echo "🔧 Starting media files deployment fix..."

# Set environment variable to disable S3
export USE_S3=False

echo "✅ Set USE_S3=False for local media storage"

# Build and deploy with correct settings
echo "🚀 Building and deploying with media fix..."

# Build the containers
docker-compose -f docker-compose.prod.yml build --no-cache

# Stop existing containers
docker-compose -f docker-compose.prod.yml down

# Start the services
docker-compose -f docker-compose.prod.yml up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Collect static files
echo "📁 Collecting static files..."
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# Check if media directory exists and has proper permissions
echo "🔍 Checking media directory..."
docker-compose -f docker-compose.prod.yml exec web ls -la /app/media/

# Test media file access
echo "🧪 Testing media file access..."
docker-compose -f docker-compose.prod.yml exec web curl -I http://localhost:8000/media/site/hero.jpg

echo "✅ Deployment fix completed!"
echo "🌐 Your site should now display images correctly at: https://shahinautoservice.ir"
echo ""
echo "📋 If images still don't show:"
echo "1. Check nginx logs: docker-compose -f docker-compose.prod.yml logs nginx"
echo "2. Check web logs: docker-compose -f docker-compose.prod.yml logs web"
echo "3. Verify media files exist: docker-compose -f docker-compose.prod.yml exec web ls -la /app/media/"
