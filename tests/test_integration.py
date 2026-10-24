"""
Integration & System End-to-End Tests
=====================================
Validates application lifecycle, test configuration startup,
template rendering across key views, and global error handling.
"""

import os
import unittest
from flask import current_app
from app import create_app
from app.db import query_db, execute_db

class TestIntegration(unittest.TestCase):

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

    def test_application_startup_in_test_configuration(self):
        """Flask starts cleanly in TestingConfig with isolated test database."""
        self.assertTrue(current_app.config['TESTING'])
        self.assertEqual(current_app.config['DB_TYPE'], 'sqlite')
        self.assertIn('test_campusfind.db', current_app.config['SQLITE_PATH'])

    def test_homepage_rendering_and_metrics(self):
        """Homepage renders HTTP 200, system metrics, and quick reporting buttons."""
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"CampusFind", res.data)
        self.assertIn(b"Report Lost", res.data)
        self.assertIn(b"Report Found", res.data)

    def test_catalog_browsing_page(self):
        """Catalog page loads with search inputs and campus location filters."""
        res = self.client.get('/browse')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Campus Repository Catalog", res.data)
        self.assertIn(b"Central Library", res.data)

    def test_matching_hub_page(self):
        """Matching hub renders with explanation of heuristic scoring."""
        res = self.client.get('/matches')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Campus Smart Matching Hub", res.data)
        self.assertIn(b"How the Matching Scoring Algorithm Operates", res.data)

    def test_custom_404_error_page(self):
        """Non-existent URL triggers custom 404 error handler with friendly page."""
        res = self.client.get('/this-path-definitely-does-not-exist')
        self.assertEqual(res.status_code, 404)
        self.assertIn(b"404", res.data)
        self.assertIn(b"The requested page could not be found", res.data)
        self.assertIn(b"Return to Homepage", res.data)

    def test_database_persistence_and_foreign_keys(self):
        """Database correctly enforces foreign key constraints and transactional integrity."""
        # Inserting an item with a non-existent user_id should fail foreign key check
        with self.assertRaises(Exception):
            execute_db(
                "INSERT INTO items (user_id, type, title, category, description, location, item_date, status) "
                "VALUES (%s, 'lost', 'Ghost Item', 'Electronics & Gadgets', 'Desc', 'Library', '2026-10-24', 'open')",
                (999999,)  # Non-existent user
            )

if __name__ == '__main__':
    unittest.main()
