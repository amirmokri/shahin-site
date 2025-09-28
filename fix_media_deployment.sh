#!/bin/bash

# Media Files Fix Script for Shahin Auto Service
# This script ensures media files are properly configured for production deployment

set -e

echo "🔧 Fixing Media Files Configuration..."

# Check if we're in production mode
if [ "${DJANGO_SETTINGS_MODULE}" = "shahin_auto.settings_production" ]; then
    echo "📋 Production mode detected"
    
    # Ensure media directory exists and has correct permissions
    echo "📁 Creating media directories..."
    mkdir -p /app/media/{site,services,lectures,bonus}
    chmod -R 755 /app/media
    
    # Copy local media files if they exist
    if [ -d "./media" ]; then
        echo "📂 Copying local media files to container..."
        cp -r ./media/* /app/media/ 2>/dev/null || true
    fi
    
    # Ensure static files are collected
    echo "🎨 Collecting static files..."
    python manage.py collectstatic --noinput --clear
    
    # Set proper permissions
    echo "🔐 Setting proper permissions..."
    chmod -R 755 /app/staticfiles
    chmod -R 755 /app/media
    
    echo "✅ Media files configuration completed!"
else
    echo "📋 Development mode detected - skipping media fixes"
fi

echo "🚀 Deployment script completed successfully!"
