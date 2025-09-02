from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q
import json

from .models import Lecture, Service, ContactMessage, SiteSettings, Bonus


def home(request):
    """Home page view"""
    try:
        site_settings = SiteSettings.objects.first()
        if not site_settings:
            site_settings = SiteSettings.objects.create()
    except:
        site_settings = SiteSettings.objects.create()
    
    # Get recent lectures (last 3)
    recent_lectures = Lecture.objects.filter(is_published=True)[:3]
    
    # Get all services
    services = Service.objects.filter(is_published=True)
    
    # Get singleton bonus if exists
    bonus = Bonus.objects.first()
    
    context = {
        'site_settings': site_settings,
        'recent_lectures': recent_lectures,
        'services': services,
        'bonus': bonus,
    }
    return render(request, 'main/home.html', context)


def lectures_list(request):
    """Lectures list page view"""
    try:
        site_settings = SiteSettings.objects.first()
        if not site_settings:
            site_settings = SiteSettings.objects.create()
    except:
        site_settings = SiteSettings.objects.create()
    
    # Get all published lectures with pagination
    lectures = Lecture.objects.filter(is_published=True)
    paginator = Paginator(lectures, 9)  # Show 9 lectures per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'site_settings': site_settings,
        'page_obj': page_obj,
        'lectures': page_obj,
    }
    return render(request, 'main/lectures.html', context)


def lecture_detail(request, slug):
    """Individual lecture detail page view"""
    try:
        site_settings = SiteSettings.objects.first()
        if not site_settings:
            site_settings = SiteSettings.objects.create()
    except:
        site_settings = SiteSettings.objects.create()
    
    lecture = get_object_or_404(Lecture, slug=slug, is_published=True)
    
    # Get related lectures (same category or recent)
    related_lectures = Lecture.objects.filter(is_published=True).exclude(id=lecture.id)[:3]
    
    context = {
        'site_settings': site_settings,
        'lecture': lecture,
        'related_lectures': related_lectures,
    }
    return render(request, 'main/lecture_detail.html', context)


def service_detail(request, slug):
    """Individual service detail page view"""
    try:
        site_settings = SiteSettings.objects.first()
        if not site_settings:
            site_settings = SiteSettings.objects.create()
    except:
        site_settings = SiteSettings.objects.create()
    
    service = get_object_or_404(Service, slug=slug, is_published=True)
    
    # Get related services
    related_services = Service.objects.filter(is_published=True).exclude(id=service.id)[:3]
    
    context = {
        'site_settings': site_settings,
        'service': service,
        'related_services': related_services,
    }
    return render(request, 'main/service_detail.html', context)


@login_required
def admin_dashboard(request):
    """Admin dashboard view"""
    try:
        site_settings = SiteSettings.objects.first()
        if not site_settings:
            site_settings = SiteSettings.objects.create()
    except:
        site_settings = SiteSettings.objects.create()
    
    lectures = Lecture.objects.all()
    services = Service.objects.all()
    contact_messages = ContactMessage.objects.all()[:10]  # Last 10 messages
    
    context = {
        'site_settings': site_settings,
        'lectures': lectures,
        'services': services,
        'contact_messages': contact_messages,
    }
    return render(request, 'main/admin_dashboard.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def contact_form(request):
    """Handle contact form submission"""
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        message = data.get('message', '').strip()
        
        # Validation
        if not name or not email or not message:
            return JsonResponse({'success': False, 'message': 'لطفاً تمام فیلدها را پر کنید'})
        
        # Create contact message
        contact_message = ContactMessage.objects.create(
            name=name,
            email=email,
            message=message
        )
        
        # Send email notification to admin
        try:
            send_mail(
                f'پیام جدید از {name}',
                f'نام: {name}\nایمیل: {email}\nپیام:\n{message}',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
        except Exception as e:
            # Log error but don't fail the request
            print(f"Email sending failed: {e}")
        
        return JsonResponse({'success': True, 'message': 'پیام شما با موفقیت ارسال شد'})
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': 'خطا در ارسال پیام'})
