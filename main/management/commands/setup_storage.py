"""
Management command to set up object storage and migrate existing files
"""

import os
import logging
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.files.storage import default_storage
from minio import Minio
from minio.error import S3Error
from main.models import Service, Lecture, Bonus, SiteSettings

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Set up object storage and migrate existing files'

    def add_arguments(self, parser):
        parser.add_argument(
            '--storage-type',
            type=str,
            choices=['minio', 'aws', 'local'],
            default='minio',
            help='Type of storage to set up'
        )
        parser.add_argument(
            '--migrate-files',
            action='store_true',
            help='Migrate existing local files to object storage'
        )
        parser.add_argument(
            '--create-buckets',
            action='store_true',
            help='Create buckets in object storage'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force operation even if buckets already exist'
        )

    def handle(self, *args, **options):
        storage_type = options['storage_type']
        
        self.stdout.write(
            self.style.SUCCESS(f'Setting up {storage_type} storage...')
        )
        
        if storage_type == 'minio':
            self.setup_minio(options)
        elif storage_type == 'aws':
            self.setup_aws(options)
        else:
            self.stdout.write(
                self.style.WARNING('Local storage setup - no additional configuration needed')
            )
        
        if options['migrate_files']:
            self.migrate_files()
        
        self.stdout.write(
            self.style.SUCCESS('Storage setup completed successfully!')
        )

    def setup_minio(self, options):
        """Set up MinIO storage"""
        try:
            # Initialize MinIO client
            client = Minio(
                settings.MINIO_ENDPOINT_URL.replace('http://', '').replace('https://', ''),
                access_key=settings.MINIO_ACCESS_KEY,
                secret_key=settings.MINIO_SECRET_KEY,
                secure=settings.MINIO_USE_SSL
            )
            
            self.stdout.write('MinIO client initialized successfully')
            
            if options['create_buckets']:
                self.create_minio_buckets(client, options['force'])
            
        except Exception as e:
            logger.error(f"Error setting up MinIO: {str(e)}")
            raise CommandError(f'Failed to set up MinIO: {str(e)}')

    def create_minio_buckets(self, client, force=False):
        """Create MinIO buckets"""
        buckets = [
            settings.MINIO_BUCKET_NAME,
            settings.MINIO_STATIC_BUCKET_NAME
        ]
        
        for bucket_name in buckets:
            try:
                if client.bucket_exists(bucket_name):
                    if force:
                        self.stdout.write(
                            self.style.WARNING(f'Bucket {bucket_name} already exists')
                        )
                    else:
                        self.stdout.write(
                            self.style.SUCCESS(f'Bucket {bucket_name} already exists')
                        )
                        continue
                else:
                    client.make_bucket(bucket_name)
                    self.stdout.write(
                        self.style.SUCCESS(f'Created bucket: {bucket_name}')
                    )
            except S3Error as e:
                logger.error(f"Error creating bucket {bucket_name}: {str(e)}")
                raise CommandError(f'Failed to create bucket {bucket_name}: {str(e)}')

    def setup_aws(self, options):
        """Set up AWS S3 storage"""
        self.stdout.write(
            self.style.SUCCESS('AWS S3 storage configured via environment variables')
        )
        
        if options['create_buckets']:
            self.stdout.write(
                self.style.WARNING('AWS S3 bucket creation not implemented in this command')
            )

    def migrate_files(self):
        """Migrate existing local files to object storage"""
        self.stdout.write('Starting file migration...')
        
        # Get all models with file fields
        models_with_files = [
            (Service, ['image', 'video']),
            (Lecture, ['image', 'video']),
            (Bonus, ['image']),
            (SiteSettings, ['hero_image', 'logo']),
        ]
        
        migrated_count = 0
        error_count = 0
        
        for model_class, file_fields in models_with_files:
            self.stdout.write(f'Migrating {model_class.__name__} files...')
            
            for instance in model_class.objects.all():
                for field_name in file_fields:
                    file_field = getattr(instance, field_name, None)
                    
                    if file_field and file_field.name:
                        try:
                            # Check if file exists locally
                            if os.path.exists(file_field.path):
                                # Read the file
                                with open(file_field.path, 'rb') as f:
                                    # Save to object storage
                                    new_name = file_field.name
                                    default_storage.save(new_name, f)
                                    
                                    # Update the field
                                    setattr(instance, field_name, new_name)
                                    instance.save()
                                    
                                    migrated_count += 1
                                    self.stdout.write(
                                        f'  Migrated: {field_name} for {instance}'
                                    )
                                    
                                    # Remove local file
                                    os.remove(file_field.path)
                            else:
                                self.stdout.write(
                                    self.style.WARNING(
                                        f'  Local file not found: {file_field.path}'
                                    )
                                )
                                
                        except Exception as e:
                            error_count += 1
                            logger.error(
                                f"Error migrating {field_name} for {instance}: {str(e)}"
                            )
                            self.stdout.write(
                                self.style.ERROR(
                                    f'  Error migrating {field_name} for {instance}: {str(e)}'
                                )
                            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Migration completed: {migrated_count} files migrated, {error_count} errors'
            )
        )

    def test_connection(self):
        """Test connection to object storage"""
        try:
            # Try to save a test file
            test_content = b'Test file content'
            test_name = 'test-connection.txt'
            
            default_storage.save(test_name, test_content)
            
            # Try to read it back
            if default_storage.exists(test_name):
                content = default_storage.open(test_name).read()
                if content == test_content:
                    self.stdout.write(
                        self.style.SUCCESS('Storage connection test passed')
                    )
                    # Clean up test file
                    default_storage.delete(test_name)
                    return True
            
            self.stdout.write(
                self.style.ERROR('Storage connection test failed')
            )
            return False
            
        except Exception as e:
            logger.error(f"Storage connection test failed: {str(e)}")
            self.stdout.write(
                self.style.ERROR(f'Storage connection test failed: {str(e)}')
            )
            return False
