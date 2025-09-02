from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import Lecture, Service, SiteSettings
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Create sample data for the Shahin Auto Service website'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Create superuser if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@shahin-auto.com',
                password='admin123'
            )
            self.stdout.write(
                self.style.SUCCESS('Superuser created: admin/admin123')
            )

        # Create site settings if not exists
        if not SiteSettings.objects.exists():
            SiteSettings.objects.create(
                site_name='شاهین',
                site_description='خدمات حرفه‌ای خودرو با کیفیت جهانی',
                phone='+98-21-12345678',
                email='info@shahin-auto.com',
                address='تهران، ایران',
                instagram_url='https://instagram.com/shahin_auto'
            )
            self.stdout.write(
                self.style.SUCCESS('Site settings created')
            )

        # Create sample lectures
        sample_lectures = [
            {
                'title': 'راهنمای کامل تعمیر موتور خودرو',
                'teaser': 'در این مقاله به بررسی کامل تعمیر موتور خودرو و نکات مهم آن می‌پردازیم.',
                'content': '''
                <h2>مقدمه</h2>
                <p>تعمیر موتور خودرو یکی از مهم‌ترین و پیچیده‌ترین کارهای مکانیکی است که نیاز به تخصص و تجربه دارد.</p>
                
                <h3>مراحل تعمیر موتور</h3>
                <ol>
                    <li>تشخیص مشکل</li>
                    <li>باز کردن موتور</li>
                    <li>تعمیر یا تعویض قطعات</li>
                    <li>مونتاژ مجدد</li>
                    <li>تست و تنظیم</li>
                </ol>
                
                <h3>نکات مهم</h3>
                <ul>
                    <li>استفاده از ابزار مناسب</li>
                    <li>رعایت ترتیب مونتاژ</li>
                    <li>استفاده از روغن مناسب</li>
                    <li>تست کامل بعد از تعمیر</li>
                </ul>
                
                <p>با رعایت این نکات می‌توانید تعمیر موتور را به درستی انجام دهید.</p>
                '''
            },
            {
                'title': 'نحوه تعویض روغن خودرو',
                'teaser': 'آموزش گام به گام تعویض روغن خودرو و انتخاب روغن مناسب.',
                'content': '''
                <h2>اهمیت تعویض روغن</h2>
                <p>تعویض منظم روغن خودرو برای سلامت موتور بسیار مهم است.</p>
                
                <h3>مراحل تعویض روغن</h3>
                <ol>
                    <li>گرم کردن موتور</li>
                    <li>خاموش کردن موتور</li>
                    <li>باز کردن پیچ تخلیه</li>
                    <li>تعویض فیلتر روغن</li>
                    <li>ریختن روغن جدید</li>
                </ol>
                
                <h3>نکات مهم</h3>
                <ul>
                    <li>استفاده از روغن مناسب</li>
                    <li>تعویض فیلتر</li>
                    <li>چک کردن سطح روغن</li>
                </ul>
                '''
            },
            {
                'title': 'تعمیر گیربکس اتوماتیک',
                'teaser': 'راهنمای کامل تعمیر و نگهداری گیربکس اتوماتیک خودرو.',
                'content': '''
                <h2>گیربکس اتوماتیک</h2>
                <p>گیربکس اتوماتیک یکی از پیچیده‌ترین قطعات خودرو است.</p>
                
                <h3>علائم خرابی</h3>
                <ul>
                    <li>تاخیر در تعویض دنده</li>
                    <li>لرزش در حین رانندگی</li>
                    <li>صداهای غیرعادی</li>
                </ul>
                
                <h3>تعمیر و نگهداری</h3>
                <p>تعمیر گیربکس اتوماتیک نیاز به تخصص خاص دارد.</p>
                '''
            }
        ]

        for lecture_data in sample_lectures:
            if not Lecture.objects.filter(title=lecture_data['title']).exists():
                Lecture.objects.create(
                    title=lecture_data['title'],
                    slug=slugify(lecture_data['title']),
                    teaser=lecture_data['teaser'],
                    content=lecture_data['content'],
                    is_published=True
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Lecture created: {lecture_data["title"]}')
                )

        # Create sample services
        sample_services = [
            {
                'name': 'سرویس روغن با شستشو رایگان موتور',
                'description': '''
                <h3>سرویس کامل روغن موتور</h3>
                <p>این سرویس شامل تعویض روغن موتور، تعویض فیلتر روغن و شستشوی رایگان موتور است.</p>
                
                <h4>خدمات شامل:</h4>
                <ul>
                    <li>تعویض روغن موتور</li>
                    <li>تعویض فیلتر روغن</li>
                    <li>شستشوی رایگان موتور</li>
                    <li>چک کردن سطح مایعات</li>
                    <li>گزارش وضعیت خودرو</li>
                </ul>
                
                <p>این سرویس برای تمامی خودروهای ایرانی و خارجی انجام می‌شود.</p>
                ''',
                'instagram_link': 'https://instagram.com/shahin_auto'
            },
            {
                'name': 'شستشو دریچه گاز و انژکتور',
                'description': '''
                <h3>شستشوی دریچه گاز و انژکتور</h3>
                <p>شستشوی دریچه گاز و انژکتور برای بهبود عملکرد موتور و کاهش مصرف سوخت.</p>
                
                <h4>مزایای این سرویس:</h4>
                <ul>
                    <li>بهبود عملکرد موتور</li>
                    <li>کاهش مصرف سوخت</li>
                    <li>کاهش آلایندگی</li>
                    <li>افزایش عمر موتور</li>
                </ul>
                ''',
                'instagram_link': 'https://instagram.com/shahin_auto'
            },
            {
                'name': 'تعمیر موتور تخصصی خودرو های هیوندای کیا',
                'description': '''
                <h3>تعمیر تخصصی موتور هیوندای و کیا</h3>
                <p>تخصص ما در تعمیر موتورهای هیوندای و کیا با استفاده از تجهیزات مدرن و قطعات اصل.</p>
                
                <h4>خدمات تخصصی:</h4>
                <ul>
                    <li>تعمیر موتورهای GDI</li>
                    <li>تعمیر سیستم توربو</li>
                    <li>تعمیر سیستم تزریق سوخت</li>
                    <li>استفاده از قطعات اصل</li>
                </ul>
                ''',
                'instagram_link': 'https://instagram.com/shahin_auto'
            },
            {
                'name': 'تعمیر گیربکس و تعویض دیسک و صفحه',
                'description': '''
                <h3>تعمیر گیربکس و کلاچ</h3>
                <p>تعمیر تخصصی گیربکس و تعویض دیسک و صفحه کلاچ با کیفیت بالا.</p>
                
                <h4>خدمات شامل:</h4>
                <ul>
                    <li>تعمیر گیربکس دستی</li>
                    <li>تعویض دیسک کلاچ</li>
                    <li>تعویض صفحه کلاچ</li>
                    <li>تنظیم کلاچ</li>
                </ul>
                ''',
                'instagram_link': 'https://instagram.com/shahin_auto'
            },
            {
                'name': 'تعویض روغن گیربکس اتومات با دستگاه تمام اتوماتیک',
                'description': '''
                <h3>تعویض روغن گیربکس اتوماتیک</h3>
                <p>تعویض روغن گیربکس اتوماتیک با استفاده از دستگاه تمام اتوماتیک.</p>
                
                <h4>مزایای دستگاه اتوماتیک:</h4>
                <ul>
                    <li>تعویض کامل روغن</li>
                    <li>شستشوی سیستم</li>
                    <li>دقت بالا</li>
                    <li>صرفه‌جویی در زمان</li>
                </ul>
                ''',
                'instagram_link': 'https://instagram.com/shahin_auto'
            },
            {
                'name': 'شستشو رادیاتور و مجاری آب خودرو با دستگاه تمام اتوماتیک',
                'description': '''
                <h3>شستشوی سیستم خنک‌کننده</h3>
                <p>شستشوی کامل رادیاتور و مجاری آب خودرو با دستگاه تمام اتوماتیک.</p>
                
                <h4>خدمات شامل:</h4>
                <ul>
                    <li>شستشوی رادیاتور</li>
                    <li>شستشوی مجاری آب</li>
                    <li>تعویض مایع خنک‌کننده</li>
                    <li>تست سیستم</li>
                </ul>
                ''',
                'instagram_link': 'https://instagram.com/shahin_auto'
            },
            {
                'name': 'تعویض فیلتر بنزین هیوندای کیا و خودرو های خارجی',
                'description': '''
                <h3>تعویض فیلتر بنزین</h3>
                <p>تعویض فیلتر بنزین برای خودروهای هیوندای، کیا و سایر خودروهای خارجی.</p>
                
                <h4>مزایای تعویض فیلتر:</h4>
                <ul>
                    <li>بهبود عملکرد موتور</li>
                    <li>کاهش مصرف سوخت</li>
                    <li>محافظت از انژکتور</li>
                    <li>افزایش عمر موتور</li>
                </ul>
                ''',
                'instagram_link': 'https://instagram.com/shahin_auto'
            },
            {
                'name': 'تعویض صافی گیربکس اتومات',
                'description': '''
                <h3>تعویض صافی گیربکس اتوماتیک</h3>
                <p>تعویض صافی گیربکس اتوماتیک برای بهبود عملکرد و افزایش عمر گیربکس.</p>
                
                <h4>نکات مهم:</h4>
                <ul>
                    <li>تعویض منظم صافی</li>
                    <li>استفاده از صافی اصل</li>
                    <li>چک کردن روغن گیربکس</li>
                </ul>
                ''',
                'instagram_link': 'https://instagram.com/shahin_auto'
            },
            {
                'name': 'خدمات مکانیکی انواع خودرو های ایرانی و خارجی',
                'description': '''
                <h3>خدمات مکانیکی جامع</h3>
                <p>ارائه خدمات مکانیکی برای تمامی خودروهای ایرانی و خارجی با کیفیت بالا.</p>
                
                <h4>خدمات شامل:</h4>
                <ul>
                    <li>تعمیر موتور</li>
                    <li>تعمیر گیربکس</li>
                    <li>تعمیر سیستم ترمز</li>
                    <li>تعمیر سیستم تعلیق</li>
                    <li>سرویس دوره‌ای</li>
                </ul>
                ''',
                'instagram_link': 'https://instagram.com/shahin_auto'
            }
        ]

        for service_data in sample_services:
            if not Service.objects.filter(name=service_data['name']).exists():
                Service.objects.create(
                    name=service_data['name'],
                    slug=slugify(service_data['name']),
                    description=service_data['description'],
                    instagram_link=service_data['instagram_link'],
                    is_published=True
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Service created: {service_data["name"]}')
                )

        self.stdout.write(
            self.style.SUCCESS('Sample data created successfully!')
        )
