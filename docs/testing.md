# CampusFind — Automated Testing Specification & Test Plan

> **Project:** Smart Lost & Found System (CampusFind)  
> **Course:** Bachelor of Technology (BTech) in Computer Science & Engineering (CSE)  
> **Author:** Two-Person BTech CSE Capstone Project Team  
> **Test Framework:** Python Standard Library `unittest`  
> **Test Status:** 51 Tests Executed / 0 Failures / 0 Errors ($51/51$ Passing)  

---

## 1. Test Strategy & Quality Assurance Approach

The testing methodology ensures end-to-end verification of CampusFind across multiple testing tiers:
1. **Unit Testing:** Validates pure algorithmic operations (Binary Search Tree node insertions, three-case deletions, in-order traversals, and Jaccard lexical similarity functions).
2. **Integration Testing:** Tests Flask request-response cycles, database persistence, session state retention, form processing, and custom error handling.
3. **Security Testing:** Verifies password hashing standards, session cookie attributes, role-based admin route gating, SQL injection resilience, and XSS auto-escaping.
4. **Boundary & Validation Testing:** Verifies graceful rejection of malformed payloads, missing required fields, oversized string inputs, and unsupported file formats.

---

## 2. Test Suite Architecture & Coverage Matrix

All tests reside in the `tests/` directory and are organized into 8 modular test suites:

