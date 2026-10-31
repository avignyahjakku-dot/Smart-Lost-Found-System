<p align="center">
  <img src="images/sit_header.png" alt="Symbiosis Institute of Technology, Hyderabad" width="100%" />
</p>

<br>

---

<br><br><br>

# PROJECT REPORT
## ON

# “CAMPUSFIND: SMART UNIVERSITY LOST & FOUND SYSTEM USING IN-MEMORY BINARY SEARCH TREE (BST) INDEXING AND MULTI-FACTOR HEURISTIC MATCHING”

<br><br>

### **Subject: Data Structures - Lab**

<br><br>

### **Submitted By:**

| Name | Branch | PRN |
| :--- | :--- | :--- |
| **Avignyah Jakku** | Computer Science & Engineering (CSE) | 25070721024 |
| **Meghana** | Computer Science & Engineering (CSE) | 25070721002 |

<br><br><br><br>

**Academic Year: 2026 – 2027**  
**Department of Computer Science & Engineering**  
**Symbiosis Institute of Technology (SIT), Hyderabad**

<div style="page-break-after: always;"></div>

---

<p align="center">
  <img src="images/sit_header.png" alt="Symbiosis Institute of Technology, Hyderabad" width="100%" />
</p>

# INDEX

| S.No. | Chapter / Topic | Page No. |
| :---: | :--- | :---: |
| **1.** | **Acknowledgement** | 3 |
| **2.** | **Abstract and Introduction** | 4 |
| **3.** | **Methodology** | 5 |
| **4.** | **Binary Search Tree (BST) Architecture & Theoretical Foundations** | 6 |
| **5.** | **Multi-Factor Heuristic Matching Engine & State Transitions** | 7 |
| **6.** | **Comparative Analysis: In-Memory BST vs. Relational B-Tree Indexing** | 8 |
| **7.** | **Applications and Future Scope** | 9 |
| **8.** | **System Prototype Walkthrough & Interface Specifications — Part I** | 10 |
| **9.** | **System Prototype Walkthrough & Interface Specifications — Part II** | 11 |
| **10.** | **System Prototype Walkthrough & Interface Specifications — Part III** | 12 |

<div style="page-break-after: always;"></div>

---

<p align="center">
  <img src="images/sit_header.png" alt="Symbiosis Institute of Technology, Hyderabad" width="100%" />
</p>

# ACKNOWLEDGEMENT

We take this opportunity to express our heartfelt gratitude to everyone who has guided and supported us throughout the conceptualization, algorithmic design, and full-stack software implementation of our project titled:

> **“CAMPUSFIND: Smart University Lost & Found System Using In-Memory Binary Search Tree (BST) Indexing and Multi-Factor Heuristic Matching.”**

First and foremost, we extend our deepest thanks to **Dr. Rakesh Salakapuri**, our professor, lab instructor, and project guide, for his constant encouragement, valuable technical guidance, and constructive feedback throughout the semester. His insightful suggestions and profound knowledge helped us bridge theoretical classroom data structures with practical, production-ready web engineering. His guidance on tree balancing, in-memory traversal paths, and heuristic similarity scoring inspired us to design and deliver a fully functional, mathematically sound system.

We would like to express our sincere gratitude to **Dr. Rajinikanth Aluvalu**, Director of Symbiosis Institute of Technology (SIT), Hyderabad, for providing us with state-of-the-art computational infrastructure, modern laboratory facilities, and an academic ecosystem that fosters rigorous technological inquiry, practical experimentation, and software innovation.

We also convey our appreciation to the faculty members and technical staff of the Department of Computer Science & Engineering for their continuous assistance during laboratory sessions.

Finally, we express our gratitude to our peers and classmates for their valuable discussions, collaborative testing, and moral support throughout the development lifecycle. We are profoundly grateful to Symbiosis Institute of Technology, Hyderabad, for granting us the platform to transform algorithmic concepts into an impactful real-world software solution.

<br><br>
**Avignyah Jakku** (PRN: 25070721024)  
**Meghana** (PRN: 25070721002)  
*Department of Computer Science & Engineering*  
*Symbiosis Institute of Technology, Hyderabad*

<div style="page-break-after: always;"></div>

---

