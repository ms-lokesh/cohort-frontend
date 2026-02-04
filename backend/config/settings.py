import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Security Settings
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-key-change-this')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# In development, allow all hosts to avoid DisallowedHost during local testing
if os.getenv('FORCE_ALLOW_ALL_HOSTS', None) == '1' or os.getenv('DJANGO_ALLOW_ALL_HOSTS', None) == '1' or (os.getenv('ENV', '').lower() != 'production' and os.getenv('DEBUG', 'True') == 'True'):
    ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'drf_yasg',
    
    # Local apps (5 main modules)
    'apps.clt',
    'apps.sri',
    'apps.cfc',
    'apps.iipc',
    'apps.scd',
    'apps.profiles',
    'apps.dashboard',
    'hackathons',
    
    # Gamification System
    'apps.gamification',
    
    # Analytics & Scaling (NEW - for 2000+ students)
    'apps.analytics_summary',
    
    # Supabase Authentication
    'apps.auth_supabase',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Static files
    'corsheaders.middleware.CorsMiddleware',  # CORS
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'apps.auth_supabase.middleware.SupabaseAuthMiddleware',  # Disabled - using Django JWT auth
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Security Settings for Production
if not DEBUG:
    # Railway handles SSL, so don't redirect (causes CORS preflight issues)
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database - PostgreSQL (production) or SQLite (development)
if os.getenv('DATABASE_URL'):
    # Production: Use PostgreSQL from DATABASE_URL (Render/Cloud provides this)
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
elif os.getenv('DB_ENGINE') == 'django.db.backends.postgresql':
    # Local PostgreSQL development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'cohort_db'),
            'USER': os.getenv('DB_USER', 'postgres'),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
            'CONN_MAX_AGE': 600,
        }
    }
else:
    # Development: Use SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Authentication Backends (allow login with email or username)
AUTHENTICATION_BACKENDS = [
    'apps.authentication.EmailOrUsernameBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = os.getenv('STATIC_URL', '/static/')
STATIC_ROOT = os.path.join(BASE_DIR, os.getenv('STATIC_ROOT', 'staticfiles'))
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (User uploads)
MEDIA_URL = os.getenv('MEDIA_URL', '/media/')
MEDIA_ROOT = os.path.join(BASE_DIR, os.getenv('MEDIA_ROOT', 'media'))

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS Settings
# Temporarily allow all origins for development
CORS_ALLOW_ALL_ORIGINS = True  # Allow all for development
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ['DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT']
CORS_ALLOW_HEADERS = ['accept', 'accept-encoding', 'authorization', 'content-type', 'dnt', 'origin', 'user-agent', 'x-csrftoken', 'x-requested-with']

# Django REST Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# JWT Settings (handled by auth team)
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(os.getenv('JWT_ACCESS_TOKEN_LIFETIME_MINUTES', 60))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=int(os.getenv('JWT_REFRESH_TOKEN_LIFETIME_DAYS', 7))),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': os.getenv('JWT_ALGORITHM', 'HS256'),
    'SIGNING_KEY': os.getenv('JWT_SECRET_KEY', SECRET_KEY),
}

# Swagger/OpenAPI Settings
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': False,
}

# File Upload Settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB

# ============================================================================
# SCALING FEATURE FLAGS (LOCAL SAFE, CLOUD READY)
# ============================================================================
# These flags enable performance optimizations without breaking existing code.
# All flags default to False/Local to keep development simple.

# Analytics Optimization
USE_ANALYTICS_SUMMARY = os.getenv('USE_ANALYTICS_SUMMARY', 'False') == 'True'
# When True: Uses pre-computed analytics summaries (fast, scales to 2000+ students)
# When False: Uses live aggregation (current behavior, development mode)

# Notification Optimization
USE_NOTIFICATION_CACHE = os.getenv('USE_NOTIFICATION_CACHE', 'False') == 'True'
# When True: Caches notification counts for 30 seconds
# When False: Always computes counts live (current behavior)

# File Storage
USE_CLOUD_STORAGE = os.getenv('USE_CLOUD_STORAGE', 'False') == 'True'
# When True: Uses AWS S3 or cloud storage (production)
# When False: Uses local filesystem (current behavior, development)

# Background Tasks
USE_ASYNC_TASKS = os.getenv('USE_ASYNC_TASKS', 'False') == 'True'
# When True: Uses Celery/Redis for background tasks (production)
# When False: Tasks run synchronously (current behavior, development)

# Database Query Logging (Debug only)
LOG_QUERY_TIMES = DEBUG and os.getenv('LOG_QUERY_TIMES', 'False') == 'True'
# When True: Logs slow queries to console (helpful for optimization)
# When False: No query logging (default)

# ============================================================================
# CACHING CONFIGURATION (LOCAL SAFE, REDIS READY)
# ============================================================================
if USE_NOTIFICATION_CACHE or USE_ANALYTICS_SUMMARY:
    # Use Redis if available in production, otherwise local memory cache
    REDIS_URL = os.getenv('REDIS_URL', None)
    if REDIS_URL and not DEBUG:
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.redis.RedisCache',
                'LOCATION': REDIS_URL,
                'OPTIONS': {
                    'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                },
                'KEY_PREFIX': 'cohort',
                'TIMEOUT': 300,  # 5 minutes default
            }
        }
    else:
        # Local development: Use in-memory cache (no Redis required)
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': 'cohort-cache',
                'TIMEOUT': 300,
            }
        }
else:
    # No caching (current behavior)
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

# ============================================================================
# AWS/CLOUD STORAGE CONFIGURATION (OPTIONAL)
# ============================================================================
if USE_CLOUD_STORAGE:
    # TODO: Add django-storages and boto3 to requirements.txt when needed
    # pip install django-storages boto3
    # 
    # INSTALLED_APPS += ['storages']
    # DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    # AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    # AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    # AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    # AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'us-east-1')
    # AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    # AWS_S3_FILE_OVERWRITE = False
    # AWS_DEFAULT_ACL = None
    # AWS_S3_OBJECT_PARAMETERS = {
    #     'CacheControl': 'max-age=86400',
    # }
    pass

# ============================================================================
# CELERY CONFIGURATION (PLACEHOLDER FOR FUTURE)
# ============================================================================
if USE_ASYNC_TASKS:
    # TODO: Add celery and redis to requirements.txt when needed
    # pip install celery redis
    #
    # CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    # CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    # CELERY_ACCEPT_CONTENT = ['json']
    # CELERY_TASK_SERIALIZER = 'json'
    # CELERY_RESULT_SERIALIZER = 'json'
    # CELERY_TIMEZONE = TIME_ZONE
    # CELERY_TASK_TRACK_STARTED = True
    # CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes
    pass
