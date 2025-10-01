"""
Management command to copy media files to static folder structure
This is an alternative approach to handle media files with Arvan Cloud
"""
import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from main.models import Lecture, Service, SiteSettings, Bonus


class Command(BaseCommand):
    help = 'Copy media files to static folder structure'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be copied without actually doing it',
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

        self.stdout.write('Starting media to static copy...')
        
        # Copy all media files to static/media
        for root, dirs, files in os.walk(media_root):
            for file in files:
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, media_root)
                dst_path = os.path.join(static_media_dir, rel_path)
                
                # Create destination directory
                if not dry_run:
                    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                
                if dry_run:
                    self.stdout.write(f'  Would copy: {rel_path}')
                else:
                    try:
                        shutil.copy2(src_path, dst_path)
                        self.stdout.write(f'  Copied: {rel_path}')
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f'  Error copying {rel_path}: {str(e)}')
                        )
        
        self.stdout.write(
            self.style.SUCCESS('Media to static copy completed!')
        )
