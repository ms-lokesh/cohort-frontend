"""
Test and Setup Configuration
==============================
Centralized configuration for test users and setup scripts.
This file contains default passwords and settings for development/testing only.

SECURITY WARNING: These values should NEVER be used in production!
Use environment variables for production credentials.
"""

import os

# ==============================================
# Test User Passwords (Development Only)
# ==============================================

DEFAULT_PASSWORDS = {
    'admin': os.getenv('TEST_ADMIN_PASSWORD', 'admin123'),
    'mentor': os.getenv('TEST_MENTOR_PASSWORD', 'mentor123'),
    'student': os.getenv('TEST_STUDENT_PASSWORD', 'pass123#'),
    'floorwing': os.getenv('TEST_FLOORWING_PASSWORD', 'floorwing123'),
    'testuser': os.getenv('TEST_USER_PASSWORD', 'testpass123'),
    'default': os.getenv('TEST_DEFAULT_PASSWORD', 'test123'),
}

# ==============================================
# Database Configuration (Development/Testing)
# ==============================================

# Local SQLite database (default for development)
DEFAULT_DB_PATH = os.getenv('TEST_DB_PATH', 'db.sqlite3')

# Railway PostgreSQL (for migration scripts only)
# NEVER hardcode production credentials - use environment variables!
RAILWAY_DB_URL = os.getenv(
    'RAILWAY_DATABASE_URL',
    None  # Must be provided via environment variable
)

# ==============================================
# Test Data Configuration
# ==============================================

# Number of test users to create
TEST_USER_COUNTS = {
    'students': int(os.getenv('TEST_STUDENT_COUNT', '10')),
    'mentors': int(os.getenv('TEST_MENTOR_COUNT', '3')),
    'floorwings': int(os.getenv('TEST_FLOORWING_COUNT', '2')),
    'admins': int(os.getenv('TEST_ADMIN_COUNT', '1')),
}

# Test user email domains
TEST_EMAIL_DOMAIN = os.getenv('TEST_EMAIL_DOMAIN', 'test.cohort.com')

# Test cohort settings
TEST_COHORT = {
    'name': os.getenv('TEST_COHORT_NAME', 'Test Cohort'),
    'batch': os.getenv('TEST_COHORT_BATCH', 'tech-f2'),
    'start_date': os.getenv('TEST_COHORT_START_DATE', '2024-01-01'),
}

# ==============================================
# Floor and Wing Configuration
# ==============================================

TEST_FLOORS = {
    'floor2': {
        'name': 'Floor 2',
        'wings': ['A', 'B', 'C', 'D'],
        'rooms_per_wing': 10,
    },
    'floor3': {
        'name': 'Floor 3',
        'wings': ['A', 'B', 'C', 'D'],
        'rooms_per_wing': 10,
    },
}

# ==============================================
# Feature Flags for Testing
# ==============================================

TEST_FEATURE_FLAGS = {
    'enable_gamification': os.getenv('TEST_ENABLE_GAMIFICATION', 'true').lower() in ('true', '1', 'yes'),
    'enable_chat': os.getenv('TEST_ENABLE_CHAT', 'true').lower() in ('true', '1', 'yes'),
    'enable_notifications': os.getenv('TEST_ENABLE_NOTIFICATIONS', 'true').lower() in ('true', '1', 'yes'),
    'enable_analytics': os.getenv('TEST_ENABLE_ANALYTICS', 'false').lower() in ('true', '1', 'yes'),
}

# ==============================================
# Helper Functions
# ==============================================

def get_test_password(user_type='default'):
    """
    Get test password for specific user type.
    
    Args:
        user_type: One of 'admin', 'mentor', 'student', 'floorwing', 'testuser', 'default'
    
    Returns:
        Password string from environment or default
    """
    return DEFAULT_PASSWORDS.get(user_type, DEFAULT_PASSWORDS['default'])

def get_test_email(username, domain=None):
    """
    Generate test email address.
    
    Args:
        username: Username for the email
        domain: Optional email domain (defaults to TEST_EMAIL_DOMAIN)
    
    Returns:
        Email address string
    """
    domain = domain or TEST_EMAIL_DOMAIN
    return f"{username}@{domain}"

def validate_railway_db():
    """
    Validate that Railway database URL is configured.
    
    Returns:
        bool: True if configured, False otherwise
    """
    if not RAILWAY_DB_URL:
        print("ERROR: RAILWAY_DATABASE_URL environment variable not set!")
        print("This is required for production database operations.")
        return False
    return True

def get_test_user_data(user_type, index=1):
    """
    Generate test user data dictionary.
    
    Args:
        user_type: One of 'admin', 'mentor', 'student', 'floorwing'
        index: User number for unique username/email
    
    Returns:
        Dictionary with user data
    """
    username = f"test_{user_type}_{index}"
    return {
        'username': username,
        'email': get_test_email(username),
        'password': get_test_password(user_type),
        'first_name': f'Test',
        'last_name': f'{user_type.title()} {index}',
        'role': user_type,
    }

# ==============================================
# Security Warnings
# ==============================================

if os.getenv('DJANGO_ENV') == 'production':
    import warnings
    warnings.warn(
        "test_config.py is being imported in production environment! "
        "This file should only be used for development and testing.",
        RuntimeWarning
    )
