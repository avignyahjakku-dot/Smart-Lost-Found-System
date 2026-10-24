"""
Integration Tests: DSA Routes & REST API
========================================
Validates the Binary Search Tree REST API endpoints consumed by
the interactive SVG visualizer frontend.
"""

import json
import unittest
from app import create_app

class TestDsaRoutes(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

        # Reset interactive tree to consistent baseline before each test
        self.client.post('/dsa/api/reset')

    def tearDown(self):
        self.ctx.pop()

    def test_visualizer_page_renders(self):
        """The /dsa/visualizer HTML route should return HTTP 200 with canvas."""
        res = self.client.get('/dsa/visualizer')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"BST Visualizer", res.data)
        self.assertIn(b"bst-svg", res.data)

    def test_api_tree_structure(self):
        """GET /dsa/api/tree returns the complete tree structure and metrics."""
        res = self.client.get('/dsa/api/tree')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertGreater(data['size'], 0)
        self.assertGreater(data['height'], 0)
        self.assertIn('key', data['tree'])

    def test_api_insert_and_validation(self):
        """POST /dsa/api/insert inserts valid keys and rejects non-integers."""
        # 1. Successful insertion of a new key
        res = self.client.post('/dsa/api/insert',
                               data=json.dumps({'key': 999, 'title': 'Gold Chain'}),
                               content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertTrue(data['inserted'])

        # 2. Key must be in the tree now
        res_search = self.client.post('/dsa/api/search',
                                      data=json.dumps({'key': 999}),
                                      content_type='application/json')
        search_data = res_search.get_json()
        self.assertTrue(search_data['found'])
        self.assertEqual(search_data['item']['title'], 'Gold Chain')

        # 3. Invalid key validation
        res_invalid = self.client.post('/dsa/api/insert',
                                       data=json.dumps({'key': 'invalid_string'}),
                                       content_type='application/json')
        self.assertEqual(res_invalid.status_code, 400)
        self.assertFalse(res_invalid.get_json()['success'])

    def test_api_search_path_tracing(self):
        """POST /dsa/api/search returns traversal comparisons and path array."""
        res = self.client.post('/dsa/api/search',
                               data=json.dumps({'key': 50}),
                               content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertTrue(data['found'])
        self.assertEqual(data['key'], 50)
        self.assertIsInstance(data['path'], list)
        self.assertGreater(len(data['path']), 0)
        self.assertEqual(data['comparisons'], len(data['path']))

    def test_api_delete_key(self):
        """POST /dsa/api/delete deletes a key and updates tree size."""
        # Insert a unique key
        self.client.post('/dsa/api/insert',
                         data=json.dumps({'key': 888, 'title': 'Temporary Item'}),
                         content_type='application/json')

        # Delete it
        res = self.client.post('/dsa/api/delete',
                               data=json.dumps({'key': 888}),
                               content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertTrue(data['deleted'])

        # Search should confirm it no longer exists
        res_check = self.client.post('/dsa/api/search',
                                     data=json.dumps({'key': 888}),
                                     content_type='application/json')
        self.assertFalse(res_check.get_json()['found'])

    def test_api_traversals(self):
        """GET /dsa/api/traverse returns ordered keys for inorder, preorder, and postorder."""
        # 1. In-order traversal must be strictly ascending
        res_inorder = self.client.get('/dsa/api/traverse?order=inorder')
        self.assertEqual(res_inorder.status_code, 200)
        inorder_keys = res_inorder.get_json()['keys']
        self.assertEqual(inorder_keys, sorted(inorder_keys))

        # 2. Pre-order traversal
        res_preorder = self.client.get('/dsa/api/traverse?order=preorder')
        self.assertEqual(res_preorder.status_code, 200)
        self.assertTrue(res_preorder.get_json()['success'])

        # 3. Post-order traversal
        res_postorder = self.client.get('/dsa/api/traverse?order=postorder')
        self.assertEqual(res_postorder.status_code, 200)
        self.assertTrue(res_postorder.get_json()['success'])

        # 4. Invalid traversal order returns HTTP 400
        res_invalid = self.client.get('/dsa/api/traverse?order=invalid_traversal')
        self.assertEqual(res_invalid.status_code, 400)

    def test_api_reset(self):
        """POST /dsa/api/reset restores the tree to default balanced dataset."""
        # Clear and modify tree
        self.client.post('/dsa/api/delete',
                         data=json.dumps({'key': 50}),
                         content_type='application/json')

        # Reset
        res = self.client.post('/dsa/api/reset')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])

        # Key 50 should be restored
        res_search = self.client.post('/dsa/api/search',
                                      data=json.dumps({'key': 50}),
                                      content_type='application/json')
        self.assertTrue(res_search.get_json()['found'])

if __name__ == '__main__':
    unittest.main()
