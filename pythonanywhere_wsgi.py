#!/usr/bin/python3.10
"""
WSGI config for PythonAnywhere deployment.

This file contains the WSGI configuration required to serve up your web application.
It works by setting the variable 'application' to a WSGI handler of some description.

For PythonAnywhere:
1. Upload this file to your PythonAnywhere account
2. Set this as your WSGI file in the Web tab
3. Update the paths below to match your PythonAnywhere directory structure
"""

import os
import sys

# Add your project directory to the Python path
# CHANGE THIS to match your PythonAnywhere username and project structure
# Example: if your files are in /home/yourusername/Academic_Library/
project_home = '/home/yourusername/Academic_Library'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'online_library.settings'

# Get the Django WSGI application
from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler

# For development/testing - serves static files
# Remove StaticFilesHandler wrapper for production with proper static file serving
application = StaticFilesHandler(get_wsgi_application())