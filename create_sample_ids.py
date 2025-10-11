#!/usr/bin/env python
"""
Script to create sample institutional IDs for testing the verification system
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_library.settings')
django.setup()

from apps.accounts.models import InstitutionalID, User

def create_sample_institutional_ids():
    """Create sample institutional IDs for testing"""
    
    # Get or create an admin user to set as the creator
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'is_staff': True,
            'is_superuser': True,
            'email': 'admin@library.edu',
            'first_name': 'Admin',
            'last_name': 'User'
        }
    )
    
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print(f"Created admin user: {admin_user.username}")
    
    # Sample student IDs
    student_ids = [
        {
            'institutional_id': 'STU2024001',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@university.edu',
            'academic_level': 'Undergraduate',
            'department': 'Computer Science'
        },
        {
            'institutional_id': 'STU2024002',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@university.edu',
            'academic_level': 'Graduate',
            'department': 'Engineering'
        },
        {
            'institutional_id': 'STU2024003',
            'first_name': 'Alice',
            'last_name': 'Johnson',
            'email': 'alice.johnson@university.edu',
            'academic_level': 'PhD',
            'department': 'Mathematics'
        },
        {
            'institutional_id': 'STU2024004',
            'first_name': 'Bob',
            'last_name': 'Wilson',
            'email': 'bob.wilson@university.edu',
            'academic_level': 'Undergraduate',
            'department': 'Physics'
        },
        {
            'institutional_id': 'STU2024005',
            'first_name': 'Carol',
            'last_name': 'Brown',
            'email': 'carol.brown@university.edu',
            'academic_level': 'Graduate',
            'department': 'Chemistry'
        }
    ]
    
    # Sample staff IDs
    staff_ids = [
        {
            'institutional_id': 'EMP2024001',
            'first_name': 'Dr. Robert',
            'last_name': 'Johnson',
            'email': 'robert.johnson@university.edu',
            'department': 'Computer Science'
        },
        {
            'institutional_id': 'EMP2024002',
            'first_name': 'Prof. Sarah',
            'last_name': 'Davis',
            'email': 'sarah.davis@university.edu',
            'department': 'Engineering'
        },
        {
            'institutional_id': 'EMP2024003',
            'first_name': 'Dr. Michael',
            'last_name': 'Miller',
            'email': 'michael.miller@university.edu',
            'department': 'Library Administration'
        }
    ]
    
    created_count = 0
    
    # Create student IDs
    for student_data in student_ids:
        obj, created = InstitutionalID.objects.get_or_create(
            institutional_id=student_data['institutional_id'],
            defaults={
                'account_type': 'student',
                'status': 'active',
                'first_name': student_data['first_name'],
                'last_name': student_data['last_name'],
                'email': student_data['email'],
                'academic_level': student_data['academic_level'],
                'department': student_data['department'],
                'expires_at': datetime.now() + timedelta(days=365*4),  # 4 years
                'added_by': admin_user,
                'notes': 'Sample student ID created for testing'
            }
        )
        
        if created:
            created_count += 1
            print(f"Created student ID: {obj.institutional_id} - {obj.full_name}")
        else:
            print(f"Student ID already exists: {obj.institutional_id}")
    
    # Create staff IDs
    for staff_data in staff_ids:
        obj, created = InstitutionalID.objects.get_or_create(
            institutional_id=staff_data['institutional_id'],
            defaults={
                'account_type': 'staff',
                'status': 'active',
                'first_name': staff_data['first_name'],
                'last_name': staff_data['last_name'],
                'email': staff_data['email'],
                'department': staff_data['department'],
                'expires_at': datetime.now() + timedelta(days=365*10),  # 10 years
                'added_by': admin_user,
                'notes': 'Sample staff ID created for testing'
            }
        )
        
        if created:
            created_count += 1
            print(f"Created staff ID: {obj.institutional_id} - {obj.full_name}")
        else:
            print(f"Staff ID already exists: {obj.institutional_id}")
    
    # Create some expired IDs for testing
    expired_ids = [
        {
            'institutional_id': 'STU2023999',
            'first_name': 'Expired',
            'last_name': 'Student',
            'email': 'expired.student@university.edu',
            'account_type': 'student',
            'status': 'expired'
        }
    ]
    
    for expired_data in expired_ids:
        obj, created = InstitutionalID.objects.get_or_create(
            institutional_id=expired_data['institutional_id'],
            defaults={
                'account_type': expired_data['account_type'],
                'status': expired_data['status'],
                'first_name': expired_data['first_name'],
                'last_name': expired_data['last_name'],
                'email': expired_data['email'],
                'expires_at': datetime.now() - timedelta(days=30),  # Expired 30 days ago
                'added_by': admin_user,
                'notes': 'Sample expired ID for testing'
            }
        )
        
        if created:
            created_count += 1
            print(f"Created expired ID: {obj.institutional_id}")
    
    print(f"\nTotal institutional IDs created: {created_count}")
    print(f"Total institutional IDs in database: {InstitutionalID.objects.count()}")
    
    # Display summary
    print("\n=== Summary ===")
    print(f"Active student IDs: {InstitutionalID.objects.filter(account_type='student', status='active').count()}")
    print(f"Active staff IDs: {InstitutionalID.objects.filter(account_type='staff', status='active').count()}")
    print(f"Expired IDs: {InstitutionalID.objects.filter(status='expired').count()}")
    print(f"Used IDs: {InstitutionalID.objects.filter(status='used').count()}")

if __name__ == '__main__':
    create_sample_institutional_ids()