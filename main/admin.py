from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Count
from django.contrib.admin.views.main import ChangeList
from .models import Lecture, Service, ContactMessage, SiteSettings, Bonus, AppointmentRequest, Appointment, ServiceCategory, Comment

# Customize the default admin site
admin.site.site_header = "پنل مدیریت شاهین خودرو"
admin.site.site_title = "شاهین خودرو"
admin.site.index_title = "خوش آمدید به پنل مدیریت"

# Custom admin index view with stats
from django.contrib.admin.views.main import ChangeList
from django.views.generic import TemplateView

class CustomAdminIndexView(TemplateView):
    template_name = 'admin/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get statistics
        stats = {
            'total_services': Service.objects.count(),
            'published_services': Service.objects.filter(is_published=True).count(),
            'total_lectures': Lecture.objects.count(),
            'published_lectures': Lecture.objects.filter(is_published=True).count(),
            'total_comments': Comment.objects.count(),
            'pending_comments': Comment.objects.filter(is_approved=False).count(),
            'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
            'pending_appointments': AppointmentRequest.objects.filter(is_processed=False).count(),
            'total_appointments': Appointment.objects.count(),
            'pending_appointment_requests': Appointment.objects.filter(status='pending').count(),
        }
        
        context['stats'] = stats
        return context

