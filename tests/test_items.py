"""
Unit & Integration Tests: Item Reporting and Browsing
=====================================================
Validates lost item submission, found item logging,
catalog search filtering, and status updates.
"""

import os
import unittest
from app import create_app
from app.db import query_db

class TestItems(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

        # Create a test student account and log in
        self.client.post('/register', data={
            'full_name': 'Test Reporter',
            'email': 'reporter@campusfind.edu',
            'password': 'Password123',
            'confirm_password': 'Password123'
        })

    def tearDown(self):
        self.ctx.pop()
        db_path = self.app.config.get('SQLITE_PATH')
        if db_path and os.path.exists(db_path):
            try:
                os.remove(db_path)
            except PermissionError:
                pass

    def test_report_lost_item(self):
        """User can successfully report a lost item."""
        res = self.client.post('/report/lost', data={
            'title': 'Blue Hydro Flask 32oz',
            'category': 'Bottles & Tumblers',
            'location': 'Central Library',
            'item_date': '2026-10-24',
            'description': 'Cobalt blue bottle with a slight dent on the base.',
            'secret_hint': 'What color is the silicone boot?'
        }, follow_redirects=True)

        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Blue Hydro Flask 32oz", res.data)

        # Check DB
        item = query_db("SELECT * FROM items WHERE title = %s", ('Blue Hydro Flask 32oz',), one=True)
        self.assertIsNotNone(item)
        self.assertEqual(item['type'], 'lost')
        self.assertEqual(item['status'], 'open')
        self.assertEqual(item['secret_hint'], 'What color is the silicone boot?')

    def test_report_found_item(self):
        """User can report a found item with physical storage custody info."""
        res = self.client.post('/report/found', data={
            'title': 'Casio FX-991EX Calculator',
            'category': 'Electronics & Gadgets',
            'location': 'Computer Science Department',
            'item_date': '2026-10-24',
            'storage_location': 'CS Dept Office Desk 3',
            'description': 'Scientific calculator found in Lab 2.'
        }, follow_redirects=True)

        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Casio FX-991EX Calculator", res.data)

        item = query_db("SELECT * FROM items WHERE title = %s", ('Casio FX-991EX Calculator',), one=True)
        self.assertIsNotNone(item)
        self.assertEqual(item['type'], 'found')
        self.assertEqual(item['storage_location'], 'CS Dept Office Desk 3')

    def test_browse_catalog_and_filtering(self):
        """Catalog should support keyword and category filtering."""
        # Report two distinct items
        self.client.post('/report/lost', data={
            'title': 'Sony WH-1000XM4 Headphones',
            'category': 'Electronics & Gadgets',
            'location': 'Central Library',
            'item_date': '2026-10-24',
            'description': 'Black over-ear noise cancelling headphones.'
        })
        self.client.post('/report/found', data={
            'title': 'Brown Leather Wallet',
            'category': 'Wallets & Purses',
            'location': 'Cafeteria / Food Court',
            'item_date': '2026-10-24',
            'storage_location': 'Cafeteria Manager Desk',
            'description': 'Wallet with coin pouch.'
        })

        # 1. Search keyword "Sony"
        res_kw = self.client.get('/browse?q=Sony')
        self.assertIn(b"Sony WH-1000XM4 Headphones", res_kw.data)
        self.assertNotIn(b"Brown Leather Wallet", res_kw.data)

        # 2. Filter category "Wallets & Purses"
        res_cat = self.client.get('/browse?category=Wallets+%26+Purses')
        self.assertIn(b"Brown Leather Wallet", res_cat.data)
        self.assertNotIn(b"Sony WH-1000XM4 Headphones", res_cat.data)

        # 3. Filter type "lost"
        res_type = self.client.get('/browse?type=lost')
        self.assertIn(b"Sony WH-1000XM4 Headphones", res_type.data)
        self.assertNotIn(b"Brown Leather Wallet", res_type.data)

if __name__ == '__main__':
    unittest.main()
