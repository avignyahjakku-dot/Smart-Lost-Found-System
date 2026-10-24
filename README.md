# CampusFind — Smart Lost & Found System

> **Degree Program:** Bachelor of Technology (BTech) in Computer Science & Engineering (CSE)  
> **Project Type:** Individual Capstone Project  
> **Domain:** Full-Stack Web Development, Relational Database Engineering, Data Structures & Algorithms (DSA)  
> **Primary Technology Stack:** Python 3.13, Flask 3.1, MySQL / SQLite, HTML5, CSS3, Modern JavaScript  

---

## 1. Project Overview & Problem Statement

Misplacing personal belongings (student ID cards, scientific calculators, laptops, room keys, headphones, water bottles) is an everyday occurrence on university campuses. Traditional campus lost-and-found practices rely on manual WhatsApp group forwards, fragmented physical notice boards, or scattered security desks. These informal methods suffer from several critical shortcomings:
- **No Centralized Repository:** Students cannot determine whether an item turned in at the cafeteria is held at the main gate, library, or department office.
- **Vulnerability to False Claims:** Open public messages reveal all item details, enabling fraudulent collections without ownership verification.
- **Zero Intelligent Correlation:** Sifting through hundreds of reports manually to match a missing item with a found item is slow and error-prone.

**CampusFind** solves this problem by providing a centralized, secure web application powered by:
1. A **Multi-Factor Heuristic Matching Engine** that mathematically correlates lost and found reports based on category compatibility, tokenized keyword overlap, campus landmark proximity, and chronological plausibility.
2. An in-memory **Binary Search Tree (BST)** data structure implementation with logarithmic $\mathcal{O}(\log n)$ indexing and an interactive SVG visualizer demonstrating core tree operations.
3. A **Role-Based Security & Claim Verification Workflow** with secret ownership questions and administrative moderation before items are released.

---

## 2. Objectives and Key Features

### User Capabilities
- **Account Management:** Student/Staff registration, secure login, password hashing (`Werkzeug`), and session management.
- **Report Lost Items:** Specify item details, category, campus location, date/time, upload an optional photo, and establish a secret ownership hint question.
- **Report Found Items:** Record discovered items, category, date, and physical custody/storage location (e.g. Central Library Front Desk).
- **Multi-Criteria Search & Filtering:** Filter repository records dynamically by item type (`lost`/`found`), category, campus location, keyword, and date sorting.
- **Item Details & Algorithmic Insights:** Inspect item attributes, view automated match predictions with percentage scores, and review the logarithmic BST lookup path.
- **Ownership Claim Submission:** Submit verified ownership claims with proof descriptions, serial numbers, and answers to secret verification questions.
- **User Activity Dashboard:** Track personal lost reports, found reports, and real-time claim evaluation statuses (`Pending`, `Approved`, `Rejected`).

### Administrative Capabilities
- **Role-Based Admin Protection:** Protected `@admin_required` decorators preventing unauthorized access.
- **Administrative Control Center:** Real-time metrics tracking total items, open lost items, open found items, pending claims, and resolved cases.
- **Claim Moderation:** Inspect submitted claimant evidence, review secret answers, approve or reject claims with administrative notes, and update item statuses.
- **Report Moderation:** Edit item statuses or permanently remove spam/duplicate reports.
- **System Audit Log:** Immutable activity log tracking all administrative interventions and claim submissions.

### Data Structures & Algorithms (DSA) Integration
- **Real Python Binary Search Tree:** Authentic, non-trivial BST class supporting:
  - Logarithmic insertion (`insert(key, data)`),
  - Search with branch path logging (`search(key)`),
  - Deletion handling all three classic cases (leaf, 1 child, 2 children with in-order successor),
  - In-order, pre-order, and post-order traversals,
  - Range queries (`range_search(min_key, max_key)`).
- **Interactive SVG Visualizer:** Web interface rendering the exact Python BST structure with step-by-step traversal highlighting, comparison counters, and an academic study comparing in-memory BSTs with on-disk B+ Tree database indexes.

---

## 3. Technology Stack

| Layer | Technologies Used | Justification |
| :--- | :--- | :--- |
| **Frontend** | HTML5, CSS3 (Custom Design System), Modern Vanilla JavaScript | Lightweight, zero external CDN dependencies, fully responsive across desktop, tablet, and mobile. |
| **Backend** | Python 3.13, Flask 3.1, Jinja2, Werkzeug | Robust WSGI framework, clean blueprint modularity, and native object-oriented data structures. |
| **Database** | MySQL 8.0+ / SQLite 3 (Dual-Engine Adapter) | Complete relational schema with foreign key constraints, indexes, and automatic fallback for immediate local testing. |
| **DSA** | Custom Python Binary Search Tree (BST) | Logarithmic in-memory indexing, sorted ordered traversals, and dynamic tree visualization. |
| **Security** | Werkzeug Password Hashing (`scrypt`/`pbkdf2`), Parametric SQL | Prevents credential leaks and SQL injection attacks. |
| **Testing** | Python `unittest` | Automated test suite covering BST operations, auth, filtering, matching, and claims. |

