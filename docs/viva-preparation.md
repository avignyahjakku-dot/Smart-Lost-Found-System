# CampusFind — College Demonstration & Viva Voce Guide

**Degree:** Bachelor of Technology in Computer Science & Engineering (BTech CSE)  
**Project:** Smart Lost & Found System (CampusFind)  
**Type:** Two-Person Team Capstone Project  
**Repository:** [https://github.com/avignyahjakku-dot/Smart-Lost-Found-System.git](https://github.com/avignyahjakku-dot/Smart-Lost-Found-System.git)  
**Test Suite Status:** 51 Automated Tests Passed (100% Pass Rate across 8 Suites)

---

## Table of Contents
1. [Part A — College Demonstration Checklist](#part-a--college-demonstration-checklist)
   - [A1. Pre-Demo Environment & Database Setup](#a1-pre-demo-environment--database-setup)
   - [A2. 10-Step Practical Demonstration Script](#a2-10-step-practical-demonstration-script)
   - [A3. Post-Demo Data Cleanup Instructions](#a3-post-demo-data-cleanup-instructions)
2. [Part B — Viva Voce Questions & Answers](#part-b--viva-voce-questions--answers)
   - [B1. Beginner Questions (Foundations & Overview)](#b1-beginner-questions-foundations--overview)
   - [B2. Intermediate Questions (Architecture, Database & Algorithms)](#b2-intermediate-questions-architecture-database--algorithms)
   - [B3. Advanced Questions (Security, Invariants, Trade-offs & DSA vs B+ Trees)](#b3-advanced-questions-security-invariants-trade-offs--dsa-vs-b-trees)
3. [Part C — Codebase Architecture & Request Lifecycle](#part-c--codebase-architecture--request-lifecycle)
   - [C1. File-by-File Technical Directory Map](#c1-file-by-file-technical-directory-map)
   - [C2. End-to-End HTTP Request Lifecycle Walkthrough](#c2-end-to-end-http-request-lifecycle-walkthrough)
4. [Part D — Honest Claims & Academic Disclosures](#part-d--honest-claims--academic-disclosures)
   - [D1. Verified vs. Unverified Features](#d1-verified-vs-unverified-features)
   - [D2. Disclosures to Proactively Acknowledge](#d2-disclosures-to-proactively-acknowledge)
5. [Summary of Remaining Tasks Prior to Presentation](#summary-of-remaining-tasks-prior-to-presentation)

---

# Part A — College Demonstration Checklist

### A1. Pre-Demo Environment & Database Setup

#### 1. Hardware & Software Prerequisites
- Laptop running Windows, macOS, or Linux.
- Python 3.10+ (tested with Python 3.13.6 64-bit).
- Web browser (Chrome, Firefox, or Edge).
- Optional: MySQL 8.0+ server running on `127.0.0.1:3306` (or use the zero-configuration default SQLite engine).

#### 2. Virtual Environment & Dependency Verification
Open PowerShell or Terminal in the project root:
```powershell
# 1. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 2. Verify dependencies
pip install -r requirements.txt

# 3. Verify that all 51 automated tests pass
python run_tests.py
```

#### 3. Database Selection (`.env` Configuration)
The system automatically connects to MySQL or falls back gracefully to SQLite:
- **Option 1: Zero-Configuration SQLite (Recommended for offline viva portability)**
  Ensure `.env` contains:
  ```env
  DB_TYPE=sqlite
  SECRET_KEY=college-viva-demo-session-secret-2026
  ```
- **Option 2: MySQL Connection (If external database demonstration is requested by examiners)**
  Start MySQL service (e.g. XAMPP or native MySQL) and set:
  ```env
  DB_TYPE=mysql
  DB_HOST=127.0.0.1
  DB_PORT=3306
  DB_NAME=campusfind
  DB_USER=root
  DB_PASSWORD=your_password
  ```
  Initialize MySQL schema:
  ```bash
  mysql -u root -p campusfind < schema.sql
  ```

#### 4. Seed Representative Campus Data
Run the database seeder to populate sample users and realistic items:
```bash
python seed.py
```
*Note: Run `python seed.py --reset` if you need to wipe previous demonstration test runs.*

---

### A2. 10-Step Practical Demonstration Script

| Step | Action | Exact Route / URL | Input Data / Demo Values | What to Highlight to the Examiner |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Start Application** | Terminal command: `python run.py` | Open `http://127.0.0.1:5000` | Point out the clean terminal boot, automatic schema verification, and default port 5000 binding. |
| **2** | **Homepage & Live Metrics** | `GET /` | Homepage landing view | Highlight live metrics counter (Total Items, Open Reports, Successful Claims), quick action buttons, and responsive navbar. |
| **3** | **Student Registration & Login** | `GET /register`<br>`GET /login` | Full Name: `Siddharth Rao`<br>Email: `siddharth@campusfind.edu`<br>Student ID: `21BCE3099`<br>Phone: `+91 9876501234`<br>Password: `DemoUser@2026` | Point out client-side password strength hint ($\ge 8$ chars), server-side hashing (`generate_password_hash`), and immediate session login upon registration. |
| **4** | **Report a Lost Item** | `GET /report/lost` | Title: `Titan Midnight Blue Analog Watch`<br>Category: `Clothing & Accessories`<br>Location: `Sports Ground / Gym`<br>Date: Today's date<br>Description: `Titan quartz watch with dark blue dial and silver stainless steel strap, misplaced near basketball court bleachers.`<br>Secret Hint: `What color is the second hand?` | Point out mandatory field indicators, 150-char title limit, 2000-char description limit, secret verification hint, and automatic insertion into in-memory BST. |
| **5** | **Report a Found Item** | `GET /report/found` (as Security/Staff user `security@campusfind.edu` / `Student@123`) | Title: `Blue Dial Titan Wristwatch`<br>Category: `Clothing & Accessories`<br>Location: `Sports Ground / Gym`<br>Date: Today's date<br>Description: `Found on bleachers near gym court. Analog watch with metal strap.`<br>Storage Location: `Gym Security Counter Locker B-4` | Point out the physical custody field (`storage_location`), preventing found items from floating unaccounted on campus. |
| **6** | **Search & Filter Catalog** | `GET /browse` | Keyword: `watch`<br>Category filter: `Clothing & Accessories`<br>Location: `Sports Ground / Gym`<br>Sort: `Newest` | Highlight multi-parameter SQL filtering with parameterized conditions (`AND i.category = %s`, `AND i.location = %s`), dynamic filter pill retainers, and card elevations. |
| **7** | **Demonstrate Smart Matching** | `GET /items/<lost_item_id>` | Click on Siddharth's lost Titan watch report | Point out the **Matching Engine** panel: **High Confidence (85%+)**. Show transparent factor breakdown: Category ($30/30$), Text overlap ($21/35$), Location match ($20/20$), and Date plausibility ($15/15$). Explain that no black box is used. |
| **8** | **Submit Ownership Claim** | Click **Claim This Item** button on the found Titan Watch | Proof Details: `Purchased in August 2025; has a faint scratch at the 4 o'clock mark.`<br>Secret Answer: `White with a red arrow`<br>Contact Phone: `+91 9876501234` | Show modal dialog accessibility (`role="dialog"`, auto-focus, Esc key close). Explain that claimants cannot claim their own items. Show status changing to `Pending Review`. |
| **9** | **Admin Dashboard & Adjudication** | `GET /admin/dashboard` (Log in as `admin@campusfind.edu` / `Admin@CampusFind2026`) | Review Claim # in Pending table.<br>Click **Approve Claim** with remarks: `Verified scratch and dial details with security officer.` | Show administrative authorization decorator (`@admin_required`), claim status transition to `Approved`, associated item status auto-updating to `Claimed`, and irreversible activity log recording. |
| **10**| **BST Visualizer & Traversal** | `GET /dsa/visualizer` | 1. Click **Search** for Item ID `15`<br>2. Click **Insert** key `42`<br>3. Click **Delete** key `20`<br>4. Click **In-Order Traversal** | Demonstrate live SVG graph rendering: highlight search path (root $\rightarrow$ node), show traversal output strictly producing sorted ascending keys in $\mathcal{O}(n)$, and explain Case 1, 2, and 3 deletion with in-order successor. |

---

### A3. Post-Demo Data Cleanup Instructions

To remove only the demonstration records created during the presentation without wiping the existing seed data or user accounts, run this clean-up query in your database tool (or execute via `python`):

```python
# Clean up demonstration records safely
from app import create_app
from app.db import execute_db, query_db

app = create_app('development')
with app.app_context():
    # 1. Identify demo user
    demo_user = query_db("SELECT id FROM users WHERE email = 'siddharth@campusfind.edu'", one=True)
    if demo_user:
        uid = demo_user['id']
        # 2. Delete demo claims submitted by or involving demo items
        execute_db("DELETE FROM claims WHERE claimant_id = %s", (uid,))
        # 3. Delete demo items reported by demo user
        execute_db("DELETE FROM items WHERE user_id = %s", (uid,))
        # 4. Delete demo user
        execute_db("DELETE FROM users WHERE id = %s", (uid,))
        print(f"Successfully cleaned up demo user {uid} and associated records.")
    
    # 5. Remove any found item created during demo
    execute_db("DELETE FROM items WHERE title = 'Blue Dial Titan Wristwatch'")
    print("Demo cleanup complete. Base database records preserved.")
```

---

# Part B — Viva Voce Questions & Answers

### B1. Beginner Questions (Foundations & Overview)

#### Q1: What is the problem statement and motivation behind CampusFind?
**Answer:**
In college campuses, hundreds of valuable personal items—such as student ID cards, laptops, calculators, keys, and wallets—are lost and found every semester. Existing mechanisms are fragmented: handwritten logbooks at security gates, chaotic WhatsApp groups, or unmonitored social media posts. Items often sit in departmental closets because finders do not know who the owner is, and owners do not know where to search. CampusFind solves this by centralizing lost and found reports into a structured web portal featuring automated similarity matching, verified ownership claims, and an educational Data Structures & Algorithms visualizer.

#### Q2: What is the Model-View-Controller (MVC) architecture, and how does CampusFind implement it?
**Answer:**
MVC separates application concerns:
- **Model:** Data persistence and business logic handled by `app/db.py` (relational queries), `app/matching.py` (heuristic similarity engine), and `app/dsa/bst.py` (in-memory tree index).
- **View:** User interface rendered using server-side Jinja2 templates (`app/templates/`) and styled with custom responsive CSS (`app/static/css/main.css`).
- **Controller:** Flask Blueprints (`app/auth.py`, `app/items.py`, `app/claims.py`, `app/admin.py`, `app/dsa/routes.py`) that receive HTTP requests, validate input, call models, and return HTTP responses or JSON.

#### Q3: What technologies and programming languages did you use to build this project?
**Answer:**
- **Backend:** Python 3.13 with Flask 3.0 web micro-framework.
- **Database:** MySQL 8.0 (production-ready relational store) with a dual-engine adapter supporting SQLite 3 for zero-configuration local portability and test isolation.
- **Frontend:** Semantic HTML5, responsive CSS3 (custom CSS variable design system without heavy bloated frameworks), and Vanilla JavaScript (ES6+).
- **Data Structures:** Custom-implemented Binary Search Tree (BST) rendered using Dynamic Scalable Vector Graphics (SVG).
- **Testing:** Python `unittest` library (51 automated tests across 8 suites).

#### Q4: How does Flask handle routing?
**Answer:**
Flask uses Python function decorators like `@blueprint.route('/url', methods=['GET', 'POST'])` to bind URL endpoints to Python view functions. In CampusFind, routes are organized into modular **Blueprints** (`auth_bp`, `items_bp`, `claims_bp`, `admin_bp`, `dsa_bp`) and registered in the application factory (`create_app()` in `app/__init__.py`). When an HTTP request reaches the WSGI server, Werkzeug matches the requested URL and HTTP method against the routing table and executes the associated view function.

---

### B2. Intermediate Questions (Architecture, Database & Algorithms)

#### Q5: How does frontend and backend communication work in CampusFind?
**Answer:**
CampusFind uses a hybrid approach:
1. **Multi-Page Application (MPA) Flow:** Standard HTML form submissions (`POST`) for actions like registration, login, item reporting, and claim filing. The backend processes the request, commits database transactions, flashes feedback messages (`flash()`), and issues an HTTP 302 redirect.
2. **Asynchronous REST API (AJAX/Fetch) Flow:** In the BST visualizer (`app/static/js/bst_visualizer.js`), the frontend issues asynchronous HTTP requests using the browser's `fetch()` API (`POST /dsa/api/search`, `POST /dsa/api/insert`, `GET /dsa/api/traverse`). The Flask backend returns JSON responses (`jsonify`), allowing the UI to animate tree nodes and search paths dynamically without reloading the web page.

#### Q6: Explain your database schema design and relational integrity.
**Answer:**
The schema consists of 5 normalized relational tables:
1. `users`: Stores user identity, student IDs, contact numbers, password hashes, and roles (`student`, `staff`, `admin`).
2. `items`: Stores lost and found reports, type (`lost`/`found`), categories, dates, campus locations, descriptions, secret verification hints, and custody storage locations. Linked to `users.id` via foreign key `ON DELETE CASCADE`.
3. `claims`: Stores ownership claims filed by claimants, with proof text, contact info, and status (`pending`, `approved`, `rejected`). Linked to both `items.id` and `users.id`.
4. `matches`: Stores pre-computed or saved similarity pairings between lost and found items.
5. `activity_logs`: Audit trail recording critical administrative and user actions (`CLAIM_APPROVED`, `ITEM_DELETED`, `CLAIM_SUBMITTED`).

#### Q7: How are user passwords secured? Can an administrator read users' passwords in the database?
**Answer:**
No. Passwords are never stored in plaintext. CampusFind uses Werkzeug's `generate_password_hash()` which implements modern salted cryptographic hashing (Scrypt or PBKDF2 with SHA-256). During registration:
$$\text{Hash} = \text{KDF}(\text{Password}, \text{Salt}, \text{Cost Factors})$$
When a user logs in, `check_password_hash(stored_hash, submitted_password)` recomputes the derivation and performs a constant-time comparison. Even if an attacker or database administrator dumps the `users` table, the original plaintext passwords cannot be reversed.

#### Q8: How does the Smart Matching algorithm determine if a lost item matches a found item?
**Answer:**
The matching engine (`app/matching.py`) implements a deterministic, multi-factor heuristic scoring system yielding a score between $0.0$ and $100.0$:
1. **Category Compatibility ($30\%$ weight):** Exact match yields $30$ points; category mismatch yields $0$ points.
2. **Textual Keyword Similarity ($35\%$ weight):** Titles and descriptions are tokenized, normalized to lowercase, stripped of punctuation, and filtered against an English stop-word list. Jaccard similarity is computed:
   $$J(A, B) = \frac{|A \cap B|}{|A \cup B|}$$
   Points are awarded based on Jaccard overlap, shared word count, and title keyword matches.
3. **Location Proximity ($20\%$ weight):** Exact campus location match yields $20$ points; shared landmark tokens yield $15$ points; different zones yield $3$ points.
4. **Chronological Plausibility ($15\%$ weight):** Compares reported dates. If the found date matches or follows the lost date within $3$ days, full points are awarded ($14\text{--}15$ points). If an item was reportedly found days *before* it was lost, a chronological penalty is applied ($0$ points).
Scores $\ge 75\%$ are categorized as **High Confidence**, $50\%\text{--}74\%$ as **Moderate**, and $30\%\text{--}49\%$ as **Plausible**.

#### Q9: What are the operations and time complexities of your Binary Search Tree (BST)?
**Answer:**
- **Insertion (`insert(key, data)`):** Traverses left if $\text{key} < \text{current.key}$, right if $\text{key} > \text{current.key}$. Average time: $\mathcal{O}(\log n)$, worst-case: $\mathcal{O}(n)$ if keys are inserted in strictly sorted order (skewed tree).
- **Search (`search(key)`):** Compares key at each node, recording the path of traversed keys. Average time: $\mathcal{O}(\log n)$, worst-case: $\mathcal{O}(n)$.
- **Deletion (`delete(key)`):** Handles 3 structural cases:
  1. *Leaf node (0 children):* Removed directly.
  2. *Single child (1 child):* Parent pointer bypassed to the child.
  3. *Two children (2 children):* Target node replaced with its in-order successor (minimum node in the right subtree), which is then deleted recursively. Average time: $\mathcal{O}(\log n)$, worst-case: $\mathcal{O}(n)$.
- **In-Order Traversal (`inorder_traversal()`):** Recursively visits Left Subtree $\rightarrow$ Root $\rightarrow$ Right Subtree. Guarantees output in strictly ascending sorted order in $\mathcal{O}(n)$ time.

---

### B3. Advanced Questions (Security, Invariants, Trade-offs & DSA vs B+ Trees)

#### Q10: Why did you implement a Binary Search Tree (BST) in Python when MySQL already has built-in indexes? When is a database index better?
**Answer:**
- **Academic and Architectural Justification:**
  In this BTech CSE project, the in-memory BST was implemented to demonstrate core algorithmic principles: pointer manipulation, recursive deletion, in-order ordering invariants, and search path tracking that powers the interactive educational visualizer (`/dsa/visualizer`).
- **When a Database B+ Tree Index is Superior:**
  1. **Disk I/O and Block Paging:** A standard BST has a branching factor of 2, resulting in a tree height of $\log_2(n)$. In disk storage, each pointer hop causes a disk read. A database index uses a **B+ Tree**, which has a branching factor of hundreds or thousands, keeping height extremely shallow (3 to 4 levels for millions of rows) and aligning nodes with filesystem page blocks ($4\text{KB}\text{--}16\text{KB}$).
  2. **Concurrency and ACID Transactions:** Relational database indexes support multi-version concurrency control (MVCC), row-level locks, and write-ahead logging (WAL). A simple in-memory Python BST cannot handle concurrent multi-threaded writes without global locks.
  3. **Self-Balancing Guarantee:** A standard BST can degenerate into a linked list ($\mathcal{O}(n)$) if items are inserted with sequential IDs ($1, 2, 3\dots$). B+ Trees are strictly self-balancing.
- **Dual-Layer Solution in CampusFind:**
  CampusFind uses **B+ Tree indexes** inside MySQL/SQLite (`CREATE INDEX idx_items_category`, `idx_items_status`, `idx_items_date`) for persistent, high-throughput queries, while maintaining an **in-memory BST cache** for instant search-path visualization and student algorithmic evaluation.

#### Q11: How did you harden CampusFind against common web vulnerabilities (OWASP Top 10)?
**Answer:**
1. **SQL Injection (SQLi):** All database operations in `app/db.py` use parameterized queries (`%s` in MySQL and `?` in SQLite). User input is treated strictly as literal data, never concatenated into SQL strings.
2. **Cross-Site Scripting (XSS):** Jinja2 template auto-escaping is active across all templates. Any `<script>` tags injected into item titles or descriptions are safely converted into HTML entities (`&lt;script&gt;`).
3. **Cross-Site Request Forgery (CSRF):** State-changing forms include cryptographic CSRF tokens stored in the session and verified using `secrets.compare_digest()` to prevent timing attacks.
4. **Broken Access Control & IDOR:** Protected endpoints use `@login_required` and `@admin_required` decorators. In item status updates and deletion routes, ownership checks (`item['user_id'] == session['user_id'] or session['user_role'] == 'admin'`) prevent Insecure Direct Object Reference (IDOR) attacks.
5. **Malicious File Uploads:** Uploaded image filenames are sanitized via `werkzeug.utils.secure_filename()`. File extensions are restricted to `{'png', 'jpg', 'jpeg', 'gif', 'webp'}`, request payload size is capped at 5 MB (`MAX_CONTENT_LENGTH`), and file headers are validated against image magic bytes (e.g., `\x89PNG\r\n\x1a\n` for PNG).
6. **Session Hijacking:** Session cookies are configured with `SESSION_COOKIE_HTTPONLY = True` (inaccessible to JavaScript) and `SESSION_COOKIE_SAMESITE = 'Lax'` (mitigates cross-site request leakage).

#### Q12: How did you ensure test isolation across your 51 automated tests?
**Answer:**
In `tests/conftest.py` and test suite setups, tests run under `TestingConfig` (`TESTING = True`). Rather than touching the development or production database (`campusfind.db` or MySQL `campusfind`), the test suite dynamically creates an isolated test database (`test_campusfind.db`). In `setUp()`, the test schema is freshly initialized, and in `tearDown()`, database connections are cleanly closed and test artifacts purged. This prevents test pollution, eliminates test execution order dependencies, and ensures repeatable test runs ($51/51$ passed).

#### Q13: If sequential item IDs ($1, 2, 3, 4\dots$) are inserted into a standard BST, the tree degenerates into a linear list ($\mathcal{O}(n)$). How does CampusFind handle or mitigate this?
**Answer:**
In a standard unaugmented BST, sequential insertions create a right-skewed tree with height equal to $n$. In CampusFind:
1. For production querying, primary lookup does not solely rely on the Python BST; persistent database queries leverage database B+ Trees which remain balanced.
2. In the DSA visualizer service (`app/dsa/bst_service.py`), when the tree is bootstrapped or reset, it inserts keys in a balanced binary sequence (e.g. root $50$, children $25, 75, 12, 37\dots$), demonstrating optimal $\mathcal{O}(\log n)$ depth.
3. In viva discussions, this limitation is openly acknowledged: an academic extension to this project would be implementing an **AVL Tree** or **Red-Black Tree** using tree rotations to maintain balance invariants dynamically.

---

# Part C — Codebase Architecture & Request Lifecycle

### C1. File-by-File Technical Directory Map

```
smart lost & found system/
│
├── run.py                          # Application entry point; runs development server on port 5000
├── seed.py                         # Realistic seed script for campus users, reports, and claims
├── schema.sql                      # Production MySQL 8 relational schema with tables and foreign keys
├── requirements.txt                # Pinned Python package dependencies (Flask, PyMySQL, etc.)
├── run_tests.py                    # Automated test discovery and execution script (51 tests)
│
├── app/
│   ├── __init__.py                 # Application factory (create_app), blueprint registrations, error handlers
│   ├── config.py                   # Configuration classes (Development, Testing, Production)
│   ├── db.py                       # Dual-engine database adapter (MySQL + SQLite fallback), query_db, execute_db
│   ├── auth.py                     # Authentication blueprint: register, login, logout, password hashing, RBAC
│   ├── items.py                    # Items blueprint: report lost/found, search, filter, item details
│   ├── claims.py                   # Claims blueprint: submit ownership claim, check status, validation
│   ├── admin.py                    # Admin blueprint: dashboard, review/approve claims, delete items, view logs
│   ├── matching.py                 # Smart Matching heuristic engine: category, tokens, location, date weights
│   │
│   ├── dsa/                        # Data Structures & Algorithms package
│   │   ├── __init__.py             # Exports BST classes and service
│   │   ├── bst.py                  # Core BinarySearchTree, BSTNode, insert, search, 3-case delete, traversals
│   │   ├── bst_service.py          # GlobalItemBST singleton indexing items by ID
│   │   └── routes.py               # DSA blueprint: visualizer page and REST API endpoints (/api/tree, /api/search)
│   │
│   ├── templates/                  # Jinja2 HTML templates
│   │   ├── base.html               # Master layout: responsive navigation, flash messages, accessibility skip link
│   │   ├── index.html              # Homepage: system metrics, feature cards, recent reports
│   │   ├── auth/                   # login.html, register.html
│   │   ├── items/                  # browse.html, detail.html, report_lost.html, report_found.html
│   │   ├── admin/                  # dashboard.html
│   │   └── dsa/                    # visualizer.html (interactive SVG BST canvas)
│   │
│   └── static/                     # Static web assets
│       ├── css/
│       │   ├── main.css            # Responsive design system, CSS variables, components, accessibility
│       │   └── visualizer.css      # BST tree node styling, SVG animations, search highlights
│       ├── js/
│       │   ├── main.js             # Mobile navbar toggle, modal dialog controller, double-submit protection
│       │   └── bst_visualizer.js   # SVG tree renderer, coordinate calculation, search path animation
│       └── uploads/                # Directory for user-uploaded item photos (git-ignored)
│
├── docs/                           # Comprehensive technical and academic documentation
│   ├── architecture.md             # High-level architecture, MVC flow, quality attributes
│   ├── database-design.md          # Mermaid ER diagrams, table schemas, B+ Tree index strategy
│   ├── testing.md                  # QA testing methodology, 51-test matrix, test isolation
│   ├── user-guide.md               # User & Admin operational guide with walkthrough steps
│   ├── security.md                 # OWASP Top 10 mitigation matrix, encryption, cookie hardening
│   └── viva-preparation.md         # Demonstration script, viva questions & answers, code explanation
│
└── tests/                          # 8 Modular Automated Test Suites (51 tests)
    ├── __init__.py                 # Test package initialization
    ├── conftest.py                 # BaseTestCase fixtures with isolated test database setup
    ├── test_auth.py                # 5 tests: registration, password hashing, login/logout, route guards
    ├── test_items.py               # 5 tests: report lost/found, search, image validation, bounds
    ├── test_claims.py              # 5 tests: claim lifecycle, approval, rejection, self-claim rejection
    ├── test_matching.py            # 7 tests: tokenization, Jaccard, location/date scoring, penalties
    ├── test_bst.py                 # 10 tests: insert, search path, 3-case delete, in-order ordering, min/max
    ├── test_dsa_routes.py          # 7 tests: /dsa/visualizer HTML, /api/tree, /api/search, /api/delete
    ├── test_security.py            # 6 tests: SQLi resilience, XSS escaping, IDOR prevention, cookie flags
    └── test_integration.py         # 6 tests: app startup, homepage, catalog, error handlers, foreign keys
```

---

### C2. End-to-End HTTP Request Lifecycle Walkthrough

To explain how the application operates from end to end, walk the examiner through what happens when a user submits a Found Item report:

```
[User Browser]
      │
      │ 1. Submits HTML Form (POST /report/found) with title, category, location, date, photo
      ▼
[Flask Application Router (app/__init__.py)]
      │
      │ 2. Routes to items_bp in app/items.py -> report_found()
      ▼
[@login_required Decorator (app/auth.py)]
      │
      │ 3. Verifies 'user_id' in session (redirects to /login if unauthenticated)
      ▼
[Input Validation & File Sanitization (app/items.py)]
      │
      │ 4. Validates required fields, checks character limits (title <= 150, desc <= 2000)
      │ 5. Validates uploaded file extension & magic bytes (PNG/JPG header check)
      │ 6. Sanitizes filename with secure_filename() and saves to app/static/uploads/
      ▼
[Database Persistence Layer (app/db.py)]
      │
      │ 7. Calls execute_db("INSERT INTO items (...) VALUES (%s, ...)", (...), return_id=True)
      │ 8. Translates %s to ? if SQLite; executes parameterized SQL query safely
      │ 9. Commits transaction and retrieves new item_id
      ▼
[In-Memory DSA Indexing (app/dsa/bst_service.py)]
      │
      │ 10. Calls global_item_index.index_item({'id': item_id, 'title': title, ...})
      │ 11. Inserts item node into in-memory BST for fast tree traversal and visualizer sync
      ▼
[Response & Redirect (app/items.py)]
      │
      │ 12. Flashes success notification: flash("Thank you for reporting this found item!", "success")
      │ 13. Issues HTTP 302 Redirect to url_for('items.detail', item_id=item_id)
      ▼
[Item Detail View & Smart Matching (app/items.py -> detail())]
      │
      │ 14. Queries item details and opposite-type candidate items from database
      │ 15. Calls find_matches_for_item() in app/matching.py
      │ 16. Evaluates multi-factor heuristic scores (category, text tokens, location, date delta)
      │ 17. Renders app/templates/items/detail.html via Jinja2 with match candidate cards
      ▼
[User Browser]
      │
      └─► Displays rendered HTML with item information, custody location, and match candidates!
```

---

# Part D — Honest Claims & Academic Disclosures

In a BTech CSE viva, examiners respect honest engineering appraisals far more than exaggerated claims. Distinguish clearly between what is verified and what is design-scoped.

### D1. Verified vs. Unverified Features

| Feature / Metric | Status in CampusFind | Exact Evidence in Codebase |
| :--- | :---: | :--- |
| **User Authentication & RBAC** | **Verified** | Werkzeug salted password hashing, permanent sessions, `@login_required`, `@admin_required` in `app/auth.py`. 5 tests passing. |
| **Dual-Engine Database Adapter** | **Verified** | Tested with both MySQL 8 and SQLite 3 in `app/db.py`, automatic `%s` to `?` translation, foreign keys enforced. |
| **Heuristic Smart Matching** | **Verified** | Deterministic 4-factor scoring ($30\%$ category, $35\%$ text Jaccard, $20\%$ location, $15\%$ date) in `app/matching.py`. 7 tests passing. |
| **Binary Search Tree Implementation** | **Verified** | Custom Python BST with 3-case deletion, in-order sorted traversal, and path tracing in `app/dsa/bst.py`. 10 tests passing. |
| **Interactive SVG Visualizer** | **Verified** | Responsive SVG tree rendering, keyboard navigation, and REST API path animation in `app/dsa/routes.py` and `bst_visualizer.js`. 7 tests passing. |
| **Verified Test Coverage** | **Verified** | Exactly **51 automated tests** across 8 modular test suites. 0 errors, 0 failures. |
| **Deep Learning / Image Embeddings** | **Not Implemented** | Matching is lexical and heuristic (Jaccard + keyword overlap), **not** convolutional neural networks (CNNs) or ResNet image embeddings. |
| **SMS / Mobile Push Gateway** | **Not Implemented** | Notifications are in-app flash messages and activity logs, **not** third-party SMS (e.g. Twilio) gateways. |
| **Real User Adoption Statistics** | **Academic Scope** | Sample data represents simulated campus testing scenarios, **not** a production deployment with thousands of live active students. |

### D2. Disclosures to Proactively Acknowledge

1. **In-Memory BST Persistence Across Server Restarts:**  
   *Viva Disclosure:* "The Binary Search Tree runs in-memory within the Python application process. If the Flask server restarts, the tree is re-populated from the relational database upon first access. In a distributed multi-worker WSGI deployment (like Gunicorn with multiple worker processes), each worker maintains its own memory space; therefore, primary persistent storage remains the relational database."
2. **Lexical Matching vs. Semantic AI Embeddings:**  
   *Viva Disclosure:* "The matching algorithm is a deterministic heuristic scoring engine combining category filtering, Jaccard token overlap, campus location proximity, and chronological plausibility. While it effectively pairs items with matching keywords (e.g., 'Dell laptop' and 'Silver Dell laptop'), it does not capture deep semantic synonyms (e.g., 'shades' vs. 'sunglasses') unless such words exist in an expanded synonym dictionary. Integrating vector embeddings (like Sentence-BERT) is documented as a future enhancement."
3. **Tree Balance Invariant:**  
   *Viva Disclosure:* "The current tree is a standard Binary Search Tree. If items are inserted with monotonically increasing IDs without shuffling, the tree depth can degenerate towards $\mathcal{O}(n)$. In a production evolution, self-balancing trees like AVL or Red-Black trees would be implemented to guarantee $\mathcal{O}(\log n)$ worst-case operations."

---

# Summary of Remaining Tasks Prior to Presentation

1. **Rehearse the 10-Step Demo Script:** Walk through the script once end-to-end on your presentation laptop to verify timing (~5 to 7 minutes).
2. **Review the Part B Viva Questions:** Practice answering the intermediate and advanced questions aloud, especially the comparison between BSTs and database B+ Tree indexes.
3. **Verify Display Resolution:** Open `http://127.0.0.1:5000/dsa/visualizer` and test zooming in your browser (Ctrl + / Ctrl -) to ensure the SVG canvas scales cleanly on classroom projectors.
4. **Keep Terminal Ready:** Keep one terminal window open running `python run.py`, and a second terminal window ready in case the examiner asks to run `python run_tests.py` live.
5. **Phase 4 Git Synchronization:** When you are ready, proceed to Phase 4 to stage, commit, and push these completed Phase 3 enhancements and documentation to your GitHub repository.
