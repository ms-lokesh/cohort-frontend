from django.apps import AppConfig


class AuthSupabaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.auth_supabase'
    verbose_name = 'Supabase Authentication'