<p align="center">
  <img src="images/sit_header.png" alt="Symbiosis Institute of Technology, Hyderabad" width="100%" />
</p>

# ABSTRACT AND INTRODUCTION

### Abstract
**CampusFind** is an applied data structures and full-stack software system designed to automate the logging, discovery, logarithmic indexing, and heuristic correlation of misplaced personal property across university campuses. At its computational core, the system models item repositories using an authentic in-memory **Binary Search Tree (BST)** to provide $O(\log n)$ average-time key lookups, range filtering, and deterministic in-order sorted traversals. Alongside tree indexing, an automated multi-factor heuristic engine evaluates candidate lost-and-found pairings across category compatibility, textual Jaccard token similarity, spatial campus zone proximity, and chronological sequence plausibility. 

The application is engineered using a layered Model-View-Controller (MVC) architecture with Python Flask, a unified dual-engine database layer (MySQL with automatic SQLite fallback), and a lightweight vanilla JavaScript vector visualizer. By bridging fundamental computer science data structures with production web workflows, CampusFind eliminates informal communication bottlenecks, mitigates fraudulent ownership claims via secret challenge verification, and provides an explainable pedagogical visualization of tree-based search trajectories.

### Introduction
Every academic semester, thousands of personal items—ranging from student identity cards and laboratory notebooks to laptops, scientific calculators, and prescription glasses—are misplaced across lecture halls, dining areas, sporting facilities, and transit routes. Conventional campus lost-and-found procedures rely on disjointed, manual mechanisms:
- **Fragmented Communication:** Information is scattered across informal WhatsApp messaging groups, handwritten security registers, and physical bulletin boards.
- **Vulnerability to Unauthorized Claims:** Public bulletin boards and social media posts openly display distinguishing characteristics (serial numbers, engravings, stickers), enabling dishonest parties to fraudulently claim valuable items.
- **Manual Administrative Burden:** Security personnel and hostel wardens spend disproportionate effort cross-referencing lost inquiries with turned-in custody items.
- **Pedagogical Gap in Data Structure Applications:** Academic coursework often studies foundational data structures (such as Binary Search Trees) in isolation as theoretical terminal scripts, rarely exploring their integration into real-time server architectures.

**CampusFind** addresses these challenges through a centralized, secure web repository that pairs an in-memory Binary Search Tree index with an automated similarity matching algorithm. By maintaining an in-memory BST parallel to persistent relational storage, the application delivers sub-millisecond retrieval of item records while animating real-time insertion, search path traces, and three-case node deletions for educational clarity.

<div style="page-break-after: always;"></div>

---

<p align="center">
  <img src="images/sit_header.png" alt="Symbiosis Institute of Technology, Hyderabad" width="100%" />
</p>

# METHODOLOGY

The development and execution of CampusFind follows a structured, six-stage engineering and algorithmic methodology:

```
[1. Data Ingestion & Dual Persistence]
                  │
                  ▼
[2. In-Memory BST Construction] ────► [3. Dynamic Node Indexing & Deletion]
                  │
                  ▼
[4. Multi-Factor Heuristic Matching Engine]
                  │
                  ▼
[5. Dual-Factor Verification & Claim Adjudication]
                  │
                  ▼
[6. Interactive Vector SVG Visualization]
```

### 1. Data Ingestion & Dual Persistence
- Users log lost and found reports with structured metadata: Title, Category, Campus Landmark, Incident Timestamp, Descriptive Attributes, Optional Photo, and Secret Ownership Verification Hints.
- Data is stored transactionally with ACID guarantees using a unified database adapter (`app/db.py`) supporting production MySQL (port 3306) and local SQLite (`campusfind.db`) with zero manual reconfiguration.

### 2. In-Memory BST Construction
- On server startup, persistent item identifiers and summary pointers are ingested into an in-memory Binary Search Tree (`BSTNode`, `BinarySearchTree` in `app/dsa/bst.py`).
- Every item identifier acts as a unique numerical key satisfying the invariant:
  $$\forall N: \quad \text{Keys}(\text{Left Subtree}) < \text{Key}(N) < \text{Keys}(\text{Right Subtree})$$

