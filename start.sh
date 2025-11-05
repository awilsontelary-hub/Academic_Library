# This file tells Render exactly how to start the Django application
gunicorn online_library.wsgi:application --bind 0.0.0.0:$PORT --workers 2