---

## 4. Project Folder Structure

```
smart lost & found system/
│
├── app/
│   ├── __init__.py                 # Flask app factory, blueprint registration, Jinja filters
│   ├── config.py                   # Environment configuration classes
│   ├── db.py                       # Unified database manager (MySQL & SQLite auto-fallback)
│   ├── auth.py                     # Authentication routes (register, login, logout, session)
│   ├── items.py                    # Lost/Found reporting, catalog browse, item detail, user dashboard
│   ├── claims.py                   # Ownership claim submissions and verification
│   ├── admin.py                    # Administrative moderation dashboard and review actions
│   ├── matching.py                 # Multi-factor lost & found similarity matching engine
│   ├── dsa/
│   │   ├── __init__.py             # DSA package initializer
│   │   ├── bst.py                  # Real Binary Search Tree implementation in Python
│   │   ├── bst_service.py          # In-memory item indexing and logarithmic search service
│   │   └── routes.py               # BST visualizer routes and REST API endpoints
│   ├── static/
│   │   ├── css/
│   │   │   ├── main.css            # Responsive layout & modern design system
│   │   │   └── visualizer.css      # BST tree canvas, animations, and console styles
│   │   ├── js/
│   │   │   ├── main.js             # Flash dismiss, modal controllers, client actions
│   │   │   └── bst_visualizer.js   # SVG tree layout engine, path animator, and traversal player
│   │   └── uploads/                # Directory for uploaded item images (.gitkeep)
│   └── templates/
│       ├── base.html               # Master layout with responsive navbar and footer
│       ├── index.html              # Landing page featuring live stats, quick search, recent items
│       ├── auth/
│       │   ├── login.html          # User login form with demo credential hints
│       │   └── register.html       # Student/staff registration form
│       ├── items/
│       │   ├── report_lost.html    # Lost item reporting form with secret verification hint
│       │   ├── report_found.html   # Found item reporting form with custody storage desk
│       │   ├── browse.html         # Filterable catalog with search and sorting
│       │   └── detail.html         # Item details, match candidate cards, claim modal
│       ├── user/
│       │   └── dashboard.html      # User's reports and claims status tracker
│       ├── admin/
│       │   └── dashboard.html      # Admin dashboard with claim decisions and audit log
│       ├── matching/
│       │   └── matches.html        # Smart matching hub with side-by-side factor breakdown
│       └── dsa/
│           └── visualizer.html     # Interactive BST visualizer and DSA comparison paper
│
├── tests/
│   ├── __init__.py                 # Test suite initializer
│   ├── test_bst.py                 # 10 unit tests for BST operations, traversals, and edge cases
│   ├── test_auth.py                # 4 unit tests for registration, hashing, login, admin protection
│   ├── test_items.py               # 3 integration tests for item creation and catalog filtering
│   ├── test_matching.py            # 6 unit tests for similarity factors and ranking heuristics
│   └── test_claims.py              # 1 integration test for claim submission and admin approval
│
├── schema.sql                      # Complete, reproducible MySQL database creation script
├── seed.py                         # Realistic campus sample data generator (users, items, claims)
├── run.py                          # Main application entry point
├── run_tests.py                    # Standalone test runner (runs all 24 unit/integration tests)
├── requirements.txt                # Locked Python dependencies
├── .env.example                    # Template environment variables file
├── .gitignore                      # Git exclusion rules for venvs, credentials, and caches
├── ARCHITECTURE.md                 # System architecture, matching formulas, and security design
├── DATABASE.md                     # Database ER design, relationships, and indexing analysis
└── README.md                       # Comprehensive project documentation
```

---

## 5. Prerequisites

Before running the application, ensure you have:
- **Python:** Version 3.10, 3.11, 3.12, or 3.13 installed (verified on Python 3.13.6 64-bit).
- **Git:** (Optional, for repository versioning).
- **MySQL / MariaDB:** (Optional for production; if MySQL is not running, the application automatically uses SQLite without any manual setup).

---

## 6. Installation & Setup Instructions

### Step 1: Clone or Open the Workspace
Open a terminal in the project directory:
```bash
cd "smart lost & found system"
```

### Step 2: (Recommended) Create and Activate a Virtual Environment
```powershell
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```
*Note:* The core dependencies are `Flask`, `Werkzeug`, `PyMySQL`, and `python-dotenv`.

---

## 7. Database Configuration

