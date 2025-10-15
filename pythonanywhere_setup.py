#!/usr/bin/env python3
"""
PythonAnywhere setup script for Academic Library Django app
Run this after uploading to your PythonAnywhere account
"""

import os
import sys
import django

def setup_pythonanywhere():
    """Setup Django application for PythonAnywhere hosting"""
    
    print("🐍 Setting up Academic Library for PythonAnywhere...")
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_library.settings')
    django.setup()
    
    from django.core.management import execute_from_command_line
    from django.contrib.auth import get_user_model
    from apps.accounts.models import InstitutionalID
    
    print("\n📋 Step 1: Running database migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("\n📁 Step 2: Collecting static files...")
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    
    print("\n👤 Step 3: Creating sample institutional IDs...")
    
    # Create sample institutional IDs
    sample_ids = [
        {
            'institutional_id': 'ADMIN001',
            'account_type': 'staff',
            'status': 'active',
            'first_name': 'Admin',
            'last_name': 'User',
            'email': 'admin@yourdomain.com',
            'academic_level': 'admin',
            'department': 'Administration'
        },
        {
            'institutional_id': 'INST001',
            'account_type': 'student',
            'status': 'active',
            'academic_level': 'sophomore',
            'department': 'Computer Science'
        },
        {
            'institutional_id': 'INST002',
            'account_type': 'student',
            'status': 'active',
            'academic_level': 'junior',
            'department': 'Engineering'
        },
        {
            'institutional_id': 'INST003',
            'account_type': 'staff',
            'status': 'active',
            'academic_level': 'faculty',
            'department': 'Library Sciences'
        },
        {
            'institutional_id': 'INST004',
            'account_type': 'student',
            'status': 'active',
            'academic_level': 'senior',
            'department': 'Mathematics'
        },
        {
            'institutional_id': 'INST005',
            'account_type': 'staff',
            'status': 'active',
            'academic_level': 'staff',
            'department': 'IT Support'
        }
    ]
    
    for id_data in sample_ids:
        obj, created = InstitutionalID.objects.get_or_create(
            institutional_id=id_data['institutional_id'],
            defaults=id_data
        )
        if created:
            print(f"✅ Created institutional ID: {id_data['institutional_id']}")
        else:
            print(f"ℹ️  Institutional ID already exists: {id_data['institutional_id']}")
    
    print("\n🎉 PythonAnywhere setup complete!")
    print("\n📋 Next steps:")
    print("1. Create admin user: python manage.py createsuperuser")
    print("2. Configure your domain in PythonAnywhere Web tab")
    print("3. Set up .env file with your domain and database details")
    print("4. Reload your web app in PythonAnywhere")
    print("\n🔗 Access your site at: https://yourusername.pythonanywhere.com")
    print("🔐 Admin panel: https://yourusername.pythonanywhere.com/admin")

if __name__ == "__main__":
    setup_pythonanywhere()