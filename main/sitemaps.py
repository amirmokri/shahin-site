from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Lecture, Service


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages"""
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return ['home', 'lectures_list']

    def location(self, item):
        return reverse(item)


class LectureSitemap(Sitemap):
    """Sitemap for lecture pages"""
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Lecture.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at


class ServiceSitemap(Sitemap):
    """Sitemap for service pages"""
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Service.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at
