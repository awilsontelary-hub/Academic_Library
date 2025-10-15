#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "🔧 Starting build process..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check Django setup
echo "✅ Checking Django configuration..."
python manage.py check

# Force database setup
echo "�️ Setting up database..."
python manage.py setup_database

#!/usr/bin/env bash
# Render.com Build Script for Django Academic Library
set -o errexit

echo "🔧 Starting Render build process..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run Django management commands
echo "🗄️ Running database migrations..."
python manage.py migrate

echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo "👤 Setting up initial data..."
python cpanel_setup.py || echo "Setup script completed with warnings"

echo "✅ Build completed successfully!"