### 3. Dynamic Node Indexing & Deletion
- **Insertion:** As new items are logged, nodes are dynamically inserted in $O(\log n)$ average time.
- **Deletion:** When items are returned or archived, nodes are removed handling all three structural cases: leaf deletion, single-child bypass, and two-child in-order successor relocation.
- **Path Tracking:** Every search operation logs the sequence of nodes evaluated from the root to provide explainable step-by-step path traces.

### 4. Multi-Factor Heuristic Matching
- Correlates unrecovered lost reports against active found inventory using a weighted mathematical scoring function combining categorical matching, Jaccard token overlap, spatial landmark proximity, and chronological delta validity.

### 5. Dual-Factor Verification & Claim Adjudication
- Prevents fraud by requiring claimants to answer private owner challenge questions set during item creation before an authorized administrator approves physical handover.

### 6. Interactive Vector SVG Visualization
- A client-side visualizer dynamically parses tree hierarchies and renders interactive SVG canvases illustrating tree geometry, balance, depth, and traversal paths.

<div style="page-break-after: always;"></div>

---

<p align="center">
  <img src="images/sit_header.png" alt="Symbiosis Institute of Technology, Hyderabad" width="100%" />
</p>

# BINARY SEARCH TREE (BST) ARCHITECTURE & THEORETICAL FOUNDATIONS

### 1. Mathematical Definition and BST Invariant
A **Binary Search Tree (BST)** is a hierarchical, non-linear linked data structure composed of nodes, each storing a key $k$, an associated satellite data payload $v$, and two disjoint child pointer references ($\text{left}$ and $\text{right}$). The tree strictly enforces the binary search invariant:

$$\text{For every node } x: \quad y \in \text{LeftSubtree}(x) \implies \text{key}(y) < \text{key}(x)$$
$$\text{For every node } x: \quad z \in \text{RightSubtree}(x) \implies \text{key}(z) > \text{key}(x)$$

```
                         [ Node (Key=15) ]
                          /             \
                         /               \
              [ Node (Key=8) ]       [ Node (Key=22) ]
                /          \           /           \
          [Key=4]      [Key=12]    [Key=18]      [Key=27]
```

### 2. Node Structural Schema
Each node in our implementation (`app/dsa/bst.py`) is encapsulated by the `BSTNode` class:

```python
class BSTNode:
    def __init__(self, key: int, data: Any = None):
        self.key: int = key          # Unique Item ID
        self.data: Any = data        # Item metadata dictionary
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None
```

### 3. Algorithmic Operations and Asymptotic Complexities

#### A. Search Operation with Path Tracing
Traversing the tree compares target key $k_t$ against the current node $k_c$. If $k_t < k_c$, navigation proceeds to the left child; if $k_t > k_c$, it proceeds to the right child. The visited keys are appended to an execution path list:

$$\text{Recurrence Relation:} \quad T(n) = T(n/2) + O(1) \implies O(\log n) \text{ Average Case}$$

#### B. In-Order Traversal ($L \to \text{Root} \to R$)
Recursively visiting the left subtree, processing the root, and visiting the right subtree guarantees sorted numerical order:
$$\text{Output Sequence:} \quad \langle k_1, k_2, k_3, \dots, k_n \rangle \quad \text{where } k_i < k_{i+1}$$
$$\text{Time Complexity:} \quad O(n), \quad \text{Space Complexity:} \quad O(h) \text{ call-stack auxiliary}$$

#### C. Three-Case Node Deletion Algorithm
1. **Case 1: Leaf Node (0 Children):** The pointer from the parent is set to `None`.
2. **Case 2: Single Child (1 Child):** The parent's pointer is updated to point directly to the child node, bypassing the deleted node.
3. **Case 3: Two Children (2 Children):** The node's in-order successor (the smallest key in the right subtree: $\min(\text{node.right})$) is identified. The target's key and data are overwritten with the successor's attributes, and the successor node is recursively pruned from the right subtree.

<div style="page-break-after: always;"></div>

---

<p align="center">
  <img src="images/sit_header.png" alt="Symbiosis Institute of Technology, Hyderabad" width="100%" />
</p>

# MULTI-FACTOR HEURISTIC MATCHING ENGINE & STATE TRANSITIONS

