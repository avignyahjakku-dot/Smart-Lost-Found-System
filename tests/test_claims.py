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

    def test_claim_on_lost_item_is_rejected(self):
        """Claims cannot be submitted for items reported lost."""
        # Bob reports a lost item
        self.client.post('/login', data={'email': 'bob@campusfind.edu', 'password': 'Password123'})
        self.client.post('/report/lost', data={
            'title': 'Lost Sony Headphones',
            'category': 'Electronics & Gadgets',
            'location': 'Central Library',
            'item_date': '2026-10-24',
            'description': 'Noise cancelling black headphones.'
        })
        item = query_db("SELECT id FROM items WHERE title = 'Lost Sony Headphones'", one=True)
        self.client.get('/logout')

        # Alice attempts to submit a claim on the lost item
        self.client.post('/login', data={'email': 'alice@campusfind.edu', 'password': 'Password123'})
        res = self.client.post(f'/claims/submit/{item["id"]}', data={
            'contact_phone': '9876543210',
            'proof_details': 'I lost these.'
        }, follow_redirects=True)
        self.assertIn(b"Ownership claims can only be filed for items reported found", res.data)

        # Confirm no claim was recorded
        claim_count = query_db("SELECT COUNT(*) as cnt FROM claims WHERE item_id = %s", (item['id'],), one=True)
        self.assertEqual(claim_count['cnt'], 0)

    def test_claim_rejection_flow(self):
        """Admin can reject a claim with notes, leaving item open."""
        # 1. Bob reports a found item
        self.client.post('/login', data={'email': 'bob@campusfind.edu', 'password': 'Password123'})
        self.client.post('/report/found', data={
            'title': 'Found Umbrella',
            'category': 'Other Accessories',
            'location': 'Cafeteria / Food Court',
            'item_date': '2026-10-24',
            'storage_location': 'Lost & Found Counter',
            'description': 'Black folding umbrella.'
        })
        item = query_db("SELECT id FROM items WHERE title = 'Found Umbrella'", one=True)
        self.client.get('/logout')

        # 2. Alice files claim
        self.client.post('/login', data={'email': 'alice@campusfind.edu', 'password': 'Password123'})
        self.client.post(f'/claims/submit/{item["id"]}', data={
            'contact_phone': '9876543210',
            'proof_details': 'It is mine.'
        })
        claim = query_db("SELECT id FROM claims WHERE item_id = %s", (item['id'],), one=True)
        self.client.get('/logout')

        # 3. Admin rejects claim
        self.client.post('/login', data={
            'email': self.app.config['DEFAULT_ADMIN_EMAIL'],
            'password': self.app.config['DEFAULT_ADMIN_PASSWORD']
        })
        res = self.client.post(f'/admin/claim/{claim["id"]}/review', data={
            'decision': 'reject',
            'admin_notes': 'Insufficient identifying proof.'
        }, follow_redirects=True)
        self.assertIn(b"rejected", res.data)

        updated_claim = query_db("SELECT * FROM claims WHERE id = %s", (claim['id'],), one=True)
        self.assertEqual(updated_claim['status'], 'rejected')
        self.assertEqual(updated_claim['admin_notes'], 'Insufficient identifying proof.')

        # Item should remain open
        updated_item = query_db("SELECT status FROM items WHERE id = %s", (item['id'],), one=True)
        self.assertEqual(updated_item['status'], 'open')

    def test_admin_item_deletion(self):
        """Admin can delete an inappropriate or spam item report."""
        # Bob reports an item
        self.client.post('/login', data={'email': 'bob@campusfind.edu', 'password': 'Password123'})
        self.client.post('/report/lost', data={
            'title': 'Spam Duplicate Post',
            'category': 'Books & Stationery',
            'location': 'Hostel Blocks',
            'item_date': '2026-10-24',
            'description': 'Test duplicate spam item.'
        })
        item = query_db("SELECT id FROM items WHERE title = 'Spam Duplicate Post'", one=True)
        self.client.get('/logout')

        # Admin deletes the item
        self.client.post('/login', data={
            'email': self.app.config['DEFAULT_ADMIN_EMAIL'],
            'password': self.app.config['DEFAULT_ADMIN_PASSWORD']
        })
        res = self.client.post(f'/admin/item/{item["id"]}/delete', follow_redirects=True)
        self.assertIn(b"deleted by administrator", res.data)

        # Ensure deleted from DB
        check_item = query_db("SELECT * FROM items WHERE id = %s", (item['id'],), one=True)
        self.assertIsNone(check_item)

    def test_claim_validation_missing_fields_and_oversized(self):
        """Claim submission rejects missing proof, missing phone, and oversized phone numbers."""
        # 1. Bob reports a found item
        self.client.post('/login', data={'email': 'bob@campusfind.edu', 'password': 'Password123'})
        self.client.post('/report/found', data={
            'title': 'Found Backpack',
            'category': 'Bags & Luggage',
            'location': 'Central Library',
            'item_date': '2026-10-24',
            'storage_location': 'Desk',
            'description': 'Black backpack.'
        })
        item = query_db("SELECT id FROM items WHERE title = 'Found Backpack'", one=True)
        self.client.get('/logout')

        # 2. Alice attempts to claim without phone
        self.client.post('/login', data={'email': 'alice@campusfind.edu', 'password': 'Password123'})
        res_no_phone = self.client.post(f'/claims/submit/{item["id"]}', data={
            'contact_phone': '',
            'proof_details': 'I lost my backpack.'
        }, follow_redirects=True)
        self.assertIn(b"Please provide identifying proof and your contact phone number", res_no_phone.data)

        # 3. Alice attempts to claim with oversized phone (> 20 chars)
        res_long_phone = self.client.post(f'/claims/submit/{item["id"]}', data={
            'contact_phone': '1234567890123456789012345',
            'proof_details': 'Valid proof details.'
        }, follow_redirects=True)
        self.assertIn(b"Phone number cannot exceed 20 characters", res_long_phone.data)

        # Confirm no claim exists in database
        claims_count = query_db("SELECT COUNT(*) as count FROM claims WHERE item_id = %s", (item['id'],), one=True)
        self.assertEqual(claims_count['count'], 0)

if __name__ == '__main__':
    unittest.main()
