"""
Supabase Integration for Django
Handles database connection, authentication, and storage
"""
import os
from supabase import create_client, Client
from typing import Optional

class SupabaseService:
    """Singleton service for Supabase operations"""
    
    _instance: Optional[Client] = None
    
    @classmethod
    def get_client(cls) -> Client:
        """Get or create Supabase client"""
        if cls._instance is None:
            supabase_url = os.getenv('SUPABASE_URL')
            supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
            
            if not supabase_url or not supabase_key:
                raise ValueError(
                    "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in environment variables"
                )
            
            cls._instance = create_client(supabase_url, supabase_key)
        
        return cls._instance
    
    @classmethod
    def upload_file(cls, bucket: str, file_path: str, file_data: bytes) -> dict:
        """
        Upload file to Supabase Storage
        
        Args:
            bucket: Storage bucket name
            file_path: Path within bucket
            file_data: File content as bytes
        
        Returns:
            dict with upload result
        """
        client = cls.get_client()
        result = client.storage.from_(bucket).upload(file_path, file_data)
        return result
    
    @classmethod
    def get_public_url(cls, bucket: str, file_path: str) -> str:
        """
        Get public URL for a file in Supabase Storage
        
        Args:
            bucket: Storage bucket name
            file_path: Path within bucket
        
        Returns:
            Public URL string
        """
        client = cls.get_client()
        result = client.storage.from_(bucket).get_public_url(file_path)
        return result
    
    @classmethod
    def delete_file(cls, bucket: str, file_path: str) -> dict:
        """
        Delete file from Supabase Storage
        
        Args:
            bucket: Storage bucket name
            file_path: Path within bucket
        
        Returns:
            dict with deletion result
        """
        client = cls.get_client()
        result = client.storage.from_(bucket).remove([file_path])
        return result


class SupabaseAuthBackend:
    """
    Django authentication backend using Supabase
    Allows JWT token validation from Supabase Auth
    """
    
    def authenticate(self, request, token=None):
        """
        Authenticate user with Supabase JWT token
        
        Args:
            request: Django request object
            token: JWT token from Supabase Auth
        
        Returns:
            User object if authentication successful, None otherwise
        """
        if not token:
            return None
        
        try:
            from django.contrib.auth.models import User
            
            client = SupabaseService.get_client()
            
            # Verify token with Supabase
            response = client.auth.get_user(token)
            
            if not response.user:
                return None
            
            supabase_user = response.user
            
            # Get or create Django user
            user, created = User.objects.get_or_create(
                email=supabase_user.email,
                defaults={
                    'username': supabase_user.email.split('@')[0],
                    'is_active': True,
                }
            )
            
            return user
            
        except Exception as e:
            print(f"Supabase authentication error: {e}")
            return None
    
    def get_user(self, user_id):
        """Get user by ID"""
        from django.contrib.auth.models import User
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


# Helper function for views
def get_supabase_user_from_request(request):
    """
    Extract Supabase user from request Authorization header
    
    Args:
        request: Django request object
    
    Returns:
        Supabase user object or None
    """
    auth_header = request.headers.get('Authorization', '')
    
    if not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.replace('Bearer ', '')
    
    try:
        client = SupabaseService.get_client()
        response = client.auth.get_user(token)
        return response.user if response else None
    except Exception as e:
        print(f"Error getting Supabase user: {e}")
        return None
