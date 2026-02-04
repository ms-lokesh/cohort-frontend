from django.contrib import admin
from .models import (
    FloorAnalyticsSummary,
    MentorAnalyticsSummary,
    GlobalAnalyticsSummary,
    AnalyticsComparisonLog
)


@admin.register(FloorAnalyticsSummary)
class FloorAnalyticsSummaryAdmin(admin.ModelAdmin):
    list_display = [
        'campus', 'floor', 'total_students', 'total_mentors', 
        'avg_completion', 'pending_reviews', 'last_updated', 'is_stale'
    ]
    list_filter = ['campus', 'floor', 'last_updated']
    search_fields = ['campus']
    readonly_fields = ['last_updated', 'computation_time_ms']
    
    fieldsets = (
        ('Identification', {
            'fields': ('campus', 'floor')
        }),
        ('Student Metrics', {
            'fields': ('total_students', 'active_students', 'assigned_students', 'unassigned_students')
        }),
        ('Mentor Metrics', {
            'fields': ('total_mentors', 'active_mentors')
        }),
        ('Submission Metrics', {
            'fields': ('total_submissions', 'pending_reviews', 'approved_submissions', 'rejected_submissions')
        }),
        ('Pillar Progress', {
            'fields': ('clt_progress', 'cfc_progress', 'sri_progress', 'iipc_progress', 'scd_progress')
        }),
        ('Overall', {
            'fields': ('avg_completion',)
        }),
        ('Metadata', {
            'fields': ('last_updated', 'computation_time_ms')
        }),
    )


@admin.register(MentorAnalyticsSummary)
class MentorAnalyticsSummaryAdmin(admin.ModelAdmin):
    list_display = [
        'mentor', 'assigned_students_count', 'pending_reviews_count',
        'approval_rate', 'workload_status', 'last_active', 'last_updated'
    ]
    list_filter = ['workload_status', 'last_updated']
    search_fields = ['mentor__username', 'mentor__email', 'mentor__first_name', 'mentor__last_name']
    readonly_fields = ['last_updated']
    
    fieldsets = (
        ('Mentor', {
            'fields': ('mentor',)
        }),
        ('Workload', {
            'fields': ('assigned_students_count', 'pending_reviews_count', 'workload_status')
        }),
        ('Performance', {
            'fields': ('total_reviews_completed', 'approval_rate', 'avg_review_time_hours')
        }),
        ('Student Progress', {
            'fields': ('avg_student_completion', 'students_at_risk')
        }),
        ('Activity', {
            'fields': ('last_active', 'reviews_this_week', 'reviews_this_month')
        }),
        ('Metadata', {
            'fields': ('last_updated',)
        }),
    )


@admin.register(GlobalAnalyticsSummary)
class GlobalAnalyticsSummaryAdmin(admin.ModelAdmin):
    list_display = [
        'date', 'total_students', 'total_mentors', 'total_submissions',
        'avg_system_completion', 'pending_reviews_count', 'last_updated'
    ]
    list_filter = ['date']
    readonly_fields = ['last_updated']
    date_hierarchy = 'date'


@admin.register(AnalyticsComparisonLog)
class AnalyticsComparisonLogAdmin(admin.ModelAdmin):
    list_display = [
        'entity_type', 'entity_id', 'matches', 'checked_at', 'check_duration_ms'
    ]
    list_filter = ['entity_type', 'matches', 'checked_at']
    search_fields = ['entity_id']
    readonly_fields = ['checked_at', 'check_duration_ms']
    
    def has_add_permission(self, request):
        return False  # Logs are created automatically
