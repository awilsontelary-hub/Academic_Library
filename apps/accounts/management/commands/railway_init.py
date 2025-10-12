from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.accounts.models import InstitutionalID


class Command(BaseCommand):
    help = 'Initialize database with admin user and sample data for Railway deployment'

    def handle(self, *args, **options):
        User = get_user_model()
        
        self.stdout.write('🚀 Initializing Railway deployment...')
        
        # Create institutional ID for admin if it doesn't exist
        admin_id, created = InstitutionalID.objects.get_or_create(
            institutional_id='ADMIN001',
            defaults={
                'account_type': 'staff',
                'status': 'active',
                'first_name': 'Railway',
                'last_name': 'Admin',
                'email': 'admin@railway.app',
                'academic_level': 'admin',
                'department': 'Administration'
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('✅ Admin institutional ID created')
            )
        else:
            self.stdout.write(
                self.style.WARNING('ℹ️ Admin institutional ID already exists')
            )
        
        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@railway.app',
                password='railway123',
                first_name='Railway',
                last_name='Admin',
                institutional_id=admin_id,
                is_approved=True
            )
            self.stdout.write(
                self.style.SUCCESS('✅ Admin user created')
            )
            self.stdout.write(
                self.style.SUCCESS('   Username: admin')
            )
            self.stdout.write(
                self.style.SUCCESS('   Password: railway123')
            )
        else:
            self.stdout.write(
                self.style.WARNING('ℹ️ Admin user already exists')
            )
            
        # Create some sample institutional IDs
        sample_institutions = [
            ('INST001', 'student', 'Harvard University'),
            ('INST002', 'student', 'Stanford University'),
            ('INST003', 'student', 'MIT'),
            ('INST004', 'staff', 'UC Berkeley'),
            ('INST005', 'staff', 'Oxford University'),
        ]
        
        for inst_id, acc_type, institution in sample_institutions:
            inst_obj, created = InstitutionalID.objects.get_or_create(
                institutional_id=inst_id,
                defaults={
                    'account_type': acc_type,
                    'status': 'active',
                    'department': institution,
                    'academic_level': 'student' if acc_type == 'student' else 'staff'
                }
            )
            if created:
                self.stdout.write(f'✅ Created institutional ID: {inst_id} - {institution}')
        
        self.stdout.write(
            self.style.SUCCESS('🎉 Railway deployment initialization complete!')
        )