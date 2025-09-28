"""
URL configuration for shahin_auto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap, index
from main.sitemaps import StaticViewSitemap, LectureSitemap, ServiceSitemap, ServiceCategorySitemap, MainSitemap

# Sitemap configuration
sitemaps = {
    'static': StaticViewSitemap,
    'service_categories': ServiceCategorySitemap,
    'services': ServiceSitemap,
    'lectures': LectureSitemap,
    'main': MainSitemap,
}

def health_view(_request):
    return HttpResponse("ok", content_type="text/plain")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('api/', include('main.api_urls')),
    path('sitemap.xml', index, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.index'),
    path('sitemap-<section>.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', lambda r: HttpResponse('User-agent: *\nDisallow: /admin/\nDisallow: /api/\nAllow: /\nSitemap: https://shahinautoservice.ir/sitemap.xml', content_type='text/plain')),
    path('health/', health_view, name='health'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)