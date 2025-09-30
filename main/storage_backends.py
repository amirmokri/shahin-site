from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'
    file_overwrite = True
    custom_domain = getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', None)


class MediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False
    custom_domain = getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', None)

