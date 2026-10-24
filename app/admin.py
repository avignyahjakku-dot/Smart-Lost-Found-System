"""
Administrator Blueprint
=======================
Role-based administrative control center for moderating reports,
evaluating ownership claims, and inspecting system activity logs.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .db import query_db, execute_db
from .auth import admin_required
from .dsa.bst_service import global_item_index

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """Administrative dashboard aggregating key metrics, claims, and reports."""
    metrics = {
        'total_users': query_db("SELECT COUNT(*) as count FROM users", one=True)['count'],
        'total_items': query_db("SELECT COUNT(*) as count FROM items", one=True)['count'],
        'open_lost': query_db("SELECT COUNT(*) as count FROM items WHERE type = 'lost' AND status = 'open'", one=True)['count'],
        'open_found': query_db("SELECT COUNT(*) as count FROM items WHERE type = 'found' AND status = 'open'", one=True)['count'],
        'pending_claims': query_db("SELECT COUNT(*) as count FROM claims WHERE status = 'pending'", one=True)['count'],
        'resolved_items': query_db("SELECT COUNT(*) as count FROM items WHERE status IN ('returned', 'resolved')", one=True)['count'],
    }

    # Retrieve all pending claims with claimant and item details
    pending_claims = query_db(
        "SELECT c.*, i.title as item_title, i.type as item_type, i.location as item_location, "
        "i.secret_hint, u.full_name as claimant_name, u.email as claimant_email "
        "FROM claims c "
        "JOIN items i ON c.item_id = i.id "
        "JOIN users u ON c.claimant_id = u.id "
        "WHERE c.status = 'pending' "
        "ORDER BY c.created_at ASC"
    )

    # Retrieve recent reports for moderation
    recent_reports = query_db(
        "SELECT i.*, u.full_name as reporter_name, u.email as reporter_email "
        "FROM items i JOIN users u ON i.user_id = u.id "
        "ORDER BY i.created_at DESC LIMIT 20"
    )

    # Retrieve recent activity logs
    logs = query_db(
        "SELECT l.*, u.full_name as user_name FROM activity_logs l "
        "LEFT JOIN users u ON l.user_id = u.id "
        "ORDER BY l.created_at DESC LIMIT 15"
    )

    return render_template(
        'admin/dashboard.html',
        metrics=metrics,
        claims=pending_claims,
        reports=recent_reports,
        logs=logs
    )

@admin_bp.route('/claim/<int:claim_id>/review', methods=['POST'])
@admin_required
def review_claim(claim_id: int):
    """Approve or reject a claim with administrator notes."""
    claim = query_db("SELECT * FROM claims WHERE id = %s", (claim_id,), one=True)
    if not claim:
        flash("Claim not found.", "danger")
        return redirect(url_for('admin.dashboard'))

    decision = request.form.get('decision')
    notes = request.form.get('admin_notes', '').strip()

    if decision == 'approve':
        execute_db("UPDATE claims SET status = 'approved', admin_notes = %s WHERE id = %s", (notes, claim_id))
        # Update associated item to claimed / returned
        execute_db("UPDATE items SET status = 'claimed' WHERE id = %s", (claim['item_id'],))
        execute_db(
            "INSERT INTO activity_logs (user_id, action, details) VALUES (%s, %s, %s)",
            (session['user_id'], 'CLAIM_APPROVED', f"Approved claim #{claim_id} for Item #{claim['item_id']}. Notes: {notes}")
        )
        flash(f"Claim #{claim_id} approved successfully.", "success")
    elif decision == 'reject':
        execute_db("UPDATE claims SET status = 'rejected', admin_notes = %s WHERE id = %s", (notes, claim_id))
        execute_db(
            "INSERT INTO activity_logs (user_id, action, details) VALUES (%s, %s, %s)",
            (session['user_id'], 'CLAIM_REJECTED', f"Rejected claim #{claim_id} for Item #{claim['item_id']}. Notes: {notes}")
        )
        flash(f"Claim #{claim_id} rejected.", "info")
    else:
        flash("Invalid decision specified.", "danger")

    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/item/<int:item_id>/delete', methods=['POST'])
@admin_required
def delete_item(item_id: int):
    """Delete an inappropriate or duplicate item report."""
    item = query_db("SELECT * FROM items WHERE id = %s", (item_id,), one=True)
    if not item:
        flash("Item not found.", "danger")
        return redirect(url_for('admin.dashboard'))

    execute_db("DELETE FROM items WHERE id = %s", (item_id,))
    global_item_index.remove_item(item_id)

    execute_db(
        "INSERT INTO activity_logs (user_id, action, details) VALUES (%s, %s, %s)",
        (session['user_id'], 'ITEM_DELETED', f"Administrator removed Item #{item_id}: {item['title']}")
    )

    flash(f"Item #{item_id} ('{item['title']}') was deleted by administrator.", "success")
    return redirect(url_for('admin.dashboard'))
