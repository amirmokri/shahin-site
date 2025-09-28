from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q
from django.db import connection
import json

from .models import Lecture, Service, ContactMessage, SiteSettings, Bonus, AppointmentRequest, Comment, ServiceCategory
from datetime import datetime
from django.core.cache import cache


def health_check(request):
    """Health check endpoint for Docker"""
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return HttpResponse("OK", status=200)
    except Exception as e:
        return HttpResponse(f"Database error: {str(e)}", status=500)


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
    
    iran_brands = [
        'ایران‌خودرو', 'سایپا', 'پارس‌خودرو', 'کرمان‌موتور', 'بهمن‌موتور',
        'پژو', 'رنو', 'تویوتا', 'هیوندای', 'کیا', 'نیسان', 'مزدا', 'میتسوبیشی', 'سوزوکی',
        'بنز', 'بی‌ام‌و', 'آئودی', 'فولکس‌واگن', 'ام‌جی', 'چری', 'جک', 'هاوال', 'دانگ‌فنگ'
    ]

    testimonials = [
        {'name': 'Kathleen M.', 'text': 'سرویس عالی و سریع. خودرو مثل روز اول شده!', 'date': '2025/09/13'},
        {'name': 'Dale B.', 'text': 'حرفه‌ای، صادق و دقیق. کاملاً راضی هستم.', 'date': '2025/09/05'},
        {'name': 'David G.', 'text': 'همیشه بهترین تجربه را دارم. توصیه می‌کنم.', 'date': '2025/08/29'},
    ]

    context = {
        'site_settings': site_settings,
        'recent_lectures': recent_lectures,
        'services': services,
        'bonus': bonus,
        'iran_brands': iran_brands,
        'testimonials': testimonials,
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
    
    # Get approved comments for this lecture
    comments = Comment.objects.filter(lecture=lecture, is_approved=True).order_by('-created_at')
    
    context = {
        'site_settings': site_settings,
        'lecture': lecture,
        'related_lectures': related_lectures,
        'comments': comments,
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
    
    # Get approved comments for this service
    comments = Comment.objects.filter(service=service, is_approved=True).order_by('-created_at')
    
    context = {
        'site_settings': site_settings,
        'service': service,
        'related_services': related_services,
        'comments': comments,
    }
    return render(request, 'main/service_detail.html', context)


def services_list(request):
    """Services listing page with filter/search"""
    try:
        site_settings = SiteSettings.objects.first()
        if not site_settings:
            site_settings = SiteSettings.objects.create()
    except:
        site_settings = SiteSettings.objects.create()

    services = Service.objects.filter(is_published=True).select_related('category')
    categories = ServiceCategory.objects.filter(is_active=True)
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        services = services.filter(category__slug=category_slug)
    
    # Filter by featured
    featured = request.GET.get('featured')
    if featured == 'true':
        services = services.filter(is_featured=True)

    context = {
        'site_settings': site_settings,
        'services': services,
        'categories': categories,
        'current_category': category_slug,
        'current_featured': featured,
    }
    return render(request, 'main/services.html', context)
def appointment(request):
    """Appointment request page"""
    try:
        site_settings = SiteSettings.objects.first()
        if not site_settings:
            site_settings = SiteSettings.objects.create()
    except:
        site_settings = SiteSettings.objects.create()
    
    # Get all services for selection
    services = Service.objects.filter(is_published=True)
    
    # Get today's date for date input min value
    from django.utils import timezone
    today = timezone.now().date()

    context = {
        'site_settings': site_settings,
        'services': services,
        'today': today,
    }
    return render(request, 'main/appointment.html', context)



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
    appointments = AppointmentRequest.objects.all()[:10]
    new_appointments_count = AppointmentRequest.objects.filter(is_processed=False).count()
    
    context = {
        'site_settings': site_settings,
        'lectures': lectures,
        'services': services,
        'contact_messages': contact_messages,
        'appointments': appointments,
        'new_appointments_count': new_appointments_count,
    }
    return render(request, 'main/admin_dashboard.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def contact_form(request):
    """Handle contact form submission"""
    try:
        data = json.loads(request.body)
        # Honeypot
        if data.get('company'):
            return JsonResponse({'success': True, 'message': 'پیام شما با موفقیت ارسال شد'})

        # Rate limit (5 per 10 minutes per IP)
        ip = request.META.get('REMOTE_ADDR', 'unknown')
        key = f"rl:contact:{ip}"
        count = cache.get(key, 0)
        if count >= 5:
            return JsonResponse({'success': False, 'message': 'تعداد درخواست‌ها زیاد است.稍后 دوباره تلاش کنید'})
        cache.set(key, count + 1, 600)
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


@csrf_exempt
@require_http_methods(["POST"])
def appointment_form(request):
    """Handle appointment submission from home quick form"""
    try:
        data = json.loads(request.body)
        # Honeypot
        if data.get('company'):
            return JsonResponse({'success': True, 'message': 'درخواست شما ثبت شد'})

        # Rate limit (5 per 10 minutes per IP)
        ip = request.META.get('REMOTE_ADDR', 'unknown')
        key = f"rl:appt:{ip}"
        count = cache.get(key, 0)
        if count >= 5:
            return JsonResponse({'success': False, 'message': 'تعداد درخواست‌ها زیاد است.稍后 دوباره تلاش کنید'})
        cache.set(key, count + 1, 600)
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        email = (data.get('email') or '').strip()
        preferred_date = (data.get('preferred_date') or '').strip()
        car_model = (data.get('car_model') or '').strip()
        service = (data.get('service') or '').strip()
        message = (data.get('message') or '').strip()

        if not name or not phone:
            return JsonResponse({'success': False, 'message': 'نام و تلفن الزامی است'})

        # parse date if present
        parsed_date = None
        if preferred_date:
            try:
                parsed_date = datetime.strptime(preferred_date, '%Y-%m-%d').date()
            except Exception:
                parsed_date = None

        appt = AppointmentRequest.objects.create(
            name=name,
            phone=phone,
            email=email or None,
            preferred_date=parsed_date,
            car_model=car_model,
            service=service,
            message=message,
        )

        # notify admin by email (best-effort)
        try:
            send_mail(
                f'درخواست رزرو جدید از {name}',
                f'نام: {name}\nتلفن: {phone}\nایمیل: {email or "-"}\nتاریخ: {preferred_date or "-"}\nخودرو: {car_model or "-"}\nسرویس: {service or "-"}\n\nپیام:\n{message or "-"}',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=True,
            )
        except Exception:
            pass

        return JsonResponse({'success': True, 'message': 'درخواست شما ثبت شد'})
    except Exception:
        return JsonResponse({'success': False, 'message': 'خطا در ثبت درخواست'})


@csrf_exempt
def comment_form(request):
    """Handle comment form submission"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'درخواست نامعتبر'})
    
    # Honeypot check
    if request.POST.get('company'):
        return JsonResponse({'success': False, 'message': 'درخواست نامعتبر'})
    
    # Rate limiting
    client_ip = request.META.get('REMOTE_ADDR')
    cache_key = f'comment_rate_limit_{client_ip}'
    if cache.get(cache_key):
        return JsonResponse({'success': False, 'message': 'لطفاً کمی صبر کنید و دوباره تلاش کنید'})
    
    # Set rate limit (5 minutes)
    cache.set(cache_key, True, 300)
    
    try:
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        rating = int(request.POST.get('rating', 5))
        comment_text = request.POST.get('comment', '').strip()
        service_id = request.POST.get('service_id')
        lecture_id = request.POST.get('lecture_id')
        parent_id = request.POST.get('parent_id')
        
        if not all([name, email, comment_text]):
            return JsonResponse({'success': False, 'message': 'لطفاً تمام فیلدهای ضروری را پر کنید'})
        
        if rating < 1 or rating > 5:
            return JsonResponse({'success': False, 'message': 'امتیاز نامعتبر'})
        
        # Create comment
        comment = Comment.objects.create(
            name=name,
            email=email,
            phone=phone,
            rating=rating,
            comment=comment_text,
            service_id=service_id if service_id else None,
            lecture_id=lecture_id if lecture_id else None,
            parent_id=parent_id if parent_id else None,
        )
        
        # Send email notification to admin
        try:
            send_mail(
                'نظر جدید ثبت شد',
                f'نظر جدید از {name} ({email}) با امتیاز {rating} ستاره:\n\n{comment_text}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=True,
            )
        except:
            pass
        
        return JsonResponse({'success': True, 'message': 'نظر شما با موفقیت ثبت شد و پس از تایید نمایش داده خواهد شد'})
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': 'خطا در ثبت نظر. لطفاً دوباره تلاش کنید'})


