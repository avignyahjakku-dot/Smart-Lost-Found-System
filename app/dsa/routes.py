"""
DSA Routes and REST API Blueprint
=================================
Exposes the Binary Search Tree algorithms and data structure operations
to the interactive web visualizer frontend.
"""

from flask import Blueprint, render_template, request, jsonify
from .bst import BinarySearchTree
from .bst_service import global_item_index
from ..db import query_db

dsa_bp = Blueprint('dsa', __name__, url_prefix='/dsa')

# Dedicated interactive visualizer tree instance for student experimentation
interactive_tree = BinarySearchTree()

def _ensure_interactive_tree_initialized():
    """Seed the interactive tree with campus item IDs if currently empty."""
    if interactive_tree.is_empty():
        # Insert a balanced initial set of campus item IDs
        sample_keys = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 65, 75, 90]
        sample_names = {
            50: "Dell Laptop (Library)",
            30: "Student ID Card (Cafeteria)",
            70: "AirPods Pro (SAC)",
            20: "Casio Calculator (CS Lab)",
            40: "Hydro Flask (Gym)",
            60: "Hostel Keyring (Hostel A)",
            80: "Titan Smartwatch (Sports)",
            10: "Blue Backpack",
            25: "Glasses Case",
            35: "Pendrive 64GB",
            45: "Umbrella",
            65: "Lab Coat",
            75: "Wallet (Admin Block)",
            90: "Bicycle Key"
        }
        for k in sample_keys:
            interactive_tree.insert(k, {"id": k, "title": sample_names.get(k, f"Item #{k}")})

@dsa_bp.route('/visualizer')
def visualizer():
    """Renders the interactive BST visualizer and academic study page."""
    _ensure_interactive_tree_initialized()
    return render_template('dsa/visualizer.html')

@dsa_bp.route('/api/tree', methods=['GET'])
def get_tree():
    """Return JSON representation of the BST."""
    _ensure_interactive_tree_initialized()
    return jsonify({
        "success": True,
        "tree": interactive_tree.to_dict(),
        "size": interactive_tree.size,
        "height": interactive_tree.get_height()
    })

@dsa_bp.route('/api/insert', methods=['POST'])
def api_insert():
    """Insert a new key into the interactive BST."""
    _ensure_interactive_tree_initialized()
    data = request.get_json() or {}
    try:
        key = int(data.get('key'))
    except (ValueError, TypeError):
        return jsonify({"success": False, "error": "Key must be a valid integer."}), 400

    title = data.get('title', f"Item #{key}").strip()
    inserted = interactive_tree.insert(key, {"id": key, "title": title})

    return jsonify({
        "success": True,
        "inserted": inserted,
        "message": f"Key {key} {'inserted' if inserted else 'updated'} successfully.",
        "tree": interactive_tree.to_dict(),
        "size": interactive_tree.size,
        "height": interactive_tree.get_height()
    })

@dsa_bp.route('/api/search', methods=['POST'])
def api_search():
    """Search for a key in the interactive BST and return visited traversal path."""
    _ensure_interactive_tree_initialized()
    data = request.get_json() or {}
    try:
        key = int(data.get('key'))
    except (ValueError, TypeError):
        return jsonify({"success": False, "error": "Key must be a valid integer."}), 400

    node, path = interactive_tree.search(key)
    return jsonify({
        "success": True,
        "found": node is not None,
        "key": key,
        "item": node.data if node else None,
        "path": path,
        "comparisons": len(path),
        "tree_height": interactive_tree.get_height()
    })

@dsa_bp.route('/api/delete', methods=['POST'])
def api_delete():
    """Delete a key from the interactive BST."""
    _ensure_interactive_tree_initialized()
    data = request.get_json() or {}
    try:
        key = int(data.get('key'))
    except (ValueError, TypeError):
        return jsonify({"success": False, "error": "Key must be a valid integer."}), 400

    deleted = interactive_tree.delete(key)
    return jsonify({
        "success": True,
        "deleted": deleted,
        "message": f"Key {key} {'deleted successfully' if deleted else 'was not found in tree'}.",
        "tree": interactive_tree.to_dict(),
        "size": interactive_tree.size,
        "height": interactive_tree.get_height()
    })

@dsa_bp.route('/api/traverse', methods=['GET'])
def api_traverse():
    """Perform in-order, pre-order, or post-order traversal."""
    _ensure_interactive_tree_initialized()
    order = request.args.get('order', 'inorder').lower()

    if order == 'inorder':
        seq = interactive_tree.inorder_traversal()
    elif order == 'preorder':
        seq = interactive_tree.preorder_traversal()
    elif order == 'postorder':
        seq = interactive_tree.postorder_traversal()
    else:
        return jsonify({"success": False, "error": "Invalid order. Choose inorder, preorder, or postorder."}), 400

    keys = [k for k, _ in seq]
    return jsonify({
        "success": True,
        "order": order,
        "keys": keys,
        "count": len(keys)
    })

@dsa_bp.route('/api/reset', methods=['POST'])
def api_reset():
    """Reset the interactive tree to default sample state."""
    interactive_tree.clear()
    _ensure_interactive_tree_initialized()
    return jsonify({
        "success": True,
        "message": "Interactive BST reset to default balanced dataset.",
        "tree": interactive_tree.to_dict(),
        "size": interactive_tree.size,
        "height": interactive_tree.get_height()
    })
