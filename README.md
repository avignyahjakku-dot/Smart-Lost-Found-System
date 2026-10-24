# CampusFind — Smart University Lost & Found System

> **Degree Program:** Bachelor of Technology (BTech) in Computer Science & Engineering (CSE)  
> **Project Type:** Two-Person Team Capstone Project  
> **Domain:** Full-Stack Web Engineering, Relational Database Systems, Applied Data Structures & Algorithms (DSA), Application Security  
> **Repository:** [https://github.com/avignyahjakku-dot/Smart-Lost-Found-System.git](https://github.com/avignyahjakku-dot/Smart-Lost-Found-System.git)  
> **Active Branch:** `main`  
> **Automated Test Status:** 51 Tests / 0 Errors / 0 Failures ($51/51$ Passing)  

---

## 1. Project Overview

**CampusFind** is a full-stack university lost-and-found web application developed as a two-person BTech CSE capstone project. It bridges the gap between misplaced personal belongings and campus finders. It integrates relational database persistence, an intelligent multi-factor heuristic matching engine, an authentic in-memory Binary Search Tree (BST) with an interactive SVG visualizer, role-based administrative moderation, and dual-factor ownership verification workflows.

---

## 2. Problem Statement

On university campuses, thousands of personal belongings—student identity cards, scientific calculators, laptops, room keys, noise-canceling headphones, and water bottles—are misplaced every semester. Conventional recovery methods suffer from systemic inefficiencies:
- **Fragmented Communication:** Information is scattered across informal WhatsApp group messages, physical notice boards, and disconnected security gates. Students have no single source of truth.
- **Vulnerability to False & Fraudulent Claims:** Public lost-and-found listings openly broadcast all details (serial numbers, colors, stickers), allowing unauthorized individuals to falsely claim items.
- **Lack of Automated Correlation:** Manually correlating hundreds of lost reports with turned-in custody items is tedious, slow, and error-prone.
- **Absence of Pedagogical DSA Integration:** Academic projects often fail to connect classroom algorithmic concepts (like tree traversals and logarithmic indexing) with real-world production web application requirements.

CampusFind resolves these challenges by providing a centralized, secure web repository with automated matching heuristics and an interactive algorithmic visualizer.

---

## 3. Project Objectives

1. **Centralized Campus Repository:** Provide an accessible, responsive platform for students, faculty, and security personnel to log and search lost and found property.
2. **Intelligent Algorithmic Matching:** Implement a multi-factor similarity scoring function that automatically pairs missing items with found inventory.
3. **Applied Data Structures (BST):** Implement a pure Python in-memory Binary Search Tree for $O(\log n)$ ordered lookups and range queries, coupled with a dynamic vector-rendered SVG visualizer.
4. **Security & Claim Verification:** Establish a verified recovery lifecycle incorporating secret owner challenge questions, proof documentation, and administrative adjudication.
5. **Robust Engineering & Testing:** Deliver a dual-engine database architecture (MySQL and SQLite fallback) validated by an automated test suite containing 51 unit, integration, and security tests.

---

## 4. Main Features

### 4.1 Student & Staff Features
- **Account Management:** User registration, secure login, password hashing, and session management.
- **Report Lost Items:** Log missing belongings with category, campus location, date/time, description, optional image, and an owner verification hint question.
- **Report Found Items:** Record discovered property, specifying the physical storage desk (e.g. Central Library Front Desk, Security Gate 1) where the item is securely held.
- **Catalog Browsing & Search:** Multi-parameter search by keyword, item type (`lost`/`found`), category, campus location, and date sorting.
- **Item Details & Algorithmic Insights:** Inspect item attributes, review the live in-memory BST logarithmic lookup path, and inspect top-ranked candidate matches with percentage scores.
- **Ownership Claim Submission:** Submit verified ownership claims with proof descriptions, contact phone numbers, and answers to secret verification questions.
- **Personal Activity Dashboard:** Track personal lost reports, found reports, and real-time claim evaluation statuses (`Pending`, `Approved`, `Rejected`).

### 4.2 Administrative Control Center
- **Role-Based Protection:** Protected `@admin_required` decorators preventing unauthorized access.
- **Live Metrics Dashboard:** Real-time metrics tracking total repository items, pending claims awaiting review, and resolved cases.
- **Claim Moderation:** Inspect claimant evidence, evaluate secret answers, and approve or reject claims with administrative notes. Approving a claim automatically transitions the found item to `claimed`.
- **Item Moderation:** Delete spam, duplicate, or inappropriate submissions with cascading cleanup.
- **System Audit Log:** Immutable activity log tracking all administrative decisions and moderation events.

### 4.3 Data Structures & Algorithms (DSA) Engine
- **Pure Python BST Class:** Supports $O(\log n)$ insertion, search with branch path tracing, three-case node deletion (leaf, 1 child, 2 children with in-order successor), and tree traversals.
- **Dynamic SVG Visualizer:** Vector canvas animating tree layout, search branch comparisons, deletion transitions, and traversals (in-order, pre-order, post-order).
- **Full Keyboard Accessibility:** Tree nodes are keyboard focusable (<kbd>Tab</kbd>) and executable (<kbd>Enter</kbd> / <kbd>Space</kbd>).

---

## 5. Technology Stack

| Layer | Technology | Version | Purpose & Justification |
| :--- | :--- | :---: | :--- |
| **Backend Framework** | Python / Flask | 3.13 / 3.1.0 | Lightweight, robust WSGI framework with clean blueprint modularity. |
| **WSGI / Security** | Werkzeug | 3.1.3 | Key derivation password hashing (`scrypt`/`pbkdf2`) and secure request routing. |
| **Template Engine** | Jinja2 | 3.1.5 | Server-side rendering with automatic HTML contextual escaping to prevent XSS. |
| **Relational Database**| MySQL / SQLite | 8.0+ / 3 | Dual-engine database adapter (`app/db.py`) supporting MySQL in production and zero-config SQLite locally. |
| **Database Driver** | PyMySQL | 1.1.1 | Pure-Python MySQL client for database connectivity. |
| **Configuration** | python-dotenv | 1.0.1 | Parses `.env` files for isolated environment variables. |
| **Frontend UI** | HTML5 / CSS3 / JavaScript | Modern / Vanilla | Custom design system; zero external CSS frameworks or CDN dependencies. |
| **Testing** | Python `unittest` | Built-in | Automated test suite comprising 51 tests across 8 modular test suites. |

---

## 6. Architecture & Directory Structure

CampusFind follows a **Layered Model-View-Controller (MVC) Architecture** augmented by an **In-Memory Algorithmic Subsystem**:

```
smart lost & found system/
│
├── app/
│   ├── __init__.py                 # Flask app factory, blueprint registry, CSRF middleware, Jinja filters
│   ├── config.py                   # Environment configuration classes (Dev, Testing, Prod)
│   ├── db.py                       # Unified dual-engine database adapter (MySQL & SQLite fallback)
│   ├── auth.py                     # Authentication routes (register, login, logout, session guards)
│   ├── items.py                    # Lost/Found reporting, catalog browse, item detail, user dashboard
│   ├── claims.py                   # Ownership claim submissions and verification
│   ├── admin.py                    # Administrative moderation dashboard and review actions
│   ├── matching.py                 # Multi-factor lost & found similarity matching engine
│   │
│   ├── dsa/
│   │   ├── __init__.py             # DSA package initializer
│   │   ├── bst.py                  # Pure Python Binary Search Tree implementation
│   │   ├── bst_service.py          # In-memory item indexing and logarithmic search service
│   │   └── routes.py               # BST visualizer routes and REST API endpoints
│   │
│   ├── static/
│   │   ├── css/
│   │   │   ├── main.css            # Responsive custom design system, accessibility, badges, mobile drawer
│   │   │   └── visualizer.css      # BST SVG tree canvas, animated node states, console styles
│   │   ├── js/
│   │   │   ├── main.js             # Mobile menu toggle, modal controllers, form double-submit lock
│   │   │   └── bst_visualizer.js   # Dynamic SVG layout engine, debounced resize, keyboard accessible nodes
│   │   └── uploads/                # Directory for user-uploaded item images (.gitkeep)
│   │
│   └── templates/
│       ├── base.html               # Master layout with skip-link, responsive navigation, flash alerts
│       ├── index.html              # Landing page featuring live metrics, quick search, recent reports
│       ├── auth/
│       │   ├── login.html          # User login form with demo credentials
│       │   └── register.html       # Account registration form with 8-character password hint
│       ├── items/
│       │   ├── report_lost.html    # Lost item reporting form with secret hint
│       │   ├── report_found.html   # Found item reporting form with physical custody desk
│       │   ├── browse.html         # Filterable catalog with search, category/location filters, sorting
│       │   └── detail.html         # Responsive detail view, match candidate cards, claim modal
│       ├── user/
│       │   └── dashboard.html      # User activity dashboard with rich empty states
│       ├── admin/
│       │   └── dashboard.html      # Admin dashboard with claim decisions, moderation, audit log
│       ├── matching/
│       │   └── matches.html        # Smart matching hub with side-by-side factor breakdowns
│       └── dsa/
│           └── visualizer.html     # Interactive BST visualizer and academic complexity study
│
├── docs/
│   ├── architecture.md             # Detailed high-level architectural specification & sequence flows
│   ├── database-design.md          # ER diagrams, table schemas, B+ Tree indexing, and SQL translations
│   ├── testing.md                  # Comprehensive test plan, 8 test suites, and QA methodology
│   ├── user-guide.md               # User & admin operational manual with step-by-step workflows
│   ├── security.md                 # OWASP Top 10 threat mitigation & application hardening specification
│   └── viva-preparation.md         # College demonstration script, viva Q&A, and honest project claims
│
├── tests/
│   ├── __init__.py                 # Test package initializer
│   ├── test_auth.py                # 5 tests: registration, password hashing, sessions, admin guards
│   ├── test_bst.py                 # 10 tests: BST insertion, traversals, 3-case deletion, range queries
│   ├── test_claims.py              # 5 tests: claim lifecycle, rejection flow, type checks, input bounds
│   ├── test_dsa_routes.py          # 7 tests: visualizer HTML, JSON tree structure, insert/search/delete API
│   ├── test_integration.py         # 6 tests: app startup, test DB isolation, 404 handler, foreign keys
│   ├── test_items.py               # 5 tests: report lost/found, catalog filters, upload warnings
│   ├── test_matching.py            # 7 tests: tokenization, Jaccard similarity, category/date heuristics
│   └── test_security.py            # 6 tests: password complexity, session cookies, IDOR, SQLi, XSS
│
├── schema.sql                      # Complete, reproducible MySQL database creation script
├── seed.py                         # Realistic campus sample data generator (pre-correlated pairs)
├── run.py                          # Main WSGI application entry point
├── run_tests.py                    # Standalone test runner (executes all 51 automated tests)
├── requirements.txt                # Locked Python dependencies
├── .env.example                    # Template environment variables file with placeholder values
├── .gitignore                      # Git exclusion rules for venvs, credentials, and caches
├── ARCHITECTURE.md                 # Architectural specification summary
├── DATABASE.md                     # Database specification summary
└── README.md                       # Master project documentation
```

---

## 7. Prerequisites

Before installing the application, ensure the host system provides:
- **Python:** Version 3.10, 3.11, 3.12, or 3.13 installed (verified on Python 3.13.6 64-bit).
- **Operating System:** Windows, macOS, or Linux.
- **Git:** Installed for version control operations.
- **MySQL Server (Optional):** MySQL 8.0+ or MariaDB 10.4+ (if choosing MySQL over the automatic SQLite engine).

---

## 8. Installation Instructions

Open your command terminal and clone the repository:
```bash
git clone https://github.com/avignyahjakku-dot/Smart-Lost-Found-System.git
cd "Smart-Lost-Found-System"
```

---

## 9. Virtual Environment Setup

Isolate project dependencies by creating a dedicated Python virtual environment:

### On Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### On macOS / Linux (Bash):
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 10. Dependency Installation

Install the locked dependencies from `requirements.txt`:
```bash
pip install -r requirements.txt
```

Core dependencies installed:
- `Flask==3.1.0` (Core WSGI framework)
- `Werkzeug==3.1.3` (Routing, password hashing, session primitives)
- `Jinja2==3.1.5` (Template rendering and auto-escaping)
- `PyMySQL==1.1.1` (MySQL database client driver)
- `python-dotenv==1.0.1` (Environment variable loader)

---

## 11. Database Configuration & Schema Setup

CampusFind provides an automated **Dual-Engine Architecture** in [`app/db.py`](file:///c:/Users/6tan5/OneDrive/Desktop/smart%20lost%20&%20found%20system/app/db.py):

### Option A: Out-of-the-Box SQLite (Default & Recommended for Local Evaluation)
No database installation or manual SQL execution is required. If MySQL is not configured or unreachable, the application automatically initializes `campusfind.db` with relational constraints, foreign keys, and indexes on first launch.

### Option B: MySQL Database Setup
If using a local MySQL instance (or XAMPP / WampServer):
1. Open the MySQL terminal or management client and apply `schema.sql`:
   ```bash
   mysql -u root -p < schema.sql
   ```
2. Update your `.env` file to select `DB_TYPE=mysql` and provide connection credentials.

---

## 12. Environment Variable Configuration

Create a local `.env` configuration file from the provided template:

### Windows (PowerShell):
```powershell
Copy-Item .env.example .env
```

### Linux / macOS:
```bash
cp .env.example .env
```

Configure the environment parameters inside `.env`:
```ini
# Flask Application Environment
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=replace_with_a_secure_random_hex_string_in_production

# Database Connection (sqlite or mysql)
DB_TYPE=sqlite
SQLITE_PATH=campusfind.db

# MySQL Configuration (Only required if DB_TYPE=mysql)
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=campusfind
DB_USER=root
DB_PASSWORD=your_mysql_password_here

# Security Settings
SESSION_COOKIE_SECURE=False

# Default Seed Administrator Credentials
DEFAULT_ADMIN_EMAIL=admin@campusfind.edu
DEFAULT_ADMIN_PASSWORD=Admin@CampusFind2026
```

> [!NOTE]
> `.env` contains local environment settings and is excluded from Git tracking via `.gitignore`. Never commit active production secrets to version control.

---

## 13. Application Startup Commands

### Step 1: Seed Realistic Demonstration Data (Optional but Recommended)
Populate the repository with realistic sample users, pre-correlated lost/found item pairs, and claim records:
```bash
python seed.py --reset
```

### Step 2: Launch the Web Server
Start the Flask development server:
```bash
python run.py
```

Open a web browser and visit:
```
http://127.0.0.1:5000
```

---

## 14. Test Execution Instructions

CampusFind includes 51 automated unit, integration, algorithmic, and security tests.

### Run All 51 Tests via Standalone Runner:
```bash
python run_tests.py
```

### Alternatively, Run via Python `unittest`:
```bash
python -m unittest discover tests
```

### Expected Output:
```
======================================================================
 CampusFind (Smart Lost & Found System) — Automated Test Suite
======================================================================
test_admin_route_protection (test_auth.TestAuth) ... ok
test_duplicate_email_registration_blocked (test_auth.TestAuth) ... ok
test_login_and_logout_flow (test_auth.TestAuth) ... ok
test_registration_validation_failures (test_auth.TestAuth) ... ok
test_user_registration_success (test_auth.TestAuth) ... ok
test_bst_ordering_and_traversal (test_bst.TestBinarySearchTree) ... ok
test_deletion_case_1_leaf (test_bst.TestBinarySearchTree) ... ok
test_deletion_case_2_one_child (test_bst.TestBinarySearchTree) ... ok
test_deletion_case_3_two_children (test_bst.TestBinarySearchTree) ... ok
test_duplicate_key_updates_data (test_bst.TestBinarySearchTree) ... ok
test_empty_tree_properties (test_bst.TestBinarySearchTree) ... ok
test_min_and_max (test_bst.TestBinarySearchTree) ... ok
test_range_search_pruning (test_bst.TestBinarySearchTree) ... ok
test_search_path_tracing (test_bst.TestBinarySearchTree) ... ok
test_single_node_insertion_and_search (test_bst.TestBinarySearchTree) ... ok
test_admin_item_deletion (test_claims.TestClaims) ... ok
test_claim_on_lost_item_is_rejected (test_claims.TestClaims) ... ok
test_claim_rejection_flow (test_claims.TestClaims) ... ok
test_claim_validation_missing_fields_and_oversized (test_claims.TestClaims) ... ok
test_submit_claim_lifecycle (test_claims.TestClaims) ... ok
test_api_delete_key (test_dsa_routes.TestDsaRoutes) ... ok
test_api_insert_and_validation (test_dsa_routes.TestDsaRoutes) ... ok
test_api_reset (test_dsa_routes.TestDsaRoutes) ... ok
test_api_search_path_tracing (test_dsa_routes.TestDsaRoutes) ... ok
test_api_traversals (test_dsa_routes.TestDsaRoutes) ... ok
test_api_tree_structure (test_dsa_routes.TestDsaRoutes) ... ok
test_visualizer_page_renders (test_dsa_routes.TestDsaRoutes) ... ok
test_application_startup_in_test_configuration (test_integration.TestIntegration) ... ok
test_catalog_browsing_page (test_integration.TestIntegration) ... ok
test_custom_404_error_page (test_integration.TestIntegration) ... ok
test_database_persistence_and_foreign_keys (test_integration.TestIntegration) ... ok
test_homepage_rendering_and_metrics (test_integration.TestIntegration) ... ok
test_matching_hub_page (test_integration.TestIntegration) ... ok
test_browse_catalog_and_filtering (test_items.TestItems) ... ok
test_report_found_item (test_items.TestItems) ... ok
test_report_item_validation_failures (test_items.TestItems) ... ok
test_report_lost_item (test_items.TestItems) ... ok
test_unsupported_image_upload_warning (test_items.TestItems) ... ok
test_category_mismatch_penalty (test_matching.TestSmartMatching) ... ok
test_chronological_sequence_penalty (test_matching.TestSmartMatching) ... ok
test_clean_tokens (test_matching.TestSmartMatching) ... ok
test_high_probability_match (test_matching.TestSmartMatching) ... ok
test_jaccard_similarity (test_matching.TestSmartMatching) ... ok
test_missing_and_malformed_fields_handled_safely (test_matching.TestSmartMatching) ... ok
test_ranking_candidates (test_matching.TestSmartMatching) ... ok
test_idor_status_modification_prevention (test_security.TestSecurity) ... ok
test_password_hashing_and_complexity (test_security.TestSecurity) ... ok
test_role_based_admin_protection (test_security.TestSecurity) ... ok
test_session_cookie_security_configurations (test_security.TestSecurity) ... ok
test_sql_injection_resilience (test_security.TestSecurity) ... ok
test_xss_auto_escaping (test_security.TestSecurity) ... ok
----------------------------------------------------------------------
Ran 51 tests in 16.105s

OK
======================================================================
 Tests Run: 51
 Errors:    0
 Failures:  0
======================================================================
[SUCCESS] ALL TESTS PASSED SUCCESSFULLY!
```

---

## 15. User and Administrator Workflows

### 15.1 Student & Staff Workflow
1. **Registration / Login:** Register with campus credentials or log in with demo account (`alex@campusfind.edu` / `Student@123`).
2. **Report Lost Belonging:** Provide title, category, campus zone, date, and a private secret hint question (e.g. *"What sticker is on the back?"*).
3. **Review Matches:** The matching engine compares reports against open found items, ranking candidates by percentage confidence score.
4. **Submit Claim:** If a candidate found item corresponds to the missing object, the student submits a claim with proof details, phone number, and the secret answer.
5. **Collection:** Once approved by administration, the student collects the property from the designated physical storage custody desk.

### 15.2 Administrator Workflow
1. **Access Control Center:** Log in with administrative credentials (`admin@campusfind.edu` / `Admin@CampusFind2026`) and click **🛡️ Admin Panel**.
2. **Review Pending Claims:** Examine claimant evidence and secret hint answers side by side.
3. **Adjudicate Claims:** Enter administrative review notes and click **Approve** (transitions item to `claimed`) or **Reject** (leaves item `open`).
4. **Moderate Content:** Delete duplicate or inappropriate submissions with cascading cleanup.
5. **Inspect Audit Log:** Monitor timestamped records of all administrative actions.

---

## 16. Matching Algorithm Explanation

Candidate pairings between lost reports ($L$) and found reports ($F$) are computed via a multi-factor scoring function:
$$\text{Score}(L, F) = S_{\text{cat}} + S_{\text{text}} + S_{\text{loc}} + S_{\text{date}} \in [0, 100]$$

1. **Category Compatibility ($S_{\text{cat}}$, Weight: 30 pts):** Strict category matching. Equal categories award 30 points; divergent categories yield 0 points.
2. **Textual Jaccard & Keyword Overlap ($S_{\text{text}}$, Weight: 35 pts):** Tokenizes titles and descriptions, strips punctuation and stop words, and evaluates the Jaccard similarity coefficient:
   $$J(T_L, T_F) = \frac{|T_L \cap T_F|}{|T_L \cup T_F|}$$
   augmented by direct title token intersections.
3. **Location Proximity ($S_{\text{loc}}$, Weight: 20 pts):** Evaluates campus zones (Central Library, Hostels, Cafeteria, Sports Complex). Exact matches award 20 points, shared landmark tokens award 15 points, and distinct zones award 3 points.
4. **Chronological Plausibility ($S_{\text{date}}$, Weight: 15 pts):** Evaluates temporal plausibility: found on or after lost date awards full points (15 pts same day, decaying to 8 pts after 30 days). Items found well before reported loss receive 0 points (physically implausible).

**Confidence Classification:**
- $\ge 75\%$: **High Match** (Strong candidate; attributes and timeline align).
- $50\% - 74\%$: **Moderate Match** (Plausible candidate; several key attributes match).
- $30\% - 49\%$: **Plausible Match** (Weak correlation; requires manual mark verification).

---

## 17. Binary Search Tree (BST) & Role in CampusFind

### 17.1 In-Memory BST Architecture
CampusFind incorporates a pure Python object-oriented Binary Search Tree (`app/dsa/bst.py`):
- **Logarithmic Lookups:** Provides in-memory $O(\log n)$ average search times without database disk I/O latency.
- **In-Order Traversal:** Delivers items sorted in ascending order in $O(n)$ linear time without requiring an external sorting algorithm.
- **Subtree Range Pruning:** Quickly retrieves records within a date or ID interval ($\text{min\_key} \le k \le \text{max\_key}$) by skipping disjoint subtrees.
- **Three-Case Deletion:**
  - *Case 1 (Leaf):* Replaces parent pointer with `None`.
  - *Case 2 (One Child):* Splices parent pointer directly to the single child.
  - *Case 3 (Two Children):* Finds the in-order successor (minimum node in right subtree), replaces the target payload, and recursively deletes the successor.

### 17.2 Comparison: In-Memory BST vs. MySQL B+ Tree Database Indexes

| Dimension | In-Memory BST (`app/dsa/bst.py`) | MySQL B+ Tree Index (InnoDB) |
| :--- | :--- | :--- |
| **Storage Medium** | Random Access Memory (RAM) | Secondary Disk Storage (SSD / HDD) |
| **Branching Factor ($M$)** | Binary ($M = 2$, at most 2 children) | High Fan-Out ($M \ge 100$, hundreds of keys per 16 KB page) |
| **Lookup Latency** | Nanoseconds (Pointer dereferencing) | Milliseconds (Cached buffer pool or disk block reads) |
| **Tree Depth** | Moderate ($\approx \log_2 n$) | Shallow ($3 - 4$ levels for millions of records) |
| **Range Queries** | Recursive in-order subtree pruning | Bidirectional linked leaf node traversal |
| **Persistence** | Volatile (Synchronized from DB at startup) | Durable (ACID write-ahead logging in redo logs) |

---

## 18. Known Limitations

1. **Text-Only Heuristic Matching:** The current matching algorithm correlates text descriptions, categories, locations, and dates. It does not extract computer vision feature embeddings from uploaded images.
2. **Unbalanced BST Mechanics:** While the custom BST implementation handles all 3 deletion cases and range searches, it does not perform self-balancing tree rotations (e.g. AVL or Red-Black balancing).
3. **Simulated Email Notifications:** System notifications (such as claim approvals and match alerts) are rendered via flash messages and audit logs rather than external SMTP email dispatches.

---

## 19. Future Improvements

1. **Deep Learning Vision Matching:** Integrate a lightweight Convolutional Neural Network (e.g. MobileNet or OpenAI CLIP) to generate image embeddings and calculate cosine similarity between photos of lost and found objects.
2. **Self-Balancing Tree Engine (AVL / Red-Black):** Implement tree rotation algorithms ensuring strict $O(\log n)$ height boundaries even under sorted sequential key insertion.
3. **Automated SMTP / SMS Notifications:** Dispatch automated alerts to students whenever a High-confidence match ($\ge 75\%$) is detected for their missing item.
4. **Geospatial Campus Map:** Embed an interactive campus map (e.g. Leaflet.js / OpenStreetMap) allowing users to pin exact GPS locations of incidents.

---

## 20. Repository Information

- **Project Name:** Smart Lost & Found System (CampusFind)
- **Degree:** Two-Person BTech Computer Science & Engineering Capstone Project
- **Target Repository:** [https://github.com/avignyahjakku-dot/Smart-Lost-Found-System.git](https://github.com/avignyahjakku-dot/Smart-Lost-Found-System.git)
- **Active Branch:** `main`

---

## Additional Documentation Files

For in-depth technical documentation, refer to the following specialized guides in the [`docs/`](file:///c:/Users/6tan5/OneDrive/Desktop/smart%20lost%20&%20found%20system/docs/) directory:
- [**System Architecture & Request Lifecycle**](file:///c:/Users/6tan5/OneDrive/Desktop/smart%20lost%20&%20found%20system/docs/architecture.md)
- [**Database Design & Schema Analysis**](file:///c:/Users/6tan5/OneDrive/Desktop/smart%20lost%20&%20found%20system/docs/database-design.md)
- [**Automated Testing Specification & Plan**](file:///c:/Users/6tan5/OneDrive/Desktop/smart%20lost%20&%20found%20system/docs/testing.md)
- [**User & Administrator Operational Manual**](file:///c:/Users/6tan5/OneDrive/Desktop/smart%20lost%20&%20found%20system/docs/user-guide.md)
- [**Security & OWASP Hardening Specification**](file:///c:/Users/6tan5/OneDrive/Desktop/smart%20lost%20&%20found%20system/docs/security.md)
- [**College Demonstration & Viva Voce Guide**](file:///c:/Users/6tan5/OneDrive/Desktop/smart%20lost%20&%20found%20system/docs/viva-preparation.md)
