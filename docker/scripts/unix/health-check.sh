#!/bin/bash
# ==============================================
# Health Check Script for Docker Services
# ==============================================
# Usage: ./health-check.sh

set -e

COMPOSE_FILE="docker/compose/docker-compose.prod.yml"

echo "🏥 Checking service health..."
echo ""

# Function to check HTTP endpoint
check_endpoint() {
    local name=$1
    local url=$2
    local expected=$3
    
    echo -n "  $name... "
    
    response=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null || echo "000")
    
    if [ "$response" = "$expected" ]; then
        echo "✅ OK (HTTP $response)"
        return 0
    else
        echo "❌ FAIL (HTTP $response, expected $expected)"
        return 1
    fi
}

# Check Docker services
echo "📦 Docker Services:"
docker-compose -f "$COMPOSE_FILE" ps

echo ""
echo "🔍 Service Health Checks:"

# Check database
echo -n "  Database... "
if docker-compose -f "$COMPOSE_FILE" exec -T db pg_isready -U cohort_user -d cohort_db > /dev/null 2>&1; then
    echo "✅ OK"
    DB_OK=1
else
    echo "❌ FAIL"
    DB_OK=0
fi

# Check Redis
echo -n "  Redis... "
if docker-compose -f "$COMPOSE_FILE" exec -T redis redis-cli ping > /dev/null 2>&1; then
    echo "✅ OK"
    REDIS_OK=1
else
    echo "❌ FAIL"
    REDIS_OK=0
fi

# Check backend API
check_endpoint "Backend API" "http://localhost:8000/api/health/" "200"
BACKEND_OK=$?

# Check frontend
check_endpoint "Frontend" "http://localhost/health" "200"
FRONTEND_OK=$?

echo ""
echo "📊 Resource Usage:"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"

echo ""
echo "💾 Volume Usage:"
docker volume ls --format "table {{.Name}}\t{{.Driver}}\t{{.Mountpoint}}" | grep cohort

echo ""
echo "📋 Summary:"
TOTAL_CHECKS=4
PASSED_CHECKS=$((DB_OK + REDIS_OK + BACKEND_OK + FRONTEND_OK))

if [ $PASSED_CHECKS -eq $TOTAL_CHECKS ]; then
    echo "✅ All checks passed ($PASSED_CHECKS/$TOTAL_CHECKS)"
    exit 0
else
    echo "⚠️  Some checks failed ($PASSED_CHECKS/$TOTAL_CHECKS)"
    echo ""
    echo "💡 Troubleshooting:"
    echo "   - View logs: docker-compose -f $COMPOSE_FILE logs -f"
    echo "   - Restart services: docker-compose -f $COMPOSE_FILE restart"
    echo "   - Check environment: docker-compose -f $COMPOSE_FILE config"
    exit 1
fi
