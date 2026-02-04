#!/usr/bin/env python3
"""
Test Supabase Database Connection
This script verifies that your Supabase PostgreSQL connection is working correctly.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add backend to path
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

# Load environment variables
load_dotenv()

def test_with_psycopg():
    """Test connection using psycopg3"""
    print("=" * 60)
    print("Testing Supabase Connection with psycopg3")
    print("=" * 60)
    
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
        print("   Please set DATABASE_URL in your .env file")
        return False
    
    # Mask password in output
    masked_url = database_url.replace(database_url.split(':')[2].split('@')[0], '****')
    print(f"\n📍 Connection String: {masked_url}")
    
    try:
        import psycopg
        
        print("\n🔄 Attempting connection...")
        conn = psycopg.connect(database_url, connect_timeout=10)
        print("✅ Connection successful!")
        
        # Test basic queries
        cur = conn.cursor()
        
        # Get PostgreSQL version
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        print(f"\n📊 PostgreSQL Version:")
        print(f"   {version.split(',')[0]}")
        
        # Get current database
        cur.execute("SELECT current_database();")
        db_name = cur.fetchone()[0]
        print(f"\n💾 Database: {db_name}")
        
        # Get connection info
        cur.execute("SELECT inet_server_addr(), inet_server_port();")
        server_info = cur.fetchone()
        if server_info[0]:
            print(f"🌐 Server: {server_info[0]}:{server_info[1]}")
        
        # Check SSL
        cur.execute("SHOW ssl;")
        ssl_status = cur.fetchone()[0]
        print(f"🔒 SSL: {ssl_status}")
        
        # Check if tables exist
        cur.execute("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        table_count = cur.fetchone()[0]
        print(f"\n📋 Tables in database: {table_count}")
        
        if table_count > 0:
            cur.execute("""
                SELECT tablename 
                FROM pg_tables 
                WHERE schemaname = 'public'
                ORDER BY tablename
                LIMIT 10
            """)
            tables = cur.fetchall()
            print("\n📝 Sample tables:")
            for table in tables:
                print(f"   - {table[0]}")
            if table_count > 10:
                print(f"   ... and {table_count - 10} more")
        
        cur.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ All tests passed! Your Supabase connection is working.")
        print("=" * 60)
        return True
        
    except ImportError:
        print("\n❌ psycopg not installed")
        print("   Install it with: pip install psycopg[binary]")
        return False
    except Exception as e:
        print(f"\n❌ Connection failed!")
        print(f"   Error: {str(e)}")
        print("\n🔍 Troubleshooting tips:")
        print("   1. Verify DATABASE_URL is correct")
        print("   2. Check if Supabase project is active")
        print("   3. Ensure SSL is configured (sslmode=require)")
        print("   4. Verify your IP is not blocked")
        print("   5. Check Supabase status: https://status.supabase.com")
        return False


def test_with_django():
    """Test connection using Django ORM"""
    print("\n" + "=" * 60)
    print("Testing Django ORM Connection")
    print("=" * 60)
    
    try:
        # Setup Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        import django
        django.setup()
        
        from django.db import connection
        from django.contrib.auth.models import User
        
        print("\n🔄 Testing Django connection...")
        
        # Test connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Django database connection successful!")
        
        # Check if tables are created
        try:
            user_count = User.objects.count()
            print(f"\n👥 Users in database: {user_count}")
        except Exception as e:
            print(f"\n⚠️  Tables not yet created")
            print(f"   Run: python manage.py migrate")
        
        print("\n" + "=" * 60)
        print("✅ Django ORM tests passed!")
        print("=" * 60)
        return True
        
    except ImportError as e:
        print(f"\n⚠️  Django not properly configured: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Django connection failed: {e}")
        return False


def main():
    """Run all connection tests"""
    print("\n🚀 Supabase Connection Test Suite")
    print("=" * 60)
    
    # Test with psycopg
    psycopg_success = test_with_psycopg()
    
    # Test with Django if psycopg succeeded
    django_success = False
    if psycopg_success:
        django_success = test_with_django()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    print(f"psycopg3 Connection: {'✅ PASS' if psycopg_success else '❌ FAIL'}")
    print(f"Django ORM Connection: {'✅ PASS' if django_success else '❌ FAIL'}")
    print("=" * 60)
    
    if psycopg_success and django_success:
        print("\n🎉 All systems operational! You're ready to deploy.")
        return 0
    elif psycopg_success:
        print("\n⚠️  Basic connection works, but Django needs setup.")
        print("   Run: python manage.py migrate")
        return 1
    else:
        print("\n❌ Connection failed. Please check your configuration.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
