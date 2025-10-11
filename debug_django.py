#!/usr/bin/env python
"""
Django configuration debug script for Render deployment
"""
import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_library.settings')

def debug_django_config():
    print("🔍 Django Configuration Debug")
    print("=" * 40)
    
    try:
        # Setup Django
        django.setup()
        print("✅ Django setup successful")
        
        # Import settings
        from django.conf import settings
        print(f"✅ Settings imported successfully")
        print(f"   DEBUG: {settings.DEBUG}")
        print(f"   ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        print(f"   SECRET_KEY: {'***' + settings.SECRET_KEY[-10:] if settings.SECRET_KEY else 'NOT SET'}")
        
        # Test database connection
        from django.db import connection
        cursor = connection.cursor()
        print("✅ Database connection successful")
        
        # Test WSGI application
        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()
        print(f"✅ WSGI application loaded: {type(application)}")
        
        print("\n🎉 All checks passed! Django should work on Render.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = debug_django_config()
    sys.exit(0 if success else 1)