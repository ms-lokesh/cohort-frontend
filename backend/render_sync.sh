#!/bin/bash
# Deploy sync script to Render and execute it
# This should be run from Render's shell

cd /opt/render/project/src/backend

echo "🔄 Running user mapping sync..."
python manage.py shell << 'PYTHON_EOF'
from django.contrib.auth.models import User
from apps.auth_supabase.models import SupabaseUserMapping
from supabase import create_client
import os

# Get Supabase credentials
url = os.environ.get('SUPABASE_URL')
key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')

if not url or not key:
    print("❌ Missing Supabase credentials")
    exit(1)

supabase = create_client(url, key)

# Get unmapped users
unmapped = User.objects.exclude(
    id__in=SupabaseUserMapping.objects.values_list('django_user_id', flat=True)
)

print(f"📊 Found {unmapped.count()} unmapped users")

# Get Supabase users
response = supabase.auth.admin.list_users()
supabase_users = {user.email.lower(): user.id for user in response if user.email}

print(f"📊 Found {len(supabase_users)} Supabase users")

# Create mappings
created = 0
for user in unmapped:
    email = user.email.lower()
    if email in supabase_users:
        try:
            SupabaseUserMapping.objects.create(
                django_user=user,
                supabase_id=supabase_users[email],
                supabase_email=email
            )
            created += 1
        except Exception as e:
            print(f"❌ Error for {email}: {e}")

print(f"✅ Created {created} mappings")

# Final status
total = User.objects.count()
mapped = SupabaseUserMapping.objects.count()
print(f"📈 Total users: {total}, Mapped: {mapped}")

PYTHON_EOF

echo "✅ Sync complete!"
