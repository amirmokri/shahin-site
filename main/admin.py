from django.contrib import admin
from .models import Lecture, Service, ContactMessage, SiteSettings, Bonus


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published', 'created_at', 'updated_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_published', 'created_at', 'updated_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
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