"""
Authentication Blueprint
========================
Handles user registration, login, logout, password hashing, and session management.
"""

import re
import logging
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from .db import query_db, execute_db

logger = logging.getLogger('campusfind.auth')
auth_bp = Blueprint('auth', __name__)

def login_required(f):
    """Decorator to protect routes requiring authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to protect routes requiring administrator privileges."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Administrator login required.", "warning")
            return redirect(url_for('auth.login', next=request.url))
        if session.get('user_role') != 'admin':
            flash("Access denied: Administrator privileges required.", "danger")
            return redirect(url_for('items.browse'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new student or staff account."""
    if 'user_id' in session:
        return redirect(url_for('items.browse'))

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        student_id = request.form.get('student_id', '').strip()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        role = request.form.get('role', 'student').strip().lower()

        # Input Validation & Length Bounds
        if not full_name or not email or not password:
            flash("Please fill in all required fields (Name, Email, Password).", "danger")
            return render_template('auth/register.html')

        if len(full_name) > 100:
            flash("Full name cannot exceed 100 characters.", "danger")
            return render_template('auth/register.html')

        if len(email) > 100 or '@' not in email:
            flash("Please provide a valid campus email address.", "danger")
            return render_template('auth/register.html')

        if len(password) < 8:
            flash("Password must be at least 8 characters long.", "danger")
            return render_template('auth/register.html')

        if len(password) > 128:
            flash("Password cannot exceed 128 characters.", "danger")
            return render_template('auth/register.html')

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template('auth/register.html')

        if role not in ('student', 'staff'):
            role = 'student'

        # Check for existing email
        existing_user = query_db("SELECT id FROM users WHERE email = %s", (email,), one=True)
        if existing_user:
            flash("An account with this email address already exists. Please log in.", "warning")
            return redirect(url_for('auth.login'))

        # Secure password hashing
        hashed_password = generate_password_hash(password)

        try:
            user_id = execute_db(
                "INSERT INTO users (full_name, email, student_id, phone, password_hash, role) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (full_name, email, student_id[:30], phone[:20], hashed_password, role),
                return_id=True
            )

            # Auto-login after registration with permanent session
            session.clear()
            session.permanent = True
            session['user_id'] = user_id
            session['user_name'] = full_name
            session['user_email'] = email
            session['user_role'] = role

            flash(f"Welcome to CampusFind, {full_name}! Your account has been created.", "success")
            return redirect(url_for('items.browse'))
        except Exception as e:
            logger.error("Failed to create user account for %s: %s", email, str(e))
            flash("Unable to complete registration. Please verify your details or contact an administrator.", "danger")

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Authenticate an existing user."""
    if 'user_id' in session:
        return redirect(url_for('items.browse'))

    next_url = request.args.get('next')

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not email or not password:
            flash("Please provide both email and password.", "danger")
            return render_template('auth/login.html')

        user = query_db("SELECT * FROM users WHERE email = %s", (email,), one=True)

        if user and check_password_hash(user['password_hash'], password):
            session.clear()
            session.permanent = True  # Enforces PERMANENT_SESSION_LIFETIME
            session['user_id'] = user['id']
            session['user_name'] = user['full_name']
            session['user_email'] = user['email']
            session['user_role'] = user['role']

            flash(f"Welcome back, {user['full_name']}!", "success")
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            if user['role'] == 'admin':
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('items.browse'))
        else:
            flash("Invalid email or password. Please try again.", "danger")

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    """Clear the session and log the user out."""
    user_name = session.get('user_name', 'User')
    session.clear()
    flash(f"You have been successfully logged out. Goodbye, {user_name}.", "info")
    return redirect(url_for('items.browse'))
