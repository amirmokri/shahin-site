@echo off
REM Media Files Deployment Fix Script for Windows
REM This script helps fix media file issues in Django deployment

echo 🔧 Starting media files deployment fix...

REM Set environment variable to disable S3
set USE_S3=False

echo ✅ Set USE_S3=False for local media storage

REM Build and deploy with correct settings
echo 🚀 Building and deploying with media fix...

REM Build the containers
docker-compose -f docker-compose.prod.yml build --no-cache

REM Stop existing containers
docker-compose -f docker-compose.prod.yml down

REM Start the services
docker-compose -f docker-compose.prod.yml up -d

REM Wait for services to be ready
echo ⏳ Waiting for services to start...
timeout /t 30 /nobreak >nul

REM Collect static files
echo 📁 Collecting static files...
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

REM Check if media directory exists and has proper permissions
echo 🔍 Checking media directory...
docker-compose -f docker-compose.prod.yml exec web ls -la /app/media/

REM Test media file access
echo 🧪 Testing media file access...
docker-compose -f docker-compose.prod.yml exec web curl -I http://localhost:8000/media/site/hero.jpg

echo ✅ Deployment fix completed!
echo 🌐 Your site should now display images correctly at: https://shahinautoservice.ir
echo.
echo 📋 If images still don't show:
echo 1. Check nginx logs: docker-compose -f docker-compose.prod.yml logs nginx
echo 2. Check web logs: docker-compose -f docker-compose.prod.yml logs web
echo 3. Verify media files exist: docker-compose -f docker-compose.prod.yml exec web ls -la /app/media/

pause
