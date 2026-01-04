"""
Production settings for shahin_auto project.
"""

import os
from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-your-secret-key-here-change-in-production')

# Allowed hosts
ALLOWED_HOSTS = os.environ.get(
    'ALLOWED_HOSTS',
    'shahinautoservice.ir,www.shahinautoservice.ir,localhost,127.0.0.1'
).split(',')
# Ensure localhost/127.0.0.1 are always allowed for internal health checks
ALLOWED_HOSTS = [h.strip() for h in ALLOWED_HOSTS if h.strip()]
for _h in ('localhost', '127.0.0.1'):
    if _h not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(_h)

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    'https://shahinautoservice.ir',
    'https://www.shahinautoservice.ir',
    'http://shahinautoservice.ir',
    'http://www.shahinautoservice.ir',
]

# Database configuration for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'shahin_db'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', '232330scmj'),
        'HOST': os.environ.get('DB_HOST', 'db'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Using PyMySQL for MySQL database connection (pure Python, no compilation required)

# Sites framework
SITE_ID = 1

# Robots.txt settings
ROBOTS_USE_SITEMAP = True
ROBOTS_SITEMAP_URLS = [
    'https://shahinautoservice.ir/sitemap.xml',
]

"""Object storage (Hamravesh/Arvan S3-compatible) configuration"""
USE_S3 = os.getenv('USE_S3', 'False').lower() == 'true'

if USE_S3:
    # Read ARVAN_* envs and map to django-storages AWS_* settings
    ARVAN_ACCESS_KEY_ID = os.getenv('ARVAN_ACCESS_KEY_ID') or os.getenv('AWS_ACCESS_KEY_ID')
    ARVAN_SECRET_ACCESS_KEY = os.getenv('ARVAN_SECRET_ACCESS_KEY') or os.getenv('AWS_SECRET_ACCESS_KEY')
    ARVAN_BUCKET_NAME = os.getenv('ARVAN_BUCKET_NAME') or os.getenv('AWS_STORAGE_BUCKET_NAME')
    ARVAN_REGION = os.getenv('ARVAN_REGION', 'ir-thr-at1') or os.getenv('AWS_S3_REGION_NAME', 'ir-thr-at1')
    ARVAN_ENDPOINT_URL = os.getenv('ARVAN_ENDPOINT_URL') or os.getenv('AWS_S3_ENDPOINT_URL')
    ARVAN_ADDRESSING_STYLE = os.getenv('ARVAN_ADDRESSING_STYLE', os.getenv('AWS_S3_ADDRESSING_STYLE', 'virtual'))
    ARVAN_CUSTOM_DOMAIN = os.getenv('ARVAN_CUSTOM_DOMAIN') or os.getenv('AWS_S3_CUSTOM_DOMAIN')
    ARVAN_SIGNATURE_VERSION = os.getenv('ARVAN_SIGNATURE_VERSION', 's3v4')

    AWS_ACCESS_KEY_ID = ARVAN_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = ARVAN_SECRET_ACCESS_KEY
    AWS_STORAGE_BUCKET_NAME = ARVAN_BUCKET_NAME
    AWS_S3_REGION_NAME = ARVAN_REGION
    AWS_S3_ENDPOINT_URL = ARVAN_ENDPOINT_URL
    AWS_S3_ADDRESSING_STYLE = ARVAN_ADDRESSING_STYLE
    AWS_S3_CUSTOM_DOMAIN = ARVAN_CUSTOM_DOMAIN
    AWS_S3_SIGNATURE_VERSION = ARVAN_SIGNATURE_VERSION

    # Public access and caching
    AWS_DEFAULT_ACL = 'public-read'
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_FILE_OVERWRITE = False
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }

    # Derive custom domain when not explicitly provided
    if not AWS_S3_CUSTOM_DOMAIN:
        _endpoint = (AWS_S3_ENDPOINT_URL or '').replace('https://', '').replace('http://', '').rstrip('/')
        AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.{_endpoint}' if _endpoint else None

    # STORAGES config for S3 storage
    STORAGES = {
        'default': {
            'BACKEND': 'main.storage_backends.MediaStorage',
        },
        'staticfiles': {
            'BACKEND': 'main.storage_backends.StaticStorage',
        },
    }

    # URLs - Always use custom domain for better performance and caching
    if AWS_S3_CUSTOM_DOMAIN:
        STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
        MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
    else:
        # Fallback to endpoint URL if no custom domain
        base = AWS_S3_ENDPOINT_URL.rstrip('/') if AWS_S3_ENDPOINT_URL else ''
        STATIC_URL = f'{base}/{AWS_STORAGE_BUCKET_NAME}/static/'
        MEDIA_URL = f'{base}/{AWS_STORAGE_BUCKET_NAME}/media/'
    
    # Ensure STATIC_ROOT is not used when using S3
    STATIC_ROOT = None
    
    # Keep STATICFILES_DIRS for collectstatic to find files
    STATICFILES_DIRS = [
        BASE_DIR / 'static',
    ]
else:
    # Local storage for production (served by nginx)
    STATIC_ROOT = '/app/staticfiles'
    STATIC_URL = '/static/'
    # Media files are served from separate media URL
    MEDIA_URL = '/media/'
    MEDIA_ROOT = '/app/media'
    
    # STORAGES config for local storage
    STORAGES = {
        'default': {
            'BACKEND': 'django.core.files.storage.FileSystemStorage',
            'OPTIONS': {
                'location': MEDIA_ROOT,
                'base_url': MEDIA_URL,
            },
        },
        'staticfiles': {
            'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
        },
    }

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Respect X-Forwarded-Proto from Nginx for HTTPS detection
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Session security
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# Rely on Nginx to enforce HTTPS; keep app accessible over HTTP on internal network
SECURE_SSL_REDIRECT = False

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'your-email@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'your-app-password')

# Cache configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f"redis://{os.environ.get('REDIS_HOST', 'redis')}:{os.environ.get('REDIS_PORT', '6379')}/1",
    }
}

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/app/logs/django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# CORS settings for production
CORS_ALLOWED_ORIGINS = [
    "https://shahinautoservice.ir",
    "https://www.shahinautoservice.ir",
]

# Add WhiteNoise for static files (only if not using S3)
if not USE_S3:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
