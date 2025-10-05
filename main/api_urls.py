from django.urls import path
from . import api_views

urlpatterns = [
    # Lecture API endpoints
    path('lectures/', api_views.LectureListAPIView.as_view(), name='api_lecture_list'),
    path('lectures/<slug:slug>/', api_views.LectureDetailAPIView.as_view(), name='api_lecture_detail'),
    path('lectures/recent/', api_views.recent_lectures_api, name='api_recent_lectures'),
    
    # Service API endpoints
    path('services/', api_views.ServiceListAPIView.as_view(), name='api_service_list'),
    path('services/<slug:slug>/', api_views.ServiceDetailAPIView.as_view(), name='api_service_detail'),
    path('services/all/', api_views.all_services_api, name='api_all_services'),
    
    # Site settings API endpoint
    path('settings/', api_views.SiteSettingsAPIView.as_view(), name='api_site_settings'),
    
    # Contact form API endpoint
    path('contact/', api_views.contact_form_api, name='api_contact_form'),
    
    # Appointment API endpoints
    path('appointments/', api_views.appointment_booking_api, name='api_appointment_booking'),
    path('appointments/list/', api_views.appointments_list_api, name='api_appointments_list'),
    path('appointment-form/', api_views.appointment_form_api, name='api_appointment_form'),
]
