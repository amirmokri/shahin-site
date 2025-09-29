# Media Files Troubleshooting Guide

## Problem
Images are not displaying on the deployed website at hamravesh.com, but they work fine locally.

## Root Causes Identified

### 1. **S3 Storage Configuration Conflict**
- **Issue**: Production settings had `USE_S3 = True` by default
- **Problem**: Django was trying to serve media files from S3 URLs that don't exist
- **Fix**: Changed default to `USE_S3 = False` for local file storage

### 2. **Missing Media URL Configuration**
- **Issue**: Media URLs were not properly configured for local storage in production
- **Problem**: Django couldn't generate correct URLs for media files
- **Fix**: Added explicit `MEDIA_URL = '/media/'` for local storage

### 3. **WhiteNoise Configuration Conflict**
- **Issue**: WhiteNoise was configured regardless of storage backend
- **Problem**: WhiteNoise can interfere with media file serving
- **Fix**: Only enable WhiteNoise when not using S3

### 4. **File Permissions**
- **Issue**: Media directory permissions might not be correct
- **Problem**: Web server couldn't access media files
- **Fix**: Added explicit permissions in Dockerfile

## Files Modified

### 1. `shahin_auto/settings_production.py`
```python
# Changed default from True to False
USE_S3 = os.getenv('USE_S3', 'False').lower() == 'true'

# Added explicit local storage configuration
else:
    STATIC_ROOT = '/app/staticfiles'
    MEDIA_ROOT = '/app/media'
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'

# Fixed WhiteNoise configuration
if not USE_S3:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
```

### 2. `env.example`
```bash
# Changed default from True to False
USE_S3=False
```

### 3. `Dockerfile`
```dockerfile
# Added explicit media directory permissions
RUN mkdir -p /app/staticfiles /app/media /app/logs \
    && chmod -R 755 /app \
    && chmod -R 755 /app/media
```

## Deployment Steps

### Option 1: Use the Fix Script (Recommended)
```bash
# For Linux/Mac
./deploy_media_fix.sh

# For Windows
deploy_media_fix.bat
```

### Option 2: Manual Deployment
```bash
# Set environment variable
export USE_S3=False

# Build and deploy
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d

# Wait for services to start
sleep 30

# Collect static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

## Verification Steps

### 1. Check Media Directory
```bash
docker-compose -f docker-compose.prod.yml exec web ls -la /app/media/
```

### 2. Test Media File Access
```bash
docker-compose -f docker-compose.prod.yml exec web curl -I http://localhost:8000/media/site/hero.jpg
```

### 3. Check Nginx Configuration
```bash
docker-compose -f docker-compose.prod.yml logs nginx
```

### 4. Check Django Logs
```bash
docker-compose -f docker-compose.prod.yml logs web
```

## Nginx Configuration (Already Correct)
Your nginx configuration is properly set up:
```nginx
# Media files
location /media/ {
    alias /app/media/;
    expires 1y;
    add_header Cache-Control "public";
}
```

## Environment Variables
Make sure your production environment has:
```bash
USE_S3=False
```

## Common Issues and Solutions

### Issue 1: 404 Errors for Media Files
**Symptoms**: Images return 404 errors
**Solution**: 
1. Verify `USE_S3=False` in environment
2. Check nginx is serving `/media/` requests
3. Ensure media files exist in `/app/media/`

### Issue 2: Permission Denied
**Symptoms**: 403 Forbidden errors
**Solution**:
1. Check file permissions: `ls -la /app/media/`
2. Ensure nginx user can read files
3. Run: `chmod -R 755 /app/media/`

### Issue 3: Wrong URLs Generated
**Symptoms**: Images try to load from S3 URLs
**Solution**:
1. Verify `MEDIA_URL = '/media/'` in production settings
2. Check `USE_S3=False` environment variable
3. Restart Django application

### Issue 4: Static Files Working but Media Not
**Symptoms**: CSS/JS loads but images don't
**Solution**:
1. Check nginx media location block
2. Verify media directory volume mounting
3. Ensure media files are copied to container

## Testing Commands

### Test Media URL Generation
```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py shell
```
```python
from django.conf import settings
print(f"MEDIA_URL: {settings.MEDIA_URL}")
print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
print(f"USE_S3: {getattr(settings, 'USE_S3', 'Not set')}")
```

### Test File Existence
```bash
docker-compose -f docker-compose.prod.yml exec web find /app/media -name "*.jpg" -o -name "*.png"
```

## Contact Information
If issues persist, check:
1. Hamravesh.com deployment logs
2. Docker container logs
3. Nginx access/error logs
4. Django application logs

## Additional Notes
- The fix ensures media files are served locally by nginx
- S3 integration is available but disabled by default
- All media files should be accessible via `/media/` URLs
- Static files continue to work with WhiteNoise or S3
