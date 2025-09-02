#!/bin/bash

echo "🔍 Shahin Auto Service - Troubleshooting Script"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    if [ $2 -eq 0 ]; then
        echo -e "${GREEN}✅ $1${NC}"
    else
        echo -e "${RED}❌ $1${NC}"
    fi
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

echo ""
print_info "Checking Docker services status..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_warning "Docker is not running. Please start Docker first."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    print_warning "docker-compose not found. Please install docker-compose."
    exit 1
fi

echo ""
print_info "Checking container status..."

# Check container status
docker-compose ps

echo ""
print_info "Checking container logs..."

# Check web container logs
echo "📋 Web container logs (last 20 lines):"
docker-compose logs --tail=20 web

echo ""
echo "📋 Nginx container logs (last 20 lines):"
docker-compose logs --tail=20 nginx

echo ""
echo "📋 Database container logs (last 20 lines):"
docker-compose logs --tail=20 db

echo ""
print_info "Testing connectivity..."

# Test if web container is responding
if docker-compose exec -T web curl -f http://localhost:8000/health/ > /dev/null 2>&1; then
    print_status "Web container health check" 0
else
    print_status "Web container health check" 1
    print_warning "Web container is not responding to health checks"
fi

# Test if nginx can reach web container
if docker-compose exec -T nginx wget --quiet --tries=1 --spider http://web:8000/health/ > /dev/null 2>&1; then
    print_status "Nginx to web container connectivity" 0
else
    print_status "Nginx to web container connectivity" 1
    print_warning "Nginx cannot reach web container"
fi

# Test database connection
if docker-compose exec -T web python manage.py dbshell --command="SELECT 1;" > /dev/null 2>&1; then
    print_status "Database connection" 0
else
    print_status "Database connection" 1
    print_warning "Cannot connect to database"
fi

echo ""
print_info "Checking resource usage..."
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"

echo ""
print_info "Checking disk space..."
df -h

echo ""
print_info "Checking network connectivity..."
# Test if port 80 is accessible
if curl -f http://localhost/health/ > /dev/null 2>&1; then
    print_status "Port 80 accessibility" 0
else
    print_status "Port 80 accessibility" 1
    print_warning "Port 80 is not accessible"
fi

echo ""
print_info "Common fixes to try:"
echo "1. Restart all services: docker-compose restart"
echo "2. Rebuild containers: docker-compose up -d --build"
echo "3. Check logs: docker-compose logs -f"
echo "4. Verify environment variables in docker-compose.yml"
echo "5. Ensure database is properly initialized"
echo "6. Check if all required files are present"

echo ""
print_info "If the issue persists, try these commands:"
echo "docker-compose down"
echo "docker-compose up -d --build"
echo "docker-compose exec web python manage.py migrate"
echo "docker-compose exec web python manage.py collectstatic --noinput"
