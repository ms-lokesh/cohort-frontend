from django.contrib import admin
from .models import SupabaseUserMapping


class SupabaseUserMappingAdmin(admin.ModelAdmin):
    list_display = ('django_user', 'supabase_id_short', 'supabase_email', 
                    'is_active', 'last_login_at', 'created_at')
    list_filter = ('is_active', 'created_at', 'last_login_at')
    search_fields = ('django_user__username', 'django_user__email', 
                     'supabase_email', 'supabase_id')
    readonly_fields = ('created_at', 'updated_at', 'last_login_at')
    
    def supabase_id_short(self, obj):
        """Display shortened Supabase ID"""
        return f'{obj.supabase_id[:8]}...' if obj.supabase_id else '-'
    supabase_id_short.short_description = 'Supabase ID'


admin.site.register(SupabaseUserMapping, SupabaseUserMappingAdmin)