# Override the admin index view
admin.site.index = CustomAdminIndexView.as_view()


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_preview', 'is_published', 'comment_count', 'created_at', 'updated_at']
    list_filter = ['is_published', 'created_at', 'updated_at']
    search_fields = ['title', 'content', 'teaser']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'image_preview']
    list_per_page = 20
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'slug', 'image', 'image_preview', 'teaser', 'content', 'is_published')
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 4px;" />', obj.image.url)
        return "بدون تصویر"
    image_preview.short_description = "پیش‌نمایش"
    
    def comment_count(self, obj):
        count = obj.comments.count()
        if count > 0:
            url = reverse('admin:main_comment_changelist') + f'?lecture__id__exact={obj.id}'
            return format_html('<a href="{}">{} نظر</a>', url, count)
        return "0 نظر"
    comment_count.short_description = "نظرات"
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            comment_count=Count('comments')
        )


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color_preview', 'service_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20
    ordering = ['name']
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('name', 'slug', 'description', 'is_active')
        }),
        ('طراحی', {
            'fields': ('icon', 'color', 'color_preview')
        }),
        ('زمان‌بندی', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'color_preview']
    
    def color_preview(self, obj):
        if obj.color:
            return format_html(
                '<div style="width: 30px; height: 20px; background-color: {}; border: 1px solid #ccc; border-radius: 3px;"></div>',
                obj.color
            )
        return "بدون رنگ"
    color_preview.short_description = "پیش‌نمایش رنگ"
    
    def service_count(self, obj):
        count = obj.services.count()
        if count > 0:
            url = reverse('admin:main_service_changelist') + f'?category__id__exact={obj.id}'
            return format_html('<a href="{}">{} سرویس</a>', url, count)
        return "0 سرویس"
    service_count.short_description = "سرویس‌ها"
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            service_count=Count('services')
        )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_preview', 'category', 'price_range_formatted', 'duration', 'is_featured', 'is_published', 'comment_count', 'created_at']
    list_filter = ['category', 'is_featured', 'is_published', 'created_at', 'updated_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at', 'image_preview']
    list_per_page = 20
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('name', 'slug', 'category', 'image', 'image_preview', 'description', 'is_published')
        }),
        ('قیمت‌گذاری و زمان', {
            'fields': ('min_price', 'max_price', 'duration', 'is_featured'),
            'description': 'برای تعیین محدوده قیمت، حداقل و حداکثر قیمت را وارد کنید'
        }),
        ('رسانه‌ها', {
            'fields': ('video', 'instagram_link'),
            'description': 'ویدیو MP4 را آپلود کنید. اندازه پیشنهادی ≤ 200MB'
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 4px;" />', obj.image.url)
        return "بدون تصویر"
    image_preview.short_description = "پیش‌نمایش"
    
    def price_range_formatted(self, obj):
        if obj.min_price and obj.max_price:
            return format_html('<span style="color: #28a745; font-weight: bold;">{} - {} تومان</span>', 
                             f"{obj.min_price:,}", f"{obj.max_price:,}")
        elif obj.min_price:
            return format_html('<span style="color: #28a745; font-weight: bold;">از {} تومان</span>', f"{obj.min_price:,}")
        elif obj.max_price:
            return format_html('<span style="color: #28a745; font-weight: bold;">تا {} تومان</span>', f"{obj.max_price:,}")
        return "قیمت نامشخص"
    price_range_formatted.short_description = "محدوده قیمت"
    
    def comment_count(self, obj):
        count = obj.comments.count()
        if count > 0:
            url = reverse('admin:main_comment_changelist') + f'?service__id__exact={obj.id}'
            return format_html('<a href="{}">{} نظر</a>', url, count)
        return "0 نظر"
    comment_count.short_description = "نظرات"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category').annotate(
            comment_count=Count('comments')
        )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'message_preview', 'is_read_status', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created_at', 'message_preview']
    actions = ['mark_as_read', 'mark_as_unread']
    list_per_page = 25
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('اطلاعات تماس', {
            'fields': ('name', 'email')
        }),
        ('پیام', {
            'fields': ('message', 'message_preview')
        }),
        ('وضعیت', {
            'fields': ('is_read', 'created_at')
        }),
    )
    
    def message_preview(self, obj):
        if len(obj.message) > 100:
            return format_html('{}...', obj.message[:100])
        return obj.message
    message_preview.short_description = "پیش‌نمایش پیام"
    
    def is_read_status(self, obj):
        if obj.is_read:
            return format_html('<span style="color: #28a745; font-weight: bold;">✓ خوانده شده</span>')
        return format_html('<span style="color: #dc3545; font-weight: bold;">✗ خوانده نشده</span>')
    is_read_status.short_description = "وضعیت"

    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} پیام به عنوان خوانده شده علامت‌گذاری شد.')
    mark_as_read.short_description = "علامت‌گذاری به عنوان خوانده شده"

    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} پیام به عنوان خوانده نشده علامت‌گذاری شد.')
    mark_as_unread.short_description = "علامت‌گذاری به عنوان خوانده نشده"


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'phone', 'email']
    readonly_fields = ['hero_image_preview']
    
    fieldsets = (
        ('اطلاعات عمومی', {
            'fields': ('site_name', 'site_description')
        }),
        ('اطلاعات تماس', {
            'fields': ('phone', 'email', 'address', 'instagram_url')
        }),
        ('رسانه‌ها', {
            'fields': ('hero_image', 'hero_image_preview', 'hero_video_url')
        }),
        ('تحلیل و سئو', {
            'fields': ('google_analytics_id', 'google_site_verification', 'bing_site_verification', 'facebook_pixel_id'),
            'classes': ('collapse',)
        }),
    )
    
    def hero_image_preview(self, obj):
        if obj.hero_image:
            return format_html('<img src="{}" width="200" height="100" style="border-radius: 8px; border: 1px solid #ddd;" />', obj.hero_image.url)
        return "بدون تصویر"
    hero_image_preview.short_description = "پیش‌نمایش تصویر اصلی"

    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the only instance
        return False


