# Get Docker Image Sizes
# Run this script after Docker build completes

$ErrorActionPreference = "Stop"

# Add Docker to PATH for this session
$env:Path += ";C:\Program Files\Docker\Docker\resources\bin"

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Docker Image Size Report" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Check if images exist
$images = docker images --format "{{.Repository}}:{{.Tag}}" | Select-String "cohort"

if ($images) {
    Write-Host "📦 Cohort Project Images:" -ForegroundColor Green
    Write-Host ""
    
    docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedSince}}" | Select-String -Pattern "cohort|REPOSITORY"
    
    Write-Host ""
    Write-Host "📊 Total Size Calculation:" -ForegroundColor Yellow
    
    $totalSize = 0
    $imageList = docker images --format "{{.Repository}}:{{.Tag}},{{.Size}}" | Select-String "cohort"
    
    foreach ($img in $imageList) {
        $parts = $img.ToString().Split(',')
        $imageName = $parts[0]
        $sizeStr = $parts[1]
        
        Write-Host "   $imageName : $sizeStr"
    }
    
    Write-Host ""
    Write-Host "📌 Base Images Used:" -ForegroundColor Cyan
    docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | Select-String -Pattern "python:3.11-slim|nginx:1.25-alpine|node:20-alpine|postgres:16-alpine|redis:7-alpine"
    
} else {
    Write-Host "⚠️  No cohort images found." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To build images, run:" -ForegroundColor Cyan
    Write-Host "   docker compose -f docker/compose/docker-compose.prod.yml build" -ForegroundColor White
    Write-Host ""
    Write-Host "Or for just backend and frontend:" -ForegroundColor Cyan
    Write-Host "   docker compose -f docker/compose/docker-compose.prod.yml build backend frontend" -ForegroundColor White
}

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
