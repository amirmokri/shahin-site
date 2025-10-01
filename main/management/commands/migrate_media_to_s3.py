"""
Management command to migrate local media files to Arvan Cloud storage
"""
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from main.models import Lecture, Service, SiteSettings, Bonus


class Command(BaseCommand):
    help = 'Migrate local media files to Arvan Cloud storage'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be migrated without actually doing it',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if not getattr(settings, 'USE_S3', False):
            self.stdout.write(
                self.style.WARNING('S3 storage is not enabled. Set USE_S3=True to use this command.')
            )
            return

        media_root = getattr(settings, 'MEDIA_ROOT', None)
        if not media_root or not os.path.exists(media_root):
            self.stdout.write(
                self.style.WARNING('No local media directory found.')
            )
            return

        self.stdout.write('Starting media migration...')
        
        # Migrate Lecture images
        self.migrate_model_media(Lecture, 'image', dry_run)
        
        # Migrate Service images and videos
        self.migrate_model_media(Service, 'image', dry_run)
        self.migrate_model_media(Service, 'video', dry_run)
        
        # Migrate SiteSettings hero image
        self.migrate_model_media(SiteSettings, 'hero_image', dry_run)
        
        # Migrate Bonus images
        self.migrate_model_media(Bonus, 'image', dry_run)
        
        self.stdout.write(
            self.style.SUCCESS('Media migration completed!')
        )

    def migrate_model_media(self, model_class, field_name, dry_run=False):
        """Migrate media files for a specific model and field"""
        field = model_class._meta.get_field(field_name)
        
        if not hasattr(field, 'upload_to'):
            return
            
        self.stdout.write(f'Migrating {model_class.__name__}.{field_name}...')
        
        # Get all instances that have files
        instances = model_class.objects.exclude(**{f'{field_name}__isnull': True}).exclude(**{f'{field_name}': ''})
        
        for instance in instances:
            file_field = getattr(instance, field_name)
            if file_field and file_field.name:
                local_path = os.path.join(settings.MEDIA_ROOT, file_field.name)
                
                if os.path.exists(local_path):
                    try:
                        if dry_run:
                            self.stdout.write(f'  Would migrate: {file_field.name}')
                        else:
                            # Read the local file
                            with open(local_path, 'rb') as f:
                                file_content = f.read()
                            
                            # Upload to S3
                            content_file = ContentFile(file_content)
                            file_field.save(
                                file_field.name,
                                content_file,
                                save=True
                            )
                            
                            self.stdout.write(f'  Migrated: {file_field.name}')
                            
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f'  Error migrating {file_field.name}: {str(e)}')
                        )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'  Local file not found: {file_field.name}')
                    )
