# 🔍 CampusFind — Classroom Presentation Deck
### Smart University Lost & Found System
**Course:** Data Structures - Lab (BTech CSE Capstone)  
**Institution:** Symbiosis Institute of Technology (SIT), Hyderabad  
**Presenters:**  
- **Avignyah Jakku** (PRN: 25070721024)  
- **Meghana** (PRN: 25070721002)  
**Project Guide:** Dr. Rakesh Salakapuri  

👉 **PowerPoint File:** [`CampusFind_Presentation.pptx`](file:///c:/Users/6tan5/OneDrive/Desktop/smart%20lost%20&%20found%20system/CampusFind_Presentation.pptx)  

---

## Slide 1: Hero Title Slide
- **Title:** 🔍 CampusFind
- **Subtitle:** Smart University Lost & Found System
- **Tagline:** Reuniting Campuses with In-Memory Binary Search Trees & Heuristic Matching
- **Presented by:** Avignyah Jakku & Meghana (SIT Hyderabad)
- **Guided by:** Dr. Rakesh Salakapuri

> **🗣️ What to say:**  
> *"Good morning everyone! Today Meghana and I are presenting CampusFind — a smart lost and found system that takes everything broken about campus lost-and-found and fixes it using real Data Structures & Algorithms."*

---

## Slide 2: The Real Problem: Losing Things on Campus Sucks
- 📱 **The WhatsApp Spam Chaos:** Lost item messages get buried under 500 unread group chats within 2 hours. Zero filters, zero searchability.
- 🕵️‍♂️ **The Fake Claim Hazard:** Public broadcasts reveal every sticker, color, and scratch. Anyone can pretend it's theirs and steal it without proof.
- 📁 **The Dusty Paper Register:** Found items sit in forgotten security guard drawers for an entire semester because students have no idea which gate has them.

> **🗣️ What to say:**  
> *"We’ve all been there: you leave your calculator in the lab or your water bottle in the library. What happens? Someone posts on a WhatsApp group, and it gets buried in minutes. Or worse, someone sees your exact laptop model posted publicly and claims it falsely. CampusFind was built to eliminate this chaos."*

---

## Slide 3: Enter CampusFind (The Solution)
- ⚡ **1. Lightning Fast DSA Search:** In-memory Binary Search Tree (BST) stores item keys in RAM for $O(\log n)$ sub-millisecond retrieval.
- 🔒 **2. Anti-Theft Verification:** The owner sets a secret challenge question when reporting; claimants must answer it correctly before custody handover.
- 🧠 **3. Smart Matching Algorithm:** Automatically correlates lost and found reports using multi-factor heuristics (Category, Keywords, Location, Date).

---

## Slide 4: The Showdown: Old School vs. CampusFind (Table 1)

| Dimension | Traditional Way ❌ | CampusFind Way 🚀 |
| :--- | :--- | :--- |
| **Where to search?** | 10 WhatsApp groups + 6 security desks | **1 Centralized Searchable Web App** |
| **How items match?** | Students scrolling endlessly for days | **Algorithm pairs them in 0.01 seconds** |
| **Fraud prevention?** | None. First person to claim gets it | **2-Factor Secret Challenge Question** |
| **Search Speed & DSA?** | $O(n)$ slow linear paper scanning | **$O(\log n)$ In-Memory Binary Search Tree** |
| **Custody Tracking?** | Items rot forgotten in drawer boxes | **Tracked holding desk (Library, Gate 1)** |

> **🗣️ What to say:**  
> *"This table summarizes the big leap we’re making: from slow, insecure, paper-based scanning to a logarithmic, authenticated, and algorithmic platform."*

---

## Slide 5: The 4-Step Recovery Journey
1. 1️⃣ **Log Item:** Report lost or found with title, photo, campus zone, and set a secret hint.
2. 2️⃣ **BST Insert:** Item ID is instantly indexed into the in-memory Binary Search Tree in $O(\log n)$ time.
3. 3️⃣ **Auto-Match:** Heuristic engine calculates match score (>75% = High Confidence).
4. 4️⃣ **Claim & Verify:** Claimant answers the secret hint; Admin verifies and approves physical handover.

---

## Slide 6: The DSA Brain: Pure Python Binary Search Tree
- **Why an In-Memory BST?**
  - ⚡ **$O(\log n)$ Search Speed:** Cuts the search space in half at each step.
  - 🗺️ **Real-Time Path Tracing:** Exposes the exact traversal trajectory: `[Root ➔ Right ➔ Left ➔ Found!]`.
  - 🔄 **In-Order Traversal:** Visiting Left-Root-Right gives sorted item keys in $O(n)$ time.
  - ✂️ **3-Case Node Deletion:** Removes claimed items cleanly (leaf, 1 child, or 2 children with in-order successor).
- **The BST Invariant:**
  $$\forall N: \text{Keys}(\text{LeftSubtree}) < \text{Key}(N) < \text{Keys}(\text{RightSubtree})$$
- **Dual Engine Architecture:** MySQL / SQLite saves permanently to disk; BST caches in RAM for instant visual search.

---

## Slide 7: How It Thinks: Multi-Factor Heuristic Match (Table 2)

$$\mathbf{\text{Match Score} = 30\% \text{ Category} + 35\% \text{ Keywords} + 20\% \text{ Location} + 15\% \text{ Date}}$$

| Dimension | Weight | How It Calculates |
| :--- | :---: | :--- |
| 🏷️ **Category Match** | **30%** | Exact category equality: 30 pts for exact match, 0 for mismatch (e.g. Electronics vs Bottle). |
| 📝 **Keyword Overlap** | **35%** | Jaccard similarity on tokens after stripping stop words ('dell', 'laptop', 'silver') + title boost. |
| 📍 **Campus Location** | **20%** | Proximity scoring: 20 pts for exact landmark (e.g. Central Library), 15 pts for shared zone. |
| ⏱️ **Date Causality** | **15%** | Chronological plausibility: 15 pts if found same day; 0 pts if item found before reported lost! |

> **🗣️ What to say:**  
> *"Our algorithm isn't a black box. It evaluates four real-world dimensions. Notice the date causality: if someone claims they lost an item on Friday, but the item was turned in on Tuesday, the algorithm detects that chronological impossibility!"*

---

## Slide 8: What You'll See in the Live Demo
- 🌳 **1. BST Visualizer (`/dsa/visualizer`):** Watch nodes animate on the canvas; enter an item ID and watch the green laser trace the search path step-by-step!
- 🎯 **2. Smart Matches Hub (`/matches`):** Real candidate pairings showing 84.5% match scores and transparent factor breakdowns.
- 🔒 **3. Anti-Theft Secret Hint:** File a lost report with a secret question; see how the public can't see the answer, but the claimant must answer it!
- 🛡️ **4. Admin Control Center (`/admin`):** Review pending claims, inspect claimant answers, and approve custody handover.

---

## Slide 9: Under the Hood: Tech Stack
- 🐍 **Python Flask:** Lightweight WSGI backend with modular blueprint routing.
- 🌳 **Pure-Python BST:** In-memory tree engine with full path tracing & 3-case deletion.
- 🗄️ **MySQL 8.0 & SQLite:** Dual database engine: production MySQL with zero-config SQLite failover.
- 🎨 **Vanilla CSS3 & SVG:** Fast, responsive UI with real-time vector canvas rendering.
- 🔒 **Werkzeug Security:** `scrypt` password hashing, session guards, and CSRF protection.
- 🧪 **51/51 Tests Passing:** 100% automated test coverage across models, routes & BST.

---

## Slide 10: What's Next: CampusFind 2.0 Roadmap
- 👁️ **AI Computer Vision:** Snap a photo of a found bottle; OpenAI CLIP embeddings match items visually even if descriptions differ completely.
- 🪪 **Smart ID Card OCR:** Found a student ID on the grass? Camera extracts PRN/Roll Number and automatically alerts the student directly.
- 📡 **Campus BLE Beacons:** Bluetooth beacons detect when you walk near the specific security desk where your item is held.

---

## Slide 11: Wrap-Up & Live Demo Time!
- 🚀 **Time for the Live Demo!**
- Let's test an item search and see the In-Memory BST in action.
- **Avignyah Jakku** (25070721024) & **Meghana** (25070721002)  
- Department of Computer Science & Engineering | SIT Hyderabad  
- 🔥 **Questions? Fire away!**
