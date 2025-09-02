from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('lectures/', views.lectures_list, name='lectures_list'),
    path('lecture/<slug:slug>/', views.lecture_detail, name='lecture_detail'),
    path('service/<slug:slug>/', views.service_detail, name='service_detail'),
    
    # Admin pages
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # API endpoints
    path('contact-form/', views.contact_form, name='contact_form'),
]