@admin.register(Bonus)
class BonusAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_preview', 'updated_at']
    readonly_fields = ['updated_at', 'image_preview']
    
    fieldsets = (
        ('پکیج تبلیغاتی', {
            'fields': ('name', 'description', 'image', 'image_preview')
        }),
        ('وضعیت', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" height="100" style="border-radius: 8px; border: 1px solid #ddd;" />', obj.image.url)
        return "بدون تصویر"
    image_preview.short_description = "پیش‌نمایش تصویر"

    def has_add_permission(self, request):
        # Enforce single instance
        return not Bonus.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the only instance
        return False


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating_stars', 'service', 'lecture', 'comment_preview', 'is_approved_status', 'is_featured_status', 'created_at']
    list_filter = ['rating', 'is_approved', 'is_featured', 'created_at', 'service', 'lecture']
    search_fields = ['name', 'email', 'comment', 'phone']
    readonly_fields = ['created_at', 'comment_preview']
    actions = ['approve_comments', 'unapprove_comments', 'feature_comments', 'unfeature_comments']
    list_per_page = 25
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('اطلاعات کاربر', {
            'fields': ('name', 'email', 'phone')
        }),
        ('نظر و امتیاز', {
            'fields': ('rating', 'comment', 'comment_preview')
        }),
        ('ارتباط', {
            'fields': ('service', 'lecture', 'parent')
        }),
        ('وضعیت', {
            'fields': ('is_approved', 'is_featured', 'created_at')
        }),
    )
    
    def rating_stars(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        color = '#ffc107' if obj.rating >= 4 else '#28a745' if obj.rating >= 3 else '#dc3545'
        return format_html('<span style="color: {}; font-size: 16px;">{}</span>', color, stars)
    rating_stars.short_description = "امتیاز"
    
    def comment_preview(self, obj):
        if len(obj.comment) > 100:
            return format_html('{}...', obj.comment[:100])
        return obj.comment
    comment_preview.short_description = "پیش‌نمایش نظر"
    
    def is_approved_status(self, obj):
        if obj.is_approved:
            return format_html('<span style="color: #28a745; font-weight: bold;">✓ تایید شده</span>')
        return format_html('<span style="color: #dc3545; font-weight: bold;">✗ تایید نشده</span>')
    is_approved_status.short_description = "وضعیت تایید"
    
    def is_featured_status(self, obj):
        if obj.is_featured:
            return format_html('<span style="color: #ffc107; font-weight: bold;">⭐ ویژه</span>')
        return "عادی"
    is_featured_status.short_description = "ویژه"

    def approve_comments(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} نظر تایید شد.')
    approve_comments.short_description = "تایید نظرات انتخاب شده"

    def unapprove_comments(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} نظر لغو تایید شد.')
    unapprove_comments.short_description = "لغو تایید نظرات انتخاب شده"

    def feature_comments(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} نظر ویژه شد.')
    feature_comments.short_description = "ویژه کردن نظرات انتخاب شده"

    def unfeature_comments(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} نظر از حالت ویژه خارج شد.')
    unfeature_comments.short_description = "خروج از حالت ویژه"


@admin.register(AppointmentRequest)
class AppointmentRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'car_model', 'service', 'preferred_date', 'is_processed_status', 'created_at']
    list_filter = ['is_processed', 'created_at', 'preferred_date']
    search_fields = ['name', 'phone', 'email', 'car_model', 'service', 'message']
    readonly_fields = ['created_at', 'message_preview']
    actions = ['mark_processed', 'mark_unprocessed']
    list_per_page = 25
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('اطلاعات مشتری', {
            'fields': ('name', 'phone', 'email')
        }),
        ('جزئیات درخواست', {
            'fields': ('car_model', 'service', 'preferred_date', 'message', 'message_preview')
        }),
        ('وضعیت', {
            'fields': ('is_processed', 'created_at')
        }),
    )
    
    def message_preview(self, obj):
        if obj.message and len(obj.message) > 100:
            return format_html('{}...', obj.message[:100])
        return obj.message or "بدون توضیحات"
    message_preview.short_description = "پیش‌نمایش توضیحات"
    
    def is_processed_status(self, obj):
        if obj.is_processed:
            return format_html('<span style="color: #28a745; font-weight: bold;">✓ پیگیری شده</span>')
        return format_html('<span style="color: #dc3545; font-weight: bold;">✗ پیگیری نشده</span>')
    is_processed_status.short_description = "وضعیت پیگیری"

    def mark_processed(self, request, queryset):
        updated = queryset.update(is_processed=True)
        self.message_user(request, f'{updated} مورد به عنوان پیگیری‌شده علامت‌گذاری شد.')
    mark_processed.short_description = "علامت‌گذاری به عنوان پیگیری‌شده"

    def mark_unprocessed(self, request, queryset):
        updated = queryset.update(is_processed=False)
        self.message_user(request, f'{updated} مورد به عنوان پیگیری‌نشده علامت‌گذاری شد.')
    mark_unprocessed.short_description = "علامت‌گذاری به عنوان پیگیری‌نشده"


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'service', 'appointment_date', 'appointment_time', 'status_display', 'is_processed_status', 'created_at']
    list_filter = ['status', 'is_processed', 'appointment_date', 'created_at', 'service']
    search_fields = ['name', 'phone', 'email', 'car_model', 'car_plate', 'service__name']
    readonly_fields = ['created_at', 'updated_at', 'message_preview', 'price_range_display']
    actions = ['mark_processed', 'mark_unprocessed', 'confirm_appointments', 'cancel_appointments']
    list_per_page = 25
    date_hierarchy = 'appointment_date'
    ordering = ['-created_at']
    
    fieldsets = (
        ('اطلاعات مشتری', {
            'fields': ('name', 'phone', 'email')
        }),
        ('اطلاعات خودرو', {
            'fields': ('car_model', 'car_year', 'car_plate')
        }),
        ('سرویس و زمان‌بندی', {
            'fields': ('service', 'appointment_date', 'appointment_time', 'estimated_duration', 'price_range_display')
        }),
        ('جزئیات اضافی', {
            'fields': ('message', 'message_preview', 'estimated_price')
        }),
        ('وضعیت و مدیریت', {
            'fields': ('status', 'is_processed', 'admin_notes')
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at', 'confirmed_at'),
            'classes': ('collapse',)
        }),
    )
    
    def message_preview(self, obj):
        if obj.message and len(obj.message) > 100:
            return format_html('{}...', obj.message[:100])
        return obj.message or "بدون توضیحات"
    message_preview.short_description = "پیش‌نمایش توضیحات"
    
    def status_display(self, obj):
        status_colors = {
            'pending': '#ffc107',
            'confirmed': '#28a745',
            'in_progress': '#17a2b8',
            'completed': '#6c757d',
            'cancelled': '#dc3545'
        }
        status_texts = {
            'pending': 'در انتظار تایید',
            'confirmed': 'تایید شده',
            'in_progress': 'در حال انجام',
            'completed': 'تکمیل شده',
            'cancelled': 'لغو شده'
        }
        color = status_colors.get(obj.status, '#6c757d')
        text = status_texts.get(obj.status, obj.status)
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, text)
    status_display.short_description = "وضعیت"
    
    def is_processed_status(self, obj):
        if obj.is_processed:
            return format_html('<span style="color: #28a745; font-weight: bold;">✓ پیگیری شده</span>')
        return format_html('<span style="color: #dc3545; font-weight: bold;">✗ پیگیری نشده</span>')
    is_processed_status.short_description = "وضعیت پیگیری"

    def mark_processed(self, request, queryset):
        updated = queryset.update(is_processed=True)
        self.message_user(request, f'{updated} نوبت به عنوان پیگیری‌شده علامت‌گذاری شد.')
    mark_processed.short_description = "علامت‌گذاری به عنوان پیگیری‌شده"

    def mark_unprocessed(self, request, queryset):
        updated = queryset.update(is_processed=False)
        self.message_user(request, f'{updated} نوبت به عنوان پیگیری‌نشده علامت‌گذاری شد.')
    mark_unprocessed.short_description = "علامت‌گذاری به عنوان پیگیری‌نشده"

    def confirm_appointments(self, request, queryset):
        from django.utils import timezone
        updated = queryset.filter(status='pending').update(status='confirmed', confirmed_at=timezone.now())
        self.message_user(request, f'{updated} نوبت تایید شد.')
    confirm_appointments.short_description = "تایید نوبت‌های انتخاب شده"

    def cancel_appointments(self, request, queryset):
        updated = queryset.filter(status__in=['pending', 'confirmed']).update(status='cancelled')
        self.message_user(request, f'{updated} نوبت لغو شد.')
    cancel_appointments.short_description = "لغو نوبت‌های انتخاب شده"