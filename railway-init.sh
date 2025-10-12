#!/bin/bash

# Railway Deployment Initialization Script
echo "🚀 Starting Railway deployment initialization..."

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install --no-cache-dir -r requirements.txt

# Run Django management commands
echo "🔄 Running Django migrations..."
python manage.py migrate --noinput

echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create initial admin user if needed (optional)
echo "👤 Creating initial admin user if needed..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
from apps.accounts.models import InstitutionalID
import os

User = get_user_model()

# Create institutional ID for admin if it doesn't exist
if not InstitutionalID.objects.filter(id_number='ADMIN001').exists():
    admin_id = InstitutionalID.objects.create(
        id_number='ADMIN001',
        institution_name='Railway Admin',
        is_verified=True
    )
    print('✅ Admin institutional ID created')

# Create superuser if it doesn't exist
if not User.objects.filter(username='admin').exists():
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@railway.app',
        password='railway123',
        first_name='Railway',
        last_name='Admin',
        institutional_id=InstitutionalID.objects.get(id_number='ADMIN001'),
        is_approved=True
    )
    print('✅ Admin user created - Username: admin, Password: railway123')
else:
    print('✅ Admin user already exists')
"

echo "✅ Railway deployment initialization complete!"