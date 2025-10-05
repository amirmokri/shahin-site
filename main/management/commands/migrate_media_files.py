from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from pathlib import Path
from main.models import SiteSettings, Service, Lecture, Bonus


class Command(BaseCommand):
    help = 'Migrate existing media files to S3 and fix file references'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be migrated without actually migrating',
        )

    def handle(self, *args, **options):
        if not getattr(settings, 'USE_S3', False):
            self.stdout.write(
                self.style.WARNING('S3 storage is not enabled. Set USE_S3=True to use this command.')
            )
            return

        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No files will be migrated'))
        
        # Migrate hero image
        self.migrate_hero_image(dry_run)
        
        # Migrate service images and videos
        self.migrate_service_files(dry_run)
        
        # Migrate lecture images
        self.migrate_lecture_files(dry_run)
        
        # Migrate bonus images
        self.migrate_bonus_files(dry_run)

    def migrate_hero_image(self, dry_run):
        """Migrate hero image from static to S3"""
        self.stdout.write('Migrating hero image...')
        
        try:
            site_settings = SiteSettings.objects.first()
            if not site_settings:
                self.stdout.write(self.style.WARNING('No site settings found'))
                return
            
            # Check if hero image exists in static directory
            static_hero_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'hero.jpg')
            if os.path.exists(static_hero_path):
                if not dry_run:
                    with open(static_hero_path, 'rb') as f:
                        site_settings.hero_image.save('hero.jpg', ContentFile(f.read()), save=True)
                    self.stdout.write(f'✅ Hero image migrated to S3: {site_settings.hero_image.url}')
                else:
                    self.stdout.write(f'Would migrate hero image from {static_hero_path}')
            else:
                self.stdout.write(self.style.WARNING('Hero image not found in static/images/hero.jpg'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error migrating hero image: {str(e)}'))

    def migrate_service_files(self, dry_run):
        """Migrate service images and videos"""
        self.stdout.write('Migrating service files...')
        
        services = Service.objects.all()
        migrated_count = 0
        
        for service in services:
            try:
                # Migrate image
                if service.image and service.image.name:
                    if not dry_run:
                        # Check if file exists in S3
                        if not default_storage.exists(service.image.name):
                            # File doesn't exist in S3, try to upload from local
                            local_path = os.path.join(settings.MEDIA_ROOT, service.image.name)
                            if os.path.exists(local_path):
                                with open(local_path, 'rb') as f:
                                    service.image.save(service.image.name, ContentFile(f.read()), save=True)
                                migrated_count += 1
                                self.stdout.write(f'✅ Service image migrated: {service.image.name}')
                    else:
                        self.stdout.write(f'Would migrate service image: {service.image.name}')
                
                # Migrate video
                if service.video and service.video.name:
                    if not dry_run:
                        # Check if file exists in S3
                        if not default_storage.exists(service.video.name):
                            # File doesn't exist in S3, try to upload from local
                            local_path = os.path.join(settings.MEDIA_ROOT, service.video.name)
                            if os.path.exists(local_path):
                                with open(local_path, 'rb') as f:
                                    service.video.save(service.video.name, ContentFile(f.read()), save=True)
                                migrated_count += 1
                                self.stdout.write(f'✅ Service video migrated: {service.video.name}')
                    else:
                        self.stdout.write(f'Would migrate service video: {service.video.name}')
                        
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error migrating service {service.name}: {str(e)}'))
        
        if not dry_run:
            self.stdout.write(f'✅ Migrated {migrated_count} service files')

    def migrate_lecture_files(self, dry_run):
        """Migrate lecture images"""
        self.stdout.write('Migrating lecture files...')
        
        lectures = Lecture.objects.all()
        migrated_count = 0
        
        for lecture in lectures:
            try:
                if lecture.image and lecture.image.name:
                    if not dry_run:
                        # Check if file exists in S3
                        if not default_storage.exists(lecture.image.name):
                            # File doesn't exist in S3, try to upload from local
                            local_path = os.path.join(settings.MEDIA_ROOT, lecture.image.name)
                            if os.path.exists(local_path):
                                with open(local_path, 'rb') as f:
                                    lecture.image.save(lecture.image.name, ContentFile(f.read()), save=True)
                                migrated_count += 1
                                self.stdout.write(f'✅ Lecture image migrated: {lecture.image.name}')
                    else:
                        self.stdout.write(f'Would migrate lecture image: {lecture.image.name}')
                        
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error migrating lecture {lecture.title}: {str(e)}'))
        
        if not dry_run:
            self.stdout.write(f'✅ Migrated {migrated_count} lecture files')

    def migrate_bonus_files(self, dry_run):
        """Migrate bonus images"""
        self.stdout.write('Migrating bonus files...')
        
        bonuses = Bonus.objects.all()
        migrated_count = 0
        
        for bonus in bonuses:
            try:
                if bonus.image and bonus.image.name:
                    if not dry_run:
                        # Check if file exists in S3
                        if not default_storage.exists(bonus.image.name):
                            # File doesn't exist in S3, try to upload from local
                            local_path = os.path.join(settings.MEDIA_ROOT, bonus.image.name)
                            if os.path.exists(local_path):
                                with open(local_path, 'rb') as f:
                                    bonus.image.save(bonus.image.name, ContentFile(f.read()), save=True)
                                migrated_count += 1
                                self.stdout.write(f'✅ Bonus image migrated: {bonus.image.name}')
                    else:
                        self.stdout.write(f'Would migrate bonus image: {bonus.image.name}')
                        
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error migrating bonus {bonus.name}: {str(e)}'))
        
        if not dry_run:
            self.stdout.write(f'✅ Migrated {migrated_count} bonus files')

    def check_file_urls(self):
        """Check if file URLs are accessible"""
        self.stdout.write('Checking file URLs...')
        
        # Check hero image
        site_settings = SiteSettings.objects.first()
        if site_settings and site_settings.hero_image:
            try:
                url = site_settings.hero_image.url
                self.stdout.write(f'Hero image URL: {url}')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Hero image URL error: {str(e)}'))
        
        # Check service files
        services = Service.objects.filter(image__isnull=False)[:3]  # Check first 3
        for service in services:
            try:
                if service.image:
                    url = service.image.url
                    self.stdout.write(f'Service image URL: {url}')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Service image URL error: {str(e)}'))