| Suite Name | Test File | Scope & Capabilities Verified | Test Count |
| :--- | :--- | :--- | :---: |
| **Authentication** | [`tests/test_auth.py`](file:///c:/Users/6tan5/OneDrive/Desktop/smart%20lost%20&%20found%20system/tests/test_auth.py) | User registration, password hashing verification, duplicate email blocking, login/logout sessions, validation failures (short passwords, missing fields, oversized names), and `@admin_required` route gating. | 5 |
| **Binary Search Tree**| [`tests/test_bst.py`](file:///c:/Users/6tan5/OneDrive/Desktop/smart%20lost%20&%20found%20system/tests/test_bst.py) | Pure Python BST operations: empty tree initial state, single-node insertion, duplicate key in-place updates, 3-case deletion (leaf, 1 child, 2 children with in-order successor), traversal invariants (in-order sorted ascending, pre-order, post-order), search path tracing (hits and misses), range queries, and min/max key lookups. | 10 |
| **Claims & Admin** | [`tests/test_claims.py`](file:///c:/Users/6tan5/OneDrive/Desktop/smart%20lost%20&%20found%20system/tests/test_claims.py) | Full claim lifecycle, self-claim prevention, type restriction (cannot claim lost items), claim rejection workflow with admin remarks, admin item deletion, and field validation (missing phone/proof or oversized input). | 5 |
| **DSA REST API** | [`tests/test_dsa_routes.py`](file:///c:/Users/6tan5/OneDrive/Desktop/smart%20lost%20&%20found%20system/tests/test_dsa_routes.py) | Visualizer HTML canvas view, `/dsa/api/tree` JSON structure, `/dsa/api/insert` with key validation, `/dsa/api/search` path comparison trace, `/dsa/api/delete`, `/dsa/api/traverse`, and `/dsa/api/reset`. | 7 |
| **Integration** | [`tests/test_integration.py`](file:///c:/Users/6tan5/OneDrive/Desktop/smart%20lost%20&%20found%20system/tests/test_integration.py) | Application test startup configuration, isolated test database, homepage rendering with live metrics, catalog search and campus location filtering, matching hub view, custom 404 error page, and database foreign key enforcement. | 6 |
| **Item Management** | [`tests/test_items.py`](file:///c:/Users/6tan5/OneDrive/Desktop/smart%20lost%20&%20found%20system/tests/test_items.py) | Lost item reporting, found item reporting with storage custody details, keyword search & category filtering, unsupported image upload warning, and input validation failures (missing fields, oversized title/description). | 5 |
| **Smart Matching** | [`tests/test_matching.py`](file:///c:/Users/6tan5/OneDrive/Desktop/smart%20lost%20&%20found%20system/tests/test_matching.py) | Token normalization, stop word removal, Jaccard intersection over union, high probability pairing, category mismatch penalty, chronological sequence penalty, candidate ranking, and safe handling of missing/malformed fields (`None`, invalid dates). | 7 |
| **Security & Hardening**| [`tests/test_security.py`](file:///c:/Users/6tan5/OneDrive/Desktop/smart%20lost%20&%20found%20system/tests/test_security.py) | Scrypt/PBKDF2 password hashing verification, password complexity, session cookie security flags (`HttpOnly`, `SameSite=Lax`, `Secure`), IDOR status modification prevention, SQL injection resilience, XSS HTML auto-escaping, and role-based admin authorization. | 6 |
| **TOTAL** | | | **51** |

---

## 3. Detailed Test Case Specifications

### 3.1 Authentication Suite (`tests/test_auth.py`)
- `test_user_registration_success`: Validates successful user registration, automatic password hashing, and session initialization.
- `test_duplicate_email_registration_blocked`: Ensures that attempting to register with an existing email address is rejected and returns a warning.
- `test_login_and_logout_flow`: Verifies login with valid credentials, session establishment, session cookie invalidation upon logout, and rejection of invalid passwords.
- `test_registration_validation_failures`: Tests server-side boundary validation: missing fields, full names exceeding 100 characters, invalid emails, and passwords under 8 characters.
- `test_admin_route_protection`: Verifies that unauthenticated visitors are redirected to `/login` when accessing `/admin/dashboard`, and that authenticated non-admin users receive HTTP 302 with an access-denied flash alert.

### 3.2 Binary Search Tree Suite (`tests/test_bst.py`)
- `test_empty_tree_properties`: Verifies size 0, height 0, and search on empty tree returning `None`.
- `test_single_node_insertion_and_search`: Inserts a key-value pair and verifies $O(1)$ search retrieval.
- `test_duplicate_key_updates_data`: Tests that inserting an existing key updates the payload in place without incrementing tree size.
- `test_bst_ordering_and_traversal`: Inserts an arbitrary sequence of keys and asserts that `inorder_traversal()` strictly yields an ascending sorted sequence ($k_1 < k_2 < \dots < k_n$).
- `test_search_path_tracing`: Ensures that `search_with_path(target)` records the exact branch comparisons (e.g. `[root, child, target]`) enabling client-side visual highlighting.
- `test_min_and_max`: Verifies minimum and maximum key retrieval.
- `test_range_search_pruning`: Tests retrieving all nodes where $\text{min\_key} \le k \le \text{max\_key}$, verifying disjoint subtrees are pruned.
- `test_deletion_case_1_leaf`: Deletes a node with zero children and verifies parent pointer nullification.
- `test_deletion_case_2_one_child`: Deletes a node with exactly one child and asserts the child splices cleanly into the parent's pointer.
- `test_deletion_case_3_two_children`: Deletes a node with two children, ensuring it is replaced by its in-order successor (minimum in right subtree) while preserving the BST invariant.

### 3.3 Claims & Administration Suite (`tests/test_claims.py`)
- `test_submit_claim_lifecycle`: Tests full end-to-end claim submission by a student, initial `pending` state, and approval by an administrator updating item status to `claimed`.
- `test_claim_rejection_flow`: Tests that an administrator can reject a claim with written review remarks, leaving the item `open` for other claimants.
- `test_claim_on_lost_item_is_rejected`: Ensures claims can only be filed against found items (not lost items).
- `test_admin_item_deletion`: Verifies that an administrator can permanently delete inappropriate or spam item submissions.
- `test_claim_validation_missing_fields_and_oversized`: Rejects claims missing proof details, contact numbers, or submitting phone numbers exceeding 30 characters.

### 3.4 DSA REST API Suite (`tests/test_dsa_routes.py`)
- `test_visualizer_page_renders`: Asserts HTTP 200 on `/dsa/visualizer` and checks presence of the SVG canvas.
- `test_api_tree_structure`: Asserts that `GET /dsa/api/tree` returns `{ "success": true, "tree": {...}, "size": N, "height": H }`.
- `test_api_insert_and_validation`: Tests `POST /dsa/api/insert` with integer keys and verifies rejection of non-numeric keys.
- `test_api_search_path_tracing`: Tests `POST /dsa/api/search` returning search path array and comparison count.
- `test_api_delete_key`: Tests `POST /dsa/api/delete` and verifies updated tree size.
- `test_api_traversals`: Tests `GET /dsa/api/traverse?order=inorder` returning keys in ascending sequence.
- `test_api_reset`: Tests `POST /dsa/api/reset` restoring the default balanced campus dataset.

### 3.5 Integration Suite (`tests/test_integration.py`)
- `test_application_startup_in_test_configuration`: Verifies Flask starts cleanly in `TestingConfig` with an isolated SQLite database.
- `test_homepage_rendering_and_metrics`: Asserts HTTP 200 on `/` with repository metrics and reporting CTAs.
- `test_catalog_browsing_page`: Tests `/browse` view with search inputs and campus location filters.
- `test_matching_hub_page`: Tests `/matches` rendering with scoring algorithm explanation.
- `test_custom_404_error_page`: Verifies that non-existent routes trigger the custom branded 404 error page.
- `test_database_persistence_and_foreign_keys`: Confirms that foreign key constraints (`PRAGMA foreign_keys = ON;`) reject records with non-existent parent IDs.

### 3.6 Item Management Suite (`tests/test_items.py`)
- `test_report_lost_item`: Tests reporting a lost item with category, date, location, and secret hint.
- `test_report_found_item`: Tests reporting a found item with physical storage custody location.
- `test_browse_catalog_and_filtering`: Validates multi-parameter search filtering: keyword queries (`?q=Sony`), category filters (`?category=Wallets`), and type filters (`?type=lost`).
- `test_unsupported_image_upload_warning`: Tests that uploading an unsupported executable or script file triggers a warning flash message and prevents storage.
- `test_report_item_validation_failures`: Rejects reports with missing titles, titles exceeding 150 characters, or descriptions exceeding 2000 characters.

### 3.7 Smart Matching Suite (`tests/test_matching.py`)
- `test_clean_tokens`: Validates lowercasing, punctuation stripping, and stop-word filtering.
- `test_jaccard_similarity`: Validates mathematical intersection-over-union calculation.
- `test_high_probability_match`: Tests pairing an identical lost and found report, verifying score $\ge 75\%$ and `High` tier classification.
- `test_category_mismatch_penalty`: Verifies that conflicting categories receive 0 category points.
- `test_chronological_sequence_penalty`: Verifies that items found well before being lost receive 0 points.
- `test_ranking_candidates`: Asserts that multiple candidates are returned in strictly descending similarity score order.
- `test_missing_and_malformed_fields_handled_safely`: Validates engine resilience when encountering `None` values, empty tokens, or malformed date formats.

### 3.8 Security Suite (`tests/test_security.py`)
- `test_password_hashing_and_complexity`: Validates password hash format (`scrypt` or `pbkdf2:sha256`) and rejection of passwords shorter than 8 characters.
- `test_session_cookie_security_configurations`: Tests that session cookies enforce `HttpOnly` and `SameSite=Lax`, and `Secure=True` in production.
- `test_role_based_admin_protection`: Asserts that unauthenticated visitors and standard users are blocked from admin moderation routes.
- `test_idor_status_modification_prevention`: Asserts that User B cannot alter the status of an item reported by User A without administrative rights.
- `test_sql_injection_resilience`: Verifies that SQL injection payloads in search queries and form inputs are evaluated as benign string literals.
- `test_xss_auto_escaping`: Asserts that `<script>alert(1)</script>` payloads injected into item descriptions are safely HTML-escaped by Jinja2.

---

## 4. Test Execution Instructions

### Running the Entire Test Suite
Execute the standalone test runner from the root directory:
```bash
python run_tests.py
```

Alternatively, use Python's built-in discovery tool:
```bash
python -m unittest discover tests
```

### Running Individual Test Suites
To run a specific test suite in isolation:
```bash
# Authentication tests
python -m unittest tests.test_auth

# Binary Search Tree tests
python -m unittest tests.test_bst

# Security tests
python -m unittest tests.test_security

# Matching engine tests
python -m unittest tests.test_matching
```

---

## 5. Test Isolation Methodology

To prevent cross-test contamination and preserve developer data:
1. **Dynamic Test Database:** Each test run instantiates an isolated SQLite database (`test_campusfind.db`).
2. **Setup and Teardown:**
   - In `setUp()`: A fresh schema is applied, and an application context is pushed.
   - In `tearDown()`: The application context is popped, connections closed, and the test database file is unlinked.
3. **Zero Production Mutation:** Automated tests never write to the production MySQL database or modify active user data.
