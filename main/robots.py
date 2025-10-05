from django.conf import settings
from robots import Rule, Disallow, Allow
from robots import Site, UserAgent

# Define robots.txt rules
UserAgent('*', [
    Disallow('/admin/'),
    Disallow('/api/'),
    Disallow('/static/admin/'),
    Disallow('/media/admin/'),
    Disallow('/health/'),
    Disallow('/.well-known/'),
    Allow('/'),
])

# Allow all search engines to access the site
UserAgent('Googlebot', [
    Disallow('/admin/'),
    Disallow('/api/'),
    Disallow('/static/admin/'),
    Disallow('/media/admin/'),
    Disallow('/health/'),
    Disallow('/.well-known/'),
    Allow('/'),
])

UserAgent('Bingbot', [
    Disallow('/admin/'),
    Disallow('/api/'),
    Disallow('/static/admin/'),
    Disallow('/media/admin/'),
    Disallow('/health/'),
    Disallow('/.well-known/'),
    Allow('/'),
])

# Sitemap URL
Sitemap = f'https://{settings.ALLOWED_HOSTS[0]}/sitemap.xml'
