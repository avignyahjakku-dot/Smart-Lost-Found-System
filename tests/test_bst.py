"""
Unit Tests: Binary Search Tree (BST)
====================================
Comprehensive tests validating BST operations, edge cases,
all 3 deletion cases, range queries, and traversal invariants.
"""

import unittest
from app.dsa.bst import BinarySearchTree, BSTNode

class TestBinarySearchTree(unittest.TestCase):

    def setUp(self):
        self.bst = BinarySearchTree()

    def test_empty_tree_properties(self):
        """Test initial state of an empty BST."""
        self.assertTrue(self.bst.is_empty())
        self.assertEqual(self.bst.size, 0)
        self.assertEqual(self.bst.get_height(), 0)
        node, path = self.bst.search(42)
        self.assertIsNone(node)
        self.assertEqual(path, [])
        self.assertFalse(self.bst.delete(42))
        self.assertIsNone(self.bst.to_dict())
        self.assertEqual(self.bst.inorder_traversal(), [])

    def test_single_node_insertion_and_search(self):
        """Test inserting and searching a single node."""
        inserted = self.bst.insert(50, {"title": "Calculus Textbook"})
        self.assertTrue(inserted)
        self.assertFalse(self.bst.is_empty())
        self.assertEqual(self.bst.size, 1)
        self.assertEqual(self.bst.get_height(), 1)

        node, path = self.bst.search(50)
        self.assertIsNotNone(node)
        self.assertEqual(node.key, 50)
        self.assertEqual(node.data["title"], "Calculus Textbook")
        self.assertEqual(path, [50])

    def test_duplicate_key_updates_data(self):
        """Inserting an existing key should update data without increasing size."""
        self.bst.insert(20, {"title": "Version 1"})
        self.assertEqual(self.bst.size, 1)

        inserted = self.bst.insert(20, {"title": "Version 2"})
        self.assertFalse(inserted)
        self.assertEqual(self.bst.size, 1)

        node, _ = self.bst.search(20)
        self.assertEqual(node.data["title"], "Version 2")

    def test_bst_ordering_and_traversal(self):
        """Verify that in-order traversal strictly produces ascending keys."""
        keys = [50, 30, 70, 20, 40, 60, 80]
        for k in keys:
            self.bst.insert(k, f"Item {k}")

        self.assertEqual(self.bst.size, 7)
        inorder = self.bst.inorder_traversal()
        inorder_keys = [k for k, _ in inorder]
        self.assertEqual(inorder_keys, sorted(keys))

        preorder_keys = [k for k, _ in self.bst.preorder_traversal()]
        self.assertEqual(preorder_keys, [50, 30, 20, 40, 70, 60, 80])

        postorder_keys = [k for k, _ in self.bst.postorder_traversal()]
        self.assertEqual(postorder_keys, [20, 40, 30, 60, 80, 70, 50])

    def test_search_path_tracing(self):
        """Ensure the search algorithm accurately traces the branch path."""
        for k in [50, 25, 75, 10, 35, 60, 90]:
            self.bst.insert(k, f"Item {k}")

        # Search for 35 (50 -> left to 25 -> right to 35)
        node, path = self.bst.search(35)
        self.assertIsNotNone(node)
        self.assertEqual(path, [50, 25, 35])

        # Search for missing key 15 (50 -> 25 -> 10 -> right=None)
        missing_node, miss_path = self.bst.search(15)
        self.assertIsNone(missing_node)
        self.assertEqual(miss_path, [50, 25, 10])

    def test_deletion_case_1_leaf(self):
        """Deletion Case 1: Removing a leaf node (0 children)."""
        for k in [50, 30, 70]:
            self.bst.insert(k)

        deleted = self.bst.delete(30)
        self.assertTrue(deleted)
        self.assertEqual(self.bst.size, 2)
        node, _ = self.bst.search(30)
        self.assertIsNone(node)
        self.assertEqual([k for k, _ in self.bst.inorder_traversal()], [50, 70])

    def test_deletion_case_2_one_child(self):
        """Deletion Case 2: Removing a node with exactly one child."""
        # 50 -> 30 -> 20 (30 has only left child 20)
        for k in [50, 30, 20, 70]:
            self.bst.insert(k)

        deleted = self.bst.delete(30)
        self.assertTrue(deleted)
        self.assertEqual(self.bst.size, 3)
        node, _ = self.bst.search(30)
        self.assertIsNone(node)
        # 20 should now be directly attached to left of 50
        self.assertEqual([k for k, _ in self.bst.inorder_traversal()], [20, 50, 70])

    def test_deletion_case_3_two_children(self):
        """Deletion Case 3: Removing a node with two children (in-order successor replacement)."""
        keys = [50, 30, 70, 20, 40, 60, 80]
        for k in keys:
            self.bst.insert(k)

        # Delete root 50 (has two children: left 30, right 70).
        # In-order successor in right subtree is 60.
        deleted = self.bst.delete(50)
        self.assertTrue(deleted)
        self.assertEqual(self.bst.size, 6)
        self.assertEqual(self.bst.root.key, 60)
        self.assertEqual([k for k, _ in self.bst.inorder_traversal()], [20, 30, 40, 60, 70, 80])

    def test_range_search_pruning(self):
        """Test retrieving items within a key interval."""
        for k in [10, 20, 30, 40, 50, 60, 70, 80]:
            self.bst.insert(k, f"Payload {k}")

        results = self.bst.range_search(25, 65)
        result_keys = [k for k, _ in results]
        self.assertEqual(result_keys, [30, 40, 50, 60])

    def test_min_and_max(self):
        """Test finding minimum and maximum keys."""
        for k in [45, 12, 89, 3, 56]:
            self.bst.insert(k, f"Val {k}")

        min_k, _ = self.bst.find_min()
        max_k, _ = self.bst.find_max()
        self.assertEqual(min_k, 3)
        self.assertEqual(max_k, 89)

if __name__ == '__main__':
    unittest.main()
