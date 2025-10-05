#!/bin/bash

# Shahin Auto Service Production Deployment Script
# This script deploys the Django application to production

set -e

echo "🚀 Starting Shahin Auto Service Production Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# .env usage removed; configure variables via docker-compose defaults or CI/CD secrets
print_status "Using docker-compose defaults and any CI/CD environment variables"

# Create SSL directory if it doesn't exist
mkdir -p ssl

# Check if SSL certificates exist
if [ ! -f ssl/cert.pem ] || [ ! -f ssl/key.pem ]; then
    print_warning "SSL certificates not found in ssl/ directory."
    print_warning "Please add your SSL certificates:"
    print_warning "  - ssl/cert.pem (SSL certificate)"
    print_warning "  - ssl/key.pem (SSL private key)"
    print_warning "Or the deployment will use HTTP only."
fi

# Stop existing containers
print_status "Stopping existing containers..."
docker-compose -f docker-compose.prod.yml down || true

# Remove old images to force rebuild
print_status "Removing old images..."
docker-compose -f docker-compose.prod.yml down --rmi all || true

# Build and start services
print_status "Building and starting services..."
docker-compose -f docker-compose.prod.yml up --build -d

# Wait for services to be healthy
print_status "Waiting for services to be healthy..."
sleep 30

# Check if services are running
print_status "Checking service status..."
docker-compose -f docker-compose.prod.yml ps

# Test database connection
print_status "Testing database connection..."
docker-compose -f docker-compose.prod.yml exec web python manage.py dbshell --command="SELECT 1;" || {
    print_error "Database connection failed!"
    exit 1
}

# Run migrations
print_status "Running database migrations..."
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Collect static files and upload to S3
print_status "Collecting static files and uploading to S3..."
docker-compose -f docker-compose.prod.yml exec web python manage.py collect_and_upload

# Migrate existing media files to S3
print_status "Migrating existing media files to S3..."
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate_media_files

# Create superuser if it doesn't exist
print_status "Creating superuser if needed..."
docker-compose -f docker-compose.prod.yml exec web python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@shahin.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

# Test the application
print_status "Testing application health..."
if curl -f http://localhost/health/ > /dev/null 2>&1; then
    print_success "Application is healthy and responding!"
else
    print_warning "Application health check failed. Check logs with: docker-compose -f docker-compose.prod.yml logs"
fi

# Display deployment information
print_success "🎉 Deployment completed successfully!"
echo ""
print_status "Application URLs:"
echo "  - Main site: http://localhost (or your domain)"
echo "  - Admin panel: http://localhost/admin/"
echo "  - Health check: http://localhost/health/"
echo ""
print_status "Default admin credentials:"
echo "  - Username: admin"
echo "  - Password: admin123"
echo ""
print_warning "IMPORTANT: Change the admin password after first login!"
echo ""
print_status "Useful commands:"
echo "  - View logs: docker-compose -f docker-compose.prod.yml logs -f"
echo "  - Stop services: docker-compose -f docker-compose.prod.yml down"
echo "  - Restart services: docker-compose -f docker-compose.prod.yml restart"
echo "  - Update application: ./deploy.sh"
echo ""

# Make the script executable
chmod +x deploy.sh
