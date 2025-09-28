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

from .models import Lecture, Service, ContactMessage, SiteSettings, Appointment, AppointmentRequest
from django.db.models import Q
from .serializers import LectureSerializer, ServiceSerializer, ContactMessageSerializer, SiteSettingsSerializer, AppointmentSerializer


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


@api_view(['POST'])
@permission_classes([])
def appointment_form_api(request):
    """API endpoint for appointment form submission (quick appointment from homepage)"""
    try:
        data = request.data
        
        # Create appointment request
        appointment_request = AppointmentRequest.objects.create(
            name=data.get('name', ''),
            phone=data.get('phone', ''),
            email=data.get('email', ''),
            preferred_date=data.get('preferred_date'),
            car_model=data.get('car_model', ''),
            service=data.get('service', ''),
            message=data.get('message', '')
        )
        
        return Response({
            'success': True, 
            'message': 'درخواست رزرو شما با موفقیت ثبت شد. در اولین فرصت با شما تماس خواهیم گرفت.'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'success': False, 
            'message': 'خطا در ثبت درخواست. لطفاً دوباره تلاش کنید.'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([])
def appointment_booking_api(request):
    """API endpoint for detailed appointment booking"""
    try:
        data = request.data
        
        # Validate required fields
        required_fields = ['name', 'phone', 'service_id', 'appointment_date', 'appointment_time', 'car_model']
        for field in required_fields:
            if not data.get(field):
                return Response({
                    'success': False,
                    'message': f'فیلد {field} الزامی است'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get service
        try:
            service = Service.objects.get(id=data['service_id'])
        except Service.DoesNotExist:
            return Response({
                'success': False,
                'message': 'سرویس انتخاب شده یافت نشد'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create appointment
        appointment = Appointment.objects.create(
            name=data['name'],
            phone=data['phone'],
            email=data.get('email', ''),
            service=service,
            car_model=data['car_model'],
            car_year=data.get('car_year', ''),
            car_plate=data.get('car_plate', ''),
            appointment_date=data['appointment_date'],
            appointment_time=data['appointment_time'],
            message=data.get('message', ''),
            estimated_duration=service.duration or '',
            estimated_price=service.min_price
        )
        
        return Response({
            'success': True,
            'message': f'نوبت شما برای {service.name} در تاریخ {data["appointment_date"]} ساعت {data["appointment_time"]} با موفقیت ثبت شد. در اولین فرصت با شما تماس خواهیم گرفت.',
            'appointment_id': appointment.id
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': 'خطا در ثبت نوبت. لطفاً دوباره تلاش کنید.'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def appointments_list_api(request):
    """API endpoint for getting appointments (admin only)"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return Response({'success': False, 'message': 'دسترسی غیرمجاز'}, status=status.HTTP_403_FORBIDDEN)
    
    appointments = Appointment.objects.all().order_by('-created_at')
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)
