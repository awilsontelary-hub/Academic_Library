from django.core.management.base import BaseCommand
from django.core.management import execute_from_command_line
from django.db import connection
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Initialize database and create required tables'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔧 Starting database setup...'))
        
        try:
            # Run migrations
            self.stdout.write('📊 Running migrations...')
            execute_from_command_line(['manage.py', 'migrate', '--noinput'])
            
            # Check database tables
            with connection.cursor() as cursor:
                if 'sqlite' in str(connection.vendor):
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = [row[0] for row in cursor.fetchall()]
                else:
                    cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname='public';")
                    tables = [row[0] for row in cursor.fetchall()]
            
            self.stdout.write(f'📋 Found {len(tables)} database tables')
            
            # Check for required tables
            required_tables = ['library_bookdetails', 'library_category', 'library_bookfile']
            for table in required_tables:
                if table in tables:
                    self.stdout.write(self.style.SUCCESS(f'✅ {table} - OK'))
                else:
                    self.stdout.write(self.style.ERROR(f'❌ {table} - MISSING'))
            
            # Create superuser if needed
            User = get_user_model()
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser('admin', 'admin@academialink.com', 'admin123')
                self.stdout.write(self.style.SUCCESS('✅ Admin user created: admin/admin123'))
            else:
                self.stdout.write('ℹ️ Admin user already exists')
            
            self.stdout.write(self.style.SUCCESS('🎉 Database setup completed!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Database setup failed: {e}'))
            raise