### 1. Multi-Criteria Scoring Formulation
To automate candidate discovery without human inspection, CampusFind implements an explainable multi-factor scoring function $S(L, F) \in [0, 100]$:

$$S(L, F) = w_c \cdot C(L, F) + w_t \cdot T(L, F) + w_l \cdot L(L, F) + w_d \cdot D(L, F)$$

Where the empirical component weights satisfy $\sum w_i = 100$:
- **Category Compatibility ($w_c = 30\%$):** 
  $$C(L, F) = \begin{cases} 30.0 & \text{if } \text{category}(L) = \text{category}(F) \\ 0.0 & \text{if mismatch} \\ 10.0 & \text{if either unspecified} \end{cases}$$
- **Textual Jaccard Similarity ($w_t = 35\%$):** Tokenizes normalized title and description strings, removes linguistic stop-words, and calculates set intersection over union boosted by title overlap:
  $$J(T_L, T_F) = \frac{|T_L \cap T_F|}{|T_L \cup T_F|}, \quad T(L, F) = \min(35.0, 25 \cdot J + 5 \cdot |\text{Title}\cap| + 1.5 \cdot |\text{Overlap}|)$$
- **Spatial Landmark Proximity ($w_l = 20\%$):** 
  $$L(L, F) = \begin{cases} 20.0 & \text{if exact campus location match} \\ 15.0 & \text{if shared campus zone landmark} \\ 10.0 & \text{if partial string match} \\ 3.0 & \text{if distinct campus zones} \end{cases}$$
- **Chronological Sequence Plausibility ($w_d = 15\%$):** Evaluates elapsed delta $\Delta t = t_{\text{found}} - t_{\text{lost}}$. If an item is found on or shortly after its reported lost date, high scores are assigned. If $\Delta t < -1$ (reported found before being lost), a score of $0$ is enforced.

### 2. Candidate Match Score Matrix (Illustrative Example)

| Lost Item $\downarrow$ \ Found Item $\rightarrow$ | #2: HP Pavilion Laptop | #4: Blue Milton Bottle | #8: Hostel Room Keys | Match Tier |
| :--- | :---: | :---: | :---: | :---: |
| **#1: Dell Inspiron Laptop** | **84.5%** *(High)* | 12.0% *(Mismatch)* | 18.2% *(Mismatch)* | **Candidate Match** |
| **#3: HydroFlask Bottle** | 8.5% *(Mismatch)* | **79.2%** *(High)* | 14.1% *(Mismatch)* | **Candidate Match** |
| **#7: Metal Key Ring** | 6.0% *(Mismatch)* | 11.4% *(Mismatch)* | **91.0%** *(High)* | **Candidate Match** |

### 3. Lifecycle State Transition Dynamics
Analogous to a finite stochastic state process, every item report transitions through defined verification states:

```
                  ┌──────────────────┐
                  │ Reported Active  │
                  └────────┬─────────┘
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
    ┌─────────────────┐         ┌─────────────────┐
    │ Plausible Match │         │ No Direct Match │
    └────────┬────────┘         └────────┬────────┘
             │                           │
             └─────────────┬─────────────┘
                           ▼
                  ┌──────────────────┐
                  │   Claim Filed    │
                  └────────┬─────────┘
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
    ┌─────────────────┐         ┌─────────────────┐
    │ Claim Rejected  │         │ Claim Approved  │
    └─────────────────┘         └────────┬────────┘
                                         ▼
                                ┌─────────────────┐
                                │ Case Resolved   │
                                │ (Pruned/Arch.)  │
                                └─────────────────┘
```

<div style="page-break-after: always;"></div>

---

<p align="center">
  <img src="images/sit_header.png" alt="Symbiosis Institute of Technology, Hyderabad" width="100%" />
</p>

# COMPARATIVE ANALYSIS: IN-MEMORY BST VS. RELATIONAL B-TREE INDEXING

A central technical theme of CampusFind is the deliberate coexistence of an in-memory Binary Search Tree alongside persistent database storage:

