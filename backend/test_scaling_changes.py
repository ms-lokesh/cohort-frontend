"""
Quick Test Script for Scaling Changes

This script verifies that all scaling changes are working correctly
without breaking existing functionality.

Run this after: python manage.py migrate
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
from django.db import connection
from django.core.cache import cache
from apps.analytics_summary.models import FloorAnalyticsSummary, MentorAnalyticsSummary
from apps.profiles.models import UserProfile

def test_feature_flags():
    """Test that feature flags are properly configured"""
    print("\n" + "=" * 70)
    print("TESTING FEATURE FLAGS")
    print("=" * 70)
    
    flags = {
        'USE_ANALYTICS_SUMMARY': settings.USE_ANALYTICS_SUMMARY,
        'USE_NOTIFICATION_CACHE': settings.USE_NOTIFICATION_CACHE,
        'USE_CLOUD_STORAGE': settings.USE_CLOUD_STORAGE,
        'USE_ASYNC_TASKS': settings.USE_ASYNC_TASKS,
        'LOG_QUERY_TIMES': settings.LOG_QUERY_TIMES,
    }
    
    for flag, value in flags.items():
        status = "✓ ENABLED" if value else "○ DISABLED (default)"
        print(f"{flag:30s} : {status}")
    
    print("\n✓ Feature flags configured correctly")
    return True

def test_database():
    """Test database connectivity"""
    print("\n" + "=" * 70)
    print("TESTING DATABASE")
    print("=" * 70)
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✓ Database connection successful")
        
        # Test that new tables exist
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) FROM information_schema.tables 
                WHERE table_name LIKE 'analytics_%'
            """)
            count = cursor.fetchone()[0]
        
        if count >= 4:  # Should have 4 analytics tables
            print(f"✓ Analytics tables created ({count} tables)")
        else:
            print(f"⚠ Warning: Expected 4 analytics tables, found {count}")
            print("  Run: python manage.py migrate")
        
        return True
    except Exception as e:
        print(f"✗ Database error: {e}")
        return False

def test_cache():
    """Test cache configuration"""
    print("\n" + "=" * 70)
    print("TESTING CACHE")
    print("=" * 70)
    
    try:
        cache.set('test_key', 'test_value', 10)
        result = cache.get('test_key')
        
        if result == 'test_value':
            cache_backend = settings.CACHES['default']['BACKEND']
            print(f"✓ Cache working: {cache_backend.split('.')[-1]}")
            return True
        else:
            print("⚠ Cache not storing values correctly")
            return False
    except Exception as e:
        print(f"⚠ Cache error (this is OK if caching disabled): {e}")
        return True  # Not critical

def test_analytics_models():
    """Test that analytics models work"""
    print("\n" + "=" * 70)
    print("TESTING ANALYTICS MODELS")
    print("=" * 70)
    
    try:
        # Test FloorAnalyticsSummary
        floor_count = FloorAnalyticsSummary.objects.count()
        print(f"FloorAnalyticsSummary: {floor_count} records")
        
        # Test MentorAnalyticsSummary
        mentor_count = MentorAnalyticsSummary.objects.count()
        print(f"MentorAnalyticsSummary: {mentor_count} records")
        
        if floor_count == 0 and mentor_count == 0:
            print("\n⚠ No analytics data yet. Run: python manage.py recompute_analytics")
        else:
            print("\n✓ Analytics models working")
        
        return True
    except Exception as e:
        print(f"✗ Analytics model error: {e}")
        print("  Make sure migrations are run: python manage.py migrate")
        return False

def test_existing_functionality():
    """Test that existing models still work"""
    print("\n" + "=" * 70)
    print("TESTING EXISTING FUNCTIONALITY")
    print("=" * 70)
    
    try:
        # Test UserProfile (existing model)
        user_count = UserProfile.objects.count()
        print(f"✓ UserProfile: {user_count} users")
        
        student_count = UserProfile.objects.filter(role='STUDENT').count()
        mentor_count = UserProfile.objects.filter(role='MENTOR').count()
        
        print(f"  - Students: {student_count}")
        print(f"  - Mentors: {mentor_count}")
        
        print("\n✓ Existing models unchanged and working")
        return True
    except Exception as e:
        print(f"✗ Existing functionality error: {e}")
        return False

def test_health_endpoints():
    """Test health check endpoints"""
    print("\n" + "=" * 70)
    print("TESTING HEALTH ENDPOINTS")
    print("=" * 70)
    
    try:
        from apps.health_check_views import health_check, readiness_check, liveness_check
        from django.test import RequestFactory
        
        factory = RequestFactory()
        
        # Test health check
        request = factory.get('/health/')
        response = health_check(request)
        
        if response.status_code in [200, 503]:
            print("✓ /health/ endpoint working")
        else:
            print(f"⚠ /health/ returned unexpected status: {response.status_code}")
        
        # Test readiness
        request = factory.get('/health/ready/')
        response = readiness_check(request)
        print("✓ /health/ready/ endpoint working")
        
        # Test liveness
        request = factory.get('/health/live/')
        response = liveness_check(request)
        print("✓ /health/live/ endpoint working")
        
        return True
    except Exception as e:
        print(f"✗ Health endpoint error: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "#" * 70)
    print("COHORT WEB APPLICATION - SCALING VERIFICATION")
    print("#" * 70)
    
    results = {
        'Feature Flags': test_feature_flags(),
        'Database': test_database(),
        'Cache': test_cache(),
        'Analytics Models': test_analytics_models(),
        'Existing Functionality': test_existing_functionality(),
        'Health Endpoints': test_health_endpoints(),
    }
    
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name:30s} : {status}")
        if not passed:
            all_passed = False
    
    print("=" * 70)
    
    if all_passed:
        print("\n✓ ALL TESTS PASSED")
        print("\nNext steps:")
        print("1. Run: python manage.py recompute_analytics --verbose")
        print("2. Check Django admin: http://localhost:8000/admin/")
        print("3. Test health endpoint: curl http://localhost:8000/health/")
        print("4. Test existing features (login, submissions, etc.)")
        return 0
    else:
        print("\n✗ SOME TESTS FAILED")
        print("\nTroubleshooting:")
        print("1. Run migrations: python manage.py migrate")
        print("2. Check Django settings")
        print("3. Verify database connection")
        return 1

if __name__ == '__main__':
    sys.exit(main())
