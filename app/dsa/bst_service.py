"""
BST Item Indexing Service
=========================
Integrates the Python Binary Search Tree with the CampusFind item catalog.
Provides in-memory logarithmic indexing by Item ID and Date Timestamps,
allowing fast range filtering and visual operational analysis.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from .bst import BinarySearchTree
from ..db import query_db

class ItemBSTIndex:
    """
    Manages in-memory BST indexes for CampusFind items.
    Maintains:
      - primary_tree: Keyed by Item ID (int)
      - chronological_tree: Keyed by Date timestamp (int epoch)
    """

    def __init__(self):
        self.primary_tree = BinarySearchTree()
        self.date_tree = BinarySearchTree()

    def build_from_database(self) -> int:
        """Loads all active items from the database into the BST indexes."""
        self.primary_tree.clear()
        self.date_tree.clear()

        items = query_db("SELECT id, type, title, category, location, item_date, status FROM items")
        count = 0
        for item in items:
            self.index_item(item)
            count += 1
        return count

    def index_item(self, item: Dict[str, Any]):
        """Index a single item in both trees."""
        item_id = int(item['id'])
        # Primary tree keyed by item_id
        self.primary_tree.insert(item_id, item)

        # Date tree keyed by epoch timestamp
        try:
            date_str = str(item['item_date'])
            # Support YYYY-MM-DD or YYYY-MM-DD HH:MM:SS
            dt = datetime.strptime(date_str[:10], "%Y-%m-%d")
            epoch_days = int(dt.timestamp() // 86400)
            self.date_tree.insert(epoch_days, item)
        except Exception:
            pass

    def remove_item(self, item_id: int):
        """Remove an item from the primary index."""
        self.primary_tree.delete(item_id)

    def search_by_id(self, item_id: int) -> Dict[str, Any]:
        """Search for an item using the primary BST and return the traversal trace."""
        node, path = self.primary_tree.search(item_id)
        return {
            "found": node is not None,
            "item": node.data if node else None,
            "path": path,
            "comparisons": len(path),
            "tree_size": self.primary_tree.size,
            "tree_height": self.primary_tree.get_height()
        }

    def get_items_in_id_range(self, min_id: int, max_id: int) -> List[Dict[str, Any]]:
        """Perform a range query using BST pruning."""
        results = self.primary_tree.range_search(min_id, max_id)
        return [data for _, data in results]

    def get_tree_state(self) -> Dict[str, Any]:
        """Return the current hierarchical state of the BST for the visualizer."""
        return {
            "tree": self.primary_tree.to_dict(),
            "size": self.primary_tree.size,
            "height": self.primary_tree.get_height(),
            "inorder_sample": [k for k, _ in self.primary_tree.inorder_traversal()[:20]]
        }

# Global singleton index
global_item_index = ItemBSTIndex()
