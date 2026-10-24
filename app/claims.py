"""
Claims Blueprint
================
Handles ownership claim submissions and claim status inspection.
"""

from flask import Blueprint, request, redirect, url_for, flash, session
from .db import query_db, execute_db
from .auth import login_required

claims_bp = Blueprint('claims', __name__)

@claims_bp.route('/claims/submit/<int:item_id>', methods=['POST'])
@login_required
def submit_claim(item_id: int):
    """Submit a formal ownership claim for a found item."""
    item = query_db("SELECT * FROM items WHERE id = %s", (item_id,), one=True)

    if not item:
        flash("The requested item does not exist.", "danger")
        return redirect(url_for('items.browse'))

    if item['user_id'] == session['user_id']:
        flash("You cannot submit an ownership claim on an item you reported.", "warning")
        return redirect(url_for('items.detail', item_id=item_id))

    if item['status'] not in ('open', 'claimed'):
        flash(f"This item is marked as '{item['status']}' and is no longer accepting claims.", "warning")
        return redirect(url_for('items.detail', item_id=item_id))

    # Check for existing pending claim by this user
    existing = query_db(
        "SELECT id FROM claims WHERE item_id = %s AND claimant_id = %s AND status = 'pending'",
        (item_id, session['user_id']),
        one=True
    )
    if existing:
        flash("You already have a pending claim under review for this item.", "info")
        return redirect(url_for('items.detail', item_id=item_id))

    proof_details = request.form.get('proof_details', '').strip()
    secret_answer = request.form.get('secret_answer', '').strip()
    contact_phone = request.form.get('contact_phone', '').strip()

    if not proof_details or not contact_phone:
        flash("Please provide identifying proof and your contact phone number.", "danger")
        return redirect(url_for('items.detail', item_id=item_id))

    try:
        execute_db(
            "INSERT INTO claims (item_id, claimant_id, proof_details, secret_answer, contact_phone, status) "
            "VALUES (%s, %s, %s, %s, %s, 'pending')",
            (item_id, session['user_id'], proof_details, secret_answer, contact_phone)
        )

        # Log system activity
        execute_db(
            "INSERT INTO activity_logs (user_id, action, details) VALUES (%s, %s, %s)",
            (session['user_id'], 'CLAIM_SUBMITTED', f"Submitted claim for Item #{item_id}: {item['title']}")
        )

        flash("Your claim has been submitted to campus administrators for review. Track progress in your dashboard.", "success")
    except Exception as e:
        flash(f"Error submitting claim: {str(e)}", "danger")

    return redirect(url_for('items.detail', item_id=item_id))