CampusFind features a **Unified Dual-Engine Database Architecture** in [`app/db.py`](file:///c:/Users/6tan5/OneDrive/Desktop/smart%20lost%20&%20found%20system/app/db.py):

### Option A: Out-of-the-Box Local Running (SQLite — Default)
No database server installation is required. The system automatically initializes `campusfind.db` with relational constraints, tables, and foreign keys on first launch.

### Option B: MySQL Database Setup
If you have MySQL Server (or XAMPP / WampServer) running locally:
1. Open MySQL Command Line or phpMyAdmin and execute `schema.sql`:
   ```bash
   mysql -u root -p < schema.sql
   ```
2. Configure `.env`:
   ```ini
   DB_TYPE=mysql
   DB_HOST=127.0.0.1
   DB_PORT=3306
   DB_NAME=campusfind
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   ```

---

## 8. Environment Variables Configuration

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Key configuration parameters:
- `SECRET_KEY`: Random secret string used for session cookie encryption.
- `DB_TYPE`: Set to `sqlite` for local file database or `mysql` for MySQL server.
- `DEFAULT_ADMIN_EMAIL`: Initial admin login (`admin@campusfind.edu`).
- `DEFAULT_ADMIN_PASSWORD`: Initial admin password (`Admin@CampusFind2026`).

---

## 9. Seeding Realistic Sample Data

To populate the repository with realistic university lost and found records (including pre-correlated high-match pairs, diverse categories, and sample claims):
```bash
python seed.py --reset
```

Pre-seeded demonstration accounts:
- **Administrator:** `admin@campusfind.edu` / `Admin@CampusFind2026`
- **Student 1:** `alex@campusfind.edu` / `Student@123`
- **Student 2:** `priya@campusfind.edu` / `Student@123`
- **Staff / Faculty:** `vance@campusfind.edu` / `Student@123`
- **Security Officer:** `security@campusfind.edu` / `Student@123`

---

## 10. Running the Application

Launch the local development server:
```bash
python run.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 11. Automated Testing

The project includes 24 automated unit and integration tests covering data structures, matching heuristics, security, and administrative workflows.

Run all tests via the standalone runner:
```bash
python run_tests.py
```
Expected output:
```
======================================================================
 CampusFind (Smart Lost & Found System) — Automated Test Suite
======================================================================
test_admin_route_protection (test_auth.TestAuth) ... ok
test_duplicate_email_registration_blocked (test_auth.TestAuth) ... ok
test_login_and_logout_flow (test_auth.TestAuth) ... ok
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
test_submit_claim_lifecycle (test_claims.TestClaims) ... ok
test_browse_catalog_and_filtering (test_items.TestItems) ... ok
test_report_found_item (test_items.TestItems) ... ok
test_report_lost_item (test_items.TestItems) ... ok
test_category_mismatch_penalty (test_matching.TestSmartMatching) ... ok
test_chronological_sequence_penalty (test_matching.TestSmartMatching) ... ok
test_clean_tokens (test_matching.TestSmartMatching) ... ok
test_high_probability_match (test_matching.TestSmartMatching) ... ok
test_jaccard_similarity (test_matching.TestSmartMatching) ... ok
test_ranking_candidates (test_matching.TestSmartMatching) ... ok
----------------------------------------------------------------------
Ran 24 tests in 6.78s

OK
[SUCCESS] ALL TESTS PASSED SUCCESSFULLY!
```

---

## 12. Main Routes & Endpoints

| URL Path | HTTP Methods | Description | Access Level |
| :--- | :--- | :--- | :--- |
| `/` | `GET` | Landing page featuring metrics, quick search, and recent reports | Public |
| `/browse` | `GET` | Catalog with multi-parameter filtering, search, and sorting | Public |
| `/items/<id>` | `GET` | Item details, match candidate cards, and claim trigger | Public |
| `/items/<id>/status` | `POST` | Update item status (`open`, `claimed`, `returned`, `resolved`) | Reporter / Admin |
| `/report/lost` | `GET`, `POST` | Submit a new lost item report with secret hint | Authenticated User |
| `/report/found` | `GET`, `POST` | Submit a new found item report with storage location | Authenticated User |
| `/matches` | `GET` | Smart Matching Hub comparing all active campus reports | Public |
| `/claims/submit/<id>` | `POST` | Submit ownership claim with proof details | Authenticated User |
| `/my-dashboard` | `GET` | User dashboard: personal reports and claim statuses | Authenticated User |
| `/admin/dashboard` | `GET` | Administrator dashboard: moderation, metrics, and audit log | Admin Only |
| `/admin/claim/<id>/review`| `POST` | Approve or reject an ownership claim with notes | Admin Only |
| `/admin/item/<id>/delete`| `POST` | Permanently remove inappropriate or duplicate reports | Admin Only |
| `/dsa/visualizer` | `GET` | Interactive SVG BST visualizer & academic study page | Public |
| `/dsa/api/tree` | `GET` | REST API returning hierarchical JSON of the BST | Public |
| `/dsa/api/search` | `POST` | REST API executing logarithmic BST search with path trace | Public |
| `/dsa/api/insert` | `POST` | REST API inserting key into interactive BST | Public |
| `/dsa/api/delete` | `POST` | REST API deleting key across all 3 BST deletion cases | Public |
| `/dsa/api/traverse` | `GET` | REST API returning in-order, pre-order, or post-order list | Public |

---

## 13. Algorithmic Architecture

### A. Multi-Factor Smart Matching System
Candidate pairings between lost reports ($L$) and found reports ($F$) are computed via a weighted multi-factor scoring function:
$$\text{Score}(L, F) = S_{\text{cat}} + S_{\text{text}} + S_{\text{loc}} + S_{\text{date}}$$

1. **Category Compatibility ($S_{\text{cat}}$, Weight: 30 pts):**
   - Exact category match earns 30 points.
   - Category divergence earns 0 points.
2. **Textual Jaccard & Keyword Overlap ($S_{\text{text}}$, Weight: 35 pts):**
   - Titles and descriptions are tokenized, normalized, and stripped of non-informative stop words.
   - Computes Jaccard index: $J(T_L, T_F) = \frac{|T_L \cap T_F|}{|T_L \cup T_F|}$, augmented by direct title token overlaps.
3. **Location Proximity ($S_{\text{loc}}$, Weight: 20 pts):**
   - Exact campus building/zone match earns 20 points.
   - Shared campus landmarks (e.g. `Library`, `Cafeteria`, `Hostel Block A`) earn 15 points.
   - Distinct campus zones earn 3 points.
4. **Chronological Plausibility ($S_{\text{date}}$, Weight: 15 pts):**
   - $\Delta_{\text{days}} = \text{Date}_{\text{found}} - \text{Date}_{\text{lost}}$.
   - If $\Delta_{\text{days}} \ge 0$: found after loss (15 pts if same day, decaying to 8 pts after 30 days).
   - If $\Delta_{\text{days}} < -1$: found well before reported loss (0 pts — physically implausible).

**Confidence Classification:**
- $\ge 75\%$: **High Match** (Strong candidate; attributes and timeline align).
- $50\% - 74\%$: **Moderate Match** (Plausible candidate; several key attributes match).
- $30\% - 49\%$: **Plausible Match** (Weak correlation; requires manual mark verification).

### B. Binary Search Tree (BST) Design & Analysis
Our real Python BST maintains in-memory indexing of active campus items keyed by `item_id` and epoch timestamps:
- **Insertion & Search:** Average $\mathcal{O}(\log n)$, worst-case $\mathcal{O}(n)$ if skewed.
- **Three-Case Deletion:**
  - Case 1 (Leaf): Set parent's pointer to `None`.
  - Case 2 (One Child): Splice out target by linking parent directly to child.
  - Case 3 (Two Children): Find in-order successor (minimum node in right subtree), copy its key and data, and recursively delete the successor.
- **Why BST vs. Database Indexes (B+ Tree)?**
  - *In-Memory BST:* Extremely fast pointer dereferences in RAM ($\approx$ nanoseconds), zero disk I/O, lightweight memory overhead per node, natural ascending in-order traversal.
  - *MySQL B+ Tree:* High fan-out ($M \ge 100$) minimizes block disk reads to $3-4$ I/O operations for millions of rows. Leaf nodes are linked in a bidirectional list for sequential range scans.

---

## 14. Known Limitations & Future Enhancements

1. **Computer Vision & Image Feature Extraction:** Currently, matching uses textual description, location, category, and date. Future versions could integrate a lightweight CNN (e.g. MobileNet or CLIP) to match photo embeddings of objects.
2. **Automated Self-Balancing (AVL / Red-Black Trees):** While the BST visualizer demonstrates standard BST mechanics, integrating self-balancing rotations would guarantee strict $\mathcal{O}(\log n)$ worst-case bounds.
3. **Push & Email Notifications:** Automated email notifications (via SMTP) when a High-confidence candidate match ($\ge 75\%$) is detected for a student's lost item.
4. **Campus Map Integration:** Visual interactive campus map (e.g. Leaflet.js / OpenStreetMap) pinning exact GPS lost and found zones.

---

## 15. Academic Integrity Statement

This project, **Smart Lost & Found System (CampusFind)**, was conceptualized, designed, implemented, and tested as an individual BTech Computer Science & Engineering capstone project. All architectural designs, database schemas, algorithms, and documentation represent authentic individual work adhering to academic standards.
