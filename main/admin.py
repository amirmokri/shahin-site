from django.contrib import admin
from .models import Lecture, Service, ContactMessage, SiteSettings, Bonus, AppointmentRequest, ServiceCategory, Comment


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published', 'created_at', 'updated_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_featured', 'is_published', 'created_at']
    list_filter = ['category', 'is_featured', 'is_published', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = []
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('name', 'slug', 'image', 'description', 'is_published')
        }),
        ('ویدیو', {
            'fields': ('video',),
            'description': 'ویدیو MP4 را آپلود کنید. اندازه پیشنهادی ≤ 200MB'
        }),
        ('شبکه‌های اجتماعی', {
            'fields': ('instagram_link',)
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created_at']
    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f'{queryset.count()} پیام به عنوان خوانده شده علامت‌گذاری شد.')
    mark_as_read.short_description = "علامت‌گذاری به عنوان خوانده شده"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
        self.message_user(request, f'{queryset.count()} پیام به عنوان خوانده نشده علامت‌گذاری شد.')
    mark_as_unread.short_description = "علامت‌گذاری به عنوان خوانده نشده"


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('اطلاعات عمومی', {
            'fields': ('site_name', 'site_description')
        }),
        ('اطلاعات تماس', {
            'fields': ('phone', 'email', 'address', 'instagram_url')
        }),
        ('رسانه‌ها', {
            'fields': ('hero_image', 'hero_video_url')
        }),
    )

    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()


@admin.register(Bonus)
class BonusAdmin(admin.ModelAdmin):
    fieldsets = (
        ('پکیج', {
            'fields': ('name', 'description', 'image')
        }),
        ('وضعیت', {
            'fields': ('updated_at',),
        }),
    )
    readonly_fields = ('updated_at',)

    def has_add_permission(self, request):
        # Enforce single instance
        return not Bonus.objects.exists()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'service', 'lecture', 'is_approved', 'is_featured', 'created_at']
    list_filter = ['rating', 'is_approved', 'is_featured', 'created_at', 'service', 'lecture']
    search_fields = ['name', 'email', 'comment']
    readonly_fields = ['created_at']
    actions = ['approve_comments', 'unapprove_comments', 'feature_comments', 'unfeature_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'{queryset.count()} نظر تایید شد.')
    approve_comments.short_description = "تایید نظرات انتخاب شده"

    def unapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f'{queryset.count()} نظر لغو تایید شد.')
    unapprove_comments.short_description = "لغو تایید نظرات انتخاب شده"

    def feature_comments(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f'{queryset.count()} نظر ویژه شد.')
    feature_comments.short_description = "ویژه کردن نظرات انتخاب شده"

    def unfeature_comments(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(request, f'{queryset.count()} نظر از حالت ویژه خارج شد.')
    unfeature_comments.short_description = "خروج از حالت ویژه"


@admin.register(AppointmentRequest)
class AppointmentRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'service', 'preferred_date', 'is_processed', 'created_at']
    list_filter = ['is_processed', 'created_at']
    search_fields = ['name', 'phone', 'email', 'car_model', 'service']
    readonly_fields = ['created_at']
    actions = ['mark_processed', 'mark_unprocessed']

    def mark_processed(self, request, queryset):
        queryset.update(is_processed=True)
        self.message_user(request, f'{queryset.count()} مورد به عنوان پیگیری‌شده علامت‌گذاری شد.')
    mark_processed.short_description = "علامت‌گذاری به عنوان پیگیری‌شده"

    def mark_unprocessed(self, request, queryset):
        queryset.update(is_processed=False)
        self.message_user(request, f'{queryset.count()} مورد به عنوان پیگیری‌نشده علامت‌گذاری شد.')
    mark_unprocessed.short_description = "علامت‌گذاری به عنوان پیگیری‌نشده"