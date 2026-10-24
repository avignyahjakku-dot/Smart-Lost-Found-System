"""
Binary Search Tree (BST) Implementation
=======================================
Smart Lost & Found System (CampusFind)
Academic BTech CSE Data Structures & Algorithms Component

This module implements an authentic Binary Search Tree in Python, supporting:
- Logarithmic average-case insertion, search, and deletion
- In-order, pre-order, and post-order traversals
- Range searches for filtered item lookups
- Step-by-step search path tracking for interactive visualization
- Full serialization to JSON-compatible hierarchical dictionaries
"""

from typing import Any, Dict, List, Optional, Tuple


class BSTNode:
    """Represents an individual node in the Binary Search Tree."""

    def __init__(self, key: int, data: Any = None):
        self.key: int = key
        self.data: Any = data
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None

    def is_leaf(self) -> bool:
        """Returns True if the node has no children."""
        return self.left is None and self.right is None

    def has_one_child(self) -> bool:
        """Returns True if the node has exactly one child."""
        return (self.left is not None) ^ (self.right is not None)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the subtree rooted at this node into a nested dictionary."""
        return {
            "key": self.key,
            "data": self.data,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None
        }

    def __repr__(self) -> str:
        return f"BSTNode(key={self.key}, data={self.data!r})"


class BinarySearchTree:
    """
    Standard Binary Search Tree (BST).
    Maintains the invariant:
        For every node N:
        - All keys in N.left subtree < N.key
        - All keys in N.right subtree > N.key
    """

    def __init__(self):
        self.root: Optional[BSTNode] = None
        self.size: int = 0

    def is_empty(self) -> bool:
        """Check if the BST is empty."""
        return self.root is None

    def insert(self, key: int, data: Any = None) -> bool:
        """
        Insert a key-value pair into the BST.
        If the key already exists, updates the associated data.
        Returns True if a new node was inserted, False if updated.
        Time Complexity: O(log n) average, O(n) worst-case (skewed tree).
        """
        if self.root is None:
            self.root = BSTNode(key, data)
            self.size += 1
            return True

        current = self.root
        while True:
            if key == current.key:
                current.data = data
                return False  # Updated existing
            elif key < current.key:
                if current.left is None:
                    current.left = BSTNode(key, data)
                    self.size += 1
                    return True
                current = current.left
            else:
                if current.right is None:
                    current.right = BSTNode(key, data)
                    self.size += 1
                    return True
                current = current.right

    def search(self, key: int) -> Tuple[Optional[BSTNode], List[int]]:
        """
        Search for a node with the given key.
        Returns a tuple: (found_node, search_path)
        where search_path is a list of node keys visited from root to target/failure.
        Time Complexity: O(log n) average, O(n) worst-case.
        """
        path: List[int] = []
        current = self.root

        while current is not None:
            path.append(current.key)
            if key == current.key:
                return current, path
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        return None, path

    def delete(self, key: int) -> bool:
        """
        Delete a node with the specified key from the BST.
        Handles all three classic BST deletion cases:
          Case 1: Target node is a leaf (0 children) -> simply remove.
          Case 2: Target node has 1 child -> replace target with its child.
          Case 3: Target node has 2 children -> replace target with in-order successor
                  (minimum node in the right subtree), then delete the successor.
        Returns True if node was found and deleted, False otherwise.
        """
        initial_size = self.size
        self.root = self._delete_recursive(self.root, key)
        return self.size < initial_size

    def _delete_recursive(self, node: Optional[BSTNode], key: int) -> Optional[BSTNode]:
        if node is None:
            return None

        if key < node.key:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.key:
            node.right = self._delete_recursive(node.right, key)
        else:
            # Node found! Decrement size
            self.size -= 1

            # Case 1: Leaf node (0 children)
            if node.left is None and node.right is None:
                return None

            # Case 2: One child (right child only)
            if node.left is None:
                return node.right

            # Case 2: One child (left child only)
            if node.right is None:
                return node.left

            # Case 3: Two children
            # Find in-order successor (minimum node in right subtree)
            successor = self._find_min_node(node.right)
            node.key = successor.key
            node.data = successor.data

            # Increment size temporarily because recursive delete of successor will decrement it
            self.size += 1
            node.right = self._delete_recursive(node.right, successor.key)

        return node

    def _find_min_node(self, node: BSTNode) -> BSTNode:
        """Helper to find the node with the minimum key in a subtree."""
        current = node
        while current.left is not None:
            current = current.left
        return current

    def find_min(self) -> Optional[Tuple[int, Any]]:
        """Return (key, data) of the minimum element in the tree."""
        if self.root is None:
            return None
        min_node = self._find_min_node(self.root)
        return min_node.key, min_node.data

    def find_max(self) -> Optional[Tuple[int, Any]]:
        """Return (key, data) of the maximum element in the tree."""
        if self.root is None:
            return None
        current = self.root
        while current.right is not None:
            current = current.right
        return current.key, current.data

    def inorder_traversal(self) -> List[Tuple[int, Any]]:
        """
        Perform an in-order traversal (Left, Root, Right).
        Returns items sorted in ascending order of their keys.
        Time Complexity: O(n)
        """
        result: List[Tuple[int, Any]] = []

        def _inorder(node: Optional[BSTNode]):
            if node is not None:
                _inorder(node.left)
                result.append((node.key, node.data))
                _inorder(node.right)

        _inorder(self.root)
        return result

    def preorder_traversal(self) -> List[Tuple[int, Any]]:
        """
        Perform a pre-order traversal (Root, Left, Right).
        Useful for copying or serializing the tree structure.
        """
        result: List[Tuple[int, Any]] = []

        def _preorder(node: Optional[BSTNode]):
            if node is not None:
                result.append((node.key, node.data))
                _preorder(node.left)
                _preorder(node.right)

        _preorder(self.root)
        return result

    def postorder_traversal(self) -> List[Tuple[int, Any]]:
        """
        Perform a post-order traversal (Left, Right, Root).
        Useful for bottom-up evaluations and deleting trees.
        """
        result: List[Tuple[int, Any]] = []

        def _postorder(node: Optional[BSTNode]):
            if node is not None:
                _postorder(node.left)
                _postorder(node.right)
                result.append((node.key, node.data))

        _postorder(self.root)
        return result

    def range_search(self, min_key: int, max_key: int) -> List[Tuple[int, Any]]:
        """
        Find all key-data pairs such that min_key <= key <= max_key.
        Prunes subtrees that cannot contain elements within the range.
        Time Complexity: O(h + k), where h = tree height, k = matching nodes.
        """
        result: List[Tuple[int, Any]] = []

        def _range_search(node: Optional[BSTNode]):
            if node is None:
                return

            # If node.key > min_key, there might be matching nodes in left subtree
            if node.key > min_key:
                _range_search(node.left)

            # Check current node
            if min_key <= node.key <= max_key:
                result.append((node.key, node.data))

            # If node.key < max_key, there might be matching nodes in right subtree
            if node.key < max_key:
                _range_search(node.right)

        _range_search(self.root)
        return result

    def get_height(self) -> int:
        """
        Compute the maximum depth / height of the tree.
        Empty tree has height 0; single node tree has height 1.
        """
        def _height(node: Optional[BSTNode]) -> int:
            if node is None:
                return 0
            return 1 + max(_height(node.left), _height(node.right))

        return _height(self.root)

    def to_dict(self) -> Optional[Dict[str, Any]]:
        """
        Serialize the entire tree into a hierarchical dictionary for JSON APIs
        and SVG/canvas visualizer rendering.
        """
        if self.root is None:
            return None
        return self.root.to_dict()

    def clear(self):
        """Remove all nodes from the tree."""
        self.root = None
        self.size = 0
