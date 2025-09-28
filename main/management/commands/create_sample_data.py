from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from main.models import SiteSettings, ServiceCategory, Service, Lecture, Bonus


class Command(BaseCommand):
    help = 'Create sample data for the website'

    def handle(self, *args, **options):
        # Update site domain
        site = Site.objects.get(id=1)
        site.domain = 'shahinautoservice.ir'
        site.name = 'شاهین خودرو'
        site.save()
        
        # Create or update site settings
        site_settings, created = SiteSettings.objects.get_or_create(
            defaults={
                'site_name': 'شاهین خودرو',
                'site_description': 'خدمات حرفه‌ای خودرو در کرج',
                'phone': '+989126098606',
                'email': 'info@shahinautoservice.ir',
                'address': 'کرج، ایران',
                'instagram_url': 'https://instagram.com/shahinautoservice',
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Site settings created successfully')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('Site settings already exist')
            )
        
        # Create service categories
        categories_data = [
            {
                'name': 'تعمیرات موتور',
                'slug': 'engine-repair',
                'description': 'تعمیرات تخصصی موتور خودرو',
                'icon': 'fas fa-cog',
                'color': '#FF6B6B',
            },
            {
                'name': 'تعمیرات گیربکس',
                'slug': 'transmission-repair',
                'description': 'تعمیرات گیربکس دستی و اتوماتیک',
                'icon': 'fas fa-cogs',
                'color': '#4ECDC4',
            },
            {
                'name': 'تعمیرات برق',
                'slug': 'electrical-repair',
                'description': 'تعمیرات سیستم برق خودرو',
                'icon': 'fas fa-bolt',
                'color': '#45B7D1',
            },
            {
                'name': 'تعمیرات کولر',
                'slug': 'ac-repair',
                'description': 'تعمیرات سیستم کولر خودرو',
                'icon': 'fas fa-snowflake',
                'color': '#96CEB4',
            },
        ]
        
        for cat_data in categories_data:
            category, created = ServiceCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('Sample data creation completed successfully!')
        )