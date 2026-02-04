# Docker Image Size Report

## Image Size Estimates

Based on the Dockerfile configurations and typical image sizes:

### Backend Image (Django + Gunicorn)
- **Base Image:** `python:3.11-slim` (~150 MB)
- **Python Dependencies:** ~200-300 MB
  - Django, DRF, psycopg, Pillow, etc.
- **Application Code:** ~50-100 MB
- **Total Estimated Size:** **~400-550 MB**

### Frontend Image (React + Nginx)
- **Build Stage:** `node:20-alpine` (used only for building, not in final image)
- **Final Image Base:** `nginx:1.25-alpine` (~40 MB)
- **Built React App:** ~5-15 MB (after Vite optimization)
- **Nginx Config:** <1 MB
- **Total Estimated Size:** **~50-60 MB**

### Database Image (PostgreSQL)
- **Image:** `postgres:16-alpine`
- **Total Size:** **~230 MB**

### Cache Image (Redis)
- **Image:** `redis:7-alpine`
- **Total Size:** **~30 MB**

## Total Stack Size

| Component | Size |
|-----------|------|
| Backend (Django) | ~400-550 MB |
| Frontend (React) | ~50-60 MB |
| PostgreSQL | ~230 MB |
| Redis | ~30 MB |
| **Total** | **~710-870 MB** |

## Actual Size Verification Script

To get actual sizes after building, run:

### Windows PowerShell
```powershell
# Build images
docker compose -f docker/compose/docker-compose.prod.yml build

# Check sizes
docker images | Select-String "cohort"

# Detailed size info
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | Select-String "cohort"
```

### Linux/Mac
```bash
# Build images
docker compose -f docker/compose/docker-compose.prod.yml build

# Check sizes
docker images | grep cohort

# Detailed size info
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | grep cohort
```

## Size Optimization Notes

### Current Optimizations
✅ Multi-stage builds (frontend only uses final nginx image)
✅ Alpine Linux base images where possible
✅ `python:3.11-slim` instead of full Python image (saves ~700 MB)
✅ `.dockerignore` files to exclude unnecessary files
✅ Single RUN commands to reduce layers
✅ Vite build optimization for frontend

### If Size Reduction Needed

**Backend (~400-550 MB):**
- Switch to `python:3.11-alpine` → Save ~100 MB (requires build-deps)
- Remove unused dependencies → Save ~50-100 MB
- Use slim variants of packages where available

**Frontend (~50-60 MB):**
- Already minimal with nginx:alpine
- Could reduce to ~40 MB with aggressive optimization
- Compress static assets further

**Overall Stack:**
- Consider distroless images → Save ~50-100 MB total
- Use nginx as reverse proxy only → Remove duplicate nginx instances
- Share base images across services

## Size Comparison

### Current Setup (Production-Ready)
- **Focus:** Functionality, compatibility, ease of maintenance
- **Size:** ~710-870 MB total
- **Build Time:** ~5-10 minutes (first build)
- **Benefits:** Well-tested, compatible, easy to debug

### Ultra-Minimal Setup (Size-Optimized)
- **Backend:** python:3.11-alpine → ~300 MB
- **Frontend:** nginx:alpine → ~40 MB
- **Total:** ~570 MB
- **Trade-offs:** Longer build time, potential compatibility issues

## Recommendations for DevOps Team

### For Production Deployment:
1. **Use current setup** (~710-870 MB)
   - Well-tested and production-ready
   - Good balance of size vs functionality
   - Easy to maintain and debug

2. **Registry Caching:**
   - Base images are shared across builds
   - Only application layers need updating (~50-100 MB typically)

3. **Build Optimization:**
   - Use Docker BuildKit for faster builds
   - Enable layer caching in CI/CD
   - Pull base images before building

4. **Runtime Considerations:**
   - Images are pulled once, then cached on host
   - Actual running container memory: 512 MB - 2 GB depending on load
   - Most space is one-time download

### CI/CD Optimization:
```yaml
# Example GitHub Actions optimization
- name: Build with cache
  uses: docker/build-push-action@v4
  with:
    context: .
    file: docker/dockerfiles/backend.Dockerfile
    cache-from: type=registry,ref=myregistry/cohort-backend:latest
    cache-to: type=inline
```

## Size Breakdown by Service

### Development vs Production

**Development Images:**
- Include dev dependencies
- No optimization
- ~20-30% larger

**Production Images:**
- Optimized builds
- No dev dependencies
- Compressed layers

## Network Transfer Considerations

### First Deploy:
- Full download: ~710-870 MB
- Time on 100 Mbps: ~1-2 minutes

### Updates (typical):
- Only changed layers: ~50-150 MB
- Time on 100 Mbps: ~10-20 seconds

### Using Registry:
- Docker Hub, ECR, GCR support layer caching
- Subsequent pulls only download deltas
- Typical update: 10-100 MB

---

## How to Generate This Report

Once Docker is installed, run:

```powershell
# PowerShell script
$report = @()
docker compose -f docker/compose/docker-compose.prod.yml build
docker images --format "{{.Repository}},{{.Tag}},{{.Size}}" | Select-String "cohort" | ForEach-Object {
    $parts = $_ -split ","
    $report += [PSCustomObject]@{
        Image = $parts[0] + ":" + $parts[1]
        Size = $parts[2]
    }
}
$report | Format-Table -AutoSize
```

---

**Created:** January 29, 2026  
**Status:** Estimates based on Dockerfile analysis  
**Note:** Install Docker to get actual sizes
