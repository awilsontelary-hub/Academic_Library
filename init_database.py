#!/usr/bin/env python
"""
Database initialization script for Render deployment
Ensures all tables are created properly
"""
import os
import sys
import django
from pathlib import Path

# Setup Django environment
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_library.settings')

def init_database():
    print("🔧 Initializing database...")
    
    try:
        django.setup()
        
        # Run migrations
        from django.core.management import execute_from_command_line
        
        print("📊 Running migrations...")
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        
        # Verify tables exist
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            
        print(f"✅ Database tables created: {len(tables)} tables")
        
        # Check for required tables
        required_tables = ['library_bookdetails', 'library_category', 'library_bookfile']
        missing_tables = []
        
        for table in required_tables:
            if table in tables:
                print(f"✅ {table} - OK")
            else:
                missing_tables.append(table)
                print(f"❌ {table} - MISSING")
        
        if missing_tables:
            print(f"⚠️ Missing tables: {missing_tables}")
            print("🔄 Attempting to create missing tables...")
            
            # Force migration of library app
            execute_from_command_line(['manage.py', 'migrate', 'library', '--noinput'])
            
        # Create admin user
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@academialink.com', 
                password='admin123'  # ⚠️ CHANGE THIS PASSWORD after first login!
            )
            print("✅ Admin user created: admin/admin123")
            print("⚠️  IMPORTANT: Change the admin password after first login!")
        
        print("🎉 Database initialization completed!")
        return True
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)
