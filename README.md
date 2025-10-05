# 🚗 Shahin Auto Service

A world-class, full-stack Django website for an auto service business with beautiful Persian design, professional animations, and comprehensive admin management.

## ✨ Features

### 🎨 Design & User Experience
- **World-class appearance** with yellow, blue, and white color palette
- **Fully responsive** design optimized for mobile devices
- **Beautiful animations** and hover effects using AOS library
- **Persian language** support throughout the site
- **Professional typography** with Vazirmatn font
- **Glassmorphism effects** and gradient backgrounds

### 📱 Pages & Functionality
- **Home Page**: Hero section with parallax, advertising video, services grid, recent lectures
- **Lectures Page**: Paginated grid of all lectures with beautiful cards
- **Service Detail Pages**: Detailed service information with professional video player
- **Admin Dashboard**: Comprehensive content management system
- **Bonus Popup**: Session-based promotional popup on homepage

### 🛠️ Technical Features
- **Django 4.2.7** with Django Rest Framework
- **MySQL database** with optimized models
- **File upload system** for images and videos
- **Professional video player** for service videos
- **Contact form** with email notifications
- **SEO optimized** with meta tags and sitemap
- **Security features** including CSRF protection
- **Performance optimized** with caching and static file optimization

### 🎯 Services Included
- سرویس روغن با شستشو رایگان موتور
- شستشو دریچه گاز و انژکتور
- تعمیر موتور تخصصی خودرو های هیونداو کیا
- تعمیر گیربکس و تعویض دیسک و صحفه
- تعویض روغن گیربکس اتومات با دستگاه تمام اتوماتیک
- شستشو رادیاتور و مجاری آب خودرو با دستگاه تمام اتوماتیک
- تعویض فیلتر بنزین هیوندا کیا و خودرو های خارجی
- تعویض صافی گیربکس اتومات
- خدمات مکانیکی انواع خودرو های ایرانی و خارجی

## 🏗️ Project Structure

```
shahin/
├── 📁 shahin_auto/           # Django project settings
│   ├── settings.py           # Development settings
│   ├── settings_production.py # Production settings
│   └── urls.py
├── 📁 main/                  # Main Django app
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── admin.py             # Admin configuration
│   ├── serializers.py       # DRF serializers
│   └── api_views.py         # API endpoints
├── 📁 templates/             # HTML templates
│   ├── base.html            # Base template
│   └── main/                # App templates
├── 📁 static/               # Static files
│   ├── css/custom.css       # Custom styles
│   ├── js/main.js          # JavaScript
│   └── images/             # Images and icons
├── 📁 media/                # User uploaded files
├── 🐳 Dockerfile            # Docker configuration
├── 🐳 docker-compose.yml    # Multi-container setup
├── 🌐 nginx.conf            # Nginx configuration
└── 📋 requirements.txt      # Python dependencies
```

## 🚀 Quick Start

### Development Setup

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd shahin
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure database:**
   - Update `shahin_auto/settings.py` with your MySQL credentials
   - Create database: `shahin_db`

5. **Run migrations:**
```bash
python manage.py migrate
```

6. **Create superuser:**
```bash
python manage.py createsuperuser
```

7. **Collect static files:**
```bash
python manage.py collectstatic
```

8. **Run development server:**
```bash
python manage.py runserver
```

9. **Access the application:**
   - Website: http://localhost:8000
   - Admin: http://localhost:8000/admin

### Media Files Setup

Upload your media files to the appropriate directories:

```
media/
├── site/
│   └── hero.jpg              # Hero background image
├── services/
│   ├── images/               # Service images
│   └── videos/               # Service videos (.mp4)
├── lectures/
│   └── images/               # Lecture images
└── bonuses/
    └── images/               # Bonus popup images
```

**Static files:**
- `static/images/logo.png` - Your logo (circular display)
- `static/css/custom.css` - Custom styles
- `static/js/main.js` - JavaScript functionality

## 🐳 Docker Deployment

### Quick Docker Setup

1. **Build and start services:**
```bash
docker-compose up -d --build
```

2. **Create superuser:**
```bash
docker-compose exec web python manage.py createsuperuser
```

3. **Access the application:**
   - Website: http://localhost
   - Admin: http://localhost/admin

### Production Deployment

For production deployment, see the comprehensive [DEPLOYMENT.md](DEPLOYMENT.md) guide which includes:

- Environment configuration
- SSL/HTTPS setup
- Security hardening
- Performance optimization
- Monitoring and logging
- Backup strategies
- Scaling options

## 🎨 Customization

### Colors
The site uses a custom color palette defined in `static/css/custom.css`:
- **Shahin Yellow**: #FFD700
- **Shahin Blue**: #1E40AF
- **Shahin Light Blue**: #3B82F6
- **Shahin Dark Blue**: #1E3A8A
- **Shahin Gold**: #FFA500

### Fonts
- **Primary Font**: Vazirmatn (Persian)
- **Fallback**: Tahoma, Arial, sans-serif

### Animations
- **AOS (Animate On Scroll)** for scroll animations
- **Custom CSS animations** for hover effects
- **Tailwind CSS** for utility classes

## 📊 Admin Features

The admin dashboard provides:

- **Content Management**: Add/edit lectures and services
- **Media Management**: Upload images and videos
- **Bonus Management**: Configure promotional popups
- **Contact Management**: View and respond to messages
- **Site Settings**: Configure site information
- **Statistics**: View content and message counts

## 🔧 API Endpoints

The site includes a REST API for content management:

- `GET /api/lectures/` - List all lectures
- `GET /api/lectures/{id}/` - Get specific lecture
- `GET /api/services/` - List all services
- `GET /api/services/{id}/` - Get specific service
- `POST /api/contact/` - Submit contact form

## 🛡️ Security Features

- **CSRF Protection** enabled
- **XSS Protection** headers
- **Content Security Policy** configured
- **Rate limiting** on API endpoints
- **Secure session management**
- **Input validation** and sanitization

## 📱 Mobile Optimization

- **Mobile-first design** approach
- **Touch-friendly navigation**
- **Optimized images** with lazy loading
- **Responsive video players**
- **Fast loading** with compressed assets

## 🚀 Performance

- **Static file optimization** with WhiteNoise
- **Database query optimization**
- **Image compression** and lazy loading
- **CSS/JS minification** in production
- **Caching** with Redis
- **CDN ready** configuration

## 📞 Support

For technical support or questions:

1. Check the [DEPLOYMENT.md](DEPLOYMENT.md) guide
2. Review the logs: `docker-compose logs -f`
3. Verify environment variables
4. Ensure all services are running: `docker-compose ps`

## 📄 License

This project is proprietary software for Shahin Auto Service.

## 🎯 Performance Metrics

Expected performance on a 2GB RAM server:
- **Page load time**: < 2 seconds
- **Database queries**: < 100ms
- **Static file serving**: < 50ms
- **Concurrent users**: 100+

---

**Built with ❤️ for Shahin Auto Service**

*Professional auto service management with world-class design and functionality.*