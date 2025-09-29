#!/usr/bin/env python
"""
Test script for object storage integration
Run this script to test the storage backend configuration
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shahin_auto.settings')
django.setup()

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from main.storage import get_storage_backend, get_static_storage_backend
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_storage_backend():
    """Test the configured storage backend"""
    print("🧪 Testing Storage Backend Configuration")
    print("=" * 50)
    
    # Get storage backend
    storage = get_storage_backend()
    static_storage = get_static_storage_backend()
    
    print(f"📦 Media Storage: {type(storage).__name__}")
    print(f"📦 Static Storage: {type(static_storage).__name__ if static_storage else 'Default'}")
    
    # Test file operations
    test_filename = 'test-storage.txt'
    test_content = b'This is a test file for storage backend validation.'
    
    try:
        # Test save
        print(f"💾 Testing file save: {test_filename}")
        saved_name = storage.save(test_filename, ContentFile(test_content))
        print(f"✅ File saved as: {saved_name}")
        
        # Test exists
        print(f"🔍 Testing file exists check...")
        exists = storage.exists(saved_name)
        print(f"✅ File exists: {exists}")
        
        # Test URL generation
        print(f"🔗 Testing URL generation...")
        url = storage.url(saved_name)
        print(f"✅ File URL: {url}")
        
        # Test file reading
        print(f"📖 Testing file reading...")
        if storage.exists(saved_name):
            file_obj = storage.open(saved_name)
            content = file_obj.read()
            file_obj.close()
            print(f"✅ File content matches: {content == test_content}")
        
        # Test delete
        print(f"🗑️ Testing file deletion...")
        storage.delete(saved_name)
        print(f"✅ File deleted successfully")
        
        print("\n🎉 Storage backend test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Storage test failed: {str(e)}")
        logger.error(f"Storage test error: {str(e)}")
        return False

def test_django_storage():
    """Test Django's default storage"""
    print("\n🧪 Testing Django Default Storage")
    print("=" * 50)
    
    test_filename = 'test-django-storage.txt'
    test_content = b'This is a test file for Django storage validation.'
    
    try:
        # Test save
        print(f"💾 Testing Django storage save: {test_filename}")
        saved_name = default_storage.save(test_filename, ContentFile(test_content))
        print(f"✅ File saved as: {saved_name}")
        
        # Test exists
        print(f"🔍 Testing file exists check...")
        exists = default_storage.exists(saved_name)
        print(f"✅ File exists: {exists}")
        
        # Test URL generation
        print(f"🔗 Testing URL generation...")
        url = default_storage.url(saved_name)
        print(f"✅ File URL: {url}")
        
        # Test delete
        print(f"🗑️ Testing file deletion...")
        default_storage.delete(saved_name)
        print(f"✅ File deleted successfully")
        
        print("\n🎉 Django storage test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Django storage test failed: {str(e)}")
        logger.error(f"Django storage test error: {str(e)}")
        return False

def test_configuration():
    """Test storage configuration"""
    print("\n🧪 Testing Storage Configuration")
    print("=" * 50)
    
    from django.conf import settings
    
    print(f"📋 Storage Type: {getattr(settings, 'STORAGE_TYPE', 'Not set')}")
    print(f"📋 Media URL: {getattr(settings, 'MEDIA_URL', 'Not set')}")
    print(f"📋 Static URL: {getattr(settings, 'STATIC_URL', 'Not set')}")
    print(f"📋 Max Upload Size: {getattr(settings, 'MAX_UPLOAD_SIZE', 'Not set')}")
    
    # Check MinIO settings
    if hasattr(settings, 'MINIO_ENDPOINT_URL'):
        print(f"📋 MinIO Endpoint: {settings.MINIO_ENDPOINT_URL}")
        print(f"📋 MinIO Bucket: {settings.MINIO_BUCKET_NAME}")
        print(f"📋 MinIO Access Key: {'Set' if settings.MINIO_ACCESS_KEY else 'Not set'}")
    
    # Check AWS settings
    if hasattr(settings, 'AWS_STORAGE_BUCKET_NAME'):
        print(f"📋 AWS Bucket: {settings.AWS_STORAGE_BUCKET_NAME}")
        print(f"📋 AWS Access Key: {'Set' if settings.AWS_ACCESS_KEY_ID else 'Not set'}")
    
    print("\n✅ Configuration test completed!")

if __name__ == '__main__':
    print("🚀 Starting Object Storage Tests")
    print("=" * 50)
    
    # Test configuration
    test_configuration()
    
    # Test storage backends
    storage_success = test_storage_backend()
    django_success = test_django_storage()
    
    print("\n📊 Test Results Summary")
    print("=" * 50)
    print(f"Storage Backend Test: {'✅ PASSED' if storage_success else '❌ FAILED'}")
    print(f"Django Storage Test: {'✅ PASSED' if django_success else '❌ FAILED'}")
    
    if storage_success and django_success:
        print("\n🎉 All tests passed! Object storage is configured correctly.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the configuration.")
        sys.exit(1)
