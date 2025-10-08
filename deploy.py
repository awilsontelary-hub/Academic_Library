#!/usr/bin/env python
"""
Deployment script for Academic Library project
"""
import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
    else:
        print(f"❌ {description} failed")
        print(result.stderr)
        return False
    return True

def main():
    """Main deployment function"""
    print("🚀 Starting Academic Library deployment preparation...")
    
    # Change to project directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    commands = [
        ("python manage.py collectstatic --noinput", "Collecting static files"),
        ("python manage.py makemigrations", "Creating migrations"),
        ("python manage.py migrate", "Applying migrations"),
        ("python manage.py check --deploy", "Running deployment checks"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            sys.exit(1)
    
    print("\n🎉 Deployment preparation completed successfully!")
    print("\nNext steps:")
    print("1. Set environment variables in production")
    print("2. Configure database (if using PostgreSQL)")
    print("3. Deploy to your hosting platform")

if __name__ == "__main__":
    main()