# Quick Reference - New Project Structure

## 📂 Where to Find Things

| What You Need | Location |
|---------------|----------|
| **Documentation** | `docs/` folder |
| **Docker Setup** | `docker/compose/docker-compose.yml` |
| **Deploy Scripts** | `docker/scripts/unix/` or `docker/scripts/windows/` |
| **Config Files** | `config/` folder |
| **Test Scripts** | `scripts/` folder |
| **Backend Code** | `backend/` folder |
| **Frontend Code** | `src/` folder |

## 🚀 Common Commands

### Development
```bash
# Backend
cd backend && python manage.py runserver

# Frontend
npm run dev

# Full Docker Stack
docker-compose -f docker/compose/docker-compose.yml up
```

### Production Deployment

**Unix/Linux/Mac:**
```bash
./docker/scripts/unix/deploy.sh
./docker/scripts/unix/health-check.sh
./docker/scripts/unix/backup.sh
```

**Windows:**
```powershell
.\docker\scripts\windows\deploy.ps1
.\docker\scripts\windows\health-check.ps1
.\docker\scripts\windows\backup.ps1
```

### Testing
```bash
python scripts/run_tests.py
./scripts/quickstart_tests.sh      # Unix/Mac
.\scripts\quickstart_tests.bat     # Windows
```

## 📁 Key Directories

```
docker/
├── compose/         → Docker Compose files
├── configs/         → Nginx, database configs
├── dockerfiles/     → Dockerfile definitions
└── scripts/         → Deployment & utility scripts
    ├── unix/        → Linux/Mac bash scripts
    └── windows/     → Windows PowerShell scripts

config/              → vite.config.js, eslint.config.js, etc.
docs/                → All .md documentation files
scripts/             → Utility & test scripts
```

## 🔗 Important Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview (in root) |
| `PROJECT_REORGANIZATION.md` | This reorganization details |
| `docs/DOCKER_DEPLOYMENT_GUIDE.md` | Complete Docker guide |
| `docs/DOCKER_QUICK_START.md` | Quick Docker setup |
| `docs/PROJECT_DOCUMENTATION.md` | Full project docs |
| `config/vite.config.js` | Frontend build config |
| `docker/compose/docker-compose.yml` | Dev environment |
| `docker/compose/docker-compose.prod.yml` | Production environment |

## ⚡ Pro Tips

1. **Documentation?** → Check `docs/` folder
2. **Need to deploy?** → Use `docker/scripts/unix/deploy.sh` or `docker/scripts/windows/deploy.ps1`
3. **Config changes?** → Look in `config/` folder
4. **Run tests?** → Use scripts in `scripts/` folder
5. **Docker files?** → Everything in `docker/` with organized subfolders

---

**Print this and keep it handy! 📌**
