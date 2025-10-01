"""
Management command to move existing media files to static/media structure
"""
import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from main.models import Lecture, Service, SiteSettings, Bonus


class Command(BaseCommand):
    help = 'Move existing media files to static/media structure'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be moved without actually doing it',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        media_root = getattr(settings, 'MEDIA_ROOT', None)
        static_root = getattr(settings, 'STATIC_ROOT', None)
        
        if not media_root or not os.path.exists(media_root):
            self.stdout.write(
                self.style.WARNING('No local media directory found.')
            )
            return

        if not static_root:
            self.stdout.write(
                self.style.WARNING('STATIC_ROOT not configured.')
            )
            return

        # Create static/media directory
        static_media_dir = os.path.join(static_root, 'media')
        if not dry_run:
            os.makedirs(static_media_dir, exist_ok=True)

        self.stdout.write('Starting media to static/media move...')
        
        # Move all media files to static/media
        for root, dirs, files in os.walk(media_root):
            for file in files:
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, media_root)
                dst_path = os.path.join(static_media_dir, rel_path)
                
                # Create destination directory
                if not dry_run:
                    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                
                if dry_run:
                    self.stdout.write(f'  Would move: {rel_path}')
                else:
                    try:
                        shutil.move(src_path, dst_path)
                        self.stdout.write(f'  Moved: {rel_path}')
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f'  Error moving {rel_path}: {str(e)}')
                        )
        
        # Update model file paths in database
        if not dry_run:
            self.update_model_paths()
        
        self.stdout.write(
            self.style.SUCCESS('Media to static/media move completed!')
        )

    def update_model_paths(self):
        """Update file paths in database to reflect new structure"""
        self.stdout.write('Updating database file paths...')
        
        # Update Lecture images
        for lecture in Lecture.objects.exclude(image__isnull=True).exclude(image=''):
            if lecture.image and not lecture.image.name.startswith('static/media/'):
                old_path = lecture.image.name
                new_path = f'static/media/{old_path}'
                lecture.image.name = new_path
                lecture.save()
                self.stdout.write(f'  Updated Lecture: {old_path} -> {new_path}')
        
        # Update Service images and videos
        for service in Service.objects.all():
            if service.image and not service.image.name.startswith('static/media/'):
                old_path = service.image.name
                new_path = f'static/media/{old_path}'
                service.image.name = new_path
                service.save()
                self.stdout.write(f'  Updated Service image: {old_path} -> {new_path}')
            
            if service.video and not service.video.name.startswith('static/media/'):
                old_path = service.video.name
                new_path = f'static/media/{old_path}'
                service.video.name = new_path
                service.save()
                self.stdout.write(f'  Updated Service video: {old_path} -> {new_path}')
        
        # Update SiteSettings hero image
        for site_setting in SiteSettings.objects.all():
            if site_setting.hero_image and not site_setting.hero_image.name.startswith('static/media/'):
                old_path = site_setting.hero_image.name
                new_path = f'static/media/{old_path}'
                site_setting.hero_image.name = new_path
                site_setting.save()
                self.stdout.write(f'  Updated SiteSettings: {old_path} -> {new_path}')
        
        # Update Bonus images
        for bonus in Bonus.objects.all():
            if bonus.image and not bonus.image.name.startswith('static/media/'):
                old_path = bonus.image.name
                new_path = f'static/media/{old_path}'
                bonus.image.name = new_path
                bonus.save()
                self.stdout.write(f'  Updated Bonus: {old_path} -> {new_path}')
