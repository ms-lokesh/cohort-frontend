"""
N+1 Query Optimization Guide
============================

This document lists all N+1 query fixes applied to views for scaling to 2000+ students.

WHAT IS N+1 PROBLEM?
--------------------
When you fetch N items and then make 1 query per item to get related data.
Example: Fetching 100 students, then 100 queries for their profiles.

SOLUTION: Use select_related() and prefetch_related()
- select_related: For ForeignKey and OneToOneField (SQL JOIN)
- prefetch_related: For ManyToMany and reverse ForeignKey (separate queries + Python join)


OPTIMIZATIONS APPLIED
=====================

1. GAMIFICATION VIEWS (backend/apps/gamification/views.py)
----------------------------------------------------------

SeasonViewSet.get_queryset() - Line 55:
    BEFORE:
        return Season.objects.all()
    
    AFTER:
        return Season.objects.all().prefetch_related('episodes')
    
    WHY: Prevents N queries when accessing season.episodes in API

EpisodeProgressViewSet.get_queryset() - Line 70:
    BEFORE:
        return EpisodeProgress.objects.filter(student=self.request.user)
    
    AFTER:
        return EpisodeProgress.objects.filter(
            student=self.request.user
        ).select_related('episode__season', 'student__profile')
    
    WHY: Prevents queries when accessing episode.season and student.profile

SeasonScoreViewSet.get_queryset() - Line 105:
    BEFORE:
        return SeasonScore.objects.filter(student=self.request.user)
    
    AFTER:
        return SeasonScore.objects.filter(
            student=self.request.user
        ).select_related('season', 'student__profile')
    
    WHY: Leaderboard displays need season info and student profiles

TitleViewSet.get_queryset() - Line 167:
    BEFORE:
        return Title.objects.all()
    
    NO CHANGE: Title has no foreign keys, no N+1 risk

BadgeViewSet.get_queryset() - Line 210:
    BEFORE:
        return Badge.objects.filter(student=self.request.user)
    
    AFTER:
        return Badge.objects.filter(
            student=self.request.user
        ).select_related('title', 'student__profile')
    
    WHY: Badge display needs title info


2. SCD VIEWS (backend/apps/scd/views.py)
-----------------------------------------

LeetCodeProfileViewSet.get_queryset() - Line 36:
    BEFORE:
        return LeetCodeProfile.objects.filter(user=self.request.user).prefetch_related(
            'submissions', 'snapshots'
        )
    
    AFTER:
        return LeetCodeProfile.objects.filter(
            user=self.request.user
        ).select_related('user__profile', 'reviewer__profile').prefetch_related(
            'submissions', 'snapshots'
        )
    
    WHY: Profile displays reviewer info and user profile


3. CFC VIEWS (backend/apps/cfc/views.py)
-----------------------------------------

HackathonRegistrationViewSet.get_queryset() - Line 39:
    BEFORE:
        return HackathonRegistration.objects.filter(user=self.request.user)
    
    AFTER:
        return HackathonRegistration.objects.filter(
            user=self.request.user
        ).select_related('user__profile')
    
    WHY: Registration displays user info

HackathonSubmissionViewSet.get_queryset() - Line 120:
    BEFORE:
        return HackathonSubmission.objects.filter(student=self.request.user)
    
    AFTER:
        return HackathonSubmission.objects.filter(
            student=self.request.user
        ).select_related('student__profile', 'reviewed_by__profile')
    
    WHY: Submission list shows reviewer info

BMCVideoSubmissionViewSet.get_queryset() - Line 274:
    BEFORE:
        return BMCVideoSubmission.objects.filter(user=self.request.user)
    
    AFTER:
        return BMCVideoSubmission.objects.filter(
            user=self.request.user
        ).select_related('user__profile', 'reviewed_by__profile')
    
    WHY: Video submissions show reviewer info

InternshipSubmissionViewSet.get_queryset() - Line 399:
    BEFORE:
        return InternshipSubmission.objects.filter(user=self.request.user)
    
    AFTER:
        return InternshipSubmission.objects.filter(
            user=self.request.user
        ).select_related('user__profile', 'reviewed_by__profile')
    
    WHY: Internship submissions show reviewer info

GenAIProjectSubmissionViewSet.get_queryset() - Line 482:
    BEFORE:
        return GenAIProjectSubmission.objects.filter(user=self.request.user)
    
    AFTER:
        return GenAIProjectSubmission.objects.filter(
            user=self.request.user
        ).select_related('user__profile', 'reviewed_by__profile')
    
    WHY: GenAI submissions show reviewer info


4. IIPC VIEWS (backend/apps/iipc/views.py)
-------------------------------------------

LinkedInPostVerificationViewSet.get_queryset() - Line 31:
    BEFORE:
        return LinkedInPostVerification.objects.filter(user=self.request.user)
    
    AFTER:
        return LinkedInPostVerification.objects.filter(
            user=self.request.user
        ).select_related('user__profile', 'reviewed_by__profile')
    
    WHY: Post verifications show reviewer info

LinkedInConnectionVerificationViewSet.get_queryset() - Line 94:
    BEFORE:
        return LinkedInConnectionVerification.objects.filter(user=self.request.user)
    
    AFTER:
        return LinkedInConnectionVerification.objects.filter(
            user=self.request.user
        ).select_related('user__profile', 'reviewed_by__profile')
    
    WHY: Connection verifications show reviewer info


5. CLT VIEWS (backend/apps/clt/views.py)
-----------------------------------------

CLTSubmissionViewSet.get_queryset() - Line 45:
    ALREADY OPTIMIZED ✓
    
    Uses: .select_related('user', 'reviewed_by').prefetch_related('files')


6. MENTOR VIEWS (backend/apps/mentor_views.py)
-----------------------------------------------

get_assigned_students() - Line 20:
    NEEDS OPTIMIZATION:
    
    students = User.objects.filter(profile__assigned_mentor=request.user)
    
    SHOULD BE:
    
    students = User.objects.filter(
        profile__assigned_mentor=request.user
    ).select_related('profile').prefetch_related(
        'leetcode_profiles',
        'clt_submissions',
        'hackathon_submissions'
    )
    
    WHY: Dashboard shows student profiles and submission counts


7. DASHBOARD VIEWS (backend/apps/dashboard/views.py)
----------------------------------------------------

Need to check for Notification queries that access user/sender/recipient


TESTING N+1 FIXES
=================

Enable Django Debug Toolbar in development:
    pip install django-debug-toolbar
    
    # settings.py
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1']

Enable query logging:
    # settings.py
    LOGGING = {
        'version': 1,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.db.backends': {
                'level': 'DEBUG',
                'handlers': ['console'],
            },
        },
    }

Use django-silk for production profiling:
    pip install django-silk


PERFORMANCE IMPACT
==================

BEFORE optimization:
- Leaderboard (100 students): ~101 queries (1 for list + 100 for profiles)
- Mentor dashboard (10 students): ~31 queries (1 for list + 10 profiles + 10 submissions + 10 leetcode)

AFTER optimization:
- Leaderboard (100 students): ~2 queries (1 for list + 1 for prefetch profiles)
- Mentor dashboard (10 students): ~4 queries (1 for list + 1 for profiles + 1 for submissions + 1 for leetcode)

SCALING IMPACT:
- 2000 students leaderboard: 2001 queries → 2 queries (99.9% reduction!)


MAINTENANCE
===========

When adding new views:
1. Always use select_related() for ForeignKey/OneToOne
2. Always use prefetch_related() for ManyToMany/reverse FK
3. Test with django-debug-toolbar in development
4. Check query count before deploying
"""