| Evaluation Dimension | In-Memory Binary Search Tree (`app/dsa/bst.py`) | Relational Database B-Tree Index (MySQL / SQLite) |
| :--- | :--- | :--- |
| **Primary Purpose** | Real-time session lookups, algorithmic path inspection, pedagogical visualization. | Durable ACID record persistence, transaction isolation, fault tolerance. |
| **Storage Medium** | Volatile Random-Access Memory (RAM). | Non-volatile block storage (NVMe / SSD / HDD). |
| **Node Fan-Out** | Binary branching factor ($m = 2$ children per node). | High branching factor ($m \approx 100 - 1000$ keys per block/page). |
| **Average Search Complexity** | $O(\log_2 n)$ comparisons. | $O(\log_B n)$ disk page I/O reads. |
| **Worst-Case Search Time** | $O(n)$ if degenerate (unbalanced insertion order). | $O(\log_B n)$ guaranteed via auto-balancing split/merge rules. |
| **Traversal Efficiency** | $O(n)$ in-order pointer traversal in memory ($< 1 \text{ ms}$). | Requires index scan and row retrieval across buffer pool. |
| **Inspection & Transparency**| Full step-by-step path array logging (`path = [root, ..., target]`). | Internal B-Tree page traversal is opaque to web application code. |
| **Concurrent Modifiability**| Fast pointer updates; requires application thread synchronization. | Engine handles row/page-level locking, MVCC, and write-ahead logging (WAL). |

### Justification of Coexistence
In production environments, relational databases efficiently manage gigabytes of data with transactional integrity. However, relational engines treat indexing as an opaque black box. In CampusFind:
1. **The Database** guarantees that reported items survive server crashes and power loss.
2. **The In-Memory BST** serves as an active algorithmic cache that provides sub-millisecond key lookups and surfaces exact traversal paths (`path: [15, 8, 12]`) to the user interface, demonstrating real-world data structures in action.

<div style="page-break-after: always;"></div>

---

<p align="center">
  <img src="images/sit_header.png" alt="Symbiosis Institute of Technology, Hyderabad" width="100%" />
</p>

# APPLICATIONS AND FUTURE SCOPE

### Real-World Applications

1. **Higher Education & University Campuses:**
   - Centralizes lost-and-found management across academic departments, student hostels, central libraries, cafeterias, and campus security posts into a unified digital register.
2. **Public Transit & Metro Hubs:**
   - Streamlines misplaced commuter property reconciliation across bus terminals, metro stations, and railway baggage counters.
3. **Airport Terminals & Aviation Logistics:**
   - Accelerates luggage, electronics, and travel document recovery at security checkpoints and boarding gates.
4. **Conference Conventions & Sports Stadiums:**
   - Manages short-term lost property spikes during major athletic meets, symposia, and cultural festivals.
5. **Academic & Pedagogical Demonstration:**
   - Functions as an interactive laboratory learning tool for Computer Science students studying tree data structures, recursion, and similarity heuristics.

### Future Scope

- **Multimodal Deep Learning & Computer Vision:**
  - Incorporate vision transformer models (e.g., OpenAI CLIP) to generate vector embeddings of uploaded photographs, enabling image-to-image similarity matching independent of user text descriptions.
- **Automated Optical Character Recognition (OCR):**
  - Implement automated text extraction for identity cards, driving licenses, and wallets to instantly cross-reference university matriculation databases.
- **Self-Balancing Tree Upgrades (AVL / Red-Black Trees):**
  - Enhance the in-memory tree implementation with balance-factor rotations, guaranteeing an $O(\log n)$ worst-case upper bound against adversarial insertion sequences.
- **Geofenced BLE Beacon & Indoor Mapping:**
  - Integrate Bluetooth Low Energy (BLE) beacons and campus GPS coordinates to automatically suggest candidate matches based on physical proximity radius.
- **Mobile Push & Automated SMS Alerts:**
  - Integrate SMS gateways and native mobile push notifications to alert students the moment a high-confidence match ($\ge 75\%$) is registered.

<div style="page-break-after: always;"></div>

---

<p align="center">
  <img src="images/sit_header.png" alt="Symbiosis Institute of Technology, Hyderabad" width="100%" />
</p>

