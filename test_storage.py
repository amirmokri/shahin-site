#!/usr/bin/env python
"""
Test script to verify S3 storage configuration
Run this script to test if your Arvan Cloud Object Storage is properly configured
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shahin_auto.settings')
django.setup()

from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib.staticfiles.storage import staticfiles_storage


def test_storage_configuration():
    """Test the storage configuration"""
    print("Testing Storage Configuration")
    print("=" * 50)
    
    # Check if S3 is enabled
    use_s3 = getattr(settings, 'USE_S3', False)
    print(f"USE_S3: {use_s3}")
    
    if not use_s3:
        print("S3 storage is not enabled. Set USE_S3=True in your environment.")
        return False
    
    # Check AWS settings
    aws_settings = [
        'AWS_ACCESS_KEY_ID',
        'AWS_SECRET_ACCESS_KEY', 
        'AWS_STORAGE_BUCKET_NAME',
        'AWS_S3_ENDPOINT_URL',
        'AWS_S3_REGION_NAME'
    ]
    
    print("\n📋 AWS Settings:")
    for setting in aws_settings:
        value = getattr(settings, setting, None)
        if value:
            # Mask sensitive values
            if 'KEY' in setting or 'SECRET' in setting:
                masked_value = value[:8] + '...' if len(value) > 8 else '***'
                print(f"  {setting}: {masked_value}")
            else:
                print(f"  {setting}: {value}")
        else:
            print(f"  {setting}: Not set")
    
    # Check URLs
    print(f"\nURLs:")
    print(f"  STATIC_URL: {settings.STATIC_URL}")
    print(f"  MEDIA_URL: {settings.MEDIA_URL}")
    
    # Test storage backends
    print(f"\nStorage Backends:")
    print(f"  Default storage: {settings.STORAGES['default']['BACKEND']}")
    print(f"  Static storage: {settings.STORAGES['staticfiles']['BACKEND']}")
    
    return True


def test_file_operations():
    """Test file operations with S3"""
    print("\nTesting File Operations")
    print("=" * 50)
    
    try:
        # Test writing a file
        test_content = "This is a test file for S3 storage"
        test_filename = "test_storage.txt"
        
        print(f"Writing test file: {test_filename}")
        default_storage.save(test_filename, test_content)
        
        # Test reading the file
        print(f"Reading test file: {test_filename}")
        if default_storage.exists(test_filename):
            with default_storage.open(test_filename, 'r') as f:
                content = f.read()
                print(f"File content: {content}")
        else:
            print("File not found after writing")
            return False
        
        # Test file URL
        print(f"File URL: {default_storage.url(test_filename)}")
        
        # Test deleting the file
        print(f"Deleting test file: {test_filename}")
        default_storage.delete(test_filename)
        
        if not default_storage.exists(test_filename):
            print("File deleted successfully")
        else:
            print("File still exists after deletion")
            return False
            
        return True
        
    except Exception as e:
        print(f"Error during file operations: {str(e)}")
        return False


def test_static_files():
    """Test static files storage"""
    print("\nTesting Static Files")
    print("=" * 50)
    
    try:
        # Test static files storage
        print("Testing static files storage...")
        
        # Check if we can access static files
        static_url = staticfiles_storage.url('css/custom.css')
        print(f"Static file URL: {static_url}")
        
        return True
        
    except Exception as e:
        print(f"Error with static files: {str(e)}")
        return False


def test_media_files():
    """Test media files storage"""
    print("\nTesting Media Files")
    print("=" * 50)
    
    try:
        from main.models import SiteSettings, Service, Lecture, Bonus
        
        # Test hero image
        print("Testing hero image...")
        site_settings = SiteSettings.objects.first()
        if site_settings and site_settings.hero_image:
            hero_url = site_settings.hero_image.url
            print(f"Hero image URL: {hero_url}")
        else:
            print("No hero image set")
        
        # Test service images
        print("Testing service images...")
        services = Service.objects.filter(image__isnull=False)[:2]
        for service in services:
            service_url = service.image.url
            print(f"Service {service.name}: {service_url}")
        
        # Test lecture images
        print("Testing lecture images...")
        lectures = Lecture.objects.filter(image__isnull=False)[:2]
        for lecture in lectures:
            lecture_url = lecture.image.url
            print(f"Lecture {lecture.title}: {lecture_url}")
        
        return True
        
    except Exception as e:
        print(f"Error with media files: {str(e)}")
        return False


def main():
    """Main test function"""
    print("Arvan Cloud Object Storage Test")
    print("=" * 50)
    
    # Test configuration
    config_ok = test_storage_configuration()
    if not config_ok:
        print("\nConfiguration test failed. Please check your settings.")
        return
    
    # Test file operations
    file_ops_ok = test_file_operations()
    if not file_ops_ok:
        print("\nFile operations test failed. Please check your S3 credentials and permissions.")
        return
    
    # Test static files
    static_ok = test_static_files()
    if not static_ok:
        print("\nStatic files test failed. Please check your static files configuration.")
        return
    
    # Test media files
    media_ok = test_media_files()
    if not media_ok:
        print("\nMedia files test failed. Please check your media files configuration.")
        return
    
    print("\nAll tests passed! Your S3 storage is properly configured.")
    print("\nNext steps:")
    print("1. Run: python manage.py collect_and_upload")
    print("2. Run: python manage.py migrate_media_files")
    print("3. Check your website to ensure files are loading")
    print("4. Monitor your S3 bucket for uploaded files")


if __name__ == "__main__":
    main()
