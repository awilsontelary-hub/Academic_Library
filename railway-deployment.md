# Railway Deployment Configuration for Academic Library

# Railway automatically detects Django apps, but this ensures proper setup

# Build and Start Commands
web: gunicorn online_library.wsgi:application --bind 0.0.0.0:$PORT

# Railway Environment Variables Needed:
# DATABASE_URL (automatically provided by Railway)
# SECRET_KEY (generate a new secure key)
# DEBUG=False
# ALLOWED_HOSTS=your-app-name.railway.app
# DISABLE_COLLECTSTATIC=1 (if using whitenoise)

# Railway will automatically:
# 1. Install requirements.txt dependencies
# 2. Run database migrations
# 3. Collect static files
# 4. Start the web server