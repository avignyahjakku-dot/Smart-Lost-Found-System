"""
Security & Hardening Test Suite
================================
Validates authentication, role-based authorization, IDOR protections,
session cookie hardening, XSS auto-escaping, and input boundary validation.
"""

import os
import unittest
from werkzeug.security import check_password_hash
from app import create_app
from app.config import ProductionConfig, DevelopmentConfig, TestingConfig
from app.db import query_db

class TestSecurity(unittest.TestCase):

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

    def test_password_hashing_and_complexity(self):
        """Passwords must be hashed securely, and short passwords (< 8 chars) rejected."""
        # 1. Attempt registration with short password (5 chars)
        res_short = self.client.post('/register', data={
            'full_name': 'Weak User',
            'email': 'weak@campusfind.edu',
            'password': 'short',
            'confirm_password': 'short'
        }, follow_redirects=True)
        self.assertIn(b"Password must be at least 8 characters long", res_short.data)

        # 2. Register valid password
        self.client.post('/register', data={
            'full_name': 'Secure User',
            'email': 'secure@campusfind.edu',
            'password': 'StrongPassword123!',
            'confirm_password': 'StrongPassword123!'
        })
        user = query_db("SELECT * FROM users WHERE email = %s", ('secure@campusfind.edu',), one=True)
        self.assertIsNotNone(user)
        # Ensure password is NOT stored in plaintext
        self.assertNotEqual(user['password_hash'], 'StrongPassword123!')
        # Ensure password hash is verified by werkzeug
        self.assertTrue(check_password_hash(user['password_hash'], 'StrongPassword123!'))

    def test_session_cookie_security_configurations(self):
        """Session cookies must enforce HttpOnly and SameSite=Lax, and Secure in Production."""
        self.assertTrue(self.app.config.get('SESSION_COOKIE_HTTPONLY'))
        self.assertEqual(self.app.config.get('SESSION_COOKIE_SAMESITE'), 'Lax')
        self.assertTrue(ProductionConfig.SESSION_COOKIE_SECURE)
        self.assertFalse(DevelopmentConfig.SESSION_COOKIE_SECURE)

    def test_idor_status_modification_prevention(self):
        """User B cannot alter the status of an item reported by User A."""
        # 1. User A reports an item
        self.client.post('/register', data={
            'full_name': 'Owner User',
            'email': 'owner@campusfind.edu',
            'password': 'Password123!',
            'confirm_password': 'Password123!'
        })
        self.client.post('/report/lost', data={
            'title': 'Owner Laptop',
            'category': 'Electronics & Gadgets',
            'location': 'Central Library',
            'item_date': '2026-10-24',
            'description': 'Owner description.'
        })
        item = query_db("SELECT id FROM items WHERE title = 'Owner Laptop'", one=True)
        self.client.get('/logout')

        # 2. User B logs in
        self.client.post('/register', data={
            'full_name': 'Attacker User',
            'email': 'attacker@campusfind.edu',
            'password': 'Password123!',
            'confirm_password': 'Password123!'
        })

        # User B attempts to change item status to 'resolved'
        res = self.client.post(f'/items/{item["id"]}/status', data={
            'status': 'resolved'
        }, follow_redirects=True)

        self.assertIn(b"You are not authorized to update this item", res.data)

        # Confirm item status in DB remains 'open'
        check_item = query_db("SELECT status FROM items WHERE id = %s", (item['id'],), one=True)
        self.assertEqual(check_item['status'], 'open')

    def test_sql_injection_resilience(self):
        """SQL injection payloads in searches and forms are safely handled as string literals."""
        sqli_payload = "' OR '1'='1' --"
        res = self.client.get(f'/browse?q={sqli_payload}')
        self.assertEqual(res.status_code, 200)
        # Should not crash or return unexpected syntax errors
        self.assertNotIn(b"OperationalError", res.data)
        self.assertNotIn(b"syntax error", res.data)

    def test_xss_auto_escaping(self):
        """XSS script payloads submitted in item reports are auto-escaped in HTML output."""
        self.client.post('/register', data={
            'full_name': 'XSS Tester',
            'email': 'xsstester@campusfind.edu',
            'password': 'Password123!',
            'confirm_password': 'Password123!'
        })
        xss_title = '<script>alert("xss")</script> Test Bag'
        self.client.post('/report/found', data={
            'title': xss_title,
            'category': 'Other Accessories',
            'location': 'Hostel Block A',
            'item_date': '2026-10-24',
            'storage_location': 'Desk',
            'description': 'Description with <b>HTML</b> test.'
        })
        item = query_db("SELECT id FROM items WHERE title = %s", (xss_title,), one=True)
        res = self.client.get(f'/items/{item["id"]}')

        # The literal tag <script> must NOT be executed raw; it must be escaped
        self.assertNotIn(b'<script>alert("xss")</script>', res.data)
        self.assertIn(b'&lt;script&gt;alert(&#34;xss&#34;)&lt;/script&gt;', res.data)

    def test_role_based_admin_protection(self):
        """Regular users and guests are denied access to admin control endpoints."""
        # Guest redirect
        res_guest = self.client.get('/admin/dashboard')
        self.assertEqual(res_guest.status_code, 302)
        self.assertIn('/login', res_guest.headers['Location'])

        # Regular student login
        self.client.post('/register', data={
            'full_name': 'Student Jane',
            'email': 'jane@campusfind.edu',
            'password': 'Password123!',
            'confirm_password': 'Password123!'
        })
        res_student = self.client.get('/admin/dashboard', follow_redirects=True)
        self.assertIn(b"Access denied: Administrator privileges required", res_student.data)

if __name__ == '__main__':
    unittest.main()
