from rest_framework import serializers
from .models import Lecture, Service, ContactMessage, SiteSettings


class LectureSerializer(serializers.ModelSerializer):
    """Serializer for Lecture model"""
    class Meta:
        model = Lecture
        fields = ['id', 'title', 'slug', 'image', 'content', 'teaser', 'created_at', 'updated_at', 'is_published']
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']


class ServiceSerializer(serializers.ModelSerializer):
    """Serializer for Service model"""
    video = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Service
        fields = ['id', 'name', 'slug', 'image', 'description', 'video', 'instagram_link', 'created_at', 'updated_at', 'is_published']
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']


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
