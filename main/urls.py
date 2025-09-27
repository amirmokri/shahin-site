from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('appointment/', views.appointment, name='appointment'),
    path('services/', views.services_list, name='services'),
    path('lectures/', views.lectures_list, name='lectures_list'),
    path('lecture/<slug:slug>/', views.lecture_detail, name='lecture_detail'),
    path('service/<slug:slug>/', views.service_detail, name='service_detail'),
    
    # Admin pages
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Health check
    path('health/', views.health_check, name='health_check'),
    
    
    # API endpoints
    path('contact-form/', views.contact_form, name='contact_form'),
    path('appointment-form/', views.appointment_form, name='appointment_form'),
    path('comment-form/', views.comment_form, name='comment_form'),
]
