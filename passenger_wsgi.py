#!/usr/bin/python3.9
# cPanel Python WSGI Configuration
# This file should be placed in your cPanel account and configured in the Python App settings

import os
import sys

# Add your Django project to the Python path
project_home = '/home/yourusername/your_domain_folder/Academic_Library'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'online_library.settings'

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()