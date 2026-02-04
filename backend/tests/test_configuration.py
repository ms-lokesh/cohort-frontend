"""
Configuration Tests
===================
Tests for centralized configuration system.
"""

import os
import sys
import unittest
from unittest.mock import patch

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__))))


class TestConfigTests(unittest.TestCase):
    """Tests for backend test_config.py"""
    
    def test_get_test_password_returns_value(self):
        """Test that get_test_password returns a value"""
        from test_config import get_test_password
        
        password = get_test_password('admin')
        self.assertIsNotNone(password)
        self.assertIsInstance(password, str)
        self.assertGreater(len(password), 0)
    
    def test_get_test_password_types(self):
        """Test all user types have passwords"""
        from test_config import get_test_password
        
        user_types = ['admin', 'mentor', 'student', 'floorwing', 'testuser', 'default']
        
        for user_type in user_types:
            password = get_test_password(user_type)
            self.assertIsNotNone(password, f"Password for {user_type} should not be None")
            self.assertGreater(len(password), 5, f"Password for {user_type} should be > 5 chars")
    
    def test_get_test_email(self):
        """Test email generation"""
        from test_config import get_test_email
        
        email = get_test_email('testuser')
        self.assertIsNotNone(email)
        self.assertIn('@', email)
        self.assertTrue(email.startswith('testuser@'))
    
    def test_get_test_email_custom_domain(self):
        """Test email generation with custom domain"""
        from test_config import get_test_email
        
        email = get_test_email('admin', 'example.com')
        self.assertEqual(email, 'admin@example.com')
    
    def test_get_test_user_data(self):
        """Test complete user data generation"""
        from test_config import get_test_user_data
        
        user_data = get_test_user_data('student', 1)
        
        self.assertIn('username', user_data)
        self.assertIn('email', user_data)
        self.assertIn('password', user_data)
        self.assertIn('first_name', user_data)
        self.assertIn('last_name', user_data)
        self.assertIn('role', user_data)
        
        self.assertEqual(user_data['role'], 'student')
        self.assertIn('@', user_data['email'])
    
    @patch.dict(os.environ, {'RAILWAY_DATABASE_URL': 'postgresql://test'})
    def test_validate_railway_db_with_env(self):
        """Test Railway DB validation with env var set"""
        from test_config import validate_railway_db
        
        # Reload module to pick up new env var
        import test_config
        import importlib
        importlib.reload(test_config)
        
        result = test_config.validate_railway_db()
        self.assertTrue(result)
    
    @patch.dict(os.environ, {}, clear=True)
    def test_validate_railway_db_without_env(self):
        """Test Railway DB validation without env var"""
        # Reload module to pick up cleared env
        import test_config
        import importlib
        
        # Save original
        original_railway_db = test_config.RAILWAY_DB_URL
        
        # Clear it
        test_config.RAILWAY_DB_URL = None
        
        result = test_config.validate_railway_db()
        
        # Restore
        test_config.RAILWAY_DB_URL = original_railway_db
        
        self.assertFalse(result)
    
    def test_default_passwords_structure(self):
        """Test DEFAULT_PASSWORDS dictionary structure"""
        from test_config import DEFAULT_PASSWORDS
        
        expected_keys = ['admin', 'mentor', 'student', 'floorwing', 'testuser', 'default']
        
        for key in expected_keys:
            self.assertIn(key, DEFAULT_PASSWORDS)
            self.assertIsInstance(DEFAULT_PASSWORDS[key], str)
            self.assertGreater(len(DEFAULT_PASSWORDS[key]), 0)


class EnvironmentVariablesTests(unittest.TestCase):
    """Tests for environment variable handling"""
    
    @patch.dict(os.environ, {'TEST_ADMIN_PASSWORD': 'custom_admin_pass'})
    def test_custom_admin_password(self):
        """Test that custom password from env var is used"""
        # Reload test_config to pick up new env var
        import test_config
        import importlib
        importlib.reload(test_config)
        
        password = test_config.get_test_password('admin')
        self.assertEqual(password, 'custom_admin_pass')
    
    @patch.dict(os.environ, {'TEST_EMAIL_DOMAIN': 'custom.com'})
    def test_custom_email_domain(self):
        """Test that custom email domain from env var is used"""
        import test_config
        import importlib
        importlib.reload(test_config)
        
        email = test_config.get_test_email('user')
        self.assertTrue(email.endswith('@custom.com'))


class SecurityTests(unittest.TestCase):
    """Security-related configuration tests"""
    
    @patch.dict(os.environ, {'DJANGO_ENV': 'production'})
    def test_production_warning(self):
        """Test that importing test_config in production shows warning"""
        import warnings
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            import test_config
            import importlib
            importlib.reload(test_config)
            
            # Check if warning was raised
            self.assertTrue(
                any("production" in str(warning.message).lower() for warning in w),
                "Should warn when test_config imported in production"
            )
    
    def test_passwords_not_empty(self):
        """Test that default passwords are not empty"""
        from test_config import DEFAULT_PASSWORDS
        
        for user_type, password in DEFAULT_PASSWORDS.items():
            self.assertIsNotNone(password, f"{user_type} password should not be None")
            self.assertNotEqual(password, '', f"{user_type} password should not be empty")
            self.assertGreater(len(password), 3, f"{user_type} password should be > 3 chars")


def run_tests():
    """Run all configuration tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestConfigTests))
    suite.addTests(loader.loadTestsFromTestCase(EnvironmentVariablesTests))
    suite.addTests(loader.loadTestsFromTestCase(SecurityTests))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
