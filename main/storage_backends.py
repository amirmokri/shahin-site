from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'
    file_overwrite = True
    custom_domain = getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', None)
    
    def __init__(self, *args, **kwargs):
        kwargs.update({
            'access_key': getattr(settings, 'AWS_ACCESS_KEY_ID', None),
            'secret_key': getattr(settings, 'AWS_SECRET_ACCESS_KEY', None),
            'bucket_name': getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None),
            'region_name': getattr(settings, 'AWS_S3_REGION_NAME', None),
            'endpoint_url': getattr(settings, 'AWS_S3_ENDPOINT_URL', None),
            'addressing_style': getattr(settings, 'AWS_S3_ADDRESSING_STYLE', 'virtual'),
            'signature_version': getattr(settings, 'AWS_S3_SIGNATURE_VERSION', 's3v4'),
        })
        super().__init__(*args, **kwargs)


class MediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False
    custom_domain = getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', None)
    
    def __init__(self, *args, **kwargs):
        kwargs.update({
            'access_key': getattr(settings, 'AWS_ACCESS_KEY_ID', None),
            'secret_key': getattr(settings, 'AWS_SECRET_ACCESS_KEY', None),
            'bucket_name': getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None),
            'region_name': getattr(settings, 'AWS_S3_REGION_NAME', None),
            'endpoint_url': getattr(settings, 'AWS_S3_ENDPOINT_URL', None),
            'addressing_style': getattr(settings, 'AWS_S3_ADDRESSING_STYLE', 'virtual'),
            'signature_version': getattr(settings, 'AWS_S3_SIGNATURE_VERSION', 's3v4'),
        })
        super().__init__(*args, **kwargs)


class StaticMediaStorage(S3Boto3Storage):
    """Storage for static files that includes media files in static structure"""
    location = 'static'
    default_acl = 'public-read'
    file_overwrite = True
    custom_domain = getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', None)
    
    def __init__(self, *args, **kwargs):
        kwargs.update({
            'access_key': getattr(settings, 'AWS_ACCESS_KEY_ID', None),
            'secret_key': getattr(settings, 'AWS_SECRET_ACCESS_KEY', None),
            'bucket_name': getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None),
            'region_name': getattr(settings, 'AWS_S3_REGION_NAME', None),
            'endpoint_url': getattr(settings, 'AWS_S3_ENDPOINT_URL', None),
            'addressing_style': getattr(settings, 'AWS_S3_ADDRESSING_STYLE', 'virtual'),
            'signature_version': getattr(settings, 'AWS_S3_SIGNATURE_VERSION', 's3v4'),
        })
        super().__init__(*args, **kwargs)
