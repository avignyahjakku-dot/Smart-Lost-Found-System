# CampusFind — User Manual & Operational Guide

> **Project:** Smart Lost & Found System (CampusFind)  
> **Course:** Bachelor of Technology (BTech) in Computer Science & Engineering (CSE)  
> **Author:** Two-Person BTech CSE Capstone Project Team  
> **Audience:** Students, Campus Staff, Security Officers, and System Administrators  

---

## 1. Introduction & Evaluation Accounts

CampusFind provides a centralized, secure web application designed to track, correlate, and reunite lost belongings with their rightful owners across a university campus.

### Demo Evaluation Accounts
For examination and evaluation, the following pre-configured credentials can be utilized after running the database seed script (`python seed.py --reset`):

| Role | Email Address | Password | Privileges |
| :--- | :--- | :--- | :--- |
| **System Administrator** | `admin@campusfind.edu` | `Admin@CampusFind2026` | Full administrative control: claim approvals, item moderation, audit log inspection. |
| **Student (Alex)** | `alex@campusfind.edu` | `Student@123` | Reporting lost/found items, submitting claims, viewing personal activity. |
| **Student (Priya)** | `priya@campusfind.edu` | `Student@123` | Reporting lost/found items, submitting claims. |
| **Faculty / Staff** | `vance@campusfind.edu` | `Student@123` | Reporting misplaced classroom equipment. |

---

## 2. Student & Staff Workflows

### 2.1 Account Registration & Login
1. Navigate to **Sign Up** (`/register`) from the top navigation bar.
2. Enter your Full Name, Campus Email (`@campusfind.edu`), Student ID / Roll Number, Contact Phone, and Campus Role (`student` or `staff`).
3. Provide a password of at least 8 characters and confirm it.
4. Upon successful registration, the system automatically authenticates you and directs you to the catalog.
5. Existing users can log in via **Login** (`/login`).

---

### 2.2 Reporting a Lost Item
If you have misplaced personal property on campus:
1. Click **+ Report Lost** (red button) in the navigation bar or homepage hero banner.
2. Complete the reporting form:
   - **Item Title / Name:** e.g., `Dell Inspiron 15 Laptop (Silver)`. Include brand, model, and primary color.
   - **Category:** Select from standardized classifications (e.g., `Electronics & Gadgets`, `Bottles & Tumblers`, `Wallets & Purses`, `Keys & Cards`, `Books & Stationery`).
   - **Last Seen Location:** Select the campus zone where the item was last in your possession (e.g., `Central Library`, `Computer Science Department`, `Cafeteria / Food Court`).
   - **Date Lost:** Specify the calendar date the item went missing.
   - **Optional Photo:** Upload a reference image (PNG, JPG, JPEG, GIF, or WEBP; maximum 5MB).
   - **Detailed Description:** Describe distinguishing features (scratches, stickers, unique wallpaper, specific contents).
   - **Secret Ownership Verification Hint:** *(Highly Recommended)* Formulate a private question that only the genuine owner can answer (e.g., *"What picture is set as the lock screen wallpaper?"* or *"What keychain is attached to the pouch?"*).
3. Click **Publish Lost Report**.
4. The system immediately indices the report into the in-memory Binary Search Tree, scans for candidate found items, and displays the item detail page.

---

### 2.3 Reporting a Found Item
If you discover unattended or misplaced property on campus:
1. Click **+ Report Found** (green button) in the navigation bar.
2. Complete the form:
   - **Item Name / Title:** e.g., `Blue Casio Scientific Calculator FX-991EX`.
   - **Category:** Select appropriate category.
   - **Found Location:** Campus area where discovered (e.g., `Hostel Block A`, `Mechanical Workshop`).
   - **Date Found:** Date discovered.
   - **Photo of Found Item:** Upload a clear image of the object.
   - **Current Storage / Custody Location:** *(Required)* State where the item has been physically deposited (e.g., `Central Library Front Desk`, `Department Office Desk 3`, `Main Security Gate 1`).
   - **Item Description & Condition:** General physical condition and exterior markings.
3. Click **Submit Found Report**.

---

### 2.4 Browsing the Campus Repository
1. Navigate to **Catalog** (`/browse`).
2. Utilize the search and filtering controls:
   - **Keyword Search:** Searches titles, descriptions, and location names.
   - **Item Type:** Toggle between *All Types*, *Lost Items Only*, or *Found Items Only*.
   - **Category & Location:** Filter records by exact campus building or item type.
   - **Sort Order:** Sort by *Newest First* or *Oldest First*.
3. Click **Filter Results** to update the grid, or **Reset** to clear all active filters.

---

