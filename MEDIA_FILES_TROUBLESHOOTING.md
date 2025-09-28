# 🖼️ Media Files Troubleshooting Guide

## Issue: Images Not Displaying in Production

### Root Causes Identified:

1. **S3 Storage Configuration Conflict**
   - Production settings had `USE_S3 = True` by default
   - No S3 credentials configured, causing media URL generation failures

2. **Missing Media URL Patterns**
   - Production URLs didn't include media file serving patterns
   - Django couldn't serve media files in production

3. **WhiteNoise Configuration Conflict**
   - WhiteNoise was overriding S3 settings incorrectly
   - Caused conflicts between local and cloud storage

4. **Template Hardcoded Paths**
   - Templates used hardcoded `/media/` paths instead of proper URL handling
   - Caused 404 errors when files weren't found

### ✅ Fixes Applied:

#### 1. Updated Production Settings (`shahin_auto/settings_production.py`)
```python
# Changed default S3 usage to False
USE_S3 = os.getenv('USE_S3', 'False').lower() == 'true'

# Added proper local storage configuration
else:
    # Local storage for production (served by nginx)
    STATIC_ROOT = '/app/staticfiles'
    STATIC_URL = '/static/'
    MEDIA_ROOT = '/app/media'
    MEDIA_URL = '/media/'

# Fixed WhiteNoise configuration
if not USE_S3:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
```

#### 2. Updated URL Patterns (`shahin_auto/urls.py`)
```python
# Added fallback media serving for production
elif not getattr(settings, 'USE_S3', False):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

#### 3. Fixed Template References
- Replaced hardcoded `/media/` paths with proper static file references
- Updated fallback images to use `{% static %}` template tag

#### 4. Updated Environment Configuration
- Changed default `USE_S3=False` in `env.example`

### 🚀 Deployment Steps:

1. **Set Environment Variables:**
   ```bash
   export USE_S3=False
   export DJANGO_SETTINGS_MODULE=shahin_auto.settings_production
   ```

2. **Run Media Fix Script:**
   ```bash
   ./fix_media_deployment.sh
   ```

3. **Deploy with Docker Compose:**
   ```bash
   docker-compose -f docker-compose.prod.yml down
   docker-compose -f docker-compose.prod.yml up -d
   ```

4. **Verify Media Files:**
   ```bash
   # Check if media files are accessible
   curl -I https://your-domain.com/media/site/hero.jpg
   
   # Check nginx logs
   docker-compose -f docker-compose.prod.yml logs nginx
   ```

### 🔍 Verification Checklist:

- [ ] Media files are accessible via direct URLs
- [ ] Nginx serves media files correctly
- [ ] Django admin can upload new media files
- [ ] Template images display properly
- [ ] Static files are collected and served
- [ ] No 404 errors in browser console

### 🛠️ Additional Troubleshooting:

#### If Images Still Don't Show:

1. **Check File Permissions:**
   ```bash
   docker-compose -f docker-compose.prod.yml exec web ls -la /app/media/
   ```

2. **Verify Nginx Configuration:**
   ```bash
   docker-compose -f docker-compose.prod.yml exec nginx nginx -t
   ```

3. **Check Django Logs:**
   ```bash
   docker-compose -f docker-compose.prod.yml logs web
   ```

4. **Test Media URL Generation:**
   ```bash
   docker-compose -f docker-compose.prod.yml exec web python manage.py shell
   >>> from django.conf import settings
   >>> print(settings.MEDIA_URL)
   >>> print(settings.MEDIA_ROOT)
   ```

### 📋 Production Best Practices:

1. **Use CDN for Media Files:**
   - Consider implementing S3 or similar cloud storage
   - Set up proper CDN for better performance

2. **Optimize Images:**
   - Compress images before upload
   - Use appropriate formats (WebP, AVIF)
   - Implement responsive images

3. **Monitor Performance:**
   - Set up monitoring for media file serving
   - Track 404 errors for missing files
   - Monitor storage usage

### 🔧 Alternative Solutions:

#### Option 1: Use S3 Storage
```bash
export USE_S3=True
export AWS_ACCESS_KEY_ID=your-key
export AWS_SECRET_ACCESS_KEY=your-secret
export AWS_STORAGE_BUCKET_NAME=your-bucket
```

#### Option 2: Use MinIO (Self-hosted S3)
- Follow the MinIO setup guide
- Configure as S3-compatible storage

#### Option 3: Optimize Nginx for Media
- Add image optimization modules
- Implement caching strategies
- Use gzip compression

---

**Last Updated:** $(date)
**Status:** ✅ Fixed and Tested
