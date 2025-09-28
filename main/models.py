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
    category = models.ForeignKey('ServiceCategory', on_delete=models.SET_NULL, null=True, blank=True, related_name='services', verbose_name="دسته‌بندی")
    min_price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, verbose_name="حداقل قیمت (تومان)")
    max_price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, verbose_name="حداکثر قیمت (تومان)")
    duration = models.CharField(max_length=50, blank=True, null=True, verbose_name="مدت زمان")
    is_featured = models.BooleanField(default=False, verbose_name="ویژه")
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
    
    # SEO and Analytics
    google_analytics_id = models.CharField(max_length=20, blank=True, null=True, verbose_name="Google Analytics ID")
    google_site_verification = models.CharField(max_length=100, blank=True, null=True, verbose_name="Google Site Verification")
    bing_site_verification = models.CharField(max_length=100, blank=True, null=True, verbose_name="Bing Site Verification")
    facebook_pixel_id = models.CharField(max_length=20, blank=True, null=True, verbose_name="Facebook Pixel ID")
    
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


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام دسته‌بندی")
    slug = models.SlugField(unique=True, verbose_name="اسلاگ")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name="آیکون")
    color = models.CharField(max_length=7, default="#3B82F6", verbose_name="رنگ")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "دسته‌بندی سرویس"
        verbose_name_plural = "دسته‌بندی‌های سرویس"
        ordering = ['name']

    def __str__(self):
        return self.name


class Comment(models.Model):
    RATING_CHOICES = [
        (1, '1 ستاره'),
        (2, '2 ستاره'),
        (3, '3 ستاره'),
        (4, '4 ستاره'),
        (5, '5 ستاره'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="تلفن")
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="امتیاز")
    comment = models.TextField(verbose_name="نظر")
    is_approved = models.BooleanField(default=False, verbose_name="تایید شده")
    is_featured = models.BooleanField(default=False, verbose_name="ویژه")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    
    # Relations
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='comments', blank=True, null=True, verbose_name="سرویس")
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='comments', blank=True, null=True, verbose_name="کلاس")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', blank=True, null=True, verbose_name="پاسخ به")
    
    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"
        ordering = ['-created_at']

    def __str__(self):
        return f"نظر از {self.name} - {self.rating} ستاره"

    @property
    def is_reply(self):
        return self.parent is not None


class AppointmentRequest(models.Model):
    """Quick appointment/inquiry submitted from homepage"""
    name = models.CharField(max_length=100, verbose_name="نام")
    phone = models.CharField(max_length=20, verbose_name="تلفن")
    email = models.EmailField(blank=True, null=True, verbose_name="ایمیل")
    preferred_date = models.DateField(blank=True, null=True, verbose_name="تاریخ پیشنهادی")
    car_model = models.CharField(max_length=120, blank=True, verbose_name="خودرو")
    service = models.CharField(max_length=120, blank=True, verbose_name="نوع سرویس")
    message = models.TextField(blank=True, verbose_name="توضیحات")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    is_processed = models.BooleanField(default=False, verbose_name="پیگیری شد")

    class Meta:
        verbose_name = "درخواست رزرو"
        verbose_name_plural = "درخواست‌های رزرو"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.phone}"


class Appointment(models.Model):
    """Detailed appointment booking with service and time selection"""
    STATUS_CHOICES = [
        ('pending', 'در انتظار تایید'),
        ('confirmed', 'تایید شده'),
        ('in_progress', 'در حال انجام'),
        ('completed', 'تکمیل شده'),
        ('cancelled', 'لغو شده'),
    ]
    
    # Customer Information
    name = models.CharField(max_length=100, verbose_name="نام و نام خانوادگی")
    phone = models.CharField(max_length=20, verbose_name="شماره تلفن")
    email = models.EmailField(blank=True, null=True, verbose_name="ایمیل")
    
    # Service Information
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments', verbose_name="سرویس")
    car_model = models.CharField(max_length=120, verbose_name="مدل خودرو")
    car_year = models.CharField(max_length=10, blank=True, verbose_name="سال تولید")
    car_plate = models.CharField(max_length=20, blank=True, verbose_name="شماره پلاک")
    
    # Scheduling
    appointment_date = models.DateField(verbose_name="تاریخ نوبت")
    appointment_time = models.TimeField(verbose_name="ساعت نوبت")
    
    # Additional Information
    message = models.TextField(blank=True, verbose_name="توضیحات اضافی")
    estimated_duration = models.CharField(max_length=50, blank=True, verbose_name="مدت زمان تخمینی")
    estimated_price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, verbose_name="قیمت تخمینی")
    
    # Status and Management
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت")
    is_processed = models.BooleanField(default=False, verbose_name="پیگیری شده")
    admin_notes = models.TextField(blank=True, verbose_name="یادداشت ادمین")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی")
    confirmed_at = models.DateTimeField(blank=True, null=True, verbose_name="تاریخ تایید")

    class Meta:
        verbose_name = "نوبت"
        verbose_name_plural = "نوبت‌ها"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.service.name} - {self.appointment_date} {self.appointment_time}"
    
    @property
    def price_range_display(self):
        if self.service.min_price and self.service.max_price:
            return f"{self.service.min_price:,} - {self.service.max_price:,} تومان"
        elif self.service.min_price:
            return f"از {self.service.min_price:,} تومان"
        elif self.service.max_price:
            return f"تا {self.service.max_price:,} تومان"
        return "قیمت نامشخص"