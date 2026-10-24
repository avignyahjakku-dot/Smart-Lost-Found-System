"""
Unit & Integration Tests: Authentication & Authorization
========================================================
Validates user registration, password hashing, session cookies,
and role-based admin route protection.
"""

import os
import unittest
from app import create_app
from app.db import execute_db, query_db

class TestAuth(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()
        db_path = self.app.config.get('SQLITE_PATH')
        if db_path and os.path.exists(db_path):
            try:
                os.remove(db_path)
            except PermissionError:
                pass

    def test_user_registration_success(self):
        """A new student should be registered, hashed, and auto-logged-in."""
        res = self.client.post('/register', data={
            'full_name': 'Sarah Connor',
            'email': 'sarah@campusfind.edu',
            'student_id': '22BCE9999',
            'phone': '1234567890',
            'role': 'student',
            'password': 'Password123',
            'confirm_password': 'Password123'
        }, follow_redirects=True)

        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Welcome to CampusFind", res.data)

        # Verify password in database is hashed, not plaintext
        user = query_db("SELECT * FROM users WHERE email = %s", ('sarah@campusfind.edu',), one=True)
        self.assertIsNotNone(user)
        self.assertEqual(user['full_name'], 'Sarah Connor')
        self.assertNotEqual(user['password_hash'], 'Password123')
        self.assertTrue(user['password_hash'].startswith('scrypt:') or user['password_hash'].startswith('pbkdf2:'))

    def test_duplicate_email_registration_blocked(self):
        """Registering with an existing email should fail."""
        self.client.post('/register', data={
            'full_name': 'Original User',
            'email': 'duplicate@campusfind.edu',
            'password': 'Password123',
            'confirm_password': 'Password123'
        })
        # Log out so subsequent request simulates a new visitor registering
        self.client.get('/logout')

        res = self.client.post('/register', data={
            'full_name': 'Clone User',
            'email': 'duplicate@campusfind.edu',
            'password': 'DifferentPass123',
            'confirm_password': 'DifferentPass123'
        }, follow_redirects=True)

        self.assertIn(b"already exists", res.data)

    def test_login_and_logout_flow(self):
        """Test valid credentials, invalid credentials, and logout."""
        # 1. Register account
        self.client.post('/register', data={
            'full_name': 'John Doe',
            'email': 'john@campusfind.edu',
            'password': 'SecretPassword123',
            'confirm_password': 'SecretPassword123'
        })

        # 2. Logout
        self.client.get('/logout', follow_redirects=True)

        # 3. Invalid login attempt
        res_fail = self.client.post('/login', data={
            'email': 'john@campusfind.edu',
            'password': 'WrongPassword'
        }, follow_redirects=True)
        self.assertIn(b"Invalid email or password", res_fail.data)

        # 4. Valid login attempt
        res_ok = self.client.post('/login', data={
            'email': 'john@campusfind.edu',
            'password': 'SecretPassword123'
        }, follow_redirects=True)
        self.assertIn(b"Welcome back, John Doe", res_ok.data)

    def test_admin_route_protection(self):
        """Unauthenticated and non-admin users must be forbidden from accessing /admin."""
        # Unauthenticated access -> redirected to login
        res_anon = self.client.get('/admin/dashboard')
        self.assertEqual(res_anon.status_code, 302)
        self.assertIn('/login', res_anon.headers['Location'])

        # Log in as a normal student
        self.client.post('/register', data={
            'full_name': 'Student User',
            'email': 'student@campusfind.edu',
            'role': 'student',
            'password': 'StudentPassword',
            'confirm_password': 'StudentPassword'
        })
        res_student = self.client.get('/admin/dashboard', follow_redirects=True)
        self.assertIn(b"Access denied", res_student.data)

        # Log out and log in as default seeded Administrator
        self.client.get('/logout')
        self.client.post('/login', data={
            'email': self.app.config['DEFAULT_ADMIN_EMAIL'],
            'password': self.app.config['DEFAULT_ADMIN_PASSWORD']
        })
        res_admin = self.client.get('/admin/dashboard')
        self.assertEqual(res_admin.status_code, 200)
        self.assertIn(b"Campus Administration Dashboard", res_admin.data)

    def test_registration_validation_failures(self):
        """Registration rejects missing fields, mismatched passwords, and oversized names."""
        # 1. Missing name
        res_no_name = self.client.post('/register', data={
            'full_name': '',
            'email': 'noname@campusfind.edu',
            'password': 'Password123!',
            'confirm_password': 'Password123!'
        }, follow_redirects=True)
        self.assertIn(b"Please fill in all required fields", res_no_name.data)

        # 2. Password mismatch
        res_mismatch = self.client.post('/register', data={
            'full_name': 'Mismatch User',
            'email': 'mismatch@campusfind.edu',
            'password': 'Password123!',
            'confirm_password': 'DifferentPassword456!'
        }, follow_redirects=True)
        self.assertIn(b"Passwords do not match", res_mismatch.data)

        # 3. Oversized name (> 100 characters)
        res_long_name = self.client.post('/register', data={
            'full_name': 'A' * 105,
            'email': 'longname@campusfind.edu',
            'password': 'Password123!',
            'confirm_password': 'Password123!'
        }, follow_redirects=True)
        self.assertIn(b"Full name cannot exceed 100 characters", res_long_name.data)

if __name__ == '__main__':
    unittest.main()
