# 🚀 Shahin Auto Service - Production Deployment Guide

This guide provides comprehensive instructions for deploying the Shahin Auto Service Django application to production using Docker and Docker Compose.

## 📋 Prerequisites

### Server Requirements
- **OS**: Ubuntu 20.04+ or CentOS 8+ (recommended)
- **RAM**: Minimum 2GB, Recommended 4GB+
- **Storage**: Minimum 20GB free space
- **CPU**: 2+ cores recommended
- **Network**: Public IP with domain name configured

### Software Requirements
- Docker 20.10+
- Docker Compose 2.0+
- Git
- SSL certificates (for HTTPS)

## 🔧 Installation Steps

### 1. Server Setup

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Logout and login again to apply docker group changes
```

### 2. Clone Repository

```bash
# Clone the repository
git clone <your-repository-url>
cd shahin

# Make deployment script executable
chmod +x deploy.sh
```

### 3. Environment Configuration

No `.env` file is required. You can override defaults defined in `docker-compose.prod.yml` by exporting variables in your shell or CI/CD.

### 4. SSL Certificates (Optional but Recommended)

```bash
# Create SSL directory
mkdir -p ssl

# Add your SSL certificates
# - ssl/cert.pem (SSL certificate)
# - ssl/key.pem (SSL private key)

# Or use Let's Encrypt (recommended)
sudo apt install certbot
sudo certbot certonly --standalone -d shahinautoservice.ir -d www.shahinautoservice.ir
sudo cp /etc/letsencrypt/live/shahinautoservice.ir/fullchain.pem ssl/cert.pem
sudo cp /etc/letsencrypt/live/shahinautoservice.ir/privkey.pem ssl/key.pem
sudo chown $USER:$USER ssl/*
```

### 5. Deploy Application

```bash
# Run deployment script
./deploy.sh
```

The deployment script will:
- ✅ Check prerequisites
- ✅ Load environment variables
- ✅ Build Docker images
- ✅ Start all services
- ✅ Run database migrations
- ✅ Collect static files
- ✅ Create admin user
- ✅ Test application health

## 🌐 Accessing the Application

After successful deployment:

- **Main Website**: `http://your-domain.com` or `https://your-domain.com`
- **Admin Panel**: `http://your-domain.com/admin/`
- **Health Check**: `http://your-domain.com/health/`

### Default Admin Credentials
- **Username**: `admin`
- **Password**: `admin123`

⚠️ **IMPORTANT**: Change the admin password immediately after first login!

## 🔧 Management Commands

### View Logs
```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f web
docker-compose -f docker-compose.prod.yml logs -f nginx
```

### Service Management
```bash
# Stop all services
docker-compose -f docker-compose.prod.yml down

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Restart specific service
docker-compose -f docker-compose.prod.yml restart web

# Update application
./deploy.sh
```

### Database Management
```bash
# Access database shell
docker-compose -f docker-compose.prod.yml exec web python manage.py dbshell

# Run migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Create superuser
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

### Backup and Restore
```bash
# Backup database
docker-compose -f docker-compose.prod.yml exec db mysqldump -u root -p shahin_db > backup.sql

# Backup media files
tar -czf media_backup.tar.gz media/

# Restore database
docker-compose -f docker-compose.prod.yml exec -T db mysql -u root -p shahin_db < backup.sql
```

## 🔒 Security Considerations

### 1. Environment Variables
- Use strong, unique passwords
- Generate a secure SECRET_KEY
- Never commit .env file to version control

### 2. SSL/HTTPS
- Always use HTTPS in production
- Keep SSL certificates updated
- Use strong SSL configurations

### 3. Firewall
```bash
# Configure UFW firewall
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### 4. Regular Updates
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Update Docker images
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
```

## 📊 Monitoring and Maintenance

### Health Monitoring
- Use the `/health/` endpoint for health checks
- Monitor Docker container status
- Set up log rotation

### Performance Optimization
- Monitor resource usage: `docker stats`
- Optimize database queries
- Use CDN for static files
- Enable Redis caching

### Log Management
```bash
# Set up log rotation
sudo nano /etc/logrotate.d/docker-compose

# Add:
/var/lib/docker/containers/*/*.log {
    rotate 7
    daily
    compress
    size=1M
    missingok
    delaycompress
    copytruncate
}
```

## 🚨 Troubleshooting

### Common Issues

#### 1. "Bad Gateway" Error
```bash
# Check if all services are running
docker-compose -f docker-compose.prod.yml ps

# Check web service logs
docker-compose -f docker-compose.prod.yml logs web

# Restart services
docker-compose -f docker-compose.prod.yml restart
```

#### 2. Database Connection Issues
```bash
# Check database logs
docker-compose -f docker-compose.prod.yml logs db

# Test database connection
docker-compose -f docker-compose.prod.yml exec web python manage.py dbshell
```

#### 3. Static Files Not Loading
```bash
# Collect static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# Check nginx logs
docker-compose -f docker-compose.prod.yml logs nginx
```

#### 4. SSL Certificate Issues
```bash
# Check certificate validity
openssl x509 -in ssl/cert.pem -text -noout

# Test SSL configuration
curl -I https://your-domain.com
```

### Performance Issues
```bash
# Monitor resource usage
docker stats

# Check disk space
df -h

# Check memory usage
free -h
```

## 📈 Scaling

### Horizontal Scaling
```yaml
# In docker-compose.prod.yml
web:
  # ... existing configuration
  deploy:
    replicas: 3
```

### Load Balancing
- Use multiple web service instances
- Configure nginx upstream with multiple servers
- Consider using Docker Swarm or Kubernetes for advanced orchestration

## 🔄 Updates and Maintenance

### Application Updates
1. Pull latest changes: `git pull origin main`
2. Run deployment script: `./deploy.sh`
3. Test application functionality
4. Monitor logs for any issues

### Database Updates
1. Backup database before major updates
2. Test migrations in staging environment
3. Run migrations: `docker-compose -f docker-compose.prod.yml exec web python manage.py migrate`

### Security Updates
1. Regularly update base Docker images
2. Update Python dependencies
3. Apply security patches
4. Monitor security advisories

## 📞 Support

For technical support or questions:
- Check application logs
- Review this documentation
- Contact system administrator

## 📝 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Nginx Configuration Guide](https://nginx.org/en/docs/)
- [MySQL Performance Tuning](https://dev.mysql.com/doc/refman/8.0/en/optimization.html)

---

**Last Updated**: $(date)
**Version**: 1.0.0
