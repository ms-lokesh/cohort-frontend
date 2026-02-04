"""
File Storage Abstraction

Provides a unified interface for file uploads that works locally
and can be switched to cloud storage via feature flag.

CRITICAL: Existing file uploads continue to work unchanged.
This module adds a parallel path for future cloud storage.
"""

from django.core.files.storage import default_storage
from django.conf import settings
from django.core.files.base import ContentFile
import os


class FileStorageService:
    """
    Unified file storage service that abstracts local vs cloud storage.
    
    Usage:
        storage = FileStorageService()
        url = storage.save_file(file, 'submissions/student123.pdf')
        file_obj = storage.get_file('submissions/student123.pdf')
        storage.delete_file('submissions/student123.pdf')
    
    When USE_CLOUD_STORAGE=False (default):
        - Uses Django's default FileSystemStorage
        - Files stored in MEDIA_ROOT
        - Works exactly as before
    
    When USE_CLOUD_STORAGE=True (production):
        - Uses AWS S3 (via django-storages)
        - Files stored in S3 bucket
        - URLs served from CloudFront/S3
    """
    
    def __init__(self):
        self.storage = default_storage
        self.using_cloud = settings.USE_CLOUD_STORAGE
    
    def save_file(self, file_obj, path):
        """
        Save a file to storage (local or cloud)
        
        Args:
            file_obj: File object (UploadedFile or File-like)
            path: Relative path within storage (e.g., 'submissions/file.pdf')
        
        Returns:
            str: URL to access the file
        
        Example:
            url = storage.save_file(request.FILES['certificate'], 'clt/cert123.pdf')
        """
        # Save file using Django's storage backend
        saved_path = self.storage.save(path, file_obj)
        
        # Get URL (works for both local and cloud)
        url = self.storage.url(saved_path)
        
        return url
    
    def get_file(self, path):
        """
        Retrieve a file from storage
        
        Args:
            path: Relative path within storage
        
        Returns:
            File object or None if not found
        """
        if self.storage.exists(path):
            return self.storage.open(path, 'rb')
        return None
    
    def delete_file(self, path):
        """
        Delete a file from storage
        
        Args:
            path: Relative path within storage
        
        Returns:
            bool: True if deleted, False if file didn't exist
        """
        if self.storage.exists(path):
            self.storage.delete(path)
            return True
        return False
    
    def file_exists(self, path):
        """
        Check if a file exists in storage
        
        Args:
            path: Relative path within storage
        
        Returns:
            bool: True if file exists
        """
        return self.storage.exists(path)
    
    def get_file_size(self, path):
        """
        Get size of a file in bytes
        
        Args:
            path: Relative path within storage
        
        Returns:
            int: File size in bytes, or None if file doesn't exist
        """
        if self.storage.exists(path):
            return self.storage.size(path)
        return None
    
    def get_file_url(self, path):
        """
        Get URL to access a file
        
        Args:
            path: Relative path within storage
        
        Returns:
            str: URL to file (local or cloud)
        
        Note: Always use this method to get URLs. Never construct URLs manually.
        """
        if self.storage.exists(path):
            return self.storage.url(path)
        return None
    
    def list_files(self, directory):
        """
        List all files in a directory
        
        Args:
            directory: Directory path
        
        Returns:
            list: List of file paths
        """
        try:
            _, files = self.storage.listdir(directory)
            return files
        except Exception:
            return []
    
    def generate_filename(self, original_filename, prefix=''):
        """
        Generate a unique filename to avoid collisions
        
        Args:
            original_filename: Original file name
            prefix: Optional prefix (e.g., 'clt_', 'student123_')
        
        Returns:
            str: Unique filename
        """
        import uuid
        from pathlib import Path
        
        # Get file extension
        ext = Path(original_filename).suffix
        
        # Generate unique name
        unique_name = f"{prefix}{uuid.uuid4().hex}{ext}"
        
        return unique_name


# Convenience functions for backward compatibility
def save_uploaded_file(file_obj, subfolder, filename=None):
    """
    Helper function to save uploaded files
    
    BACKWARD COMPATIBLE: Works with existing code
    
    Args:
        file_obj: Uploaded file object
        subfolder: Subfolder within MEDIA_ROOT (e.g., 'clt_files')
        filename: Optional custom filename
    
    Returns:
        str: URL to saved file
    """
    storage = FileStorageService()
    
    if filename is None:
        filename = storage.generate_filename(file_obj.name)
    
    path = os.path.join(subfolder, filename)
    return storage.save_file(file_obj, path)


def get_file_url(file_path):
    """
    Get URL for a file path
    
    BACKWARD COMPATIBLE: Works with existing code
    
    Args:
        file_path: Relative path to file
    
    Returns:
        str: URL to access file
    """
    storage = FileStorageService()
    return storage.get_file_url(file_path)


def delete_file(file_path):
    """
    Delete a file
    
    BACKWARD COMPATIBLE: Works with existing code
    
    Args:
        file_path: Relative path to file
    
    Returns:
        bool: True if deleted
    """
    storage = FileStorageService()
    return storage.delete_file(file_path)


# TODO: When enabling cloud storage (USE_CLOUD_STORAGE=True):
# 1. Install dependencies: pip install django-storages boto3
# 2. Add 'storages' to INSTALLED_APPS in settings.py
# 3. Configure AWS settings in settings.py (see commented section)
# 4. Set environment variables:
#    - AWS_ACCESS_KEY_ID
#    - AWS_SECRET_ACCESS_KEY
#    - AWS_STORAGE_BUCKET_NAME
#    - AWS_S3_REGION_NAME
# 5. Test locally with MinIO (S3-compatible) before using AWS
# 6. Migrate existing files: python manage.py migrate_files_to_s3