# SYSTEM PROTOTYPE WALKTHROUGH — PART I

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 🔍 CampusFind                       Catalog   Smart Matches   BST Visualizer│
├─────────────────────────────────────────────────────────────────────────────┤
│                           BST VISUALIZER & DSA ENGINE                       │
│                                                                             │
│  [ Input Key: [ 14 ] ]  [ + Insert Node ]  [ 🔍 Search Key ]  [ 🗑 Delete ] │
│                                                                             │
│                                ( 10 )                                       │
│                                /    \                                       │
│                               /      \                                      │
│                            ( 5 )    ( 15 )                                  │
│                            /   \     /   \                                  │
│                          ( 2 ) ( 8 )( 12 )( 18 )                            │
│                                       \                                     │
│                                       ( 14 ) <── (Searched Node Found!)     │
│                                                                             │
│  Traversals:                                                                │
│  In-Order Traversal:   [ 2, 5, 8, 10, 12, 14, 15, 18 ] (Sorted Order)       │
│  Search Execution Path: Root(10) ──► Right(15) ──► Left(12) ──► Right(14)   │
└─────────────────────────────────────────────────────────────────────────────┘
```
*(Figure 1: Interactive In-Memory Binary Search Tree Visualizer showing dynamic SVG node rendering)*

*(this is a basic prototype of the website)*

*(it involves a series of item nodes indexed in logarithmic hierarchy)*

*(tree operations like insertion, search, and deletion execute in $O(\log n)$ average time)*

<br>

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ ⚡ Algorithmic Execution Path Trace                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  Target Search Key: 14                                                      │
│  Status: KEY FOUND IN TREE                                                  │
│                                                                             │
│  Step 1: Evaluate Root Node (Key = 10)                                      │
│          Condition: Target (14) > Current (10) ──► Traverse Right Subtree   │
│  Step 2: Evaluate Node (Key = 15)                                           │
│          Condition: Target (14) < Current (15) ──► Traverse Left Subtree    │
│  Step 3: Evaluate Node (Key = 12)                                           │
│          Condition: Target (14) > Current (12) ──► Traverse Right Subtree   │
│  Step 4: Evaluate Node (Key = 14)                                           │
│          Condition: Target (14) == Current (14) ──► Target Located!        │
│                                                                             │
│  Total Comparisons: 4 | Tree Height: 4 | Traversal Time: 0.04 ms            │
└─────────────────────────────────────────────────────────────────────────────┘
```
*(Figure 2: Execution path trace output displaying search progression from root to target)*

*(this is the step-by-step comparison trace logging each branch decision)*

*(the educational trace visually reinforces algorithmic tree traversal concepts)*

<div style="page-break-after: always;"></div>

---

<p align="center">
  <img src="images/sit_header.png" alt="Symbiosis Institute of Technology, Hyderabad" width="100%" />
</p>

