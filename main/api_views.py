from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

from .models import Lecture, Service, ContactMessage, SiteSettings
from django.db.models import Q
from .serializers import LectureSerializer, ServiceSerializer, ContactMessageSerializer, SiteSettingsSerializer


class LectureListAPIView(generics.ListCreateAPIView):
    """API view for listing and creating lectures"""
    queryset = Lecture.objects.filter(is_published=True)
    serializer_class = LectureSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Lecture.objects.filter(is_published=True)
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )
        return queryset.order_by('-created_at')


class LectureDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API view for retrieving, updating and deleting individual lectures"""
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly]


class ServiceListAPIView(generics.ListCreateAPIView):
    """API view for listing and creating services"""
    queryset = Service.objects.filter(is_published=True)
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Service.objects.filter(is_published=True)
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        return queryset.order_by('-created_at')


class ServiceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API view for retrieving, updating and deleting individual services"""
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly]


class SiteSettingsAPIView(generics.RetrieveUpdateAPIView):
    """API view for retrieving and updating site settings"""
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        obj, created = SiteSettings.objects.get_or_create(pk=1)
        return obj


@api_view(['POST'])
@permission_classes([])
def contact_form_api(request):
    """API endpoint for contact form submission"""
    serializer = ContactMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'message': 'پیام شما با موفقیت ارسال شد'}, status=status.HTTP_201_CREATED)
    return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def recent_lectures_api(request):
    """API endpoint for getting recent lectures"""
    lectures = Lecture.objects.filter(is_published=True)[:3]
    serializer = LectureSerializer(lectures, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def all_services_api(request):
    """API endpoint for getting all services"""
    services = Service.objects.filter(is_published=True)
    serializer = ServiceSerializer(services, many=True)
    return Response(serializer.data)
