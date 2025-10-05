from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.storage import default_storage
import os
from pathlib import Path


class Command(BaseCommand):
    help = 'Upload existing media files to S3 storage'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be uploaded without actually uploading',
        )

    def handle(self, *args, **options):
        if not getattr(settings, 'USE_S3', False):
            self.stdout.write(
                self.style.WARNING('S3 storage is not enabled. Set USE_S3=True to use this command.')
            )
            return

        dry_run = options['dry_run']
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
                self.style.SUCCESS(f'Dry run complete. Would upload {uploaded_count} files.')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Upload complete. Uploaded: {uploaded_count}, '
                    f'Skipped: {skipped_count}, Errors: {error_count}'
                )
            )
