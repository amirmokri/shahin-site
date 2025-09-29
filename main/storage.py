"""
Custom storage backends for Shahin Auto Service
Handles object storage with proper error handling and fallbacks
"""

import os
import logging
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from storages.backends.s3boto3 import S3Boto3Storage, S3StaticStorage
from storages.utils import setting

logger = logging.getLogger(__name__)


class MinIOStaticStorage(S3StaticStorage):
    """
    Custom static storage for MinIO
    """
    location = 'static'
    default_acl = 'public-read'
    file_overwrite = False
    
    def __init__(self, *args, **kwargs):
        # Override settings for MinIO
        kwargs.update({
            'bucket_name': setting('MINIO_BUCKET_NAME', 'shahin-static'),
            'custom_domain': setting('MINIO_CUSTOM_DOMAIN'),
            'endpoint_url': setting('MINIO_ENDPOINT_URL'),
            'access_key': setting('MINIO_ACCESS_KEY'),
            'secret_key': setting('MINIO_SECRET_KEY'),
            'region_name': setting('MINIO_REGION_NAME', 'us-east-1'),
            'use_ssl': setting('MINIO_USE_SSL', True),
            'querystring_auth': setting('MINIO_QUERYSTRING_AUTH', False),
            'signature_version': setting('MINIO_SIGNATURE_VERSION', 's3v4'),
        })
        super().__init__(*args, **kwargs)


class MinIOMediaStorage(S3Boto3Storage):
    """
    Custom media storage for MinIO with error handling
    """
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False
    
    def __init__(self, *args, **kwargs):
        # Override settings for MinIO
        kwargs.update({
            'bucket_name': setting('MINIO_BUCKET_NAME', 'shahin-media'),
            'custom_domain': setting('MINIO_CUSTOM_DOMAIN'),
            'endpoint_url': setting('MINIO_ENDPOINT_URL'),
            'access_key': setting('MINIO_ACCESS_KEY'),
            'secret_key': setting('MINIO_SECRET_KEY'),
            'region_name': setting('MINIO_REGION_NAME', 'us-east-1'),
            'use_ssl': setting('MINIO_USE_SSL', True),
            'querystring_auth': setting('MINIO_QUERYSTRING_AUTH', False),
            'signature_version': setting('MINIO_SIGNATURE_VERSION', 's3v4'),
        })
        super().__init__(*args, **kwargs)
    
    def _save(self, name, content):
        """
        Save file with error handling and logging
        """
        try:
            # Validate file size
            content.seek(0, 2)  # Seek to end
            file_size = content.tell()
            content.seek(0)  # Reset to beginning
            
            max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 50 * 1024 * 1024)  # 50MB default
            if file_size > max_size:
                raise ValueError(f"File size {file_size} exceeds maximum allowed size {max_size}")
            
            # Generate unique filename if file exists
            if self.exists(name):
                name = self._get_available_name(name, max_length=255)
            
            logger.info(f"Uploading file to MinIO: {name} (size: {file_size} bytes)")
            return super()._save(name, content)
            
        except Exception as e:
            logger.error(f"Error saving file {name} to MinIO: {str(e)}")
            # Fallback to local storage if configured
            if getattr(settings, 'USE_FALLBACK_STORAGE', False):
                return self._save_to_local(name, content)
            raise
    
    def _save_to_local(self, name, content):
        """
        Fallback to local storage when MinIO fails
        """
        try:
            from django.core.files.storage import default_storage
            local_path = os.path.join(settings.MEDIA_ROOT, name)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            with open(local_path, 'wb') as f:
                for chunk in content.chunks():
                    f.write(chunk)
            
            logger.warning(f"File {name} saved to local storage as fallback")
            return name
            
        except Exception as e:
            logger.error(f"Error saving file {name} to local storage: {str(e)}")
            raise
    
    def delete(self, name):
        """
        Delete file with error handling
        """
        try:
            if self.exists(name):
                super().delete(name)
                logger.info(f"File deleted from MinIO: {name}")
            else:
                logger.warning(f"File not found in MinIO: {name}")
        except Exception as e:
            logger.error(f"Error deleting file {name} from MinIO: {str(e)}")
            raise
    
    def exists(self, name):
        """
        Check if file exists with error handling
        """
        try:
            return super().exists(name)
        except Exception as e:
            logger.error(f"Error checking if file {name} exists in MinIO: {str(e)}")
            return False
    
    def url(self, name):
        """
        Get file URL with error handling and fallback
        """
        try:
            return super().url(name)
        except Exception as e:
            logger.error(f"Error getting URL for file {name} from MinIO: {str(e)}")
            # Return fallback URL
            return f"{settings.MEDIA_URL}{name}"


