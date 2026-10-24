# CampusFind — Architectural Specification

> **Project:** Smart Lost & Found System (CampusFind)  
> **Course:** Bachelor of Technology (BTech) in Computer Science & Engineering (CSE)  
> **Author:** Two-Person BTech CSE Capstone Project Team  
> **Framework:** Python Flask (Layered MVC + Algorithmic Subsystem)  

---

## 1. High-Level Architectural Model

CampusFind implements a **Layered Model-View-Controller (MVC) Architecture** augmented by an **In-Memory Algorithmic Subsystem**. The architecture separates concerns between presentation, business rules, algorithmic analysis, and persistence:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        Client Presentation Tier                        │
│  - Semantic HTML5 & Modern CSS3 Custom Design System (Responsive)      │
│  - Interactive SVG Tree Canvas & Algorithmic Trace Console             │
│  - Vanilla JavaScript DOM Controllers, Modal Triggers, & Input Checks  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP / HTTPS (RESTful Requests)
┌───────────────────────────────────▼────────────────────────────────────┐
│                    Application Tier (Flask 3.1 WSGI)                   │
│                                                                        │
│  ┌───────────────────────┐  ┌───────────────────────┐                  │
│  │  Authentication BP    │  │  Item Management BP   │                  │
│  │  - User Registration  │  │  - Catalog Browsing   │                  │
│  │  - Session Control    │  │  - Lost/Found Reports │                  │
│  │  - Password Hashing   │  │  - Item Details View  │                  │
│  └──────────┬────────────┘  └───────────┬───────────┘                  │
│             │                           │                              │
│  ┌──────────▼────────────┐  ┌───────────▼───────────┐                  │
│  │  Claims Management BP │  │  Administration BP    │                  │
│  │  - Claim Submission   │  │  - Claim Review / Notes│                 │
│  │  - Secret Hint Verify │  │  - Item Moderation    │                  │
│  │  - Status Tracking    │  │  - Immutable Audit Log│                  │
│  └──────────┬────────────┘  └───────────┬───────────┘                  │
│             │                           │                              │
│             └─────────────┬─────────────┘                              │
│                           ▼                                            │
│  ┌──────────────────────────────────────────────────┐                  │
│  │       Multi-Factor Heuristic Matching Engine     │                  │
│  │  - Category Compatibility Filter (30 pts)        │                  │
│  │  - Tokenized Jaccard Lexical Similarity (35 pts) │                  │
│  │  - Spatial Landmark Proximity Scoring (20 pts)   │                  │
│  │  - Chronological Validity & Decay (15 pts)       │                  │
│  └──────────────────────────────────────────────────┘                  │
└───────────────────────────┬────────────────────────────────────────────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
┌─────────────▼───────────────┐ ┌─────────▼──────────────────────────────┐
│     In-Memory Algorithmic   │ │         Relational Data Tier           │
│           Subsystem         │ │        (Unified DB Adapter)            │
│  - Pure Python BST Class    │ │  - Primary: MySQL 8.0+ (InnoDB)        │
│  - O(log n) Key Lookups     │ │  - Fallback / Test: SQLite 3           │
│  - 3-Case Deletion Logic    │ │  - Parameterized Query Abstraction     │
│  - Sorted In-Order Stream   │ │  - Foreign Key Cascades & Transactions │
│  - Dynamic SVG REST API     │ │  - Relational Schema (ACID Compliance) │
└─────────────────────────────┘ └────────────────────────────────────────┘
```

---

## 2. Component Breakdown & Responsibilities

### 2.1 Application Factory (`app/__init__.py`)
- Initializes the Flask application context using the factory pattern (`create_app(config_name)`).
- Loads configurations (`DevelopmentConfig`, `TestingConfig`, `ProductionConfig`).
- Registers all functional blueprints:
  - `auth_bp` (`/login`, `/register`, `/logout`)
  - `items_bp` (`/`, `/browse`, `/report/lost`, `/report/found`, `/items/<id>`, `/matches`, `/my-dashboard`)
  - `claims_bp` (`/claims/submit/<id>`)
  - `admin_bp` (`/admin/dashboard`, `/admin/claim/<id>/review`, `/admin/item/<id>/delete`)
  - `dsa_bp` (`/dsa/visualizer`, `/dsa/api/*`)
- Injects global CSRF token generation and verification middleware (`@app.before_request`).
- Registers custom Jinja template filters (`format_date`, `badge_status`).
- Configures custom error handlers (HTTP 404, HTTP 500) that render user-friendly, branded error pages without exposing stack traces.

### 2.2 Unified Database Adapter (`app/db.py`)
- Provides an engine-agnostic database access interface:
  - `query_db(query, args=(), one=False)`: Executes SQL `SELECT` queries returning dictionaries or lists of dictionaries.
  - `execute_db(query, args=(), return_id=False)`: Executes SQL `INSERT`, `UPDATE`, `DELETE` queries with automatic transaction commits and optional auto-generated primary key retrieval.
- **Dual-Engine Auto-Fallback:**
  - Attempts connection to MySQL using `pymysql.cursors.DictCursor`.
  - If MySQL is unreachable, unconfigured, or configured with `DB_TYPE=sqlite`, it seamlessly initializes and connects to local SQLite file `campusfind.db`.
- **Parameter Translation:** Automatically transforms `%s` parameter placeholders to `?` when operating in SQLite mode, allowing developers to write consistent, parameterized SQL queries safe from SQL injection.
- **Connection Teardown:** Leverages Flask's `teardown_appcontext` hook to close database connections cleanly when each HTTP request context terminates.

### 2.3 Authentication & Authorization Subsystem (`app/auth.py`)
- Implements secure session management using signed HTTP cookies.
- Hashes passwords using Werkzeug's key derivation functions (`scrypt` or `pbkdf2:sha256`) with unique per-user salts.
- Enforces role-based route decorators:
  - `@login_required`: Prevents unauthenticated users from reporting items, filing claims, or viewing personal dashboards.
  - `@admin_required`: Restricts administrative moderation endpoints to users possessing the `admin` role in their session.

### 2.4 Multi-Factor Smart Matching Engine (`app/matching.py`)
Correlates active lost item reports against open found item reports through a weighted mathematical scoring algorithm:
$$\text{Total Score}(L, F) = S_{\text{cat}} + S_{\text{text}} + S_{\text{loc}} + S_{\text{date}} \in [0, 100]$$

| Factor | Maximum Weight | Calculation Rationale |
| :--- | :---: | :--- |
| **Category Match ($S_{\text{cat}}$)** | 30 pts | Exact category alignment earns 30 points; divergent categories yield 0 points. |
| **Lexical Overlap ($S_{\text{text}}$)** | 35 pts | Tokenizes and normalizes titles and descriptions, removes English stop words, and evaluates the Jaccard similarity coefficient $J(T_L, T_F) = \frac{\|T_L \cap T_F\|}{\|T_L \cup T_F\|}$ with bonus points for direct title token intersections. |
| **Location Proximity ($S_{\text{loc}}$)** | 20 pts | Matches reported campus zones (e.g. Central Library, Hostels, Cafeteria, Sports Complex). Exact matches earn 20 points, shared landmark tokens earn 15 points, and distinct zones receive 3 points. |
| **Chronological Validity ($S_{\text{date}}$)** | 15 pts | Evaluates temporal plausibility: an item discovered on or after the reported lost date receives full points (15 pts on the same day, decaying to 8 pts after 30 days). Items found well before the reported lost date receive 0 points (physically implausible). |

Candidates are ranked in descending order of similarity and categorized into confidence tiers:
- **High Confidence ($\ge 75\%$):** Primary candidate for recovery.
- **Moderate Confidence ($50\% - 74\%$):** Plausible match requiring verification.
- **Plausible Confidence ($30\% - 49\%$):** Weak match; candidate kept open for manual review.

### 2.5 In-Memory Binary Search Tree (BST) Subsystem (`app/dsa/`)
- Pure Python object-oriented implementation (`app/dsa/bst.py`):
  - `Node` class storing `key`, `data`, `left`, `right`.
  - `BinarySearchTree` class supporting $O(\log n)$ average insertion, search, and deletion.
  - Three-case node deletion (leaf, single child splice, two children with in-order successor replacement).
  - In-order traversal yielding strictly ascending keys in $O(n)$ linear time.
  - Subtree range query pruning (`range_search(min_key, max_key)`).
- **Service Layer (`app/dsa/bst_service.py`):**
  - Maintains an in-memory index of active repository items.
  - Synchronizes item insertions, status changes, and deletions with relational database operations.
- **Visualizer REST API (`app/dsa/routes.py`):**
  - Exposes endpoints (`/dsa/api/tree`, `/dsa/api/search`, `/dsa/api/insert`, `/dsa/api/delete`, `/dsa/api/traverse`, `/dsa/api/reset`) returning structured JSON for client-side SVG rendering.

---

## 3. Client-Side Presentation Architecture

### 3.1 Custom CSS Design System (`app/static/css/main.css`)
- Zero external CSS frameworks or CDN dependencies (ensures fast offline loading and zero third-party tracking).
- Built on modern CSS Custom Properties (`--primary`, `--secondary`, `--success`, `--danger`, `--warning`, `--dark`, `--border`).
- Fully responsive across desktop ($\ge 1024$px), tablet ($768$px - $991$px), and mobile ($\le 767$px) viewports.
- WCAG 2.1 AA compliant keyboard focus visible outlines (`:focus-visible`), high-contrast status badges, and off-screen skip links (`.skip-link`).

### 3.2 Dynamic SVG Tree Canvas (`app/static/js/bst_visualizer.js`)
- Renders hierarchical tree graphics directly in an SVG viewport.
- Computes non-overlapping node coordinates dynamically:
  - In-order node traversal index determines horizontal $X$ positioning.
  - Tree node depth determines vertical $Y$ positioning.
- Interactive animation controller executes step-by-step visual search path tracing with color-coded node states (`state-visited`, `state-found`, `state-delete`).
- Full keyboard navigation: tree nodes are keyboard focusable (`tabindex="0"`) with <kbd>Enter</kbd> / <kbd>Space</kbd> execution.
- Window resize listener automatically recalculates coordinates and re-renders tree dimensions.

---

## 4. Request Lifecycle Sequence

```
User Action (e.g. Submit Lost Report)
   │
   ▼
Browser (HTTP POST /report/lost)
   │  [CSRF Token + Form Payload]
   ▼
WSGI Dispatcher (run.py)
   │
   ▼
Flask App Factory (app/__init__.py)
   │  [Global @before_request: Validate CSRF Token]
   ▼
Items Blueprint (app/items.py -> report_lost())
   │  1. Check Authentication (@login_required)
   │  2. Sanitize & Validate Inputs (Bounds, Data Types)
   │  3. Optional Image Magic-Byte Inspection
   │  4. Execute Parameterized SQL INSERT via Unified DB Adapter (app/db.py)
   │  5. Index Item Key into In-Memory BST (app/dsa/bst_service.py)
   │  6. Trigger Multi-Factor Matching Scan against Open Found Items (app/matching.py)
   │  7. Flash User Notification & Return HTTP 302 Redirect
   ▼
Browser (HTTP GET /items/<id>)
   │
   ▼
Items Blueprint (detail view)
   │  1. Retrieve Item Record from Database
   │  2. Retrieve BST Path & Comparison Metrics
   │  3. Retrieve Ranked Match Candidates with Score Justifications
   ▼
Jinja2 Template Engine (app/templates/items/detail.html)
   │  Render HTML with auto-escaped context variables
   ▼
Browser Displays Rendered Page
```

---

## 5. Architectural Quality Attributes

1. **Maintainability:** Modular Flask blueprints cleanly separate concerns across authentication, catalog management, claims verification, administration, and algorithmic data structures.
2. **Portability:** The dual-engine database layer allows seamless operation in local single-file environments (SQLite) and enterprise production deployments (MySQL).
3. **Resilience:** If the database engine fails or a route encounters an unhandled exception, custom error handlers log the incident and render helpful, branded error interfaces rather than raw tracebacks.
4. **Security:** Built-in defenses against OWASP Top 10 vulnerabilities including SQL injection, cross-site scripting, CSRF, IDOR, and privilege escalation.
