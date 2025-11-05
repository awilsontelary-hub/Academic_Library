"""
Management command to generate institutional IDs.
"""
from django.core.management.base import BaseCommand
from apps.accounts.models import InstitutionalID
from apps.accounts.admin import generate_unique_institutional_id


class Command(BaseCommand):
    help = 'Generate institutional IDs for students or staff'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=1,
            help='Number of IDs to generate (default: 1)'
        )
        parser.add_argument(
            '--type',
            type=str,
            choices=['student', 'staff'],
            default='student',
            help='Account type: student or staff (default: student)'
        )
        parser.add_argument(
            '--academic-level',
            type=str,
            default='',
            help='Academic level (optional)'
        )
        parser.add_argument(
            '--department',
            type=str,
            default='',
            help='Department (optional)'
        )

    def handle(self, *args, **options):
        count = options['count']
        account_type = options['type']
        academic_level = options.get('academic_level', '')
        department = options.get('department', '')

        if count < 1 or count > 100:
            self.stdout.write(
                self.style.ERROR('Count must be between 1 and 100')
            )
            return

        self.stdout.write(
            self.style.SUCCESS(
                f'\nGenerating {count} institutional ID(s) for {account_type}(s)...\n'
            )
        )
        self.stdout.write(
            self.style.WARNING(
                f'Format: {"2XXXXXXX (students start with 2)" if account_type == "student" else "3XXXXXXX (staff start with 3)"}\n'
            )
        )

        created_ids = []
        for i in range(count):
            inst_id = generate_unique_institutional_id(account_type)
            
            obj = InstitutionalID.objects.create(
                institutional_id=inst_id,
                account_type=account_type,
                academic_level=academic_level if academic_level else None,
                department=department if department else None,
                status='active'
            )
            
            created_ids.append(inst_id)
            self.stdout.write(
                self.style.SUCCESS(f'  ✓ {inst_id}')
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Successfully generated {count} institutional ID(s)'
            )
        )
        self.stdout.write(
            self.style.WARNING(
                '\nUsers can now log in directly using these IDs.'
            )
        )
