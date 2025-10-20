from django.core.management.base import BaseCommand
from django.db import connection
from django.conf import settings


class Command(BaseCommand):
    help = 'Fix MySQL database character set to support UTF-8 properly'

    def handle(self, *args, **options):
        self.stdout.write('Fixing database character set...')
        
        try:
            with connection.cursor() as cursor:
                # Get database name from settings
                db_name = settings.DATABASES['default']['NAME']
                
                # Convert database to utf8mb4
                cursor.execute(f"ALTER DATABASE `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                self.stdout.write(f'Database {db_name} converted to utf8mb4')
                
                # Get all tables
                cursor.execute(f"SHOW TABLES FROM `{db_name}`")
                tables = cursor.fetchall()
                
                for table in tables:
                    table_name = table[0]
                    
                    # Convert table to utf8mb4
                    cursor.execute(f"ALTER TABLE `{table_name}` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                    self.stdout.write(f'Table {table_name} converted to utf8mb4')
                
                self.stdout.write(
                    self.style.SUCCESS('Database character set fixed successfully!')
                )
                self.stdout.write('You can now add services with Persian text and emojis.')
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error fixing database charset: {e}')
            )
            self.stdout.write(
                'You may need to run this command with database administrator privileges.'
            )
