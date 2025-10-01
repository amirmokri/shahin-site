# Arvan Cloud Storage Setup Guide

This guide explains how to configure and use Arvan Cloud object storage with your Django project.

## Prerequisites

1. Arvan Cloud account with Object Storage service enabled
2. Access key and secret key from Arvan Cloud
3. Bucket created in Arvan Cloud

## Environment Configuration

Create a `.env` file in your project root with the following variables:

```env
# Storage Settings (Arvan S3-compatible)
USE_S3=True
ARVAN_ACCESS_KEY_ID=your-object-storage-access-key
ARVAN_SECRET_ACCESS_KEY=your-object-storage-secret-key
ARVAN_BUCKET_NAME=your-bucket-name
ARVAN_REGION=ir-thr-at1
ARVAN_ENDPOINT_URL=https://s3.ir-thr-at1.arvanstorage.com
ARVAN_ADDRESSING_STYLE=virtual
ARVAN_CUSTOM_DOMAIN=your-custom-domain.com  # Optional
ARVAN_SIGNATURE_VERSION=s3v4
```

## Installation

1. Install required packages:
```bash
pip install django-storages boto3
```

2. Add to `INSTALLED_APPS` in `settings.py`:
```python
INSTALLED_APPS = [
    # ... other apps
    'storages',
]
```

## Configuration

The project is already configured with the following:

### Settings Configuration
- Automatic detection of S3 settings from environment variables
- Custom storage backends for media and static files
- Proper URL generation for Arvan Cloud

### Storage Backends
- `MediaStorage`: Handles user-uploaded media files
- `StaticStorage`: Handles static files (CSS, JS, images)

### Models Configuration
All models with media fields are configured to use the custom storage:
- `Lecture.image`
- `Service.image` and `Service.video`
- `SiteSettings.hero_image`
- `Bonus.image`

## Migration Commands

### Migrate Existing Media Files

To migrate existing local media files to Arvan Cloud:

```bash
# Dry run (see what would be migrated)
python manage.py migrate_media_to_s3 --dry-run

# Actually migrate files
python manage.py migrate_media_to_s3
```

### Alternative: Copy to Static Structure

If you prefer to keep media files in static structure:

```bash
# Dry run
python manage.py copy_media_to_static --dry-run

# Actually copy files
python manage.py copy_media_to_static
```

## Static Files Deployment

To deploy static files to Arvan Cloud:

```bash
python manage.py collectstatic --noinput
```

## Troubleshooting

### Common Issues

1. **Media files not uploading**: Check that `USE_S3=True` and credentials are correct
2. **Images not displaying**: Verify that `ARVAN_CUSTOM_DOMAIN` is set correctly
3. **500 errors in admin**: Ensure all required packages are installed and settings are correct

### Debug Mode

To debug storage issues, you can temporarily set `DEBUG=True` and check Django logs for storage-related errors.

### Testing Storage

You can test the storage configuration by:

1. Going to Django admin
2. Creating a new Lecture or Service
3. Uploading an image
4. Checking if the image appears correctly

## Best Practices

1. **Use CDN**: Configure a custom domain with Arvan Cloud CDN for better performance
2. **Image Optimization**: Consider using image optimization libraries before upload
3. **Backup**: Regularly backup your Arvan Cloud bucket
4. **Monitoring**: Monitor storage usage and costs in Arvan Cloud dashboard

## File Structure

```
your-bucket/
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── fontawesome/
└── media/
    ├── lectures/
    ├── services/
    │   └── videos/
    ├── site/
    └── bonus/
```

## Security

1. Keep your access keys secure and never commit them to version control
2. Use IAM policies to restrict access to only necessary operations
3. Enable bucket versioning for important files
4. Consider using signed URLs for sensitive content

## Performance Optimization

1. Enable compression in Arvan Cloud settings
2. Use appropriate cache headers
3. Consider using Arvan Cloud CDN for global distribution
4. Optimize images before upload

## Support

For Arvan Cloud specific issues, refer to:
- [Arvan Cloud Documentation](https://docs.arvancloud.ir/en/object-storage/)
- [Arvan Cloud Support](https://www.arvancloud.com/support)

For Django storage issues, refer to:
- [django-storages Documentation](https://django-storages.readthedocs.io/)
- [Django File Storage Documentation](https://docs.djangoproject.com/en/stable/topics/files/)
