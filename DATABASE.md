# CampusFind — Database Design & Schema Specification

> **Project:** Smart Lost & Found System (CampusFind)  
> **Course:** BTech Computer Science & Engineering Capstone  
> **Target RDBMS:** MySQL 8.0+ / MariaDB 10.4+ (with SQLite fallback)  

---

## 1. Entity-Relationship (ER) Overview

CampusFind utilizes an ACID-compliant relational schema consisting of five interconnected entities:

```
┌─────────────────────────┐               ┌─────────────────────────┐
│          users          │1             *│          items          │
├─────────────────────────┼───────────────┼─────────────────────────┤
│ id (PK)                 │               │ id (PK)                 │
│ full_name               │               │ user_id (FK -> users.id)│
│ email (UNIQUE)          │               │ type ('lost' / 'found') │
│ student_id              │               │ title                   │
│ password_hash           │               │ category                │
│ role ('student'/'staff'/│               │ description             │
│       'admin')          │               │ location                │
│ phone                   │               │ item_date               │
│ created_at              │               │ storage_location        │
└────────────┬────────────┘               │ secret_hint             │
             │1                           │ status                  │
             │                            └────────────┬────────────┘
             │                                         │1
             │                                         │
             │*                                        │*
┌────────────▼────────────┐               ┌────────────▼────────────┐
│      activity_logs      │               │         claims          │
├─────────────────────────┤               ├─────────────────────────┤
│ id (PK)                 │               │ id (PK)                 │
│ user_id (FK -> users.id)│               │ item_id (FK -> items.id)│
│ action                  │               │ claimant_id (FK -> users│
│ details                 │               │ proof_details           │
│ timestamp               │               │ secret_answer           │
└─────────────────────────┘               │ contact_phone           │
                                          │ status ('pending'/      │
                                          │   'approved'/'rejected')│
                                          │ admin_notes             │
                                          │ created_at              │
                                          └─────────────────────────┘
```

---

## 2. Table Specifications

### 2.1 Table: `users`
Stores registered students, staff members, and administrators.
- `id`: `INT AUTO_INCREMENT PRIMARY KEY`
- `full_name`: `VARCHAR(120) NOT NULL`
- `email`: `VARCHAR(150) NOT NULL UNIQUE`
- `student_id`: `VARCHAR(50) DEFAULT NULL`
- `phone`: `VARCHAR(30) DEFAULT NULL`
- `password_hash`: `VARCHAR(255) NOT NULL`
- `role`: `ENUM('student', 'staff', 'admin') NOT NULL DEFAULT 'student'`
- `created_at`: `TIMESTAMP DEFAULT CURRENT_TIMESTAMP`
- **Indexes:** `idx_user_email` on `email`, `idx_user_role` on `role`.

### 2.2 Table: `items`
Maintains records for both lost and found belongings.
- `id`: `INT AUTO_INCREMENT PRIMARY KEY`
- `user_id`: `INT NOT NULL` (Foreign Key referencing `users(id)` ON DELETE CASCADE)
- `type`: `ENUM('lost', 'found') NOT NULL`
- `title`: `VARCHAR(180) NOT NULL`
- `category`: `VARCHAR(60) NOT NULL`
- `description`: `TEXT NOT NULL`
- `location`: `VARCHAR(150) NOT NULL`
- `item_date`: `DATE NOT NULL`
- `image_filename`: `VARCHAR(255) DEFAULT NULL`
- `storage_location`: `VARCHAR(150) DEFAULT NULL` (Physical custody desk for found items)
- `secret_hint`: `VARCHAR(255) DEFAULT NULL` (Ownership test question for lost items)
- `status`: `ENUM('open', 'claimed', 'returned', 'resolved', 'closed') NOT NULL DEFAULT 'open'`
- `created_at`: `TIMESTAMP DEFAULT CURRENT_TIMESTAMP`
- `updated_at`: `TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP`
- **Indexes:**
  - `idx_items_type` on `type`
  - `idx_items_category` on `category`
  - `idx_items_status` on `status`
  - `idx_items_date` on `item_date`
  - `idx_items_location` on `location`

### 2.3 Table: `claims`
Tracks ownership verification claims submitted by claimants.
- `id`: `INT AUTO_INCREMENT PRIMARY KEY`
- `item_id`: `INT NOT NULL` (Foreign Key referencing `items(id)` ON DELETE CASCADE)
- `claimant_id`: `INT NOT NULL` (Foreign Key referencing `users(id)` ON DELETE CASCADE)
- `proof_details`: `TEXT NOT NULL`
- `secret_answer`: `VARCHAR(255) DEFAULT NULL`
- `contact_phone`: `VARCHAR(30) NOT NULL`
- `status`: `ENUM('pending', 'approved', 'rejected') NOT NULL DEFAULT 'pending'`
- `admin_notes`: `TEXT DEFAULT NULL`
- `created_at`: `TIMESTAMP DEFAULT CURRENT_TIMESTAMP`
- `updated_at`: `TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP`
- **Indexes:** `idx_claims_status` on `status`, `idx_claims_item` on `item_id`, `idx_claims_claimant` on `claimant_id`.

### 2.4 Table: `activity_logs`
Audit log recording system and moderation events.
- `id`: `INT AUTO_INCREMENT PRIMARY KEY`
- `user_id`: `INT DEFAULT NULL` (Foreign Key referencing `users(id)` ON DELETE SET NULL)
- `action`: `VARCHAR(80) NOT NULL`
- `details`: `TEXT DEFAULT NULL`
- `created_at`: `TIMESTAMP DEFAULT CURRENT_TIMESTAMP`
- **Indexes:** `idx_logs_action` on `action`, `idx_logs_created_at` on `created_at`.

---

## 3. Database Indexing Analysis

In MySQL InnoDB, tables are organized as clustered B+ Trees where primary keys dictate the physical disk layout:
1. **Secondary B+ Tree Indexes:** Indexing `category`, `type`, `status`, and `item_date` enables the storage engine to resolve multi-criteria browse queries without scanning full table pages.
2. **Comparison with In-Memory BST:** While on-disk B+ Trees are optimized for block I/O (hundreds of keys per 16 KB page), our in-memory BST in Python allows $O(\log n)$ memory pointer traversals and range lookups without database transaction overhead.
