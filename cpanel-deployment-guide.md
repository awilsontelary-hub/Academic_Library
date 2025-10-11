# Django Academic Library - cPanel Deployment Guide

## Prerequisites
- cPanel hosting account with Python support
- SSH access (preferred) or File Manager
- Domain or subdomain configured

## Step 1: Check Python Version
1. Login to cPanel
2. Go to "Python App" or "Setup Python App"
3. Verify Python 3.8+ is available
4. Note the Python path (usually /usr/bin/python3)

## Step 2: Upload Your Application
```bash
# Via SSH (recommended)
cd public_html
git clone https://github.com/your-username/Academic_Library.git
cd Academic_Library

# Or upload via File Manager (ZIP method)
# Upload your project ZIP and extract to public_html/Academic_Library
```

## Step 3: Create Virtual Environment
```bash
# In cPanel Python App section
App Directory: Academic_Library
Python Version: 3.8+ (latest available)
App URL: your-domain.com (or subdomain)
```

## Step 4: Install Dependencies
```bash
# SSH method
cd Academic_Library
pip install -r requirements.txt

# Or via cPanel Python App interface
# Add packages: Django, gunicorn, psycopg2-binary, etc.
```

## Step 5: Database Setup
1. In cPanel, go to "MySQL Databases"
2. Create database: `yourusername_library`
3. Create user with full privileges
4. Note: Database host, name, user, password

## Step 6: Configure Settings
Create production settings file:

```python
# online_library/settings_production.py
from .settings import *
import os

DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'yourusername_library',
        'USER': 'yourusername_libuser',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

## Step 7: WSGI Configuration
Create or modify passenger_wsgi.py in your app root:

```python
# passenger_wsgi.py
import os
import sys

# Add your project directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'online_library.settings_production'

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## Step 8: Static Files and Media
```bash
# Collect static files
python manage.py collectstatic --settings=online_library.settings_production

# Set proper permissions
chmod -R 755 staticfiles/
chmod -R 755 media/
```

## Step 9: Database Migration
```bash
python manage.py migrate --settings=online_library.settings_production
python manage.py createsuperuser --settings=online_library.settings_production
```

## Step 10: Domain Configuration
1. In cPanel, ensure your domain points to public_html/Academic_Library
2. Or create subdomain pointing to the app directory
3. Set up SSL certificate (Let's Encrypt usually available)

## Institutional ID Setup
```bash
# Create sample institutional IDs
python manage.py shell --settings=online_library.settings_production
# Run your create_sample_ids.py script
```

## File Structure on cPanel:
```
public_html/
├── Academic_Library/          # Your Django app
│   ├── apps/
│   ├── online_library/
│   ├── static/
│   ├── media/
│   ├── manage.py
│   ├── requirements.txt
│   └── passenger_wsgi.py      # WSGI entry point
├── staticfiles/               # Collected static files
└── error_logs/               # Log files
```

## Troubleshooting Common Issues:

### 1. Python Path Issues
```python
# Add to passenger_wsgi.py
import sys
sys.path.insert(0, '/home/yourusername/public_html/Academic_Library')
```

### 2. Database Connection Issues
- Verify database credentials in cPanel
- Check if remote connections are allowed
- Ensure correct hostname (usually localhost)

### 3. Static Files Not Loading
```python
# In settings_production.py
STATIC_URL = '/Academic_Library/static/'
MEDIA_URL = '/Academic_Library/media/'
```

### 4. Permission Issues
```bash
chmod 644 passenger_wsgi.py
chmod -R 755 Academic_Library/
chmod -R 755 staticfiles/
chmod -R 777 media/  # For file uploads
```

## Performance Optimization:
1. Enable cPanel caching if available
2. Optimize database queries
3. Use compressed static files
4. Enable Gzip compression
5. Set up proper cache headers

## Security Considerations:
1. Use strong database passwords
2. Enable SSL certificate
3. Set proper file permissions
4. Hide sensitive files (.env, settings)
5. Regular backups via cPanel

## Maintenance:
1. Regular database backups via cPanel
2. Monitor error logs in cPanel
3. Update dependencies regularly
4. Monitor disk space usage
5. Check application performance

## Cost Estimate:
- Free hosting: $0/month (limited features)
- Shared hosting: $2-5/month
- VPS with cPanel: $10-20/month (better performance)
```