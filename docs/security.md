# CampusFind — Application Security & Hardening Specification

> **Project:** Smart Lost & Found System (CampusFind)  
> **Course:** Bachelor of Technology (BTech) in Computer Science & Engineering (CSE)  
> **Author:** Two-Person BTech CSE Capstone Project Team  
> **Focus:** Web Application Security, Threat Mitigation, and OWASP Top 10 Compliance  

---

## 1. Security Philosophy & Overview

CampusFind handles sensitive student records, personal identifying information, and ownership claims for valuable physical property. The application implements defense-in-depth security principles across authentication, session management, input validation, database querying, and file handling.

---

## 2. Threat Mitigation Matrix

| OWASP Top 10 Threat Category | Specific Attack Vector | CampusFind Defense Implementation |
| :--- | :--- | :--- |
| **A01: Broken Access Control** | Unauthorized access to admin moderation or modifying another user's item. | Role-based route decorators (`@admin_required`, `@login_required`) and explicit ownership verification queries preventing Insecure Direct Object References (IDOR). |
| **A02: Cryptographic Failures** | Plaintext credential exposure or weak password hashing. | Password hashing using Werkzeug (`scrypt` / `pbkdf2:sha256`) with per-user cryptographic salts and minimum 8-character length enforcement. |
| **A03: Injection** | SQL Injection in catalog search queries, filter parameters, or claim submissions. | 100% parameterized SQL queries (`%s` in MySQL, `?` in SQLite) executed via the unified database adapter (`app/db.py`). |
| **A04: Insecure Design** | Fraudulent claims claiming high-value items without proof. | Dual-factor ownership verification requiring distinguishing mark descriptions and answers to secret owner challenge questions. |
| **A05: Security Misconfiguration** | Debug mode in production or insecure session cookies. | Production configuration class enforcing `DEBUG=False`, `SESSION_COOKIE_HTTPONLY=True`, `SESSION_COOKIE_SAMESITE='Lax'`, and `SESSION_COOKIE_SECURE=True`. |
| **A06: Vulnerable & Outdated Components** | Unnecessary third-party library dependencies. | Minimal dependency footprint: zero client-side CDN dependencies and locked, audited server packages in `requirements.txt`. |
| **A07: Identification & Auth Failures** | Session hijacking or session fixation. | Fresh session ID regeneration on login and complete session clearing on logout. |
| **A08: Software & Data Integrity Failures** | Malicious file uploads (e.g. PHP/shell scripts disguised as images). | File extension allowlisting (`png`, `jpg`, `jpeg`, `gif`, `webp`), `MAX_CONTENT_LENGTH` enforcement (5MB), and magic-byte header verification. |
| **A09: Security Logging & Monitoring** | Undetected administrative actions or moderation abuses. | Immutable `activity_logs` table recording all administrative interventions, claim decisions, and item deletions with timestamps. |
| **A10: Server-Side Request Forgery & XSS** | Injected JavaScript executing in user browsers. | Automatic HTML escaping across all Jinja2 template renderings. |

---

## 3. Defense Mechanisms & Implementation Details

### 3.1 Password Hashing & Key Derivation (`app/auth.py`)
- Passwords are never stored in plaintext or reversible encryption.
- On user registration and password updates, passwords are processed through `werkzeug.security.generate_password_hash()`:
  - Employs `scrypt` (or `pbkdf2:sha256`) with high iteration counts and random salts.
  - Generates hashes of length 150+ characters stored in `password_hash VARCHAR(255)`.
- Verification via `check_password_hash()` uses constant-time comparison to prevent timing side-channel attacks.
- Passwords must be at least 8 characters and no more than 128 characters.

### 3.2 Session Management & Cookie Security (`app/config.py`)
- Sessions are stored in cryptographically signed, tamper-resistant HTTP cookies signed with `Config.SECRET_KEY`.
- Cookie security attributes:
  - `SESSION_COOKIE_HTTPONLY = True`: Blocks client-side JavaScript access via `document.cookie`, mitigating XSS session theft.
  - `SESSION_COOKIE_SAMESITE = 'Lax'`: Protects cookies against Cross-Site Request Forgery (CSRF) in cross-origin requests.
  - `SESSION_COOKIE_SECURE = True`: (Enforced in `ProductionConfig`) Ensures cookies are transmitted exclusively over encrypted HTTPS channels.
  - `PERMANENT_SESSION_LIFETIME = timedelta(days=7)`: Bounds session validity windows.