class AWSStaticStorage(S3StaticStorage):
    """
    Custom static storage for AWS S3
    """
    location = 'static'
    default_acl = 'public-read'
    file_overwrite = False


class AWSMediaStorage(S3Boto3Storage):
    """
    Custom media storage for AWS S3 with error handling
    """
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False
    
    def _save(self, name, content):
        """
        Save file with error handling and logging
        """
        try:
            # Validate file size
            content.seek(0, 2)  # Seek to end
            file_size = content.tell()
            content.seek(0)  # Reset to beginning
            
            max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 50 * 1024 * 1024)  # 50MB default
            if file_size > max_size:
                raise ValueError(f"File size {file_size} exceeds maximum allowed size {max_size}")
            
            # Generate unique filename if file exists
            if self.exists(name):
                name = self._get_available_name(name, max_length=255)
            
            logger.info(f"Uploading file to AWS S3: {name} (size: {file_size} bytes)")
            return super()._save(name, content)
            
        except Exception as e:
            logger.error(f"Error saving file {name} to AWS S3: {str(e)}")
            raise
    
    def delete(self, name):
        """
        Delete file with error handling
        """
        try:
            if self.exists(name):
                super().delete(name)
                logger.info(f"File deleted from AWS S3: {name}")
            else:
                logger.warning(f"File not found in AWS S3: {name}")
        except Exception as e:
            logger.error(f"Error deleting file {name} from AWS S3: {str(e)}")
            raise


class LocalMediaStorage:
    """
    Local storage fallback with error handling
    """
    def __init__(self):
        self.location = settings.MEDIA_ROOT
        self.base_url = settings.MEDIA_URL
    
    def save(self, name, content):
        """
        Save file to local storage
        """
        try:
            full_path = os.path.join(self.location, name)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, 'wb') as f:
                for chunk in content.chunks():
                    f.write(chunk)
            
            logger.info(f"File saved to local storage: {name}")
            return name
            
        except Exception as e:
            logger.error(f"Error saving file {name} to local storage: {str(e)}")
            raise
    
    def delete(self, name):
        """
        Delete file from local storage
        """
        try:
            full_path = os.path.join(self.location, name)
            if os.path.exists(full_path):
                os.remove(full_path)
                logger.info(f"File deleted from local storage: {name}")
            else:
                logger.warning(f"File not found in local storage: {name}")
        except Exception as e:
            logger.error(f"Error deleting file {name} from local storage: {str(e)}")
            raise
    
    def exists(self, name):
        """
        Check if file exists in local storage
        """
        full_path = os.path.join(self.location, name)
        return os.path.exists(full_path)
    
    def url(self, name):
        """
        Get file URL
        """
        return f"{self.base_url}{name}"


def get_storage_backend():
    """
    Get the appropriate storage backend based on configuration
    """
    storage_type = getattr(settings, 'STORAGE_TYPE', 'local')
    
    if storage_type == 'minio':
        if not all([
            getattr(settings, 'MINIO_ENDPOINT_URL', None),
            getattr(settings, 'MINIO_ACCESS_KEY', None),
            getattr(settings, 'MINIO_SECRET_KEY', None),
        ]):
            logger.warning("MinIO configuration incomplete, falling back to local storage")
            return LocalMediaStorage()
        return MinIOMediaStorage()
    
    elif storage_type == 'aws':
        if not all([
            getattr(settings, 'AWS_ACCESS_KEY_ID', None),
            getattr(settings, 'AWS_SECRET_ACCESS_KEY', None),
            getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None),
        ]):
            logger.warning("AWS S3 configuration incomplete, falling back to local storage")
            return LocalMediaStorage()
        return AWSMediaStorage()
    
    else:
        return LocalMediaStorage()


def get_static_storage_backend():
    """
    Get the appropriate static storage backend based on configuration
    """
    storage_type = getattr(settings, 'STORAGE_TYPE', 'local')
    
    if storage_type == 'minio':
        if not all([
            getattr(settings, 'MINIO_ENDPOINT_URL', None),
            getattr(settings, 'MINIO_ACCESS_KEY', None),
            getattr(settings, 'MINIO_SECRET_KEY', None),
        ]):
            logger.warning("MinIO configuration incomplete, using default static storage")
            return None
        return MinIOStaticStorage()
    
    elif storage_type == 'aws':
        if not all([
            getattr(settings, 'AWS_ACCESS_KEY_ID', None),
            getattr(settings, 'AWS_SECRET_ACCESS_KEY', None),
            getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None),
        ]):
            logger.warning("AWS S3 configuration incomplete, using default static storage")
            return None
        return AWSStaticStorage()
    
    else:
        return None
