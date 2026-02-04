#!/usr/bin/env python3
"""
Environment Variables Validation Script
========================================
Validates that all required environment variables are properly set
for the current environment (development, staging, or production).

Usage:
    python validate_env.py                    # Check development environment
    python validate_env.py --env production   # Check production environment
    python validate_env.py --env staging      # Check staging environment
"""

import os
import sys
import argparse
from typing import List, Dict, Tuple


class EnvValidator:
    """Validates environment variables for different environments"""
    
    # Required variables for all environments
    REQUIRED_ALL = []
    
    # Required for production only
    REQUIRED_PRODUCTION = [
        'SECRET_KEY',
        'DATABASE_URL',
        'CORS_ALLOWED_ORIGINS',
        'JWT_SECRET_KEY',
    ]
    
    # Recommended for all environments
    RECOMMENDED_ALL = [
        'DEBUG',
        'ALLOWED_HOSTS',
    ]
    
    # Recommended for production
    RECOMMENDED_PRODUCTION = [
        'DJANGO_ENV',
        'JWT_ACCESS_TOKEN_LIFETIME_MINUTES',
        'JWT_REFRESH_TOKEN_LIFETIME_DAYS',
    ]
    
    # Variables that should NOT be set in production
    FORBIDDEN_PRODUCTION = [
        'TEST_ADMIN_PASSWORD',
        'TEST_MENTOR_PASSWORD',
        'TEST_STUDENT_PASSWORD',
        'TEST_FLOORWING_PASSWORD',
        'RAILWAY_DATABASE_URL',  # Only for migration scripts
    ]
    
    # Dangerous values that should never be used
    DANGEROUS_VALUES = {
        'SECRET_KEY': ['your-secret-key-here', 'dev-secret-key', 'change-me'],
        'JWT_SECRET_KEY': ['your-jwt-secret-key', 'change-me'],
        'DEBUG': ['True', 'true', '1'],  # Only dangerous in production
    }
    
    def __init__(self, environment='development'):
        self.environment = environment
        self.errors = []
        self.warnings = []
        self.info = []
    
    def validate(self) -> bool:
        """
        Run all validation checks.
        Returns True if validation passes, False otherwise.
        """
        print(f"\n{'='*60}")
        print(f"Environment Variables Validation - {self.environment.upper()}")
        print(f"{'='*60}\n")
        
        # Check required variables
        self._check_required_variables()
        
        # Check recommended variables
        self._check_recommended_variables()
        
        # Check for dangerous values
        self._check_dangerous_values()
        
        # Environment-specific checks
        if self.environment == 'production':
            self._check_production_specific()
        
        # Display results
        self._display_results()
        
        return len(self.errors) == 0
    
    def _check_required_variables(self):
        """Check that all required variables are set"""
        required = self.REQUIRED_ALL.copy()
        
        if self.environment == 'production':
            required.extend(self.REQUIRED_PRODUCTION)
        
        for var in required:
            value = os.getenv(var)
            if not value:
                self.errors.append(
                    f"❌ REQUIRED: {var} is not set"
                )
            elif value.strip() == '':
                self.errors.append(
                    f"❌ REQUIRED: {var} is empty"
                )
            else:
                self.info.append(
                    f"✅ {var} is set"
                )
    
    def _check_recommended_variables(self):
        """Check recommended variables"""
        recommended = self.RECOMMENDED_ALL.copy()
        
        if self.environment == 'production':
            recommended.extend(self.RECOMMENDED_PRODUCTION)
        
        for var in recommended:
            value = os.getenv(var)
            if not value:
                self.warnings.append(
                    f"⚠️  RECOMMENDED: {var} is not set (will use default)"
                )
            else:
                self.info.append(
                    f"✅ {var} is set"
                )
    
    def _check_dangerous_values(self):
        """Check for dangerous/default values"""
        for var, dangerous_vals in self.DANGEROUS_VALUES.items():
            value = os.getenv(var)
            if value:
                if var == 'DEBUG' and self.environment != 'production':
                    # DEBUG=True is OK in development
                    continue
                    
                if value in dangerous_vals:
                    self.errors.append(
                        f"❌ DANGEROUS: {var}='{value}' is a default/unsafe value"
                    )
    
    def _check_production_specific(self):
        """Production-specific checks"""
        # Check DEBUG is False
        debug_value = os.getenv('DEBUG', 'False')
        if debug_value.lower() in ('true', '1', 't', 'yes'):
            self.errors.append(
                "❌ SECURITY: DEBUG must be False in production"
            )
        
        # Check SECRET_KEY length
        secret_key = os.getenv('SECRET_KEY', '')
        if len(secret_key) < 50:
            self.errors.append(
                f"❌ SECURITY: SECRET_KEY too short ({len(secret_key)} chars, need 50+)"
            )
        
        # Check for test passwords
        for var in self.FORBIDDEN_PRODUCTION:
            if os.getenv(var):
                self.warnings.append(
                    f"⚠️  SECURITY: {var} should not be set in production"
                )
        
        # Check DATABASE_URL doesn't contain 'localhost' or '127.0.0.1'
        db_url = os.getenv('DATABASE_URL', '')
        if db_url:
            if 'localhost' in db_url or '127.0.0.1' in db_url:
                self.errors.append(
                    "❌ PRODUCTION: DATABASE_URL contains localhost/127.0.0.1"
                )
        
        # Check CORS_ALLOWED_ORIGINS doesn't contain localhost
        cors_origins = os.getenv('CORS_ALLOWED_ORIGINS', '')
        if cors_origins:
            if 'localhost' in cors_origins or '127.0.0.1' in cors_origins:
                self.warnings.append(
                    "⚠️  PRODUCTION: CORS_ALLOWED_ORIGINS contains localhost"
                )
    
    def _display_results(self):
        """Display validation results"""
        print()
        
        # Show errors
        if self.errors:
            print("ERRORS:")
            print("-" * 60)
            for error in self.errors:
                print(error)
            print()
        
        # Show warnings
        if self.warnings:
            print("WARNINGS:")
            print("-" * 60)
            for warning in self.warnings:
                print(warning)
            print()
        
        # Show info if verbose
        if not self.errors and not self.warnings:
            print("INFO:")
            print("-" * 60)
            for info_msg in self.info[:10]:  # Show first 10
                print(info_msg)
            if len(self.info) > 10:
                print(f"... and {len(self.info) - 10} more")
            print()
        
        # Summary
        print("SUMMARY:")
        print("-" * 60)
        print(f"Errors:   {len(self.errors)}")
        print(f"Warnings: {len(self.warnings)}")
        print(f"Checks:   {len(self.info)}")
        print()
        
        if self.errors:
            print("❌ VALIDATION FAILED")
            print("\nPlease fix the errors above before proceeding.")
            print(f"See backend/.env.example for required variables.\n")
            return False
        elif self.warnings:
            print("⚠️  VALIDATION PASSED WITH WARNINGS")
            print("\nConsider addressing the warnings above.\n")
            return True
        else:
            print("✅ VALIDATION PASSED")
            print(f"\nAll required environment variables are properly set for {self.environment}.\n")
            return True


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Validate environment variables for Django application'
    )
    parser.add_argument(
        '--env',
        choices=['development', 'staging', 'production'],
        default='development',
        help='Environment to validate (default: development)'
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Fail on warnings (not just errors)'
    )
    
    args = parser.parse_args()
    
    # Create validator
    validator = EnvValidator(environment=args.env)
    
    # Run validation
    success = validator.validate()
    
    # Exit with appropriate code
    if not success:
        sys.exit(1)
    elif args.strict and validator.warnings:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
