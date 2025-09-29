# 🗄️ Object Storage Setup Guide

## Overview

This guide explains how to set up and use object storage for the Shahin Auto Service Django application. The implementation supports multiple storage backends with automatic fallbacks and comprehensive error handling.

## 🏗️ Architecture

### Supported Storage Types

1. **MinIO** (Recommended) - Self-hosted S3-compatible object storage
2. **AWS S3** - Amazon Web Services Simple Storage Service
3. **Local Storage** - Traditional file system storage (fallback)

### Key Features

- ✅ **Automatic Fallback**: Falls back to local storage if object storage fails
- ✅ **Error Handling**: Comprehensive error handling and logging
- ✅ **File Validation**: File size limits and type validation
- ✅ **Unique Naming**: Automatic unique filename generation
- ✅ **Migration Support**: Easy migration from local to object storage
- ✅ **Multiple Backends**: Support for MinIO, AWS S3, and local storage

## 🚀 Quick Start

### 1. Deploy with MinIO (Recommended)

```bash
# Set environment variables
export STORAGE_TYPE=minio
export MINIO_ACCESS_KEY=minioadmin
export MINIO_SECRET_KEY=minioadmin

# Deploy the application
./deploy_object_storage.sh
```

### 2. Deploy with AWS S3

```bash
# Set environment variables
export STORAGE_TYPE=aws
export AWS_ACCESS_KEY_ID=your-access-key
export AWS_SECRET_ACCESS_KEY=your-secret-key
export AWS_STORAGE_BUCKET_NAME=your-bucket-name

# Deploy the application
./deploy_object_storage.sh
```

### 3. Deploy with Local Storage

```bash
# Set environment variables
export STORAGE_TYPE=local

# Deploy the application
./deploy_object_storage.sh
```

## ⚙️ Configuration

### Environment Variables

#### MinIO Configuration
```bash
STORAGE_TYPE=minio
MINIO_ENDPOINT_URL=http://minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_NAME=shahin-media
MINIO_STATIC_BUCKET_NAME=shahin-static
MINIO_REGION_NAME=us-east-1
MINIO_USE_SSL=False
MINIO_CUSTOM_DOMAIN=
MINIO_QUERYSTRING_AUTH=False
MINIO_SIGNATURE_VERSION=s3v4
```

#### AWS S3 Configuration
```bash
STORAGE_TYPE=aws
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1
```

#### File Upload Settings
```bash
MAX_UPLOAD_SIZE=52428800  # 50MB
USE_FALLBACK_STORAGE=True
```

## 🛠️ Management Commands

### Setup Storage
```bash
# Set up MinIO storage and create buckets
python manage.py setup_storage --storage-type=minio --create-buckets

# Migrate existing files to object storage
python manage.py setup_storage --storage-type=minio --migrate-files

# Full setup with migration
python manage.py setup_storage --storage-type=minio --create-buckets --migrate-files
```

### Test Storage Connection
```bash
python manage.py shell -c "
from main.storage import get_storage_backend
storage = get_storage_backend()
print('Storage backend:', type(storage).__name__)
"
```

## 📁 File Structure

```
main/
├── storage.py                 # Custom storage backends
├── management/
│   └── commands/
│       └── setup_storage.py   # Storage setup command
└── models.py                  # Updated models with file fields
```

## 🔧 Custom Storage Classes

### MinIOMediaStorage
- Handles media file uploads to MinIO
- Automatic error handling and fallback
- File size validation
- Unique filename generation

### MinIOStaticStorage
- Handles static file uploads to MinIO
- Optimized for static content delivery
- CDN-friendly configuration

### AWSMediaStorage
- AWS S3 media file storage
- Full S3 feature support
- Error handling and logging

### LocalMediaStorage
- Fallback local storage
- Used when object storage fails
- Simple file system operations

## 📊 Monitoring and Logging

### Logging Configuration
All storage operations are logged with appropriate levels:
- `INFO`: Successful operations
- `WARNING`: Fallback operations
- `ERROR`: Failed operations

### Health Checks
```bash
# Check MinIO health
curl http://minio:9000/minio/health/live

# Check application health
curl http://localhost/health/
```

## 🔄 Migration Process

### From Local to Object Storage

1. **Backup existing files**
   ```bash
   tar -czf media_backup.tar.gz media/
   ```

2. **Deploy with object storage**
   ```bash
   ./deploy_object_storage.sh
   ```

3. **Migrate files**
   ```bash
   python manage.py setup_storage --migrate-files
   ```

### From Object Storage to Local

1. **Change storage type**
   ```bash
   export STORAGE_TYPE=local
   ```

2. **Redeploy**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

## 🚨 Troubleshooting

### Common Issues

#### 1. MinIO Connection Failed
```bash
# Check MinIO logs
docker-compose -f docker-compose.prod.yml logs minio

# Check MinIO health
curl http://minio:9000/minio/health/live

# Restart MinIO
docker-compose -f docker-compose.prod.yml restart minio
```

#### 2. File Upload Errors
```bash
# Check file size limits
python manage.py shell -c "
from django.conf import settings
print('Max upload size:', settings.MAX_UPLOAD_SIZE)
"

# Check storage backend
python manage.py shell -c "
from django.core.files.storage import default_storage
print('Storage backend:', type(default_storage).__name__)
"
```

#### 3. Permission Errors
```bash
# Check MinIO bucket permissions
docker-compose -f docker-compose.prod.yml exec minio mc ls minio/

# Recreate buckets
python manage.py setup_storage --storage-type=minio --create-buckets --force
```

### Debug Commands

```bash
# Test storage connection
python manage.py shell -c "
from main.storage import get_storage_backend
storage = get_storage_backend()
test_content = b'Test file'
test_name = 'test.txt'
storage.save(test_name, test_content)
print('Test file saved:', storage.exists(test_name))
storage.delete(test_name)
print('Test file deleted')
"

# Check bucket contents
docker-compose -f docker-compose.prod.yml exec minio mc ls minio/shahin-media/
```

## 🔒 Security Considerations

### Access Control
- Use strong credentials for MinIO/AWS
- Enable SSL/TLS for production
- Configure proper bucket policies
- Use IAM roles for AWS S3

### File Validation
- File size limits enforced
- File type validation
- Virus scanning (recommended)
- Content-Type validation

### Backup Strategy
- Regular backups of object storage
- Cross-region replication for AWS S3
- Versioning enabled for important files
- Automated backup scripts

## 📈 Performance Optimization

### MinIO Optimization
- Use SSD storage for MinIO data
- Configure appropriate cache settings
- Use CDN for static files
- Enable compression

### AWS S3 Optimization
- Use appropriate storage classes
- Enable CloudFront CDN
- Configure lifecycle policies
- Use transfer acceleration

### Monitoring
- Monitor storage usage
- Track upload/download speeds
- Monitor error rates
- Set up alerts for failures

## 🔄 Maintenance

### Regular Tasks
- Monitor storage usage
- Clean up old files
- Update credentials
- Test backup/restore procedures

### Updates
- Keep MinIO/AWS SDK updated
- Monitor security advisories
- Update storage configurations
- Test migration procedures

## 📞 Support

### Getting Help
1. Check application logs
2. Review storage configuration
3. Test with debug commands
4. Check MinIO/AWS service status

### Useful Resources
- [MinIO Documentation](https://docs.min.io/)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [Django Storage Documentation](https://docs.djangoproject.com/en/stable/topics/files/)

---

**Last Updated:** $(date)
**Version:** 1.0.0
