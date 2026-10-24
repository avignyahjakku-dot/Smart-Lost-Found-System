"""
Unit & Integration Tests: Ownership Claims & Verification
=========================================================
Validates the claim submission lifecycle, self-claim prevention,
and role-based administrator approval/rejection workflows.
"""

import os
import unittest
from app import create_app
from app.db import query_db, execute_db

class TestClaims(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

        # Create two student users
        self.client.post('/register', data={
            'full_name': 'Reporter Bob',
            'email': 'bob@campusfind.edu',
            'password': 'Password123',
            'confirm_password': 'Password123'
        })
        self.client.get('/logout')

        self.client.post('/register', data={
            'full_name': 'Claimant Alice',
            'email': 'alice@campusfind.edu',
            'password': 'Password123',
            'confirm_password': 'Password123'
        })
        self.client.get('/logout')

    def tearDown(self):
        self.ctx.pop()
        db_path = self.app.config.get('SQLITE_PATH')
        if db_path and os.path.exists(db_path):
            try:
                os.remove(db_path)
            except PermissionError:
                pass

    def test_submit_claim_lifecycle(self):
        """Alice can claim an item reported found by Bob, and admin can approve it."""
        # 1. Bob logs in and reports a found item
        self.client.post('/login', data={'email': 'bob@campusfind.edu', 'password': 'Password123'})
        self.client.post('/report/found', data={
            'title': 'Apple Watch Series 8',
            'category': 'Electronics & Gadgets',
            'location': 'Sports Ground / Gym',
            'item_date': '2026-10-24',
            'storage_location': 'Gym Reception',
            'description': 'Black sport band.'
        })
        item = query_db("SELECT id FROM items WHERE title = 'Apple Watch Series 8'", one=True)
        item_id = item['id']
        self.client.get('/logout')

        # 2. Bob cannot claim his own found item
        self.client.post('/login', data={'email': 'bob@campusfind.edu', 'password': 'Password123'})
        res_self = self.client.post(f'/claims/submit/{item_id}', data={
            'contact_phone': '1234567890',
            'proof_details': 'I am claiming it.'
        }, follow_redirects=True)
        self.assertIn(b"cannot submit an ownership claim on an item you reported", res_self.data)
        self.client.get('/logout')

        # 3. Alice logs in and claims the item
        self.client.post('/login', data={'email': 'alice@campusfind.edu', 'password': 'Password123'})
        res_claim = self.client.post(f'/claims/submit/{item_id}', data={
            'contact_phone': '+91 9999988888',
            'proof_details': 'Serial number is #A89234 and the battery is at 45%.'
        }, follow_redirects=True)
        self.assertIn(b"Your claim has been submitted", res_claim.data)

        # Verify claim exists with pending status
        claim = query_db("SELECT * FROM claims WHERE item_id = %s", (item_id,), one=True)
        self.assertIsNotNone(claim)
        self.assertEqual(claim['status'], 'pending')
        self.client.get('/logout')

        # 4. Administrator reviews and approves the claim
        self.client.post('/login', data={
            'email': self.app.config['DEFAULT_ADMIN_EMAIL'],
            'password': self.app.config['DEFAULT_ADMIN_PASSWORD']
        })
        res_approve = self.client.post(f'/admin/claim/{claim["id"]}/review', data={
            'decision': 'approve',
            'admin_notes': 'Verified serial number matches Apple account invoice.'
        }, follow_redirects=True)
        self.assertIn(b"approved successfully", res_approve.data)

        # Check updated statuses
        updated_claim = query_db("SELECT * FROM claims WHERE id = %s", (claim['id'],), one=True)
        self.assertEqual(updated_claim['status'], 'approved')
        self.assertEqual(updated_claim['admin_notes'], 'Verified serial number matches Apple account invoice.')

        updated_item = query_db("SELECT * FROM items WHERE id = %s", (item_id,), one=True)
        self.assertEqual(updated_item['status'], 'claimed')

if __name__ == '__main__':
    unittest.main()
