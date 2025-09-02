from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone


class Lecture(models.Model):
    """Model for storing lecture content"""
    title = models.CharField(max_length=200, verbose_name="عنوان")
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="اسلاگ")
    image = models.ImageField(upload_to='lectures/', verbose_name="تصویر")
    content = models.TextField(verbose_name="محتوای کامل")
    teaser = models.TextField(max_length=300, verbose_name="متن کوتاه")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    is_published = models.BooleanField(default=True, verbose_name="منتشر شده")

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('lecture_detail', kwargs={'slug': self.slug})


class Service(models.Model):
    """Model for storing service information"""
    name = models.CharField(max_length=200, verbose_name="نام سرویس")
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="اسلاگ")
    image = models.ImageField(upload_to='services/', verbose_name="تصویر")
    description = models.TextField(verbose_name="توضیحات")
    # Replaced URL-based video with file upload for professional playback
    video = models.FileField(upload_to='services/videos/', blank=True, null=True, verbose_name="ویدیو (MP4)")
    instagram_link = models.URLField(blank=True, null=True, verbose_name="لینک اینستاگرام")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    is_published = models.BooleanField(default=True, verbose_name="منتشر شده")

    class Meta:
        verbose_name = "سرویس"
        verbose_name_plural = "سرویس‌ها"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'slug': self.slug})


class ContactMessage(models.Model):
    """Model for storing contact form messages"""
    name = models.CharField(max_length=100, verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل")
    message = models.TextField(verbose_name="پیام")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ارسال")
    is_read = models.BooleanField(default=False, verbose_name="خوانده شده")

    class Meta:
        verbose_name = "پیام تماس"
        verbose_name_plural = "پیام‌های تماس"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.email}"


class SiteSettings(models.Model):
    """Model for storing site-wide settings"""
    site_name = models.CharField(max_length=100, default="شاهین", verbose_name="نام سایت")
    site_description = models.TextField(default="خدمات حرفه‌ای خودرو  ", verbose_name="توضیحات سایت")
    phone = models.CharField(max_length=20, default="+989126098606", verbose_name="تلفن")
    email = models.EmailField(default="info@shahin-auto.com", verbose_name="ایمیل")
    address = models.TextField(default="کرج، ایران", verbose_name="آدرس")
    instagram_url = models.URLField(default="https://instagram.com/shahinautoservice", verbose_name="لینک اینستاگرام")
    hero_image = models.ImageField(upload_to='site/', default='site/hero.jpg', verbose_name="تصویر اصلی")
    hero_video_url = models.URLField(blank=True, null=True, verbose_name="لینک ویدیو تبلیغاتی")
    
    class Meta:
        verbose_name = "تنظیمات سایت"
        verbose_name_plural = "تنظیمات سایت"

    def __str__(self):
        return "تنظیمات سایت"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SiteSettings.objects.exists():
            return SiteSettings.objects.first()
        super().save(*args, **kwargs)


class Bonus(models.Model):
    """Singleton model to store promotional bonus (offer/advertising) for homepage popup"""
    name = models.CharField(max_length=150, verbose_name="نام پکیج")
    description = models.TextField(verbose_name="توضیحات")
    image = models.ImageField(upload_to='bonus/', verbose_name="تصویر")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی")

    class Meta:
        verbose_name = "پکیج تبلیغاتی"
        verbose_name_plural = "پکیج تبلیغاتی"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and Bonus.objects.exists():
            # Replace existing singleton instead of creating new
            existing = Bonus.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)