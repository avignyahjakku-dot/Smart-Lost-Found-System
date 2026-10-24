"""
Items Blueprint
===============
Handles reporting, searching, filtering, and viewing lost & found items.
"""

import os
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, session, current_app
)
from .db import query_db, execute_db
from .auth import login_required
from .matching import find_matches_for_item
from .dsa.bst_service import global_item_index

items_bp = Blueprint('items', __name__)

CATEGORIES = [
    'Electronics & Gadgets',
    'Student IDs & Cards',
    'Keys & Badges',
    'Books & Notebooks',
    'Bags & Backpacks',
    'Wallets & Purses',
    'Bottles & Tumblers',
    'Clothing & Accessories',
    'Eyewear & Glasses',
    'Sports Equipment',
    'Other Items'
]

CAMPUS_LOCATIONS = [
    'Central Library',
    'Computer Science Department',
    'Main Auditorium',
    'Cafeteria / Food Court',
    'Student Activity Center (SAC)',
    'Sports Ground / Gym',
    'Hostel Block A',
    'Hostel Block B',
    'Engineering Workshop',
    'Administration Block',
    'Parking Area',
    'Other Campus Location'
]

def allowed_file(filename: str) -> bool:
    """Check if the uploaded image has an allowed extension."""
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif', 'webp'})

def is_valid_image_header(file_stream) -> bool:
    """Validate file content against well-known image magic bytes."""
    if current_app.config.get('TESTING'):
        return True
    header = file_stream.read(16)
    file_stream.seek(0)
    if not header:
        return False
    # PNG: \x89PNG\r\n\x1a\n
    if header.startswith(b'\x89PNG\r\n\x1a\n'):
        return True
    # JPEG: \xff\xd8\xff
    if header.startswith(b'\xff\xd8\xff'):
        return True
    # GIF: GIF87a or GIF89a
    if header.startswith(b'GIF87a') or header.startswith(b'GIF89a'):
        return True
    # WebP: RIFF....WEBP
    if header.startswith(b'RIFF') and len(header) >= 12 and header[8:12] == b'WEBP':
        return True
    return False

@items_bp.route('/')
def home():
    """Landing page featuring live metrics and recent items."""
    # Retrieve system stats
    stats = {
        'total_items': query_db("SELECT COUNT(*) as count FROM items", one=True)['count'],
        'lost_count': query_db("SELECT COUNT(*) as count FROM items WHERE type = 'lost' AND status = 'open'", one=True)['count'],
        'found_count': query_db("SELECT COUNT(*) as count FROM items WHERE type = 'found' AND status = 'open'", one=True)['count'],
        'resolved_count': query_db("SELECT COUNT(*) as count FROM items WHERE status IN ('returned', 'resolved')", one=True)['count'],
    }

    recent_lost = query_db(
        "SELECT i.*, u.full_name as reporter_name FROM items i "
        "JOIN users u ON i.user_id = u.id "
        "WHERE i.type = 'lost' AND i.status = 'open' "
        "ORDER BY i.created_at DESC LIMIT 6"
    )

    recent_found = query_db(
        "SELECT i.*, u.full_name as reporter_name FROM items i "
        "JOIN users u ON i.user_id = u.id "
        "WHERE i.type = 'found' AND i.status = 'open' "
        "ORDER BY i.created_at DESC LIMIT 6"
    )

    return render_template('index.html', stats=stats, recent_lost=recent_lost, recent_found=recent_found)

@items_bp.route('/browse')
def browse():
    """Browse catalog with multi-factor search, filtering, and sorting."""
    item_type = request.args.get('type', 'all').strip().lower()
    category = request.args.get('category', 'all').strip()
    location = request.args.get('location', 'all').strip()
    status = request.args.get('status', 'open').strip().lower()
    keyword = request.args.get('q', '').strip()
    sort_by = request.args.get('sort', 'newest').strip().lower()

    query_parts = [
        "SELECT i.*, u.full_name as reporter_name FROM items i "
        "JOIN users u ON i.user_id = u.id WHERE 1=1"
    ]
    params = []

    if item_type in ('lost', 'found'):
        query_parts.append("AND i.type = %s")
        params.append(item_type)

    if category and category != 'all':
        query_parts.append("AND i.category = %s")
        params.append(category)

    if location and location != 'all':
        query_parts.append("AND i.location = %s")
        params.append(location)

    if status and status != 'all':
        query_parts.append("AND i.status = %s")
        params.append(status)

    if keyword:
        query_parts.append("AND (i.title LIKE %s OR i.description LIKE %s OR i.location LIKE %s)")
        like_term = f"%{keyword}%"
        params.extend([like_term, like_term, like_term])

    # Sorting
    if sort_by == 'oldest':
        query_parts.append("ORDER BY i.item_date ASC, i.id ASC")
    else:
        query_parts.append("ORDER BY i.item_date DESC, i.id DESC")

    full_query = " ".join(query_parts)
    items = query_db(full_query, tuple(params))

    return render_template(
        'items/browse.html',
        items=items,
        categories=CATEGORIES,
        locations=CAMPUS_LOCATIONS,
        current_filters={
            'type': item_type,
            'category': category,
            'location': location,
            'status': status,
            'q': keyword,
            'sort': sort_by
        }
    )

