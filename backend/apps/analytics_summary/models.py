"""
Analytics Summary Models

These models store pre-computed analytics to improve performance at scale.
They coexist with the existing live analytics - nothing is removed.

CRITICAL: These models are ADDITIVE. All existing queries still work.
Dashboard views can switch between live and cached data using the
USE_ANALYTICS_SUMMARY feature flag.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class FloorAnalyticsSummary(models.Model):
    """
    Pre-computed analytics for a specific campus + floor combination.
    
    Updated by the `recompute_analytics` management command.
    Used when USE_ANALYTICS_SUMMARY=True in settings.
    """
    
    # Identification
    campus = models.CharField(max_length=10, db_index=True)  # TECH, ARTS
    floor = models.IntegerField(db_index=True)  # 1, 2, 3, 4
    
    # Student Metrics
    total_students = models.IntegerField(default=0)
    active_students = models.IntegerField(default=0)
    assigned_students = models.IntegerField(default=0)
    unassigned_students = models.IntegerField(default=0)
    
    # Mentor Metrics
    total_mentors = models.IntegerField(default=0)
    active_mentors = models.IntegerField(default=0)
    
    # Submission Metrics
    total_submissions = models.IntegerField(default=0)
    pending_reviews = models.IntegerField(default=0)
    approved_submissions = models.IntegerField(default=0)
    rejected_submissions = models.IntegerField(default=0)
    
    # Pillar Progress (0-100 percentages)
    clt_progress = models.FloatField(default=0.0)
    cfc_progress = models.FloatField(default=0.0)
    sri_progress = models.FloatField(default=0.0)
    iipc_progress = models.FloatField(default=0.0)
    scd_progress = models.FloatField(default=0.0)
    
    # Average Completion
    avg_completion = models.FloatField(default=0.0)
    
    # Metadata
    last_updated = models.DateTimeField(auto_now=True)
    computation_time_ms = models.IntegerField(default=0, help_text="Time taken to compute in milliseconds")
    
    class Meta:
        db_table = 'analytics_floor_summary'
        unique_together = [['campus', 'floor']]
        indexes = [
            models.Index(fields=['campus', 'floor']),
            models.Index(fields=['last_updated']),
        ]
        verbose_name = 'Floor Analytics Summary'
        verbose_name_plural = 'Floor Analytics Summaries'
        ordering = ['campus', 'floor']
    
    def __str__(self):
        return f"{self.campus} - Floor {self.floor} (Updated: {self.last_updated.strftime('%Y-%m-%d %H:%M')})"
    
    @property
    def is_stale(self):
        """Check if data is older than 10 minutes"""
        return (timezone.now() - self.last_updated).total_seconds() > 600


class MentorAnalyticsSummary(models.Model):
    """
    Pre-computed analytics for each mentor.
    
    Tracks workload, approval rates, and student progress.
    """
    
    mentor = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='analytics_summary',
        limit_choices_to={'profile__role': 'MENTOR'}
    )
    
    # Workload
    assigned_students_count = models.IntegerField(default=0)
    pending_reviews_count = models.IntegerField(default=0)
    total_reviews_completed = models.IntegerField(default=0)
    
    # Performance Metrics
    approval_rate = models.FloatField(default=0.0, help_text="Percentage of approved submissions")
    avg_review_time_hours = models.FloatField(default=0.0, help_text="Average time to review in hours")
    
    # Student Progress
    avg_student_completion = models.FloatField(default=0.0)
    students_at_risk = models.IntegerField(default=0, help_text="Students below 50% completion")
    
    # Activity
    last_active = models.DateTimeField(null=True, blank=True)
    reviews_this_week = models.IntegerField(default=0)
    reviews_this_month = models.IntegerField(default=0)
    
    # Workload Status (computed)
    WORKLOAD_LOW = 'low'
    WORKLOAD_BALANCED = 'balanced'
    WORKLOAD_HIGH = 'overloaded'
    WORKLOAD_CHOICES = [
        (WORKLOAD_LOW, 'Low'),
        (WORKLOAD_BALANCED, 'Balanced'),
        (WORKLOAD_HIGH, 'Overloaded'),
    ]
    workload_status = models.CharField(
        max_length=20,
        choices=WORKLOAD_CHOICES,
        default=WORKLOAD_BALANCED
    )
    
    # Metadata
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'analytics_mentor_summary'
        indexes = [
            models.Index(fields=['workload_status']),
            models.Index(fields=['last_updated']),
            models.Index(fields=['approval_rate']),
        ]
        verbose_name = 'Mentor Analytics Summary'
        verbose_name_plural = 'Mentor Analytics Summaries'
        ordering = ['-assigned_students_count']
    
    def __str__(self):
        return f"{self.mentor.get_full_name()} - {self.assigned_students_count} students ({self.workload_status})"
    
    def compute_workload_status(self):
        """
        Compute workload status based on student count and pending reviews.
        
        Low: <= 8 students
        Balanced: 9-15 students
        Overloaded: >= 16 students OR > 15 pending reviews
        """
        if self.assigned_students_count <= 8:
            return self.WORKLOAD_LOW
        elif self.assigned_students_count <= 15 and self.pending_reviews_count <= 15:
            return self.WORKLOAD_BALANCED
        else:
            return self.WORKLOAD_HIGH


class GlobalAnalyticsSummary(models.Model):
    """
    System-wide analytics across all campuses and floors.
    
    Used for admin dashboards and reporting.
    """
    
    # Date
    date = models.DateField(unique=True, db_index=True)
    
    # Global Counts
    total_students = models.IntegerField(default=0)
    total_mentors = models.IntegerField(default=0)
    total_submissions = models.IntegerField(default=0)
    
    # Daily Activity
    new_students_today = models.IntegerField(default=0)
    new_submissions_today = models.IntegerField(default=0)
    reviews_completed_today = models.IntegerField(default=0)
    
    # System Health
    avg_system_completion = models.FloatField(default=0.0)
    campuses_active = models.IntegerField(default=0)
    floors_active = models.IntegerField(default=0)
    
    # Performance
    avg_review_time_hours = models.FloatField(default=0.0)
    pending_reviews_count = models.IntegerField(default=0)
    
    # Metadata
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'analytics_global_summary'
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['last_updated']),
        ]
        verbose_name = 'Global Analytics Summary'
        verbose_name_plural = 'Global Analytics Summaries'
        ordering = ['-date']
    
    def __str__(self):
        return f"Global Analytics - {self.date}"


class AnalyticsComparisonLog(models.Model):
    """
    Validation log comparing live analytics vs cached analytics.
    
    Used to ensure cached data matches live data before switching.
    Helps identify discrepancies during the transition period.
    """
    
    entity_type = models.CharField(max_length=20, choices=[
        ('floor', 'Floor'),
        ('mentor', 'Mentor'),
        ('global', 'Global'),
    ])
    entity_id = models.CharField(max_length=100)  # e.g., "TECH-1" for floor, mentor ID
    
    # Comparison Results
    live_value = models.JSONField()
    cached_value = models.JSONField()
    matches = models.BooleanField(default=True)
    discrepancies = models.JSONField(null=True, blank=True)
    
    # Metadata
    checked_at = models.DateTimeField(auto_now_add=True)
    check_duration_ms = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'analytics_comparison_log'
        indexes = [
            models.Index(fields=['entity_type', 'checked_at']),
            models.Index(fields=['matches']),
        ]
        verbose_name = 'Analytics Comparison Log'
        verbose_name_plural = 'Analytics Comparison Logs'
        ordering = ['-checked_at']
    
    def __str__(self):
        status = "✓ Match" if self.matches else "✗ Mismatch"
        return f"{status} - {self.entity_type.title()} {self.entity_id}"