### 2.5 Inspecting Items & Algorithmic Predictions
Click **View Details** on any item card:
- **Left Column:** Displays item photograph, status badge, reporter information, and an **In-Memory BST Lookup Box** showing the exact branch comparison path visited in RAM to locate the item's integer ID.
- **Right Column:** Displays campus location, occurrence date, custody desk, and the full description.
- **Smart Matching Engine Predictions:** Below the item details, the system displays opposite-type candidates ranked by similarity score:
  - **Match Confidence Tier:** `High Match` ($\ge 75\%$), `Moderate Match` ($50\% - 74\%$), or `Plausible Match` ($30\% - 49\%$).
  - **4-Factor Score Breakdown:** View exact point allocations for Category (30%), Text Similarity (35%), Location Proximity (20%), and Timeline Plausibility (15%).

---

### 2.6 Submitting an Ownership Claim
When you identify your missing belonging among the found items catalog:
1. Open the item's detail view (`/items/<id>`).
2. Click **Submit Ownership Claim** (visible only on found items to authenticated users who are not the original finder).
3. In the accessible modal dialog:
   - Enter your **Contact Phone Number** for verification calls.
   - If the finder configured a secret verification hint, provide the **Answer to Verification Question**.
   - Provide **Proof of Ownership / Distinguishing Marks** (e.g., serial number, invoice details, contents).
4. Click **Submit Claim**.
5. Your claim is dispatched to the campus administration queue with an initial status of `Pending`.

---

### 2.7 Tracking Personal Activity
Navigate to **My Activity** (`/my-dashboard`):
- **My Ownership Claims:** Real-time table displaying submitted claims, target items, review statuses (`Pending`, `Approved`, `Rejected`), and administrator review remarks.
- **Lost Items I Reported:** Overview of active and resolved lost reports.
- **Found Items I Reported:** Overview of turned-in property and current custody desks.

---

## 3. Administrator Workflows

Users logged in with administrative privileges (`admin@campusfind.edu`) have access to specialized moderation controls.

### 3.1 Accessing the Admin Dashboard
Click the prominent **🛡️ Admin Panel** link in the navigation bar to access `/admin/dashboard`.

### 3.2 Reviewing Ownership Claims
The **Pending Ownership Claims Requiring Review** section lists all unadjudicated claims:
1. Inspect the target item, claimant identity, submitted proof details, and secret verification answer.
2. In the decision box, enter optional **Admin verification remarks** (e.g., *"Serial number verified against student laptop invoice"* or *"Incorrect answer to verification hint"*).
3. Click **Approve** or **Reject**:
   - **Approve:** Updates claim status to `approved`, transitions the found item status to `claimed`, and logs an audit record.
   - **Reject:** Updates claim status to `rejected`, leaves the item `open` for valid claims, and logs an audit record.

### 3.3 Repository Item Moderation & Deletion
Under **Repository Items Moderation**:
- Administrators can review any active report on campus.
- To permanently remove an inappropriate, duplicate, or spam submission, click **Delete** and confirm the prompt.
- The item, its associated claims, match correlations, and uploaded images are removed in an ACID cascade.

### 3.4 Administrative Audit Trail
The **Administrative Audit Log** table displays an immutable, chronological record of system events:
- Timestamp, Action Code (e.g., `CLAIM_APPROVE`, `CLAIM_REJECT`, `ITEM_DELETE`), Operator Name, and Details.

---

## 4. Interactive Binary Search Tree (BST) Visualizer

Navigate to **BST Visualizer** (`/dsa/visualizer`) to explore the application's underlying algorithmic data structure:

### 4.1 Interface Overview
- **Metrics Bar:** Shows real-time Node Count (Size), Tree Height, and Theoretical Optimal Comparisons $\lfloor\log_2 n\rfloor + 1$.
- **Control Inputs:** Input numeric keys and optional labels.
- **SVG Canvas:** Dynamically rendered vector graphic of the tree with branches and circular nodes.
- **Execution Console:** Terminal-styled output logging comparisons, branching directions, and traversal sequences.

### 4.2 Interactive Actions
1. **Insert Node:** Enter a numeric key (e.g., `42`) and click **+ Insert Node**. The node is inserted preserving the invariant ($left < key \le right$) and highlighted in green.
2. **Search Key:** Enter a key and click **🔍 Search Key** (or click directly on any tree node). The engine traces the search path, highlighting visited nodes in yellow (`state-visited`), concluding on the target node in green (`state-found`) or logging an un-found status.
3. **Delete Key:** Enter a key and click **🗑️ Delete Key**. The visualizer animates the deletion, handling leaf removal, single child splicing, or two-child replacement via in-order successor.
4. **Traversals:** Click **In-Order**, **Pre-Order**, or **Post-Order** to trigger an animated sequence visiting all nodes in order.
5. **Reset Tree:** Click **🔄 Reset Balanced Tree** to restore the default balanced campus dataset.
6. **Keyboard Navigation:** Press <kbd>Tab</kbd> to focus on individual nodes, and press <kbd>Enter</kbd> or <kbd>Space</kbd> to execute a search trace on the focused node.
