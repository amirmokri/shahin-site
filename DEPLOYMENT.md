# Shahin Auto Service - Deployment Guide

## 🚀 Production Deployment

This guide covers deploying the Shahin Auto Service Django application using Docker and Docker Compose.

## 📋 Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- Git
- At least 2GB RAM and 10GB disk space

## 🏗️ Project Structure

```
shahin/
├── Dockerfile                 # Docker image configuration
├── docker-compose.yml         # Multi-container setup
├── nginx.conf                 # Nginx reverse proxy config
├── requirements.txt           # Python dependencies
├── .dockerignore             # Docker ignore file
├── shahin_auto/
│   ├── settings.py           # Development settings
│   ├── settings_production.py # Production settings
│   └── ...
├── main/                     # Django app
├── templates/                # HTML templates
├── static/                   # Static files (CSS, JS, images)
└── media/                    # User uploaded files
```

## 🔧 Configuration

### 1. Environment Variables

Create a `.env` file in the project root:

```bash
# Database
DB_NAME=shahin_db
DB_USER=root
DB_PASSWORD=your-secure-password
DB_HOST=db
DB_PORT=3306

# Django
SECRET_KEY=your-very-secure-secret-key-here
DEBUG=0
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Email (for contact form)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
```

### 2. Media Files Setup

Upload your media files to the `media/` directory:

```
media/
├── site/
│   └── hero.jpg              # Hero background image
├── services/
│   ├── images/               # Service images
│   └── videos/               # Service videos (.mp4)
├── lectures/
│   └── images/               # Lecture images
└── bonuses/
    └── images/               # Bonus popup images
```

### 3. Static Files

Static files are automatically collected during deployment:
- `static/images/logo.png` - Your logo
- `static/css/custom.css` - Custom styles
- `static/js/main.js` - JavaScript functionality

## 🐳 Docker Deployment

### Quick Start

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd shahin
```

2. **Create environment file:**
```bash
cp env.example .env
# Edit .env with your configuration
```

3. **Build and start services:**
```bash
docker-compose up -d --build
```

4. **Create superuser:**
```bash
docker-compose exec web python manage.py createsuperuser
```

5. **Access the application:**
- Website: http://localhost
- Admin: http://localhost/admin

### Production Deployment

1. **Update docker-compose.yml:**
```yaml
# Remove development volumes
volumes:
  - static_volume:/app/staticfiles
  - media_volume:/app/media
  # Remove: - .:/app
```

2. **Set production environment:**
```bash
export DJANGO_SETTINGS_MODULE=shahin_auto.settings_production
```

3. **Deploy:**
```bash
docker-compose -f docker-compose.yml up -d --build
```

## 🔒 Security Configuration

### SSL/HTTPS Setup

1. **Obtain SSL certificates** (Let's Encrypt recommended)

2. **Update nginx.conf:**
```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    # ... rest of configuration
}
```

3. **Update docker-compose.yml:**
```yaml
nginx:
  volumes:
    - ./ssl:/etc/nginx/ssl
```

### Security Headers

The nginx.conf includes security headers:
- X-Frame-Options: SAMEORIGIN
- X-Content-Type-Options: nosniff
- X-XSS-Protection: 1; mode=block
- Content-Security-Policy

## 📊 Monitoring & Logs

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f nginx
docker-compose logs -f db
```

### Health Checks
```bash
# Application health
curl http://localhost/health/

# Database connection
docker-compose exec web python manage.py dbshell
```

## 🔄 Updates & Maintenance

### Update Application
```bash
git pull origin main
docker-compose down
docker-compose up -d --build
```

### Database Migrations
```bash
docker-compose exec web python manage.py migrate
```

### Collect Static Files
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### Backup Database
```bash
docker-compose exec db mysqldump -u root -p shahin_db > backup.sql
```

### Restore Database
```bash
docker-compose exec -T db mysql -u root -p shahin_db < backup.sql
```

## 🛠️ Troubleshooting

### Common Issues

1. **MySQL Connection Error:**
```bash
# Check database status
docker-compose ps db
docker-compose logs db

# Restart database
docker-compose restart db
```

2. **Static Files Not Loading:**
```bash
# Recollect static files
docker-compose exec web python manage.py collectstatic --noinput --clear
```

3. **Permission Issues:**
```bash
# Fix file permissions
docker-compose exec web chown -R appuser:appuser /app
```

4. **Memory Issues:**
```bash
# Check resource usage
docker stats

# Increase memory limits in docker-compose.yml
```

### Performance Optimization

1. **Enable Redis Caching:**
```python
# Already configured in settings_production.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
    }
}
```

2. **Database Optimization:**
```bash
# Add database indexes
docker-compose exec web python manage.py dbshell
```

3. **Static File Optimization:**
- Images are automatically compressed by WhiteNoise
- CSS/JS are minified in production

## 📱 Mobile Optimization

The application is fully responsive and optimized for mobile devices:
- Mobile-first design with Tailwind CSS
- Touch-friendly navigation
- Optimized images and videos
- Fast loading with lazy loading

## 🌐 Domain Configuration

### DNS Setup
Point your domain to your server's IP address:
```
A    yourdomain.com      -> YOUR_SERVER_IP
A    www.yourdomain.com  -> YOUR_SERVER_IP
```

### Nginx Configuration
Update `server_name` in nginx.conf:
```nginx
server_name yourdomain.com www.yourdomain.com;
```

## 📈 Scaling

### Horizontal Scaling
```yaml
# docker-compose.yml
web:
  deploy:
    replicas: 3
```

### Load Balancer
Use a load balancer (HAProxy, Nginx) in front of multiple web containers.

## 🔧 Development vs Production

| Feature | Development | Production |
|---------|-------------|------------|
| Debug | True | False |
| Database | SQLite/MySQL | MySQL |
| Static Files | Django | WhiteNoise + Nginx |
| Media Files | Local | Volume |
| Logging | Console | File + Console |
| SSL | No | Yes (recommended) |

## 📞 Support

For deployment issues:
1. Check logs: `docker-compose logs -f`
2. Verify environment variables
3. Ensure all services are running: `docker-compose ps`
4. Check disk space and memory usage

## 🎯 Performance Metrics

Expected performance on a 2GB RAM server:
- Page load time: < 2 seconds
- Database queries: < 100ms
- Static file serving: < 50ms
- Concurrent users: 100+

## 🔄 Backup Strategy

### Automated Backups
Create a backup script:
```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec -T db mysqldump -u root -p shahin_db > "backup_${DATE}.sql"
```

### Schedule with Cron
```bash
# Add to crontab
0 2 * * * /path/to/backup.sh
```

This deployment setup provides a production-ready, scalable, and secure environment for the Shahin Auto Service website.
