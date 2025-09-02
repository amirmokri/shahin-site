# شاهین - وب‌سایت خدمات خودرو

یک وب‌سایت کامل و حرفه‌ای برای ارائه خدمات خودرو با استفاده از Django، Django Rest Framework، MySQL و طراحی ریسپانسیو.

## ویژگی‌ها

### 🎨 طراحی و رابط کاربری
- **طراحی ریسپانسیو**: بهینه‌سازی شده برای موبایل، تبلت و دسکتاپ
- **رنگ‌بندی حرفه‌ای**: ترکیب زرد، آبی و سفید
- **انیمیشن‌های زیبا**: استفاده از AOS و CSS animations
- **حالت تاریک**: قابلیت تغییر تم
- **فونت فارسی**: استفاده از فونت Vazir

### 🏗️ معماری و فناوری
- **Backend**: Django 4.2.7 + Django Rest Framework
- **Database**: MySQL 8.0
- **Frontend**: Django Templates + Tailwind CSS
- **API**: RESTful API با DRF
- **Deployment**: Docker + Nginx

### 📱 صفحات و عملکردها
- **صفحه اصلی**: Hero section، سرویس‌ها، مقالات اخیر
- **مقالات**: لیست مقالات با pagination
- **جزئیات مقاله**: محتوای کامل با قابلیت اشتراک‌گذاری
- **سرویس‌ها**: نمایش سرویس‌ها با ویدیو و توضیحات
- **پنل مدیریت**: مدیریت محتوا و پیام‌ها

### 🔧 ویژگی‌های فنی
- **SEO**: Meta tags، sitemap، structured data
- **امنیت**: CSRF protection، rate limiting، input validation
- **عملکرد**: Lazy loading، caching، image optimization
- **دسترسی**: RTL support، keyboard navigation، screen reader friendly

## نصب و راه‌اندازی

### پیش‌نیازها
- Python 3.11+
- MySQL 8.0+
- Node.js (برای Tailwind CSS)
- Docker (اختیاری)

### نصب در Windows

#### 1. کلون کردن پروژه
```bash
git clone <repository-url>
cd shahin-auto
```

#### 2. ایجاد محیط مجازی
```bash
python -m venv venv
venv\Scripts\activate
```

#### 3. نصب وابستگی‌ها
```bash
pip install -r requirements.txt
```

#### 4. تنظیم پایگاه داده MySQL
```sql
CREATE DATABASE shahin_auto_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'shahin_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON shahin_auto_db.* TO 'shahin_user'@'localhost';
FLUSH PRIVILEGES;
```

#### 5. تنظیم متغیرهای محیطی
فایل `.env` ایجاد کنید:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=mysql://shahin_user:your_password@localhost:3306/shahin_auto_db
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

#### 6. اجرای migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 7. ایجاد superuser
```bash
python manage.py createsuperuser
```

#### 8. ایجاد داده‌های نمونه
```bash
python manage.py create_sample_data
```

#### 9. جمع‌آوری فایل‌های استاتیک
```bash
python manage.py collectstatic
```

#### 10. اجرای سرور
```bash
python manage.py runserver
```

## استفاده از Docker

### اجرای با Docker Compose
```bash
# ساخت و اجرای کانتینرها
docker-compose up --build

# اجرای در پس‌زمینه
docker-compose up -d

# مشاهده لاگ‌ها
docker-compose logs -f

# توقف سرویس‌ها
docker-compose down
```

### دسترسی‌ها
- **وب‌سایت**: http://localhost:8000
- **پنل مدیریت**: http://localhost:8000/admin
- **API**: http://localhost:8000/api/

## ساختار پروژه

```
shahin-auto/
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── nginx.conf
├── shahin_auto/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── main/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── api_views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── api_urls.py
│   ├── admin.py
│   ├── sitemaps.py
│   └── management/
│       └── commands/
│           └── create_sample_data.py
├── templates/
│   ├── base.html
│   └── main/
│       ├── home.html
│       ├── lectures.html
│       ├── lecture_detail.html
│       ├── service_detail.html
│       └── admin_dashboard.html
├── static/
│   ├── css/
│   │   └── custom.css
│   ├── js/
│   │   └── main.js
│   └── images/
│       ├── logo.png
│       └── favicon.ico
└── media/
    ├── lectures/
    ├── services/
    └── site/
```

## مدل‌های پایگاه داده

### Lecture (مقاله)
- `title`: عنوان مقاله
- `slug`: URL slug
- `image`: تصویر مقاله
- `content`: محتوای کامل
- `teaser`: متن کوتاه
- `created_at`: تاریخ ایجاد
- `is_published`: وضعیت انتشار

### Service (سرویس)
- `name`: نام سرویس
- `slug`: URL slug
- `image`: تصویر سرویس
- `description`: توضیحات
- `video_url`: لینک ویدیو
- `instagram_link`: لینک اینستاگرام
- `created_at`: تاریخ ایجاد
- `is_published`: وضعیت انتشار

