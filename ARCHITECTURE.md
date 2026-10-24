# CampusFind — Architectural Specification

> **Project:** Smart Lost & Found System (CampusFind)  
> **Course:** BTech Computer Science & Engineering Capstone  
> **Author:** Individual BTech Developer  

---

## 1. High-Level Architectural Model

CampusFind implements a **Layered Model-View-Controller (MVC) Architecture** augmented with an in-memory algorithmic subsystem:

```
┌────────────────────────────────────────────────────────┐
│               Client Tier (Browser UI)                 │
│  - Modern CSS3 Custom Design System (Responsive)       │
│  - Dynamic SVG Tree Canvas & Algorithmic Trace Console  │
│  - Asynchronous REST & DOM Modal Controllers           │
└───────────────────────────┬────────────────────────────┘
                            │ HTTP / HTTPS
┌───────────────────────────▼────────────────────────────┐
│              Application Tier (Flask WSGI)             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Auth BP    │  │   Items BP   │  │  Claims BP   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Admin BP   │  │    DSA BP    │  │ Matching Eng │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────┬───────────────────────────────┬──────────┘
              │                               │
              ▼                               ▼
┌───────────────────────────────┐ ┌───────────────────────────────┐
│     In-Memory Subsystem       │ │      Data Tier (Unified DB)   │
│  - Binary Search Tree (BST)   │ │  - Primary Engine: MySQL 8.0+ │
│  - Sequential ID Indexing     │ │  - Local Fallback: SQLite 3   │
│  - Subtree Range Pruning      │ │  - Parameterized SQL Adapter  │
└───────────────────────────────┘ └───────────────────────────────┘
```

---

## 2. Core Subsystems

### 2.1 Unified Database Adapter (`app/db.py`)
- **Engine Independence:** Automatically detects whether MySQL server is reachable. If reachable, it utilizes `pymysql.cursors.DictCursor`. If unreachable or configured with `DB_TYPE=sqlite`, it seamlessly connects to SQLite with identical schema relations.
- **Parametric SQL Translation:** Developers write standard `%s` placeholders. The adapter automatically transforms `%s` into `?` when operating in SQLite mode, completely insulating application code from SQL injection vulnerabilities.
- **Connection Teardown:** Leverages Flask's `teardown_appcontext` hook to prevent connection leaks across concurrent HTTP worker threads.

### 2.2 Heuristic Similarity Engine (`app/matching.py`)
Matches are computed across four orthogonal vectors:
1. **Categorical Agreement ($30\%$):** Strict semantic match of reported item classifications.
2. **Lexical Overlap ($35\%$):** Tokenization, stop-word removal, and Jaccard similarity:
   $$J(A, B) = \frac{|A \cap B|}{|A \cup B|}$$
   augmented by direct title token overlaps.
3. **Spatial Landmark Compatibility ($20\%$):** Token overlap across campus zones (Library, Gym, SAC, Hostels, Cafeteria).
4. **Chronological Plausibility ($15\%$):** Temporal sequencing ensuring found date occurs on or after lost date.

### 2.3 Binary Search Tree (BST) Engine (`app/dsa/bst.py`)
- Provides an authentic Python tree structure:
  - Average time complexity: $\mathcal{O}(\log n)$
  - Worst-case time complexity: $\mathcal{O}(n)$
- Implements complete node deletion:
  - **Leaf Removal (0 children):** Disconnects child pointer from parent.
  - **Single Child Splice (1 child):** Connects parent directly to target's sole child.
  - **Two Children In-Order Successor (2 children):** Identifies minimum node in right subtree, copies payload, and recursively deletes successor.
- Integrates with SVG renderer via `/dsa/api/tree` and animated traversal endpoints.

---

## 3. Security Architecture

1. **Authentication:** Passwords are never stored in plaintext. They are salted and hashed using Werkzeug's secure key derivation functions (`scrypt` or `pbkdf2:sha256`).
2. **Authorization Guards:** Role-based decorators (`@login_required`, `@admin_required`) protect sensitive operations, ensuring standard students cannot access moderation panels or approve claims.
3. **Secret Verification Questions:** Lost item reporters can establish a private challenge (e.g., "What is the laptop wallpaper?"). Claimants must answer this challenge during claim submission.
4. **Environment Isolation:** Application secrets (`SECRET_KEY`, database passwords) are read from `.env` and kept out of version control via `.gitignore`.
