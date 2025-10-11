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

# Collect static files
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

echo "🎉 Build completed successfully!"