### ContactMessage (پیام تماس)
- `name`: نام فرستنده
- `email`: ایمیل
- `message`: متن پیام
- `created_at`: تاریخ ارسال
- `is_read`: وضعیت خوانده شدن

### SiteSettings (تنظیمات سایت)
- `site_name`: نام سایت
- `site_description`: توضیحات سایت
- `phone`: شماره تلفن
- `email`: ایمیل
- `address`: آدرس
- `instagram_url`: لینک اینستاگرام
- `hero_image`: تصویر اصلی
- `hero_video_url`: لینک ویدیو تبلیغاتی

## API Endpoints

### Lectures
- `GET /api/lectures/` - لیست مقالات
- `GET /api/lectures/{slug}/` - جزئیات مقاله
- `GET /api/lectures/recent/` - مقالات اخیر
- `POST /api/lectures/` - ایجاد مقاله (نیاز به احراز هویت)
- `PUT /api/lectures/{slug}/` - ویرایش مقاله (نیاز به احراز هویت)
- `DELETE /api/lectures/{slug}/` - حذف مقاله (نیاز به احراز هویت)

### Services
- `GET /api/services/` - لیست سرویس‌ها
- `GET /api/services/{slug}/` - جزئیات سرویس
- `GET /api/services/all/` - همه سرویس‌ها
- `POST /api/services/` - ایجاد سرویس (نیاز به احراز هویت)
- `PUT /api/services/{slug}/` - ویرایش سرویس (نیاز به احراز هویت)
- `DELETE /api/services/{slug}/` - حذف سرویس (نیاز به احراز هویت)

### Other
- `GET /api/settings/` - تنظیمات سایت
- `POST /api/contact/` - ارسال پیام تماس

## پنل مدیریت

### دسترسی
- URL: `/admin/`
- کاربر پیش‌فرض: `admin`
- رمز عبور: `admin123` (در محیط توسعه)

### قابلیت‌ها
- مدیریت مقالات و سرویس‌ها
- مدیریت پیام‌های تماس
- تنظیمات سایت
- آپلود تصاویر و فایل‌ها
- پیش‌نمایش محتوا

## امنیت

### ویژگی‌های امنیتی
- CSRF Protection
- XSS Protection
- SQL Injection Prevention
- Rate Limiting
- Secure Headers
- Input Validation
- File Upload Security

### تنظیمات امنیتی
```python
# در settings.py
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SESSION_COOKIE_AGE = 3600
```

## SEO

### بهینه‌سازی موتورهای جستجو
- Meta tags کامل
- Open Graph tags
- Twitter Card tags
- Sitemap.xml
- Robots.txt
- Structured data
- Alt text برای تصاویر
- URL های SEO-friendly

## عملکرد

### بهینه‌سازی‌ها
- Lazy loading تصاویر
- Minification CSS/JS
- Browser caching
- Database indexing
- Query optimization
- Static file compression

## استقرار (Deployment)

### با Docker
```bash
# ساخت image
docker build -t shahin-auto .

# اجرای container
docker run -p 8000:8000 shahin-auto
```

### با Docker Compose
```bash
# اجرای کامل stack
docker-compose up -d
```

### تنظیمات Production
1. تغییر `DEBUG = False`
2. تنظیم `ALLOWED_HOSTS`
3. استفاده از HTTPS
4. تنظیم متغیرهای محیطی
5. پیکربندی Nginx
6. تنظیم SSL certificate

## نگهداری

### Backup پایگاه داده
```bash
mysqldump -u shahin_user -p shahin_auto_db > backup.sql
```

### Restore پایگاه داده
```bash
mysql -u shahin_user -p shahin_auto_db < backup.sql
```

### Log ها
- Django logs: `/var/log/django/`
- Nginx logs: `/var/log/nginx/`
- Application logs: در console

## عیب‌یابی

### مشکلات رایج
1. **خطای اتصال به پایگاه داده**: بررسی تنظیمات MySQL
2. **خطای static files**: اجرای `collectstatic`
3. **خطای permissions**: بررسی دسترسی‌های فایل‌ها
4. **خطای email**: بررسی تنظیمات SMTP

### دستورات مفید
```bash
# بررسی وضعیت Django
python manage.py check

# بررسی migrations
python manage.py showmigrations

# پاک کردن cache
python manage.py clear_cache

# بررسی static files
python manage.py findstatic
```

## مشارکت

### راهنمای مشارکت
1. Fork کردن پروژه
2. ایجاد branch جدید
3. اعمال تغییرات
4. تست کردن
5. ارسال Pull Request

### استانداردهای کد
- استفاده از PEP 8
- کامنت‌گذاری مناسب
- نام‌گذاری واضح
- تست‌نویسی

## لایسنس

این پروژه تحت لایسنس MIT منتشر شده است.

## پشتیبانی

برای پشتیبانی و سوالات:
- ایمیل: info@shahin-auto.com
- تلفن: +98-21-12345678
- اینستاگرام: @shahin_auto

---

**توسعه‌دهنده**: تیم توسعه شاهین  
**نسخه**: 1.0.0  
**تاریخ**: 2024
