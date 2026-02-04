"""
Management Command: update_seasons

Updates gamification season status (active/expired) and creates new seasons.
Replaces cron job with an idempotent, manually runnable command.

Usage:
    python manage.py update_seasons
    python manage.py update_seasons --create-next
    python manage.py update_seasons --verbose

This command:
- Marks expired seasons as inactive
- Activates upcoming seasons
- Optionally creates next season
- Is idempotent (safe to run multiple times)
- Logs all actions clearly

Setup as Cron Job (runs daily at 1 AM):
    0 1 * * * cd /path/to/backend && python manage.py update_seasons

TODO: When USE_ASYNC_TASKS=True:
    Convert to Celery periodic task for better scheduling
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Update gamification season status and create new seasons'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-next',
            action='store_true',
            help='Create next season automatically',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed progress',
        )

    def handle(self, *args, **options):
        self.verbose = options['verbose']
        create_next = options['create_next']
        
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('SEASON STATUS UPDATE'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(f'Current time: {timezone.now()}')
        self.stdout.write('')

        try:
            # Import here to avoid circular imports
            from apps.gamification.models import Season, Episode
            
            today = timezone.now().date()
            
            # Deactivate expired seasons
            expired = self.deactivate_expired_seasons(Season, today)
            
            # Activate upcoming seasons
            activated = self.activate_upcoming_seasons(Season, today)
            
            # Create next season if requested
            if create_next:
                self.create_next_season(Season, Episode, today)
            
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('✓ UPDATE COMPLETE'))
            self.stdout.write(f'  Expired: {expired}')
            self.stdout.write(f'  Activated: {activated}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n✗ ERROR: {str(e)}'))
            raise

    def deactivate_expired_seasons(self, Season, today):
        """Mark expired seasons as inactive"""
        expired_seasons = Season.objects.filter(
            is_active=True,
            end_date__lt=today
        )
        
        count = expired_seasons.count()
        
        if count > 0:
            with transaction.atomic():
                for season in expired_seasons:
                    season.is_active = False
                    season.save(update_fields=['is_active'])
                    
                    if self.verbose:
                        self.stdout.write(
                            f'  ✓ Deactivated: {season.name} (ended {season.end_date})'
                        )
            
            self.stdout.write(f'Deactivated {count} expired season(s)')
        else:
            self.stdout.write('No expired seasons to deactivate')
        
        return count

    def activate_upcoming_seasons(self, Season, today):
        """Activate seasons that should start today"""
        upcoming_seasons = Season.objects.filter(
            is_active=False,
            start_date__lte=today,
            end_date__gte=today
        )
        
        count = upcoming_seasons.count()
        
        if count > 0:
            with transaction.atomic():
                for season in upcoming_seasons:
                    season.is_active = True
                    season.save(update_fields=['is_active'])
                    
                    if self.verbose:
                        self.stdout.write(
                            f'  ✓ Activated: {season.name} (starts {season.start_date})'
                        )
            
            self.stdout.write(f'Activated {count} season(s)')
        else:
            self.stdout.write('No seasons to activate today')
        
        return count

    def create_next_season(self, Season, Episode, today):
        """Create next season if none exists"""
        # Get latest season
        latest_season = Season.objects.order_by('-season_number').first()
        
        if not latest_season:
            self.stdout.write(self.style.WARNING('No existing seasons found. Create first season manually.'))
            return
        
        # Check if next season already exists
        next_start = latest_season.end_date + timedelta(days=1)
        next_exists = Season.objects.filter(start_date=next_start).exists()
        
        if next_exists:
            self.stdout.write('Next season already exists')
            return
        
        # Create next season
        next_number = latest_season.season_number + 1
        next_end = next_start + timedelta(days=30)  # 1 month
        
        with transaction.atomic():
            new_season = Season.objects.create(
                name=f'Season {next_number}',
                season_number=next_number,
                start_date=next_start,
                end_date=next_end,
                is_active=False
            )
            
            # Create 4 episodes (1 week each)
            for i in range(1, 5):
                episode_start = next_start + timedelta(days=(i-1) * 7)
                episode_end = episode_start + timedelta(days=6)
                
                Episode.objects.create(
                    season=new_season,
                    episode_number=i,
                    name=f'Episode {i}',
                    start_date=episode_start,
                    end_date=episode_end
                )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Created: {new_season.name} ({next_start} to {next_end})'
                )
            )


# TODO: When Celery is enabled (USE_ASYNC_TASKS=True):
# 
# from celery import shared_task
# 
# @shared_task
# def update_seasons_task():
#     """Celery task wrapper"""
#     from django.core.management import call_command
#     call_command('update_seasons', '--create-next')
# 
# # In celery.py, add:
# from celery.schedules import crontab
# 
# app.conf.beat_schedule = {
#     'update-seasons-daily': {
#         'task': 'apps.gamification.tasks.update_seasons_task',
#         'schedule': crontab(hour=1, minute=0),  # Daily at 1 AM
#     },
# }
