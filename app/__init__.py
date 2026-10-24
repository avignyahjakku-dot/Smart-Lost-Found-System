"""
CampusFind - Application Factory
================================
Initializes Flask extensions, database schema, blueprints, and BST indexes.
"""

import os
from datetime import datetime
from flask import Flask, render_template, session
from .config import config_by_name, Config
from .db import close_db, init_db
from .dsa.bst_service import global_item_index

def create_app(config_name=None):
    """Factory function to configure and return the Flask application."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, Config))
    app.config['BASE_DIR'] = Config.BASE_DIR

    # Ensure uploads directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Database teardown registration
    app.teardown_appcontext(close_db)

    # Register Blueprints
    from .auth import auth_bp
    from .items import items_bp
    from .claims import claims_bp
    from .admin import admin_bp
    from .dsa.routes import dsa_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(items_bp)
    app.register_blueprint(claims_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(dsa_bp)

    # Context processors for global template variables
    @app.context_processor
    def inject_global_template_vars():
        return {
            'now': datetime.now(),
            'current_user': {
                'id': session.get('user_id'),
                'name': session.get('user_name'),
                'email': session.get('user_email'),
                'role': session.get('user_role'),
                'is_authenticated': 'user_id' in session,
                'is_admin': session.get('user_role') == 'admin'
            }
        }

    # Custom Jinja Template Filters
    @app.template_filter('format_date')
    def format_date_filter(value):
        if not value:
            return 'N/A'
        try:
            val_str = str(value)[:10]
            dt = datetime.strptime(val_str, "%Y-%m-%d")
            return dt.strftime("%b %d, %Y")
        except Exception:
            return str(value)

    @app.template_filter('badge_status')
    def badge_status_filter(status):
        badges = {
            'open': 'badge-success',
            'claimed': 'badge-warning',
            'returned': 'badge-info',
            'resolved': 'badge-secondary',
            'closed': 'badge-dark',
            'pending': 'badge-warning',
            'approved': 'badge-success',
            'rejected': 'badge-danger'
        }
        return badges.get(str(status).lower(), 'badge-secondary')

    # Global HTTP Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('base.html', error_code=404, error_message="The requested page could not be found."), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('base.html', error_code=500, error_message="An unexpected server error occurred."), 500

    # Auto-initialize database schema and BST in-memory index
    with app.app_context():
        try:
            init_db(app)
            # Index existing records into BST
            global_item_index.build_from_database()
        except Exception as e:
            app.logger.warning("Database startup notice: %s", str(e))

    return app
