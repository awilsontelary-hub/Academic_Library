#!/usr/bin/env python
"""
Simple startup script for deployment debugging
"""
import os
import sys
import django
from django.core.wsgi import get_wsgi_application

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_library.settings')

# Setup Django
django.setup()

# Get WSGI application
application = get_wsgi_application()

if __name__ == "__main__":
    print("✅ Django WSGI application loaded successfully!")
    print(f"✅ Settings module: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
    print(f"✅ Application: {application}")