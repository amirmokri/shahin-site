from rest_framework import serializers
from .models import Lecture, Service, ContactMessage, SiteSettings, Appointment


class LectureSerializer(serializers.ModelSerializer):
    """Serializer for Lecture model"""
    class Meta:
        model = Lecture
        fields = ['id', 'title', 'slug', 'image', 'content', 'teaser', 'created_at', 'updated_at', 'is_published']
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']


class ServiceSerializer(serializers.ModelSerializer):
    """Serializer for Service model"""
    video = serializers.FileField(required=False, allow_null=True)
    price_range = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ['id', 'name', 'slug', 'image', 'description', 'video', 'instagram_link', 'min_price', 'max_price', 'duration', 'price_range', 'created_at', 'updated_at', 'is_published']
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']
    
    def get_price_range(self, obj):
        if obj.min_price and obj.max_price:
            return f"{obj.min_price:,} - {obj.max_price:,} تومان"
        elif obj.min_price:
            return f"از {obj.min_price:,} تومان"
        elif obj.max_price:
            return f"تا {obj.max_price:,} تومان"
        return "قیمت نامشخص"


class ContactMessageSerializer(serializers.ModelSerializer):
    """Serializer for ContactMessage model"""
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']


class SiteSettingsSerializer(serializers.ModelSerializer):
    """Serializer for SiteSettings model"""
    class Meta:
        model = SiteSettings
        fields = ['site_name', 'site_description', 'phone', 'email', 'address', 'instagram_url', 'hero_image', 'hero_video_url']


class AppointmentSerializer(serializers.ModelSerializer):
    """Serializer for Appointment model"""
    service_name = serializers.CharField(source='service.name', read_only=True)
    service_image = serializers.CharField(source='service.image.url', read_only=True)
    price_range_display = serializers.CharField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'name', 'phone', 'email', 'service', 'service_name', 'service_image',
            'car_model', 'car_year', 'car_plate', 'appointment_date', 'appointment_time',
            'message', 'estimated_duration', 'estimated_price', 'price_range_display',
            'status', 'status_display', 'is_processed', 'admin_notes',
            'created_at', 'updated_at', 'confirmed_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at']
