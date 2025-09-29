#!/bin/bash

# Test sitemap functionality
echo "🧪 Testing Sitemap Functionality..."

# Test main sitemap index
echo "📋 Testing main sitemap index..."
curl -s -o /dev/null -w "%{http_code}" http://localhost/sitemap.xml

if [ $? -eq 0 ]; then
    echo "✅ Main sitemap is accessible"
else
    echo "❌ Main sitemap is not accessible"
fi

# Test individual sitemaps
echo "📋 Testing individual sitemaps..."

sitemaps=("static" "services" "lectures")

for sitemap in "${sitemaps[@]}"; do
    echo "Testing sitemap-$sitemap.xml..."
    status=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost/sitemap-$sitemap.xml")
    if [ "$status" = "200" ]; then
        echo "✅ sitemap-$sitemap.xml is accessible"
    else
        echo "❌ sitemap-$sitemap.xml returned status: $status"
    fi
done

echo ""
echo "🎉 Sitemap testing completed!"
echo "📋 Sitemap URLs:"
echo "  Main: https://shahinautoservice.ir/sitemap.xml"
echo "  Static: https://shahinautoservice.ir/sitemap-static.xml"
echo "  Services: https://shahinautoservice.ir/sitemap-services.xml"
echo "  Lectures: https://shahinautoservice.ir/sitemap-lectures.xml"
