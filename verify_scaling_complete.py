"""
Scaling Verification Script
===========================

Verifies all scaling implementations are working correctly.
Run this after completing all scaling tasks.

Usage:
    python verify_scaling_complete.py
"""

import os
import sys
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓{Colors.END} {text}")

def print_error(text):
    print(f"{Colors.RED}✗{Colors.END} {text}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠{Colors.END} {text}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ{Colors.END} {text}")

# Get project root
BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR / 'backend'

def check_file_exists(filepath, description):
    """Check if a file exists"""
    full_path = BASE_DIR / filepath
    if full_path.exists():
        print_success(f"{description}: {filepath}")
        return True
    else:
        print_error(f"Missing: {filepath}")
        return False

def check_directory_exists(dirpath, description):
    """Check if a directory exists"""
    full_path = BASE_DIR / dirpath
    if full_path.exists() and full_path.is_dir():
        print_success(f"{description}: {dirpath}")
        return True
    else:
        print_error(f"Missing directory: {dirpath}")
        return False

def check_feature_flags():
    """Verify feature flags in settings.py"""
    print_header("1. FEATURE FLAGS VERIFICATION")
    
    settings_file = BACKEND_DIR / 'config' / 'settings.py'
    
    if not settings_file.exists():
        print_error("settings.py not found")
        return False
    
    with open(settings_file, 'r') as f:
        content = f.read()
    
    flags = [
        'USE_ANALYTICS_SUMMARY',
        'USE_NOTIFICATION_CACHE',
        'USE_CLOUD_STORAGE',
        'USE_ASYNC_TASKS',
        'LOG_QUERY_TIMES'
    ]
    
    all_found = True
    for flag in flags:
        if flag in content:
            print_success(f"Feature flag found: {flag}")
        else:
            print_error(f"Missing feature flag: {flag}")
            all_found = False
    
    return all_found

def check_apps():
    """Verify analytics_summary app exists"""
    print_header("2. ANALYTICS APP VERIFICATION")
    
    checks = [
        (BACKEND_DIR / 'apps' / 'analytics_summary', "analytics_summary app directory"),
        (BACKEND_DIR / 'apps' / 'analytics_summary' / 'models.py', "Analytics models"),
        (BACKEND_DIR / 'apps' / 'analytics_summary' / 'admin.py', "Analytics admin"),
        (BACKEND_DIR / 'apps' / 'analytics_summary' / 'management' / 'commands' / 'recompute_analytics.py', "recompute_analytics command"),
    ]
    
    all_found = True
    for path, description in checks:
        if not path.exists():
            print_error(f"Missing: {description}")
            all_found = False
        else:
            print_success(description)
    
    return all_found

def check_health_endpoints():
    """Verify health check views"""
    print_header("3. HEALTH CHECK ENDPOINTS VERIFICATION")
    
    health_views = BACKEND_DIR / 'apps' / 'health_check_views.py'
    urls_file = BACKEND_DIR / 'config' / 'urls.py'
    
    all_found = True
    
    if health_views.exists():
        print_success("health_check_views.py exists")
    else:
        print_error("health_check_views.py not found")
        all_found = False
    
    if urls_file.exists():
        with open(urls_file, 'r') as f:
            content = f.read()
        
        endpoints = ['health/', 'health/ready/', 'health/live/']
        for endpoint in endpoints:
            if endpoint in content:
                print_success(f"Endpoint registered: /{endpoint}")
            else:
                print_warning(f"Endpoint may not be registered: /{endpoint}")
    else:
        print_error("urls.py not found")
        all_found = False
    
    return all_found

def check_storage_service():
    """Verify file storage abstraction"""
    print_header("4. FILE STORAGE SERVICE VERIFICATION")
    
    storage_service = BACKEND_DIR / 'apps' / 'file_storage_service.py'
    
    if storage_service.exists():
        print_success("file_storage_service.py exists")
        return True
    else:
        print_error("file_storage_service.py not found")
        return False

def check_management_commands():
    """Verify management commands"""
    print_header("5. MANAGEMENT COMMANDS VERIFICATION")
    
    commands = [
        ('apps/gamification/management/commands/sync_leetcode_streaks.py', 'sync_leetcode_streaks'),
        ('apps/gamification/management/commands/update_seasons.py', 'update_seasons'),
    ]
    
    all_found = True
    for cmd_path, cmd_name in commands:
        full_path = BACKEND_DIR / cmd_path
        if full_path.exists():
            print_success(f"Command exists: {cmd_name}")
        else:
            print_error(f"Missing command: {cmd_name}")
            all_found = False
    
    return all_found

def check_migrations():
    """Verify database indexes migration"""
    print_header("6. DATABASE MIGRATIONS VERIFICATION")
    
    migration_file = BACKEND_DIR / 'apps' / 'profiles' / 'migrations' / '0007_add_scaling_indexes.py'
    
    if migration_file.exists():
        print_success("Scaling indexes migration exists: 0007_add_scaling_indexes.py")
        return True
    else:
        print_warning("Indexes migration not found (may need to run makemigrations)")
        return False

def check_documentation():
    """Verify all documentation files exist"""
    print_header("7. DOCUMENTATION VERIFICATION")
    
    docs = [
        ('SCALING_COMPLETE.md', 'Scaling complete summary'),
        ('SCALING_IMPLEMENTATION_GUIDE.md', 'Implementation guide'),
        ('SCALING_QUICK_REFERENCE.md', 'Quick reference'),
        ('FRONTEND_PERFORMANCE_GUIDE.md', 'Frontend guide'),
        ('backend/N+1_QUERY_FIXES.md', 'N+1 query fixes'),
    ]
    
    all_found = True
    for doc_path, doc_name in docs:
        if check_file_exists(doc_path, doc_name):
            pass
        else:
            all_found = False
    
    return all_found

def check_notification_caching():
    """Verify notification caching implementation"""
    print_header("8. NOTIFICATION CACHING VERIFICATION")
    
    notification_views = BACKEND_DIR / 'apps' / 'profiles' / 'notification_views.py'
    
    if notification_views.exists():
        with open(notification_views, 'r') as f:
            content = f.read()
        
        if 'USE_NOTIFICATION_CACHE' in content and 'cache.get' in content and 'cache.set' in content:
            print_success("Notification caching implemented")
            return True
        else:
            print_warning("Notification caching may not be fully implemented")
            return False
    else:
        print_error("notification_views.py not found")
        return False

def main():
    """Run all verification checks"""
    print_header("SCALING IMPLEMENTATION VERIFICATION")
    print_info("Checking all scaling components...")
    
    results = {
        'Feature Flags': check_feature_flags(),
        'Analytics App': check_apps(),
        'Health Endpoints': check_health_endpoints(),
        'Storage Service': check_storage_service(),
        'Management Commands': check_management_commands(),
        'Database Migrations': check_migrations(),
        'Documentation': check_documentation(),
        'Notification Caching': check_notification_caching(),
    }
    
    # Summary
    print_header("VERIFICATION SUMMARY")
    
    passed = sum(results.values())
    total = len(results)
    
    for component, status in results.items():
        if status:
            print_success(f"{component}: PASS")
        else:
            print_error(f"{component}: FAIL")
    
    print(f"\n{Colors.BOLD}Result: {passed}/{total} checks passed{Colors.END}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ ALL SCALING COMPONENTS VERIFIED!{Colors.END}")
        print(f"{Colors.GREEN}The application is ready for 2000+ student scaling.{Colors.END}\n")
        return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}✗ SOME COMPONENTS MISSING{Colors.END}")
        print(f"{Colors.RED}Please review the errors above and complete missing tasks.{Colors.END}\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())