# SYSTEM PROTOTYPE WALKTHROUGH — PART II

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 🎯 SMART MATCHING ENGINE & SIMILARITY ANALYSIS                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Lost Report:  Dell Inspiron 15 (Silver, Core i7, Asset Tag #8821)          │
│  Found Report: Dell Laptop in Black Sleeve (Found at Central Library)       │
│                                                                             │
│  OVERALL MATCH CONFIDENCE: 84.5%  [ HIGH CONFIDENCE TIER ]                  │
│  =========================================================================  │
│                                                                             │
│  Factor Breakdown:                                                          │
│  • Category Compatibility (Weight: 30%): Earned: 30.0 / 30.0                │
│    └─ Reason: Exact match on category [Electronics]                         │
│                                                                             │
│  • Textual Jaccard Similarity (Weight: 35%): Earned: 24.5 / 35.0            │
│    └─ Reason: Shared informative keywords ['dell', 'laptop', 'inspiron']    │
│                                                                             │
│  • Spatial Proximity (Weight: 20%): Earned: 15.0 / 20.0                     │
│    └─ Reason: Shared campus landmark ['library', 'reading hall']            │
│                                                                             │
│  • Chronological Validity (Weight: 15%): Earned: 15.0 / 15.0                │
│    └─ Reason: Found report logged within 24 hours of reported loss          │
└─────────────────────────────────────────────────────────────────────────────┘
```
*(Figure 3: Heuristic Multi-Factor Matching Analysis Interface)*

*(this is the transparent scoring breakdown displaying weighted factor contributions)*

*(candidates exceeding the 75% threshold are tagged as High Confidence matches)*

<br>

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 📢 REPORT MISPLACED ITEM                                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  Item Title:        [ Blue HydroFlask Steel Bottle                        ] │
│  Item Category:     [ Personal Accessories & Bottles                    ▼ ] │
│  Campus Location:   [ Central Library Reading Room, 2nd Floor           ▼ ] │
│  Date Misplaced:    [ 2026-10-24                                          ] │
│  Description:       [ Blue 750ml vacuum insulated bottle with SIT sticker ] │
│                                                                             │
│  🔒 Anti-Fraud Ownership Verification Challenge:                            │
│  Secret Hint Question: [ What specific sticker is placed on the bottom?   ] │
│  Correct Answer:       [ [ Confidential - Stored Hashed in Database ]     ] │
│                                                                             │
│  [ Submit Item Report ]                                                     │
└─────────────────────────────────────────────────────────────────────────────┘
```
*(Figure 4: Secure Item Reporting Portal with Ownership Challenge Question)*

*(this is where students register lost items with private ownership verification hints)*

*(the secret verification answer ensures only the true owner can claim discovered property)*

<div style="page-break-after: always;"></div>

---

<p align="center">
  <img src="images/sit_header.png" alt="Symbiosis Institute of Technology, Hyderabad" width="100%" />
</p>

# SYSTEM PROTOTYPE WALKTHROUGH — PART III

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 🔍 CAMPUSFIND REPOSITORY CATALOG                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│  Search: [ Search by keywords...        ] Category: [ All Categories    ▼ ] │
│  Type:   [ All (Lost & Found)         ▼ ] Location: [ All Campus Zones  ▼ ] │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────┐  ┌──────────────────────┐  ┌────────────────────┐ │
│  │ [Found] Oct 24, 2026 │  │ [Lost] Oct 23, 2026  │  │ [Found] Oct 24     │ │
│  │ Calculator Casio fx  │  │ Lenovo ThinkPad X1   │  │ Set of 3 Brass Keys│ │
│  │ 📍 Main Auditorium   │  │ 📍 Mech Lab Room 204 │  │ 📍 Hostel Block A  │ │
│  │ Status: Available    │  │ Status: Active Lost  │  │ Status: Available  │ │
│  │ [ Claim Item -> ]    │  │ [ View Matches -> ]  │  │ [ Claim Item -> ]  │ │
│  └──────────────────────┘  └──────────────────────┘  └────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```
*(Figure 5: Centralized Campus Repository Catalog with Multi-Parameter Filters)*

*(here is where all active lost and found items are cataloged with status badges)*

*(users can filter records dynamically by campus zone, category, and report status)*

<br>

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 🛡️ ADMINISTRATIVE ADJUDICATION & AUDIT LOG PANEL                           │
├─────────────────────────────────────────────────────────────────────────────┤
│  Total Items: 10  │  Active Lost: 5  │  Active Found: 5  │  Resolved: 0     │
├─────────────────────────────────────────────────────────────────────────────┤
│  PENDING CLAIMS AWAITING VERIFICATION:                                      │
│  Claim ID: #104 | Item: Casio fx-991CW Calculator                           │
│  Claimant: Priya Sharma (PRN: 21BCE2045) | Submitted: 2 hours ago          │
│  Owner Challenge Question: "What is written on the back battery cover?"      │
│  Claimant Answer Provided: "Priya S. - Batch 2024"                          │
│                                                                             │
│  Action: [  Approve & Issue Claim  ]     [ ❌ Reject Fraudulent Claim ]     │
├─────────────────────────────────────────────────────────────────────────────┤
│  IMMUTABLE AUDIT TRAIL:                                                     │
│  [2026-10-24 14:15] Admin approved claim #102 for item #6 (Owner: Alex J.)  │
│  [2026-10-24 11:30] Security Officer logged turned-in Found item #10        │
└─────────────────────────────────────────────────────────────────────────────┘
```
*(Figure 6: Administrative Control Center and Audit Trail Panel)*

*(this is where authorized campus administrators evaluate submitted ownership claims)*

*(approving a claim automatically updates the item status and records an immutable log)*

---

### **End of Project Report**
*(Total Pages: 12 of 12)*
