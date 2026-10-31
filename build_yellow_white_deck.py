"""
CampusFind - White & Yellow Professional Deck Generator
======================================================
Strictly modeled after the user's sample presentation style:
- Crisp White background
- Warm Yellow & Golden Amber cards/accents (#FFFBEB, #FEF3C7, #F59E0B, #B45309)
- Deep Navy blue headers & titles (#1E3A8A, #0F172A)
- Exactly 7 slides:
  Slide 1: Project Name, Core Algorithm Banner, Student Details
  Slide 2: Problem Statement & Project Objectives
  Slide 3: Algorithm Selection: Why In-Memory BST is the Best Choice
  Slide 4: System Architecture & Implementation
  Slide 5: Algorithm Performance Comparison (Clean Table)
  Slide 6: Key Technical Findings & Viva Highlights
  Slide 7: Thank You! Questions & Discussion
"""

import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_filename="CampusFind_Presentation.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # White & Yellow Academic Theme Colors (Matching Sample)
    C_WHITE = RGBColor(255, 255, 255)
    C_BG_PAGE = RGBColor(255, 255, 255)
    C_YELLOW_LIGHT = RGBColor(254, 249, 195) # #FEF08A / #FEF9C3 soft yellow card
    C_YELLOW_ACCENT = RGBColor(254, 240, 138)# #FEF08A
    C_GOLD = RGBColor(217, 119, 6)           # #D97706 warm amber gold
    C_NAVY_TITLE = RGBColor(30, 58, 138)     # #1E3A8A deep academic blue
    C_NAVY_DARK = RGBColor(15, 23, 42)       # #0F172A deep slate text
    C_TEXT_MUTED = RGBColor(71, 85, 105)     # #475569 muted slate
    C_BORDER_GOLD = RGBColor(245, 158, 11)   # #F59E0B border
    C_BORDER_LIGHT = RGBColor(226, 232, 240) # light divider
    C_BLUE_CARD = RGBColor(239, 246, 255)    # #EFF6FF soft blue card

    def add_page_header(slide, subtitle_tag, title_text):
        # Top Small Tag
        tb_sub = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.35))
        tf_s = tb_sub.text_frame
        p_s = tf_s.paragraphs[0]
        p_s.text = subtitle_tag.upper()
        p_s.font.size = Pt(10)
        p_s.font.bold = True
        p_s.font.color.rgb = C_GOLD

        # Title
        tb_t = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.733), Inches(0.65))
        tf_t = tb_t.text_frame
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = C_NAVY_TITLE

        # Subtle gold divider line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.38), Inches(11.733), Inches(0.025))
        line.fill.solid()
        line.fill.fore_color.rgb = C_GOLD
        line.line.color.rgb = C_GOLD

        # Subtle bottom footer
        tb_f = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.3))
        tf_f = tb_f.text_frame
        p_f = tf_f.paragraphs[0]
        p_f.text = "CampusFind: Smart Lost & Found System  |  Data Structures & Algorithms Lab  |  SIT Hyderabad"
        p_f.font.size = Pt(9)
        p_f.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 1: COVER SLIDE (Strictly matching sample layout)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)

    # Top Left Banner (Yellow Badge like sample "CORE ALGORITHM")
    c_algo = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.5), Inches(3.2), Inches(6.3))
    c_algo.fill.solid()
    c_algo.fill.fore_color.rgb = C_YELLOW_LIGHT
    c_algo.line.color.rgb = C_BORDER_GOLD
    c_algo.line.width = Pt(1.5)
    tf_a = c_algo.text_frame
    tf_a.margin_left = Inches(0.25)
    tf_a.margin_top = Inches(0.3)

    p_ah = tf_a.paragraphs[0]
    p_ah.text = "CORE ALGORITHM"
    p_ah.font.size = Pt(12)
    p_ah.font.bold = True
    p_ah.font.color.rgb = C_GOLD

    p_an = tf_a.add_paragraph()
    p_an.text = "Binary Search Tree"
    p_an.font.size = Pt(16)
    p_an.font.bold = True
    p_an.font.color.rgb = C_NAVY_TITLE

    algo_points = [
        "✔  Time: O(log N) Avg",
        "✔  Space: O(N) in RAM",
        "✔  In-Order: Sorted O(N)",
        "✔  Path: Fully Traced",
        "✔  Deletion: 3-Case Clean",
        "✔  Heuristic Similarity",
        "✔  Deterministic Lookups"
    ]
    for pt in algo_points:
        p_p = tf_a.add_paragraph()
        p_p.text = "\n" + pt
        p_p.font.size = Pt(11)
        p_p.font.bold = True
        p_p.font.color.rgb = C_NAVY_DARK

    # Top Right Main Info Box (White with Gold Border)
    c_main = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.3), Inches(0.5), Inches(8.233), Inches(3.4))
    c_main.fill.solid()
    c_main.fill.fore_color.rgb = C_WHITE
    c_main.line.color.rgb = C_BORDER_GOLD
    c_main.line.width = Pt(1.5)
    tf_m = c_main.text_frame
    tf_m.margin_left = Inches(0.4)
    tf_m.margin_top = Inches(0.3)

    p_lab = tf_m.paragraphs[0]
    p_lab.text = "DATA STRUCTURES - LAB  |  CAPSTONE PROJECT"
    p_lab.font.size = Pt(11)
    p_lab.font.bold = True
    p_lab.font.color.rgb = C_GOLD

    p_mtitle = tf_m.add_paragraph()
    p_mtitle.text = "CampusFind: Smart Lost & Found System"
    p_mtitle.font.size = Pt(25)
    p_mtitle.font.bold = True
    p_mtitle.font.color.rgb = C_NAVY_TITLE

    p_msub = tf_m.add_paragraph()
    p_msub.text = "In-Memory Binary Search Tree Indexing & Multi-Factor Heuristic Matching"
    p_msub.font.size = Pt(13)
    p_msub.font.color.rgb = C_TEXT_MUTED

    p_dept = tf_m.add_paragraph()
    p_dept.text = "\nSymbiosis Institute of Technology (SIT), Hyderabad\nConstituent of Symbiosis International (Deemed University), Pune"
    p_dept.font.size = Pt(11)
    p_dept.font.color.rgb = C_NAVY_DARK

    # Bottom Right Student Details Box (Warm Yellow Background like sample)
    c_stu = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.3), Inches(4.1), Inches(8.233), Inches(2.7))
    c_stu.fill.solid()
    c_stu.fill.fore_color.rgb = C_YELLOW_LIGHT
    c_stu.line.color.rgb = C_BORDER_GOLD
    c_stu.line.width = Pt(1.5)
    tf_s = c_stu.text_frame
    tf_s.margin_left = Inches(0.4)
    tf_s.margin_top = Inches(0.2)

    p_sh = tf_s.paragraphs[0]
    p_sh.text = "STUDENT & PROJECT DETAILS"
    p_sh.font.size = Pt(11)
    p_sh.font.bold = True
    p_sh.font.color.rgb = C_GOLD

    p_s1 = tf_s.add_paragraph()
    p_s1.text = "Student Names: Avignyah Jakku  &  Meghana"
    p_s1.font.size = Pt(13)
    p_s1.font.bold = True
    p_s1.font.color.rgb = C_NAVY_TITLE

    p_s2 = tf_s.add_paragraph()
    p_s2.text = "PRN Numbers: 25070721024 (Avignyah)  |  25070721002 (Meghana)"
    p_s2.font.size = Pt(11.5)
    p_s2.font.bold = True
    p_s2.font.color.rgb = C_NAVY_DARK

    p_s3 = tf_s.add_paragraph()
    p_s3.text = "Course: Data Structures - Lab (B.Tech CSE, 2nd Year)  |  Dept of CSE, SIT-H"
    p_s3.font.size = Pt(10.5)
    p_s3.font.color.rgb = C_TEXT_MUTED

    p_s4 = tf_s.add_paragraph()
    p_s4.text = "Project Mentor: Dr. Rakesh Salakapuri  (Under Directorate of Dr. Rajinikanth Aluvalu)"
    p_s4.font.size = Pt(10.5)
    p_s4.font.bold = True
    p_s4.font.color.rgb = C_GOLD

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT & PROJECT OBJECTIVES
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_page_header(s2, "DSA EXPERIENTIAL LEARNING | CAMPUSFIND", "Problem Statement & Project Objectives")

    # Left: Problem Statement Card
    c_p = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    c_p.fill.solid()
    c_p.fill.fore_color.rgb = C_WHITE
    c_p.line.color.rgb = C_BORDER_GOLD
    c_p.line.width = Pt(1.5)
    tf_p = c_p.text_frame
    tf_p.margin_left = Inches(0.3)
    tf_p.margin_top = Inches(0.25)

    p_ph = tf_p.paragraphs[0]
    p_ph.text = "PROBLEM STATEMENT"
    p_ph.font.size = Pt(13)
    p_ph.font.bold = True
    p_ph.font.color.rgb = C_GOLD

    p_pbody = tf_p.add_paragraph()
    p_pbody.text = "On university campuses, personal belongings (student IDs, calculators, laptops, keys) are frequently misplaced. Current recovery relies on informal manual methods.\n"
    p_pbody.font.size = Pt(11)
    p_pbody.font.color.rgb = C_NAVY_DARK

    p_ch = tf_p.add_paragraph()
    p_ch.text = "Key Challenges in Campus Recovery:"
    p_ch.font.size = Pt(11.5)
    p_ch.font.bold = True
    p_ch.font.color.rgb = C_NAVY_TITLE

    p_ch1 = tf_p.add_paragraph()
    p_ch1.text = "• WhatsApp Spam: Messages buried under 500 chats within hours.\n• False Claim Hazards: Public listings openly expose identifying details, inviting dishonest claims.\n• Slow Paper Registers: Items sit forgotten in security guard drawers across 6 disconnected campus gates.\n• Zero Algorithmic Search: No indexing or automated pairing."
    p_ch1.font.size = Pt(10.5)
    p_ch1.font.color.rgb = C_NAVY_DARK

    # Right: Objectives Card (Warm Yellow)
    c_o = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.2))
    c_o.fill.solid()
    c_o.fill.fore_color.rgb = C_YELLOW_LIGHT
    c_o.line.color.rgb = C_BORDER_GOLD
    c_o.line.width = Pt(1.5)
    tf_o = c_o.text_frame
    tf_o.margin_left = Inches(0.3)
    tf_o.margin_top = Inches(0.25)

    p_oh = tf_o.paragraphs[0]
    p_oh.text = "CORE PROJECT OBJECTIVES"
    p_oh.font.size = Pt(13)
    p_oh.font.bold = True
    p_oh.font.color.rgb = C_GOLD

    objs = [
        ("🎯  CO3 : Algorithm Formulation", "Implement an authentic in-memory Binary Search Tree from scratch in Python with logarithmic insertion, search path logging, and 3-case deletion."),
        ("🎯  CO4 : Performance & Complexity", "Mathematically analyze and empirically demonstrate O(log N) lookup and O(N) in-order traversal versus O(N) linear scanning."),
        ("🎯  CO5 : Practical Full-Stack Demonstration", "Build a complete web application with Flask, multi-factor heuristic matching, anti-fraud secret questions, and an interactive SVG tree visualizer.")
    ]
    for o_title, o_desc in objs:
        p_ot = tf_o.add_paragraph()
        p_ot.text = "\n" + o_title
        p_ot.font.size = Pt(12)
        p_ot.font.bold = True
        p_ot.font.color.rgb = C_NAVY_TITLE
        p_od = tf_o.add_paragraph()
        p_od.text = o_desc
        p_od.font.size = Pt(10.5)
        p_od.font.color.rgb = C_NAVY_DARK

    # =========================================================================
    # SLIDE 3: ALGORITHM SELECTION: WHY BST IS BEST (Matching Sample Slide 3)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_page_header(s3, "DSA EXPERIENTIAL LEARNING | CAMPUSFIND", "Algorithm Selection: Why In-Memory BST is the Best Choice")

    bst_reasons = [
        ("1. SUB-MILLISECOND LOOKUP GUARANTEE", "Logarithmic O(log N) Scaling in RAM", [
            "Binary branching splits search space in half at every comparison step: T(N) = T(N/2) + O(1).",
            "Eliminates disk I/O latency by operating directly in system RAM.",
            "Sub-millisecond retrieval across hundreds of active campus inventory records."
        ]),
        ("2. PEDAGOGICAL WHITE-BOX PATH TRACING", "Real-Time Algorithmic Visibility", [
            "Unlike database B-Trees that act as opaque black boxes, our BST logs exact traversal trajectories.",
            "Visual path array [Root ➔ Right ➔ Left ➔ Target] exposed directly to interactive SVG canvas.",
            "Provides clear white-box academic demonstration during viva examinations."
        ]),
        ("3. ORDERED TRAVERSAL & 3-CASE DELETION", "Deterministic Inventory Management", [
            "In-Order Traversal (Left, Root, Right) generates monotonically sorted item IDs in O(N) linear time.",
            "Handles item recovery through authentic 3-case deletion (leaf, 1-child bypass, 2-child successor).",
            "Memory footprint in RAM is negligible (<2 MB for 10,000 items)."
        ])
    ]

    for idx, (h1, h2, bullets) in enumerate(bst_reasons):
        x = Inches(0.8 + idx * 4.0)
        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.6), Inches(3.733), Inches(5.2))
        card.fill.solid()
        card.fill.fore_color.rgb = C_YELLOW_LIGHT if idx == 0 else C_WHITE
        card.line.color.rgb = C_BORDER_GOLD
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_top = Inches(0.25)

        p = tf.paragraphs[0]
        p.text = h1
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_GOLD

        p_sub = tf.add_paragraph()
        p_sub.text = h2
        p_sub.font.size = Pt(11)
        p_sub.font.bold = True
        p_sub.font.color.rgb = C_NAVY_TITLE

        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.text = "\n• " + b
            p_b.font.size = Pt(10)
            p_b.font.color.rgb = C_NAVY_DARK

    # =========================================================================
    # SLIDE 4: SYSTEM ARCHITECTURE & IMPLEMENTATION
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_page_header(s4, "DSA EXPERIENTIAL LEARNING | CAMPUSFIND", "System Architecture & Implementation")

    # Left: Architecture components
    c_arch = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2))
    c_arch.fill.solid()
    c_arch.fill.fore_color.rgb = C_WHITE
    c_arch.line.color.rgb = C_BORDER_GOLD
    c_arch.line.width = Pt(1.5)
    tf_ar = c_arch.text_frame
    tf_ar.margin_left = Inches(0.3)
    tf_ar.margin_top = Inches(0.25)

    p = tf_ar.paragraphs[0]
    p.text = "MODULAR SYSTEM ARCHITECTURE"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_GOLD

    modules = [
        ("⚡ Core DSA Engine (app/dsa/bst.py)", "Pure Python Binary Search Tree with BSTNode class, logarithmic insertion, search path tracking, and in-order traversals."),
        ("⚡ Multi-Criteria Matching (app/matching.py)", "Heuristic engine calculating weighted similarity: Category (30%), Keyword Overlap (35%), Landmark (20%), and Date (15%)."),
        ("⚡ Anti-Fraud Security Gate (app/claims.py)", "Private verification hint questions set by owner; claimant must answer correctly before admin authorizes custody release."),
        ("⚡ Dual Persistence Engine (app/db.py)", "Production MySQL 8.0 support with automatic zero-config SQLite fallback ensuring 100% offline reliability.")
    ]
    for m_title, m_desc in modules:
        p_mt = tf_ar.add_paragraph()
        p_mt.text = "\n" + m_title
        p_mt.font.size = Pt(11.5)
        p_mt.font.bold = True
        p_mt.font.color.rgb = C_NAVY_TITLE
        p_md = tf_ar.add_paragraph()
        p_md.text = m_desc
        p_md.font.size = Pt(10)
        p_md.font.color.rgb = C_NAVY_DARK

    # Right: Workflow Visual Card (Warm Yellow)
    c_flow = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.2))
    c_flow.fill.solid()
    c_flow.fill.fore_color.rgb = C_YELLOW_LIGHT
    c_flow.line.color.rgb = C_BORDER_GOLD
    c_flow.line.width = Pt(1.5)
    tf_fl = c_flow.text_frame
    tf_fl.margin_left = Inches(0.3)
    tf_fl.margin_top = Inches(0.25)

    p_fh = tf_fl.paragraphs[0]
    p_fh.text = "END-TO-END RECOVERY WORKFLOW"
    p_fh.font.size = Pt(13)
    p_fh.font.bold = True
    p_fh.font.color.rgb = C_GOLD

    wflows = [
        ("1️⃣ Item Registration", "User reports lost/found item with photo, location, and secret challenge question."),
        ("2️⃣ In-Memory BST Indexing", "Item record is saved to DB and numerical ID is inserted into RAM BST in O(log N)."),
        ("3️⃣ Heuristic Correlation", "Engine evaluates candidate pairings. Scores >= 75% trigger High-Confidence match alerts."),
        ("4️⃣ Claimant Verification", "Claimant answers secret owner question; Admin compares answer and approves handover."),
        ("5️⃣ Node Deletion & Resolution", "Claimed item transitions to 'Resolved' and node is pruned from BST.")
    ]
    for w_h, w_d in wflows:
        p_wh = tf_fl.add_paragraph()
        p_wh.text = "\n" + w_h
        p_wh.font.size = Pt(11.5)
        p_wh.font.bold = True
        p_wh.font.color.rgb = C_NAVY_TITLE
        p_wd = tf_fl.add_paragraph()
        p_wd.text = w_d
        p_wd.font.size = Pt(10)
        p_wd.font.color.rgb = C_NAVY_DARK

    # =========================================================================
    # SLIDE 5: ALGORITHM COMPARISON & BENCHMARK TABLE (Matching Sample Slide 5)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_page_header(s5, "DSA EXPERIENTIAL LEARNING | CAMPUSFIND", "Algorithm Performance Comparison (In-Memory BST vs Others)")

    # Benchmark Table
    t_shape = s5.shapes.add_table(6, 5, Inches(0.8), Inches(1.6), Inches(11.733), Inches(3.6))
    table = t_shape.table
    table.columns[0].width = Inches(2.7)
    table.columns[1].width = Inches(2.2)
    table.columns[2].width = Inches(2.2)
    table.columns[3].width = Inches(2.2)
    table.columns[4].width = Inches(2.433)

    t_headers = ["Algorithm / Structure", "Search Time", "Insert Time", "Ordered Traversal", "Path Traceability"]
    for col_idx, h_text in enumerate(t_headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY_TITLE
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = C_WHITE

    t_rows = [
        ["In-Memory BST [BEST CHOICE]", "O(log N) Avg", "O(log N) Avg", "O(N) In-Order", "100% Transparent"],
        ["Linear Array / List", "O(N) Scan", "O(1) Append", "O(N log N) Sort", "None (Opaque)"],
        ["Hash Table (Dict)", "O(1) Average", "O(1) Average", "O(N log N) Sort", "None (No Order)"],
        ["Database B-Tree Index", "O(log_B N) Disk I/O", "O(log_B N) Disk", "O(N) Index Scan", "Opaque Engine Internal"],
        ["AVL / Red-Black Tree", "O(log N) Strict", "O(log N) + Rotate", "O(N) In-Order", "Complex Rotations"]
    ]

    for row_idx, r_data in enumerate(t_rows):
        is_best = (row_idx == 0)
        is_alt = (row_idx % 2 == 1)
        for col_idx, text in enumerate(r_data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_YELLOW_LIGHT if is_best else (C_YELLOW_ACCENT if is_alt else C_WHITE)
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(10.5)
            p.font.color.rgb = C_GOLD if is_best and col_idx == 0 else C_NAVY_DARK
            if is_best or col_idx == 1:
                p.font.bold = True

    # Bottom Takeaway Card (Warm Yellow like sample)
    c_take = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.4), Inches(11.733), Inches(1.4))
    c_take.fill.solid()
    c_take.fill.fore_color.rgb = C_YELLOW_LIGHT
    c_take.line.color.rgb = C_BORDER_GOLD
    c_take.line.width = Pt(1.5)
    tf_tk = c_take.text_frame
    tf_tk.margin_left = Inches(0.3)
    tf_tk.margin_top = Inches(0.15)

    p_tkh = tf_tk.paragraphs[0]
    p_tkh.text = "Key Takeaway: Dual-Engine Synergy"
    p_tkh.font.size = Pt(12)
    p_tkh.font.bold = True
    p_tkh.font.color.rgb = C_GOLD

    p_tkb = tf_tk.add_paragraph()
    p_tkb.text = "Relational databases provide permanent ACID disk persistence, but treat indexing as an opaque black box. In CampusFind, the in-memory BST operates in RAM to give instant O(log N) search and exposes the complete step-by-step traversal path [Root ➔ Right ➔ Left ➔ Target] to the live visualizer."
    p_tkb.font.size = Pt(10.5)
    p_tkb.font.color.rgb = C_NAVY_DARK

    # =========================================================================
    # SLIDE 6: KEY TECHNICAL FINDINGS & VIVA HIGHLIGHTS
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_page_header(s6, "DSA EXPERIENTIAL LEARNING | CAMPUSFIND", "Key Technical Findings & Viva Highlights")

    findings = [
        ("💡  O(log N) SEARCH SPEED VALIDATION", [
            "Empirical search latency measured under 0.05 ms in Python RAM.",
            "Average comparisons reduced from N = 1,000 to ~10 tree branch checks.",
            "Visual path logging incurs negligible space overhead (O(h) array)."
        ]),
        ("💡  EXPLAINABLE HEURISTIC MATCHING", [
            "Multi-factor scoring formula: Category (30%) + Keywords (35%) + Location (20%) + Date (15%).",
            "Jaccard tokenization reliably detects matching titles ('dell', 'laptop').",
            "Temporal delta penalizes chronologically impossible claims (found before lost)."
        ]),
        ("💡  ANTI-FRAUD VERIFICATION GATE", [
            "Owner sets private challenge question during item creation.",
            "Answers stored securely in database, never shown publicly.",
            "Guarantees that discovered property is returned only to genuine owners."
        ]),
        ("💡  COURSE OUTCOMES ACHIEVED", [
            "CO3: Built authentic Binary Search Tree with 3-case deletion from scratch.",
            "CO4: Derived and verified O(log N) search and O(N) traversal complexities.",
            "CO5: Delivered complete web application with 51/51 automated tests passing."
        ])
    ]

    for idx, (title, points) in enumerate(findings):
        row = idx // 2
        col = idx % 2
        x = Inches(0.8 + col * 6.0)
        y = Inches(1.6 + row * 2.65)

        card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.733), Inches(2.45))
        card.fill.solid()
        card.fill.fore_color.rgb = C_YELLOW_LIGHT if idx % 2 == 0 else C_WHITE
        card.line.color.rgb = C_BORDER_GOLD
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.margin_left = Inches(0.3)
        tf.margin_top = Inches(0.18)

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_GOLD

        for pt in points:
            p_pt = tf.add_paragraph()
            p_pt.text = "• " + pt
            p_pt.font.size = Pt(10)
            p_pt.font.color.rgb = C_NAVY_DARK

    # =========================================================================
    # SLIDE 7: THANK YOU & DISCUSSION (Matching Sample Closing Slide)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)

    # Large Center Card (White with Gold Border)
    c_ty = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.8), Inches(1.0), Inches(9.733), Inches(5.5))
    c_ty.fill.solid()
    c_ty.fill.fore_color.rgb = C_WHITE
    c_ty.line.color.rgb = C_BORDER_GOLD
    c_ty.line.width = Pt(2)
    tf_ty = c_ty.text_frame
    tf_ty.margin_top = Inches(0.5)

    p1 = tf_ty.paragraphs[0]
    p1.text = "Thank You!"
    p1.font.size = Pt(40)
    p1.font.bold = True
    p1.font.color.rgb = C_NAVY_TITLE
    p1.alignment = PP_ALIGN.CENTER

    p2 = tf_ty.add_paragraph()
    p2.text = "Questions & Discussion"
    p2.font.size = Pt(20)
    p2.font.bold = True
    p2.font.color.rgb = C_GOLD
    p2.alignment = PP_ALIGN.CENTER

    p_div = tf_ty.add_paragraph()
    p_div.text = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    p_div.font.size = Pt(12)
    p_div.font.color.rgb = C_BORDER_GOLD
    p_div.alignment = PP_ALIGN.CENTER

    p3 = tf_ty.add_paragraph()
    p3.text = "\nAvignyah Jakku  (PRN: 25070721024)\nMeghana  (PRN: 25070721002)"
    p3.font.size = Pt(14)
    p3.font.bold = True
    p3.font.color.rgb = C_NAVY_DARK
    p3.alignment = PP_ALIGN.CENTER

    p4 = tf_ty.add_paragraph()
    p4.text = "\nB.Tech Computer Science and Engineering  |  2nd Year"
    p4.font.size = Pt(12)
    p4.font.color.rgb = C_TEXT_MUTED
    p4.alignment = PP_ALIGN.CENTER

    p5 = tf_ty.add_paragraph()
    p5.text = "Symbiosis Institute of Technology (SIT), Hyderabad"
    p5.font.size = Pt(12)
    p5.font.bold = True
    p5.font.color.rgb = C_NAVY_TITLE
    p5.alignment = PP_ALIGN.CENTER

    p6 = tf_ty.add_paragraph()
    p6.text = "\nGitHub Repository: https://github.com/avignyahjakku-dot/Smart-Lost-Found-System.git"
    p6.font.size = Pt(11)
    p6.font.bold = True
    p6.font.color.rgb = C_GOLD
    p6.alignment = PP_ALIGN.CENTER

    # Save to both target filenames to avoid open file locks
    try:
        prs.save(output_filename)
        print(f"Deck saved to: {output_filename}")
    except PermissionError:
        alt_filename = "CampusFind_White_Yellow.pptx"
        prs.save(alt_filename)
        print(f"Target locked, saved to alternate: {alt_filename}")

if __name__ == '__main__':
    create_deck()
