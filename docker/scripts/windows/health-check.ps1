# ==============================================
# Health Check Script for Docker Services (Windows)
# ==============================================
# Usage: .\health-check.ps1

$COMPOSE_FILE = "docker\compose\docker-compose.prod.yml"

Write-Host "🏥 Checking service health..." -ForegroundColor Cyan
Write-Host ""

# Function to check HTTP endpoint
function Test-Endpoint {
    param(
        [string]$Name,
        [string]$Url,
        [int]$Expected
    )
    
    Write-Host "  $Name... " -NoNewline
    
    try {
        $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 5
        $statusCode = $response.StatusCode
    } catch {
        $statusCode = 0
    }
    
    if ($statusCode -eq $Expected) {
        Write-Host "✅ OK (HTTP $statusCode)" -ForegroundColor Green
        return $true
    } else {
        Write-Host "❌ FAIL (HTTP $statusCode, expected $Expected)" -ForegroundColor Red
        return $false
    }
}

# Check Docker services
Write-Host "📦 Docker Services:" -ForegroundColor Yellow
docker-compose -f $COMPOSE_FILE ps

Write-Host ""
Write-Host "🔍 Service Health Checks:" -ForegroundColor Yellow

# Check database
Write-Host "  Database... " -NoNewline
$dbCheck = docker-compose -f $COMPOSE_FILE exec -T db pg_isready -U cohort_user -d cohort_db 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ OK" -ForegroundColor Green
    $DB_OK = 1
} else {
    Write-Host "❌ FAIL" -ForegroundColor Red
    $DB_OK = 0
}

# Check Redis
Write-Host "  Redis... " -NoNewline
$redisCheck = docker-compose -f $COMPOSE_FILE exec -T redis redis-cli ping 2>$null
if ($redisCheck -match "PONG") {
    Write-Host "✅ OK" -ForegroundColor Green
    $REDIS_OK = 1
} else {
    Write-Host "❌ FAIL" -ForegroundColor Red
    $REDIS_OK = 0
}

# Check backend API
$BACKEND_OK = if (Test-Endpoint "Backend API" "http://localhost:8000/api/health/" 200) { 1 } else { 0 }

# Check frontend
$FRONTEND_OK = if (Test-Endpoint "Frontend" "http://localhost/health" 200) { 1 } else { 0 }

Write-Host ""
Write-Host "📊 Resource Usage:" -ForegroundColor Yellow
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"

Write-Host ""
Write-Host "💾 Volume Usage:" -ForegroundColor Yellow
docker volume ls --filter "name=cohort" --format "table {{.Name}}\t{{.Driver}}"

Write-Host ""
Write-Host "📋 Summary:" -ForegroundColor Cyan
$TOTAL_CHECKS = 4
$PASSED_CHECKS = $DB_OK + $REDIS_OK + $BACKEND_OK + $FRONTEND_OK

if ($PASSED_CHECKS -eq $TOTAL_CHECKS) {
    Write-Host "✅ All checks passed ($PASSED_CHECKS/$TOTAL_CHECKS)" -ForegroundColor Green
    exit 0
} else {
    Write-Host "⚠️  Some checks failed ($PASSED_CHECKS/$TOTAL_CHECKS)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "💡 Troubleshooting:" -ForegroundColor Cyan
    Write-Host "   - View logs: docker-compose -f $COMPOSE_FILE logs -f" -ForegroundColor White
    Write-Host "   - Restart services: docker-compose -f $COMPOSE_FILE restart" -ForegroundColor White
    Write-Host "   - Check environment: docker-compose -f $COMPOSE_FILE config" -ForegroundColor White
    exit 1
}
