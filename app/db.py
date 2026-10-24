import os
import sqlite3
import logging
from flask import g, current_app
from werkzeug.security import generate_password_hash

logger = logging.getLogger('campusfind.db')

def get_db():
    """Retrieve or establish the database connection for the current request context."""
    if '_db' not in g:
        db_type = current_app.config.get('DB_TYPE', 'sqlite').lower()
        if db_type == 'mysql':
            try:
                import pymysql
                import pymysql.cursors
                g._db = pymysql.connect(
                    host=current_app.config.get('DB_HOST', '127.0.0.1'),
                    port=current_app.config.get('DB_PORT', 3306),
                    user=current_app.config.get('DB_USER', 'root'),
                    password=current_app.config.get('DB_PASSWORD', ''),
                    database=current_app.config.get('DB_NAME', 'campusfind'),
                    cursorclass=pymysql.cursors.DictCursor,
                    autocommit=False,
                    charset='utf8mb4'
                )
                g._db_type = 'mysql'
                return g._db
            except Exception as e:
                logger.warning(
                    "Failed to connect to MySQL database '%s' at %s:%s (%s). "
                    "Falling back to local SQLite database (%s).",
                    current_app.config.get('DB_NAME'),
                    current_app.config.get('DB_HOST'),
                    current_app.config.get('DB_PORT'),
                    str(e),
                    current_app.config.get('SQLITE_PATH')
                )
                # Graceful fallback to SQLite
                db_type = 'sqlite'

        # SQLite Connection
        sqlite_path = current_app.config.get('SQLITE_PATH', 'campusfind.db')
        conn = sqlite3.connect(sqlite_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        # Enable foreign keys in SQLite
        conn.execute("PRAGMA foreign_keys = ON;")
        g._db = conn
        g._db_type = 'sqlite'

    return g._db

def close_db(e=None):
    """Close the database connection at the end of the request."""
    db = g.pop('_db', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    """
    Execute a parameterized SELECT query.
    Always use `%s` placeholders; this function translates them to `?` for SQLite.
    Returns dictionaries or a list of dictionaries.
    """
    db = get_db()
    db_type = getattr(g, '_db_type', 'sqlite')

    if db_type == 'sqlite':
        query = query.replace('%s', '?')
        cur = db.execute(query, args)
        rv = cur.fetchall()
        cur.close()
        # Convert sqlite3.Row objects to real python dicts for consistency
        results = [dict(row) for row in rv]
        return (results[0] if results else None) if one else results
    else:
        with db.cursor() as cur:
            cur.execute(query, args)
            rv = cur.fetchall()
            return (rv[0] if rv else None) if one else rv

def execute_db(query, args=(), return_id=False):
    """
    Execute an INSERT, UPDATE, or DELETE query and commit the transaction.
    Always use `%s` placeholders.
    Returns the newly inserted row ID if return_id=True, else affected rows.
    """
    db = get_db()
    db_type = getattr(g, '_db_type', 'sqlite')

    try:
        if db_type == 'sqlite':
            query = query.replace('%s', '?')
            cur = db.cursor()
            cur.execute(query, args)
            db.commit()
            last_id = cur.lastrowid
            row_count = cur.rowcount
            cur.close()
            return last_id if return_id else row_count
        else:
            with db.cursor() as cur:
                cur.execute(query, args)
                db.commit()
                last_id = cur.lastrowid
                row_count = cur.rowcount
                return last_id if return_id else row_count
    except Exception:
        db.rollback()
        raise

def init_db(app):
    """Initialize tables in the configured database and seed the default admin."""
    with app.app_context():
        db_type = app.config.get('DB_TYPE', 'sqlite').lower()

        # Check if we should initialize MySQL or SQLite
        if db_type == 'mysql':
            try:
                import pymysql
                conn = pymysql.connect(
                    host=app.config.get('DB_HOST', '127.0.0.1'),
                    port=app.config.get('DB_PORT', 3306),
                    user=app.config.get('DB_USER', 'root'),
                    password=app.config.get('DB_PASSWORD', ''),
                    charset='utf8mb4'
                )
                schema_path = os.path.join(app.config['BASE_DIR'], 'schema.sql')
                if os.path.exists(schema_path):
                    with open(schema_path, 'r', encoding='utf-8') as f:
                        sql_script = f.read()
                    with conn.cursor() as cur:
                        for statement in sql_script.split(';'):
                            stmt = statement.strip()
                            if stmt:
                                cur.execute(stmt)
                    conn.commit()
                    conn.close()
                    logger.info("Successfully initialized MySQL database schema.")
            except Exception as ex:
                logger.warning("Could not initialize MySQL (%s). Using SQLite schema.", ex)
                _init_sqlite(app)
        else:
            _init_sqlite(app)

        # Seed initial admin account if not already present
        _seed_default_admin(app)

def _init_sqlite(app):
    """Set up SQLite relational schema with constraints and foreign keys."""
    sqlite_path = app.config.get('SQLITE_PATH', 'campusfind.db')
    conn = sqlite3.connect(sqlite_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        student_id TEXT,
        phone TEXT,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'student' CHECK(role IN ('student', 'staff', 'admin')),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        type TEXT NOT NULL CHECK(type IN ('lost', 'found')),
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT NOT NULL,
        location TEXT NOT NULL,
        item_date TEXT NOT NULL,
        image_filename TEXT,
        storage_location TEXT,
        secret_hint TEXT,
        status TEXT NOT NULL DEFAULT 'open' CHECK(status IN ('open', 'claimed', 'returned', 'resolved', 'closed')),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS claims (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER NOT NULL,
        claimant_id INTEGER NOT NULL,
        proof_details TEXT NOT NULL,
        secret_answer TEXT,
        contact_phone TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'approved', 'rejected')),
        admin_notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (item_id) REFERENCES items (id) ON DELETE CASCADE,
        FOREIGN KEY (claimant_id) REFERENCES users (id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lost_item_id INTEGER NOT NULL,
        found_item_id INTEGER NOT NULL,
        similarity_score REAL NOT NULL,
        match_details TEXT,
        status TEXT NOT NULL DEFAULT 'potential' CHECK(status IN ('potential', 'verified', 'dismissed')),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (lost_item_id) REFERENCES items (id) ON DELETE CASCADE,
        FOREIGN KEY (found_item_id) REFERENCES items (id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS activity_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT NOT NULL,
        details TEXT,
        ip_address TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL
    );

    CREATE INDEX IF NOT EXISTS idx_items_type ON items (type);
    CREATE INDEX IF NOT EXISTS idx_items_category ON items (category);
    CREATE INDEX IF NOT EXISTS idx_items_status ON items (status);
    CREATE INDEX IF NOT EXISTS idx_items_date ON items (item_date);
    """)
    conn.commit()
    conn.close()
    logger.info("SQLite schema initialized successfully.")

def _seed_default_admin(app):
    """Seed the initial administrator user if not already in the database."""
    admin_email = app.config.get('DEFAULT_ADMIN_EMAIL', 'admin@campusfind.edu')
    admin_pass = app.config.get('DEFAULT_ADMIN_PASSWORD', 'Admin@CampusFind2026')
    admin_name = app.config.get('DEFAULT_ADMIN_NAME', 'Campus Administrator')

    existing = query_db("SELECT id FROM users WHERE email = %s", (admin_email,), one=True)
    if not existing:
        hashed = generate_password_hash(admin_pass)
        execute_db(
            "INSERT INTO users (full_name, email, student_id, phone, password_hash, role) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (admin_name, admin_email, 'ADMIN-001', '000-000-0000', hashed, 'admin')
        )
        logger.info("Default admin user created: %s", admin_email)