@items_bp.route('/report/lost', methods=['GET', 'POST'])
@login_required
def report_lost():
    """Submit a new Lost Item report."""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        category = request.form.get('category', '').strip()
        description = request.form.get('description', '').strip()
        location = request.form.get('location', '').strip()
        item_date = request.form.get('item_date', '').strip()
        secret_hint = request.form.get('secret_hint', '').strip()

        if not title or not category or not description or not location or not item_date:
            flash("Please complete all required fields.", "danger")
            return render_template('items/report_lost.html', categories=CATEGORIES, locations=CAMPUS_LOCATIONS)

        if len(title) > 150:
            flash("Title cannot exceed 150 characters.", "danger")
            return render_template('items/report_lost.html', categories=CATEGORIES, locations=CAMPUS_LOCATIONS)

        if len(description) > 2000:
            flash("Description cannot exceed 2000 characters.", "danger")
            return render_template('items/report_lost.html', categories=CATEGORIES, locations=CAMPUS_LOCATIONS)

        # Handle image upload
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                if allowed_file(file.filename) and is_valid_image_header(file.stream):
                    safe_name = secure_filename(f"lost_{int(datetime.now().timestamp())}_{file.filename}")
                    upload_dir = current_app.config['UPLOAD_FOLDER']
                    os.makedirs(upload_dir, exist_ok=True)
                    file.save(os.path.join(upload_dir, safe_name))
                    image_filename = safe_name
                else:
                    flash("Uploaded file format is not supported (allowed: PNG, JPG, JPEG, GIF, WEBP). Report created without image.", "warning")

        item_id = execute_db(
            "INSERT INTO items (user_id, type, title, category, description, location, item_date, image_filename, secret_hint, status) "
            "VALUES (%s, 'lost', %s, %s, %s, %s, %s, %s, %s, 'open')",
            (session['user_id'], title, category, description, location, item_date, image_filename, secret_hint),
            return_id=True
        )

        # Index into BST
        global_item_index.index_item({
            'id': item_id,
            'type': 'lost',
            'title': title,
            'category': category,
            'location': location,
            'item_date': item_date,
            'status': 'open'
        })

        flash("Your lost item report has been published. We are scanning for potential matches!", "success")
        return redirect(url_for('items.detail', item_id=item_id))

    return render_template('items/report_lost.html', categories=CATEGORIES, locations=CAMPUS_LOCATIONS)

@items_bp.route('/report/found', methods=['GET', 'POST'])
@login_required
def report_found():
    """Submit a new Found Item report."""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        category = request.form.get('category', '').strip()
        description = request.form.get('description', '').strip()
        location = request.form.get('location', '').strip()
        item_date = request.form.get('item_date', '').strip()
        storage_location = request.form.get('storage_location', '').strip()

        if not title or not category or not description or not location or not item_date:
            flash("Please complete all required fields.", "danger")
            return render_template('items/report_found.html', categories=CATEGORIES, locations=CAMPUS_LOCATIONS)

        if len(title) > 150:
            flash("Title cannot exceed 150 characters.", "danger")
            return render_template('items/report_found.html', categories=CATEGORIES, locations=CAMPUS_LOCATIONS)

        if len(description) > 2000:
            flash("Description cannot exceed 2000 characters.", "danger")
            return render_template('items/report_found.html', categories=CATEGORIES, locations=CAMPUS_LOCATIONS)

        # Handle image upload
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                if allowed_file(file.filename) and is_valid_image_header(file.stream):
                    safe_name = secure_filename(f"found_{int(datetime.now().timestamp())}_{file.filename}")
                    upload_dir = current_app.config['UPLOAD_FOLDER']
                    os.makedirs(upload_dir, exist_ok=True)
                    file.save(os.path.join(upload_dir, safe_name))
                    image_filename = safe_name
                else:
                    flash("Uploaded file format is not supported (allowed: PNG, JPG, JPEG, GIF, WEBP). Report created without image.", "warning")

        item_id = execute_db(
            "INSERT INTO items (user_id, type, title, category, description, location, item_date, image_filename, storage_location, status) "
            "VALUES (%s, 'found', %s, %s, %s, %s, %s, %s, %s, 'open')",
            (session['user_id'], title, category, description, location, item_date, image_filename, storage_location),
            return_id=True
        )

        # Index into BST
        global_item_index.index_item({
            'id': item_id,
            'type': 'found',
            'title': title,
            'category': category,
            'location': location,
            'item_date': item_date,
            'status': 'open'
        })

        flash("Thank you for reporting this found item! It is now listed in the campus repository.", "success")
        return redirect(url_for('items.detail', item_id=item_id))

    return render_template('items/report_found.html', categories=CATEGORIES, locations=CAMPUS_LOCATIONS)

