# Generated manually for scaling optimizations
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_remove_floorannouncement_valid_floor_announcement_floor_range_and_more'),
    ]

    operations = [
        # Add indexes for UserProfile (performance for lookups by role, campus, floor)
        migrations.AddIndex(
            model_name='userprofile',
            index=models.Index(fields=['role', 'campus'], name='profiles_role_campus_idx'),
        ),
        migrations.AddIndex(
            model_name='userprofile',
            index=models.Index(fields=['assigned_mentor', 'role'], name='profiles_mentor_role_idx'),
        ),
        
        # Note: Notification model already has indexes from migration 0005
        # No additional indexes needed for profiles.Notification
        
        # Add indexes for FloorAnnouncement (performance for floor-specific announcements)
        migrations.AddIndex(
            model_name='floorannouncement',
            index=models.Index(fields=['campus', 'status', '-created_at'], name='floor_ann_campus_status_idx'),
        ),
    ]
