from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone
from .models import Lecture, Service, ServiceCategory


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages"""
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return [
            'home',
            'lectures_list', 
            'services_list',
            'contact',
            'about'
        ]

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        return timezone.now()


class ServiceCategorySitemap(Sitemap):
    """Sitemap for service category pages"""
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return ServiceCategory.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse('services_by_category', kwargs={'category_slug': obj.slug})


class ServiceSitemap(Sitemap):
    """Sitemap for service pages"""
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return Service.objects.filter(is_published=True).select_related('category')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('service_detail', kwargs={'slug': obj.slug})


class LectureSitemap(Sitemap):
    """Sitemap for lecture pages"""
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Lecture.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('lecture_detail', kwargs={'slug': obj.slug})


class MainSitemap(Sitemap):
    """Main sitemap that includes all other sitemaps"""
    def __init__(self):
        self.static_sitemap = StaticViewSitemap()
        self.service_category_sitemap = ServiceCategorySitemap()
        self.service_sitemap = ServiceSitemap()
        self.lecture_sitemap = LectureSitemap()

    def items(self):
        items = []
        # Add static pages
        items.extend(self.static_sitemap.items())
        # Add service categories
        items.extend(self.service_category_sitemap.items())
        # Add services
        items.extend(self.service_sitemap.items())
        # Add lectures
        items.extend(self.lecture_sitemap.items())
        return items

    def location(self, item):
        if hasattr(item, 'slug'):
            if hasattr(item, 'category'):
                return reverse('service_detail', kwargs={'slug': item.slug})
            else:
                return reverse('lecture_detail', kwargs={'slug': item.slug})
        elif isinstance(item, str):
            return reverse(item)
        else:
            return reverse('services_by_category', kwargs={'category_slug': item.slug})

    def lastmod(self, item):
        if hasattr(item, 'updated_at'):
            return item.updated_at
        elif hasattr(item, 'created_at'):
            return item.created_at
        else:
            return timezone.now()

    def priority(self, item):
        if isinstance(item, str):
            return 0.8  # Static pages
        elif hasattr(item, 'category'):
            return 0.8  # Services
        elif hasattr(item, 'is_active'):
            return 0.7  # Service categories
        else:
            return 0.7  # Lectures

    def changefreq(self, item):
        if isinstance(item, str):
            return 'weekly'  # Static pages
        else:
            return 'monthly'  # Dynamic content