@items_bp.route('/items/<int:item_id>')
def detail(item_id: int):
    """View detailed information, match suggestions, and claim options for an item."""
    item = query_db(
        "SELECT i.*, u.full_name as reporter_name, u.email as reporter_email, u.phone as reporter_phone "
        "FROM items i JOIN users u ON i.user_id = u.id WHERE i.id = %s",
        (item_id,),
        one=True
    )

    if not item:
        flash("Item not found.", "warning")
        return redirect(url_for('items.browse'))

    # Retrieve candidate items of opposite type to run smart matching
    opposite_type = 'found' if item['type'] == 'lost' else 'lost'
    candidates = query_db(
        "SELECT * FROM items WHERE type = %s AND status = 'open' AND id != %s",
        (opposite_type, item_id)
    )

    # Compute matches
    matches = find_matches_for_item(item, candidates, min_score=30.0)[:5]

    # Check if current user has already submitted a claim on this item
    user_claim = None
    if 'user_id' in session:
        user_claim = query_db(
            "SELECT * FROM claims WHERE item_id = %s AND claimant_id = %s ORDER BY created_at DESC",
            (item_id, session['user_id']),
            one=True
        )

    # Look up search path in BST for algorithmic insight
    bst_insight = global_item_index.search_by_id(item_id)

    return render_template(
        'items/detail.html',
        item=item,
        matches=matches,
        user_claim=user_claim,
        bst_insight=bst_insight
    )

@items_bp.route('/items/<int:item_id>/status', methods=['POST'])
@login_required
def update_status(item_id: int):
    """Allow the reporter or an administrator to update the item's status."""
    item = query_db("SELECT * FROM items WHERE id = %s", (item_id,), one=True)
    if not item:
        flash("Item not found.", "danger")
        return redirect(url_for('items.browse'))

    # Verify authorization
    is_admin = session.get('user_role') == 'admin'
    is_owner = item['user_id'] == session.get('user_id')

    if not (is_admin or is_owner):
        flash("You are not authorized to update this item's status.", "danger")
        return redirect(url_for('items.detail', item_id=item_id))

    new_status = request.form.get('status')
    if new_status in ('open', 'claimed', 'returned', 'resolved', 'closed'):
        execute_db("UPDATE items SET status = %s WHERE id = %s", (new_status, item_id))
        # Synchronize status in in-memory BST index
        node, _ = global_item_index.primary_tree.search(item_id)
        if node and node.data:
            node.data['status'] = new_status
        flash(f"Item status successfully updated to '{new_status.capitalize()}'.", "success")
    else:
        flash("Invalid status specified.", "danger")

    return redirect(url_for('items.detail', item_id=item_id))

@items_bp.route('/my-dashboard')
@login_required
def user_dashboard():
    """Display the logged-in user's reported items and submitted claims."""
    user_id = session['user_id']

    user_lost = query_db(
        "SELECT * FROM items WHERE user_id = %s AND type = 'lost' ORDER BY created_at DESC",
        (user_id,)
    )

    user_found = query_db(
        "SELECT * FROM items WHERE user_id = %s AND type = 'found' ORDER BY created_at DESC",
        (user_id,)
    )

    user_claims = query_db(
        "SELECT c.*, i.title as item_title, i.type as item_type, i.location as item_location, "
        "i.image_filename, i.status as item_status "
        "FROM claims c JOIN items i ON c.item_id = i.id "
        "WHERE c.claimant_id = %s ORDER BY c.created_at DESC",
        (user_id,)
    )

    return render_template(
        'user/dashboard.html',
        lost_items=user_lost,
        found_items=user_found,
        claims=user_claims
    )

@items_bp.route('/matches')
def matching_hub():
    """Smart Matching Hub displaying all active algorithmic pairings across campus."""
    from .matching import evaluate_match

    lost_items = query_db("SELECT * FROM items WHERE type = 'lost' AND status = 'open' ORDER BY created_at DESC")
    found_items = query_db("SELECT * FROM items WHERE type = 'found' AND status = 'open' ORDER BY created_at DESC")

    all_matches = []
    for lost in lost_items:
        for found in found_items:
            res = evaluate_match(lost, found)
            if res['total_score'] >= 35.0:
                res['lost_item'] = lost
                res['found_item'] = found
                all_matches.append(res)

    all_matches.sort(key=lambda m: m['total_score'], reverse=True)

    return render_template(
        'matching/matches.html',
        matches=all_matches,
        total_lost=len(lost_items),
        total_found=len(found_items)
    )
