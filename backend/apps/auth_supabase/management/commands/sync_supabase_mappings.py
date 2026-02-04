"""
Django management command to sync Supabase user mappings
Run this on production: python manage.py sync_supabase_mappings
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.auth_supabase.models import SupabaseUserMapping
from supabase import create_client
import os


class Command(BaseCommand):
    help = 'Sync Django users with Supabase authentication users'

    def handle(self, *args, **options):
        self.stdout.write('\n🔄 SYNCING USER MAPPINGS')
        self.stdout.write('=' * 80)
        
        # Get Supabase credentials
        url = os.environ.get('SUPABASE_URL')
        key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
        
        if not url or not key:
            self.stdout.write(self.style.ERROR('❌ Missing Supabase credentials'))
            return
        
        # Get unmapped users
        unmapped = User.objects.exclude(
            id__in=SupabaseUserMapping.objects.values_list('django_user_id', flat=True)
        ).order_by('email')
        
        total_users = User.objects.count()
        already_mapped = SupabaseUserMapping.objects.count()
        
        self.stdout.write(f'📊 Total Django users: {total_users}')
        self.stdout.write(f'📊 Already mapped: {already_mapped}')
        self.stdout.write(f'📊 Need mapping: {unmapped.count()}\n')
        
        if unmapped.count() == 0:
            self.stdout.write(self.style.SUCCESS('✅ All users already mapped!'))
            return
        
        # Connect to Supabase
        try:
            supabase = create_client(url, key)
            self.stdout.write('📥 Fetching Supabase users...')
            response = supabase.auth.admin.list_users()
            supabase_users = {user.email.lower(): user.id for user in response if user.email}
            self.stdout.write(f'✅ Found {len(supabase_users)} Supabase users\n')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Failed to fetch Supabase users: {e}'))
            return
        
        # Create mappings
        created = 0
        not_found = 0
        errors = 0
        
        self.stdout.write('🔗 Creating mappings...\n')
        
        for i, user in enumerate(unmapped, 1):
            email = user.email.lower()
            
            # Show progress for first 5, every 10th, and last 5
            show_progress = i <= 5 or i % 10 == 0 or i > unmapped.count() - 5
            
            if show_progress:
                self.stdout.write(f'[{i}/{unmapped.count()}] {user.email}')
            
            if email in supabase_users:
                try:
                    SupabaseUserMapping.objects.create(
                        django_user=user,
                        supabase_id=supabase_users[email],
                        supabase_email=email
                    )
                    if show_progress:
                        self.stdout.write(self.style.SUCCESS('   ✅ Created mapping'))
                    created += 1
                except Exception as e:
                    if show_progress:
                        self.stdout.write(self.style.ERROR(f'   ❌ Error: {str(e)[:50]}'))
                    errors += 1
            else:
                if i <= 5:
                    self.stdout.write(self.style.WARNING('   ⚠️  Not found in Supabase'))
                not_found += 1
        
        # Summary
        self.stdout.write('\n' + '=' * 80)
        self.stdout.write('📊 SYNC SUMMARY')
        self.stdout.write('=' * 80)
        self.stdout.write(self.style.SUCCESS(f'✅ Mappings created: {created}'))
        self.stdout.write(self.style.WARNING(f'⚠️  Users not in Supabase: {not_found}'))
        if errors > 0:
            self.stdout.write(self.style.ERROR(f'❌ Errors: {errors}'))
        self.stdout.write('=' * 80)
        
        # Final status
        total_mapped = SupabaseUserMapping.objects.count()
        remaining = total_users - total_mapped
        
        self.stdout.write(f'\n📈 FINAL STATUS')
        self.stdout.write(f'   Total users: {total_users}')
        self.stdout.write(f'   Mapped: {total_mapped}')
        self.stdout.write(f'   Remaining: {remaining}')
        
        if remaining == 0:
            self.stdout.write(self.style.SUCCESS('\n🎉 All users are now mapped! Users can login.'))
        else:
            self.stdout.write(self.style.WARNING(f'\n⚠️  {remaining} users still need Supabase accounts'))