### 3.3 Role-Based Access Control (RBAC) & Authorization (`app/auth.py`)
Routes are guarded by explicit Python decorators:
```python
def admin_required(f):
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
```
Non-admin users attempting to forge direct requests to `/admin/dashboard` or administrative moderation endpoints are immediately deflected with HTTP 302 and an access violation flash alert.

### 3.4 Insecure Direct Object Reference (IDOR) Mitigation (`app/items.py`)
When updating item lifecycle states (e.g. from `open` to `returned`):
```python
# app/items.py - IDOR verification check:
item = query_db("SELECT user_id FROM items WHERE id = %s", (item_id,), one=True)
if not item:
    flash("Item not found.", "danger")
    return redirect(url_for('items.browse'))

if item['user_id'] != session.get('user_id') and session.get('user_role') != 'admin':
    flash("You do not have permission to modify this item.", "danger")
    return redirect(url_for('items.detail', item_id=item_id))
```
A standard student cannot alter the status or details of items submitted by other students.

### 3.5 SQL Injection Protection (`app/db.py`)
- The unified database adapter rejects raw SQL string concatenation.
- Every query utilizes parameterized placeholders:
  ```python
  # Safe parameterized execution:
  query_db("SELECT * FROM items WHERE category = %s AND location = %s", (category, location))
  ```
- User inputs (such as `' OR 1=1 --`) are treated as literal strings by database query engines rather than executable SQL syntax.

### 3.6 Cross-Site Request Forgery (CSRF) Protection (`app/__init__.py`)
- Built-in, zero-dependency CSRF token generator:
  - Generates cryptographically strong random tokens using `secrets.token_hex(32)`.
  - Injects `csrf_token()` into all Jinja2 HTML forms as a hidden input.
  - Intercepts state-changing HTTP requests (`POST`, `PUT`, `DELETE`) in `@app.before_request`.
  - Performs constant-time comparison via `secrets.compare_digest(session_token, form_token)` to prevent timing side-channel attacks.
  - Aborts invalid or missing tokens with HTTP 400 Bad Request.

### 3.7 Secure File Upload Validation (`app/items.py`)
- **Extension Allowlisting:** Only extensions in `{'png', 'jpg', 'jpeg', 'gif', 'webp'}` are accepted.
- **Filename Sanitization:** Uploaded files are renamed using UUID hexadecimal strings (`uuid.uuid4().hex + ext`), preventing path traversal attacks (e.g. `../../etc/passwd`).
- **File Size Capping:** Enforced by `MAX_CONTENT_LENGTH = 5 * 1024 * 1024` (5 MB).
- **Magic-Byte Signature Inspection:** File header signatures are checked to ensure uploaded files are genuine images rather than disguised executable or shell binaries.

### 3.8 Server-Side Input Bounds & Validation
Every user-controlled input field is validated and constrained server-side before database persistence:
- **Full Name:** 1 to 100 characters.
- **Email:** Validated with RFC-compliant `@` structure, maximum 100 characters.
- **Password:** Minimum 8 characters, maximum 128 characters.
- **Item Title:** 1 to 150 characters.
- **Item Description:** 1 to 2000 characters.
- **Contact Phone:** 1 to 30 characters.
- **Proof Details:** 1 to 2000 characters.

---

## 4. Automated Security Verification

The project includes a dedicated automated security test suite in [`tests/test_security.py`](file:///c:/Users/6tan5/OneDrive/Desktop/smart%20lost%20&%20found%20system/tests/test_security.py):

| Test Method | Security Verification Target |
| :--- | :--- |
| `test_password_hashing_and_complexity` | Asserts hashes are not plaintext and rejects passwords $< 8$ characters. |
| `test_session_cookie_security_configurations` | Verifies `HttpOnly`, `SameSite=Lax`, and `Secure` attributes across environments. |
| `test_role_based_admin_protection` | Tests that guests and regular students cannot access `/admin/*` routes. |
| `test_idor_status_modification_prevention` | Tests that User B cannot modify User A's item status. |
| `test_sql_injection_resilience` | Executes classic SQL injection payloads and verifies they are treated as string literals. |
| `test_xss_auto_escaping` | Injects script tags into reports and verifies they are HTML-escaped on output. |

All 6 automated security tests pass cleanly ($6/6$ OK) within the overall 51-test suite.
