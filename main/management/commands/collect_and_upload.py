from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from django.core.files.storage import default_storage
import os
from pathlib import Path


class Command(BaseCommand):
    help = 'Collect static files and upload both static and media files to S3'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be uploaded without actually uploading',
        )
        parser.add_argument(
            '--no-static',
            action='store_true',
            help='Skip static files collection and upload',
        )
        parser.add_argument(
            '--no-media',
            action='store_true',
            help='Skip media files upload',
        )

    def handle(self, *args, **options):
        if not getattr(settings, 'USE_S3', False):
            self.stdout.write(
                self.style.WARNING('S3 storage is not enabled. Set USE_S3=True to use this command.')
            )
            return

        dry_run = options['dry_run']
        no_static = options['no_static']
        no_media = options['no_media']

        # Collect and upload static files
        if not no_static:
            self.stdout.write('Collecting static files...')
            try:
                if not dry_run:
                    call_command('collectstatic', '--noinput', '--clear')
                else:
                    self.stdout.write('Would run: python manage.py collectstatic --noinput --clear')
                self.stdout.write(self.style.SUCCESS('Static files collected successfully'))
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error collecting static files: {str(e)}')
                )
                return

        # Upload media files
        if not no_media:
            self.upload_media_files(dry_run)

    def upload_media_files(self, dry_run):
        """Upload existing media files to S3 storage"""
        media_root = getattr(settings, 'MEDIA_ROOT', None)
        
        if not media_root or not os.path.exists(media_root):
            self.stdout.write(
                self.style.WARNING(f'Media root {media_root} does not exist or is not configured.')
            )
            return

        self.stdout.write(f'Scanning media files in {media_root}...')
        
        uploaded_count = 0
        skipped_count = 0
        error_count = 0

        for root, dirs, files in os.walk(media_root):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, media_root)
                
                # Skip hidden files and directories
                if file.startswith('.'):
                    continue
                
                try:
                    if dry_run:
                        self.stdout.write(f'Would upload: {relative_path}')
                        uploaded_count += 1
                    else:
                        # Check if file already exists in S3
                        if default_storage.exists(relative_path):
                            self.stdout.write(f'Skipping (exists): {relative_path}')
                            skipped_count += 1
                            continue
                        
                        # Upload file to S3
                        with open(file_path, 'rb') as f:
                            default_storage.save(relative_path, f)
                        
                        self.stdout.write(f'Uploaded: {relative_path}')
                        uploaded_count += 1
                        
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error uploading {relative_path}: {str(e)}')
                    )
                    error_count += 1

        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(f'Dry run complete. Would upload {uploaded_count} media files.')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Media upload complete. Uploaded: {uploaded_count}, '
                    f'Skipped: {skipped_count}, Errors: {error_count}'
                )
            )
