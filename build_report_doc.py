"""
CampusFind - Academic Word Report Generator
===========================================
Generates a 12-page Word (.docx) document matching the exact Symbiosis Institute of Technology
sample report format:
- Official SIT-H header banner image on top of every page
- Exact 12-page structure with clean page breaks
- Double / clean styling
- Formatted tables, headings, and captions in parentheses
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def create_report(output_filename="CampusFind_Project_Report.docx"):
    doc = Document()
    
    # Page Setup (Letter / A4 with standard margins)
    for section in doc.sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.6)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)
        section.header_distance = Inches(0.2)
        section.footer_distance = Inches(0.3)

    # Styles & Fonts
    COLOR_PRIMARY = RGBColor(163, 29, 35)   # Symbiosis Crimson
    COLOR_DARK = RGBColor(20, 20, 20)
    COLOR_MUTED = RGBColor(100, 100, 100)
    
    img_path = os.path.abspath("docs/images/sit_header.png")
    
    def add_page_header(page_num):
        # Insert header image
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(0)
        p_img.paragraph_format.space_after = Pt(12)
        if os.path.exists(img_path):
            p_img.add_run().add_picture(img_path, width=Inches(6.6))
        else:
            p_alt = p_img.add_run("SYMBIOSIS INSTITUTE OF TECHNOLOGY, HYDERABAD\nConstituent of Symbiosis International (Deemed University), Pune")
            p_alt.font.bold = True
            p_alt.font.color.rgb = COLOR_PRIMARY

    def add_page_footer(page_num, total_pages=12):
        p_foot = doc.add_paragraph()
        p_foot.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_foot.paragraph_format.space_before = Pt(18)
        p_foot.paragraph_format.space_after = Pt(0)
        r = p_foot.add_run(f"Page {page_num} of {total_pages}")
        r.font.size = Pt(9)
        r.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    add_page_header(1)
    
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(24)
    
    p_pr = doc.add_paragraph()
    p_pr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_pr = p_pr.add_run("PROJECT REPORT\nON")
    r_pr.font.size = Pt(22)
    r_pr.font.bold = True
    r_pr.font.color.rgb = COLOR_DARK
    p_pr.paragraph_format.space_after = Pt(24)
    
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("“CAMPUSFIND:\nSmart University Lost & Found System Using\nIn-Memory Binary Search Tree (BST) Indexing\nand Multi-Factor Heuristic Matching”")
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_DARK
    p_title.paragraph_format.space_after = Pt(36)
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_sub = p_sub.add_run("Subject: Data Structures - Lab")
    r_sub.font.size = Pt(14)
    r_sub.font.bold = True
    r_sub.font.color.rgb = COLOR_DARK
    p_sub.paragraph_format.space_after = Pt(12)
    
    p_by = doc.add_paragraph()
    p_by.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_by = p_by.add_run("Submitted By:")
    r_by.font.size = Pt(13)
    r_by.font.bold = True
    r_by.font.color.rgb = COLOR_DARK
    p_by.paragraph_format.space_after = Pt(8)
    
    # Table on Cover Page
    t1 = doc.add_table(rows=3, cols=3)
    t1.alignment = WD_TABLE_ALIGNMENT.LEFT
    t1.autofit = False
    
    col_widths = [Inches(2.5), Inches(1.5), Inches(2.2)]
    for row in t1.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width
            
    headers = ["Name", "Branch", "PRN"]
    for i, h in enumerate(headers):
        cell = t1.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(11)
        set_cell_background(cell, "F2F2F2")
        
    data = [
        ("Avignyah Jakku", "CSE", "25070721024"),
        ("Meghana", "CSE", "25070721002")
    ]
    for row_idx, (name, branch, prn) in enumerate(data):
        cell_name = t1.cell(row_idx + 1, 0)
        cell_branch = t1.cell(row_idx + 1, 1)
        cell_prn = t1.cell(row_idx + 1, 2)
        cell_name.text = name
        cell_branch.text = branch
        cell_prn.text = prn
        for c in [cell_name, cell_branch, cell_prn]:
            c.paragraphs[0].runs[0].font.size = Pt(11)

    add_page_footer(1)
    doc.add_page_break()

    # =========================================================================
    # PAGE 2: INDEX
    # =========================================================================
    add_page_header(2)
    
    p_idx_h = doc.add_paragraph()
    p_idx_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_idx = p_idx_h.add_run("INDEX")
    r_idx.font.size = Pt(20)
    r_idx.font.bold = True
    p_idx_h.paragraph_format.space_before = Pt(12)
    p_idx_h.paragraph_format.space_after = Pt(24)
    
    index_items = [
        "1.  Acknowledgement",
        "2.  Abstract and Introduction",
        "3.  Methodology",
        "4.  Binary Search Tree (BST) Architecture & Theoretical Foundations",
        "5.  Multi-Factor Heuristic Matching Engine",
        "6.  Applications and Future Scope",
        "7.  Prototype Walkthrough & User Interface Specifications"
    ]
    
    for item in index_items:
        p_item = doc.add_paragraph()
        r = p_item.add_run(item)
        r.font.size = Pt(13)
        r.font.color.rgb = COLOR_DARK
        p_item.paragraph_format.space_after = Pt(10)
        
    add_page_footer(2)
    doc.add_page_break()

    # =========================================================================
    # PAGE 3: ACKNOWLEDGEMENT
    # =========================================================================
    add_page_header(3)
    
    p_ack_h = doc.add_paragraph()
    p_ack_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_ack = p_ack_h.add_run("ACKNOWLEDGEMENT")
    r_ack.font.size = Pt(18)
    r_ack.font.bold = True
    p_ack_h.paragraph_format.space_after = Pt(18)
    
    ack_paras = [
        "We take this opportunity to express our heartfelt gratitude to everyone who has guided and supported us throughout the completion of our project titled “CAMPUSFIND: Smart University Lost & Found System Using In-Memory Binary Search Tree Indexing and Multi-Factor Heuristic Matching.”",
        "First and foremost, we extend our deepest thanks to Dr. Rakesh Salakapuri, our professor and project guide, for his constant encouragement, valuable guidance, and continuous support. His insightful feedback and in-depth knowledge helped us understand the algorithmic intricacies of tree structures, search path optimizations, and web integration, bringing our concept to life as a fully functional prototype. His mentorship has been a constant source of inspiration throughout this journey.",
        "We would like to express our sincere gratitude to Dr. Rajinikanth Aluvalu, Director of Symbiosis Institute of Technology, Hyderabad, for providing us with the necessary infrastructure, resources, and an environment that encourages innovation, experimentation, and research. His vision for academic excellence has motivated us to pursue this project with dedication and creativity.",
        "Finally, we would like to express our gratitude to our peers and classmates for their helpful suggestions, cooperation, and moral support throughout the project. We are also thankful to Symbiosis Institute of Technology, Hyderabad, for providing us with the platform and resources to transform our ideas into reality."
    ]
    
    for text in ack_paras:
        p = doc.add_paragraph()
        r = p.add_run(text)
        r.font.size = Pt(11)
        p.paragraph_format.line_spacing = 1.2
        p.paragraph_format.space_after = Pt(12)
        
    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(24)
    r_s = p_sig.add_run("Avignyah Jakku (PRN: 25070721024)\nMeghana (PRN: 25070721002)")
    r_s.font.bold = True
    r_s.font.size = Pt(11)
    
    add_page_footer(3)
    doc.add_page_break()

    # =========================================================================
    # PAGE 4: ABSTRACT AND INTRODUCTION
    # =========================================================================
    add_page_header(4)
    
    p_abs_h = doc.add_paragraph()
    p_abs_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_abs = p_abs_h.add_run("ABSTRACT AND INTRODUCTION")
    r_abs.font.size = Pt(18)
    r_abs.font.bold = True
    p_abs_h.paragraph_format.space_after = Pt(16)
    
    intro_paras = [
        "The CampusFind system is an engineered software platform designed to simulate and optimize real-time lost and found item management using applied tree data structures and heuristic modeling. Each reported item is indexed as a node within an authentic in-memory Binary Search Tree (BST), while automated correlations between lost and found items are modeled using a multi-factor similarity scoring function.",
        "This project bridges foundational Data Structures & Algorithms (DSA) with full-stack web engineering, providing an accessible, real-time approach to visualizing how hierarchical tree indexing and logarithmic search paths accelerate item retrieval.",
        "On university campuses, personal belongings—ranging from student identity cards and notebooks to expensive electronics, calculators, and keys—are constantly misplaced. While traditional recovery relies on disorganized manual logs or noisy social media broadcasts, computational models now enable automated, authenticated reconciliation.",
        "CampusFind designs a tree-based catalog of campus items—a system that treats each item report as a structured unit of inventory and correlates them based on heuristic similarity weights. By leveraging Binary Search Trees alongside persistent database storage, the framework achieves sub-millisecond query responses while animating search path traversals in an interactive visualizer.",
        "This approach not only supports pedagogical data structure comprehension but also provides concrete security against false ownership claims through secret owner verification questions."
    ]
    
    for text in intro_paras:
        p = doc.add_paragraph()
        r = p.add_run(text)
        r.font.size = Pt(11)
        p.paragraph_format.line_spacing = 1.25
        p.paragraph_format.space_after = Pt(11)

    add_page_footer(4)
    doc.add_page_break()

    # =========================================================================
    # PAGE 5: METHODOLOGY
    # =========================================================================
    add_page_header(5)
    
    p_met_h = doc.add_paragraph()
    p_met_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_met = p_met_h.add_run("METHODOLOGY")
    r_met.font.size = Pt(18)
    r_met.font.bold = True
    p_met_h.paragraph_format.space_after = Pt(16)
    
    method_steps = [
        ("1. Data Ingestion & Storage:", [
            "Create or import structured records of misplaced items (Title, Category, Landmark, Incident Date, Secret Hint Question).",
            "Store records with ACID transaction safety using a dual-engine database adapter (MySQL & SQLite fallback)."
        ]),
        ("2. Tree Construction:", [
            "Each item record becomes a node in an in-memory Binary Search Tree.",
            "Items are sorted by unique numerical item IDs enforcing the BST property."
        ]),
        ("3. Weighting & Similarity Mechanism:", [
            "Features are extracted from reports: Category, Normalized Keyword Tokens, Campus Landmark, and Date.",
            "Sum of feature weights = 100% (Category 30%, Text Overlap 35%, Location 20%, Chronology 15%)."
        ]),
        ("4. Algorithmic Search & Path Tracking:", [
            "Search operations traverse binary branches comparing target key with current node key in O(log n) average time.",
            "Execution logs store the exact sequence of evaluated nodes [root -> ... -> target]."
        ]),
        ("5. Simulation & Verification:", [
            "Heuristic engine evaluates unrecovered lost items against found inventory.",
            "Scores >= 75% trigger High Confidence pairing; claimants answer secret owner hint to verify ownership."
        ]),
        ("6. Visualization:", [
            "This program has been developed using Python Flask backend frameworks, in-memory Python BST data structures, and client-side vector SVG."
        ])
    ]
    
    for step_title, bullets in method_steps:
        p_st = doc.add_paragraph()
        r_st = p_st.add_run(step_title)
        r_st.font.bold = True
        r_st.font.size = Pt(11.5)
        p_st.paragraph_format.space_before = Pt(6)
        p_st.paragraph_format.space_after = Pt(3)
        for b in bullets:
            p_b = doc.add_paragraph()
            p_b.paragraph_format.left_indent = Inches(0.25)
            p_b.paragraph_format.space_after = Pt(2)
            r_b = p_b.add_run("•  " + b)
            r_b.font.size = Pt(10.5)

    add_page_footer(5)
    doc.add_page_break()

    # =========================================================================
    # PAGE 6: BST THEORETICAL FOUNDATION
    # =========================================================================
    add_page_header(6)
    
    p_bst_h = doc.add_paragraph()
    p_bst_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_bst = p_bst_h.add_run("Binary Search Tree (BST) Architecture &\nTheoretical Foundations")
    r_bst.font.size = Pt(16)
    r_bst.font.bold = True
    p_bst_h.paragraph_format.space_after = Pt(14)
    
    bst_paras = [
        "The Binary Search Tree (BST) is one of the foundational non-linear data structures in Computer Science. It organizes keys hierarchically such that search, insertion, and deletion operations can be performed efficiently without scanning every element sequentially.",
        "A Binary Search Tree strictly enforces the BST Invariant:",
        "• Left Subtree Property:\n   For every node N, every key in LeftSubtree(N) < key(N).\n   → In our model, this routes all smaller item IDs to the left branch.",
        "• Right Subtree Property:\n   For every node N, every key in RightSubtree(N) > key(N).\n   → In our model, this routes all larger item IDs to the right branch.",
        "In-Order Traversal (Left, Root, Right) recursively visits the left subtree, processes the root, and visits the right subtree. Mathematically, this produces a monotonically increasing sorted sequence of item IDs in linear O(n) time.",
        "The Role of In-Memory Indexing and Asymptotics",
        "In traditional database applications, lookups query disk-based B-Trees. By implementing an in-memory BST in Python RAM, CampusFind eliminates disk I/O latency for frequent session inquiries.",
        "When balanced, a BST splits the search space in half at each level, achieving O(log n) search time complexity with recurrence T(n) = T(n/2) + O(1).",
        "→ Computationally, this enables the visualizer to trace and illuminate the exact branch path from the root to the target item in fractions of a millisecond."
    ]
    
    for text in bst_paras:
        p = doc.add_paragraph()
        r = p.add_run(text)
        r.font.size = Pt(11)
        p.paragraph_format.line_spacing = 1.2
        p.paragraph_format.space_after = Pt(8)

    add_page_footer(6)
    doc.add_page_break()

    # =========================================================================
    # PAGE 7: HEURISTIC MATCHING
    # =========================================================================
    add_page_header(7)
    
    p_mat_h = doc.add_paragraph()
    p_mat_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_mat = p_mat_h.add_run("MULTI-FACTOR HEURISTIC MATCHING ENGINE")
    r_mat.font.size = Pt(16)
    r_mat.font.bold = True
    p_mat_h.paragraph_format.space_after = Pt(14)
    
    mat_paras = [
        "Heuristic matching is a probabilistic mathematical model used to determine the similarity between two distinct reports—a reported lost item and a reported found item.",
        "The similarity function calculates a composite score S(Lost, Found) between 0% and 100% based on four weighted parameters:",
        "S(L, F) = 0.30 · Category + 0.35 · TextOverlap + 0.20 · Location + 0.15 · Date",
        "2. Candidate Match Score Matrix (Illustrative Example)",
        "Imagine an active campus repository where candidate items are cross-evaluated:"
    ]
    for text in mat_paras:
        p = doc.add_paragraph()
        r = p.add_run(text)
        r.font.size = Pt(11)
        p.paragraph_format.space_after = Pt(6)

    # Matrix Table
    t_mat = doc.add_table(rows=4, cols=4)
    t_mat.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_w_m = [Inches(2.5), Inches(1.3), Inches(1.3), Inches(1.3)]
    for row in t_mat.rows:
        for idx, w in enumerate(col_w_m):
            row.cells[idx].width = w

    mat_headers = ["Lost Item \\ Found Item", "Laptop #2", "Bottle #4", "Keys #8"]
    for i, h in enumerate(mat_headers):
        cell = t_mat.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(10)
        set_cell_background(cell, "F2F2F2")

    mat_data = [
        ("Dell Inspiron Laptop", "84.5%", "12.0%", "18.2%"),
        ("HydroFlask Steel Bottle", "8.5%", "79.2%", "14.1%"),
        ("Ring with Brass Keys", "6.0%", "11.4%", "91.0%")
    ]
    for r_idx, row in enumerate(mat_data):
        for c_idx, val in enumerate(row):
            cell = t_mat.cell(r_idx + 1, c_idx)
            cell.text = val
            cell.paragraphs[0].runs[0].font.size = Pt(10)
            if "%" in val and float(val.replace("%", "")) >= 75:
                cell.paragraphs[0].runs[0].font.bold = True

    p_post = doc.add_paragraph()
    p_post.paragraph_format.space_before = Pt(12)
    p_post.add_run(
        "If a Lost Laptop is compared against Found Inventory, there is an:\n"
        "• 84.5% chance it matches Found Laptop #2 (High Confidence Match),\n"
        "• 12.0% chance it matches Found Bottle #4 (Mismatch),\n"
        "• 18.2% chance it matches Found Keys #8 (Mismatch).\n\n"
        "These multi-factor probabilities define the matching pipeline—ensuring that students receive prioritized notifications for plausible matches without manual human browsing."
    ).font.size = Pt(11)

    add_page_footer(7)
    doc.add_page_break()

    # =========================================================================
    # PAGE 8: COMPARATIVE ANALYSIS
    # =========================================================================
    add_page_header(8)
    
    p_cmp_h = doc.add_paragraph()
    p_cmp_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cmp = p_cmp_h.add_run("COMPARATIVE ANALYSIS:\nIN-MEMORY BST VS. DATABASE B-TREE INDEXING")
    r_cmp.font.size = Pt(16)
    r_cmp.font.bold = True
    p_cmp_h.paragraph_format.space_after = Pt(14)

    p_c_intro = doc.add_paragraph()
    p_c_intro.add_run(
        "A foundational design question in CampusFind is why an in-memory Binary Search Tree is implemented when modern databases like MySQL already incorporate B-Tree indexing. The table below outlines the architectural comparison:"
    ).font.size = Pt(11)
    p_c_intro.paragraph_format.space_after = Pt(10)

    # Comparison Table
    t_cmp = doc.add_table(rows=7, cols=3)
    t_cmp.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_w_c = [Inches(1.8), Inches(2.4), Inches(2.4)]
    for row in t_cmp.rows:
        for idx, w in enumerate(col_w_c):
            row.cells[idx].width = w

    c_headers = ["Dimension", "In-Memory BST (app/dsa/bst.py)", "Relational Database B-Tree"]
    for i, h in enumerate(c_headers):
        cell = t_cmp.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(10)
        set_cell_background(cell, "F2F2F2")

    c_rows = [
        ("Primary Goal", "Sub-millisecond lookup & visual path trace", "Durable ACID storage & disk paging"),
        ("Storage Medium", "Volatile System RAM", "Non-volatile Block Storage (SSD/NVMe)"),
        ("Fan-out", "Binary (m = 2 children per node)", "Multi-way (m ≈ 100 - 1000 per page)"),
        ("Search Cost", "O(log₂ n) CPU memory comparisons", "O(log_B n) disk page I/O reads"),
        ("Path Transparency", "Exposes step-by-step visited keys array", "Opaque black-box engine internal"),
        ("Coexistence Role", "Interactive Algorithmic Layer", "Persistent Relational Backend")
    ]
    for r_idx, (d, bst_val, db_val) in enumerate(c_rows):
        t_cmp.cell(r_idx + 1, 0).text = d
        t_cmp.cell(r_idx + 1, 1).text = bst_val
        t_cmp.cell(r_idx + 1, 2).text = db_val
        for c in range(3):
            t_cmp.cell(r_idx + 1, c).paragraphs[0].runs[0].font.size = Pt(9.5)

    p_c_sum = doc.add_paragraph()
    p_c_sum.paragraph_format.space_before = Pt(12)
    p_c_sum.add_run(
        "Conclusion: In CampusFind, the relational database guarantees that reports survive server restarts, while the in-memory BST provides high-speed white-box algorithmic inspection for classroom demonstration."
    ).font.size = Pt(10.5)

    add_page_footer(8)
    doc.add_page_break()

    # =========================================================================
    # PAGE 9: APPLICATIONS AND FUTURE SCOPE
    # =========================================================================
    add_page_header(9)
    
    p_app_h = doc.add_paragraph()
    p_app_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_app = p_app_h.add_run("APPLICATIONS AND FUTURE SCOPE")
    r_app.font.size = Pt(18)
    r_app.font.bold = True
    p_app_h.paragraph_format.space_after = Pt(16)
    
    p_a1 = doc.add_paragraph()
    p_a1.add_run("Applications").font.bold = True
    p_a1.paragraph_format.space_after = Pt(6)
    
    apps_list = [
        "1. Centralizing lost property management across college hostels, labs, and libraries.",
        "2. Automating item correlation to reduce administrative security desk overhead.",
        "3. Mitigating fraudulent ownership claims through cryptographic challenge verification.",
        "4. Real-time visual tracking of hierarchical tree search paths in academic DSA labs.",
        "5. Deployable across airports, convention centers, and municipal transit terminals."
    ]
    for a in apps_list:
        p = doc.add_paragraph()
        p.add_run(a).font.size = Pt(11)
        p.paragraph_format.space_after = Pt(4)
        
    p_f1 = doc.add_paragraph()
    p_f1.paragraph_format.space_before = Pt(14)
    p_f1.add_run("Future Scope").font.bold = True
    p_f1.paragraph_format.space_after = Pt(6)
    
    future_list = [
        "• Integrating deep computer vision (OpenAI CLIP embeddings) for visual photo matching.",
        "• Implementing automated OCR to scan lost student identity cards and driving licenses.",
        "• Upgrading the in-memory tree to self-balancing AVL trees to guarantee O(log n) worst-case bounds.",
        "• Adding Bluetooth Low Energy (BLE) beacon geofencing to ping students near held items."
    ]
    for f in future_list:
        p = doc.add_paragraph()
        p.add_run(f).font.size = Pt(11)
        p.paragraph_format.space_after = Pt(4)

    add_page_footer(9)
    doc.add_page_break()

    # =========================================================================
    # PAGE 10: PROTOTYPE WALKTHROUGH — PART I
    # =========================================================================
    add_page_header(10)
    
    def add_mock_card(title, content_lines, captions):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        cell.width = Inches(6.6)
        set_cell_background(cell, "1E293B")
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(3)
        r_t = p.add_run("  " + title + "\n")
        r_t.font.bold = True
        r_t.font.size = Pt(11)
        r_t.font.color.rgb = RGBColor(56, 189, 248) # Cyan
        
        for line in content_lines:
            p_l = cell.add_paragraph()
            p_l.paragraph_format.space_after = Pt(2)
            r_l = p_l.add_run("  " + line)
            r_l.font.size = Pt(9.5)
            r_l.font.color.rgb = RGBColor(241, 245, 249)
            
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(4)
        p_sp.paragraph_format.space_after = Pt(10)
        for c in captions:
            p_c = doc.add_paragraph()
            p_c.paragraph_format.space_after = Pt(2)
            r_c = p_c.add_run(c)
            r_c.font.italic = True
            r_c.font.size = Pt(10)
            r_c.font.color.rgb = COLOR_DARK

    add_mock_card(
        "🌳 BST VISUALIZER (Interactive Tree Canvas)",
        [
            "[Key: 14]   [+ Insert Node]   [🔍 Search Key]   [🗑 Delete Node]",
            "",
            "                       ( 10 )",
            "                       /    \\",
            "                   ( 5 )    ( 15 )",
            "                   /   \\     /   \\",
            "                 ( 2 ) ( 8 )( 12 )( 18 )",
            "                              \\",
            "                              ( 14 ) <── (Searched Node Found!)",
            "",
            "In-Order Traversal:  [ 2, 5, 8, 10, 12, 14, 15, 18 ] (Sorted Keys)",
            "Search Path:  Root(10) ──► Right(15) ──► Left(12) ──► Right(14)"
        ],
        [
            "(this is a basic prototype of the website)",
            "(it involves a series of item nodes indexed in logarithmic hierarchy)",
            "(transitions and branches are dynamically traversed in O(log n) time)"
        ]
    )

    add_mock_card(
        "⚡ EXECUTION PATH TRACE OUTPUT",
        [
            "Target Search Key: 14 | Status: KEY FOUND IN TREE",
            "Step 1: Evaluate Root Node (10)  ──► 14 > 10 ──► Traverse Right Subtree",
            "Step 2: Evaluate Node (15)       ──► 14 < 15 ──► Traverse Left Subtree",
            "Step 3: Evaluate Node (12)       ──► 14 > 12 ──► Traverse Right Subtree",
            "Step 4: Evaluate Node (14)       ──► 14 == 14 ──► Target Node Located!",
            "Total Comparisons: 4 | Traversal Latency: 0.04 ms"
        ],
        [
            "(this is the step-by-step search execution trace)",
            "(the educational trace visually reinforces algorithmic tree traversal concepts)"
        ]
    )

    add_page_footer(10)
    doc.add_page_break()

    # =========================================================================
    # PAGE 11: PROTOTYPE WALKTHROUGH — PART II
    # =========================================================================
    add_page_header(11)

    add_mock_card(
        "🎯 SMART MATCHING ENGINE & CONFIDENCE ANALYSIS",
        [
            "Lost Report: Dell Inspiron 15 (Silver, Core i7, Tag #8821)",
            "Found Report: Dell Laptop in Black Sleeve (Found at Central Library)",
            "OVERALL MATCH CONFIDENCE: 84.5%  [ HIGH CONFIDENCE TIER ]",
            "----------------------------------------------------------------",
            "• Category Match (Weight: 30%): Earned 30.0 / 30.0  (Exact Category: Electronics)",
            "• Text Similarity (Weight: 35%): Earned 24.5 / 35.0  (Shared: ['dell', 'laptop'])",
            "• Spatial Proximity (Weight: 20%): Earned 15.0 / 20.0 (Shared zone: Central Library)",
            "• Date Causality (Weight: 15%): Earned 15.0 / 15.0  (Found within 24 hours of loss)"
        ],
        [
            "(this is the matching analysis mentioning the weighted probability)",
            "(candidates exceeding 75% are automatically classified as high-confidence)"
        ]
    )

    add_mock_card(
        "📢 REPORT MISPLACED ITEM & OWNERSHIP CHALLENGE",
        [
            "Item Title:      [ Blue HydroFlask Steel Bottle                      ]",
            "Item Category:   [ Personal Accessories & Bottles                  ▼ ]",
            "Campus Location: [ Central Library Reading Room, 2nd Floor         ▼ ]",
            "Date Misplaced:  [ 2026-10-24                                        ]",
            "🔒 Anti-Theft Verification Question:",
            "Secret Hint:     [ What specific sticker is placed on the bottom?    ]",
            "Correct Answer:  [ [ Confidential - Hashed in Database ]             ]"
        ],
        [
            "(this is where each lost item can be manually added)",
            "(the secret verification hint ensures only the genuine owner can claim goods)"
        ]
    )

    add_page_footer(11)
    doc.add_page_break()

    # =========================================================================
    # PAGE 12: PROTOTYPE WALKTHROUGH — PART III
    # =========================================================================
    add_page_header(12)

    add_mock_card(
        "🔍 CAMPUSFIND REPOSITORY INVENTORY CATALOG",
        [
            "Search: [ Search by keywords...       ]   Category: [ All Categories   ▼ ]",
            "Type:   [ All (Lost & Found)        ▼ ]   Location: [ All Campus Zones ▼ ]",
            "----------------------------------------------------------------",
            "Item #1: [Lost]  Dell Inspiron Laptop 15      📍 Library Reading Room",
            "Item #2: [Found] HP Pavilion Laptop Silver    📍 Central Library Desk",
            "Item #3: [Lost]  HydroFlask Bottle (750ml)    📍 Mess Hall 1",
            "Item #4: [Found] Blue Milton Water Bottle     📍 Hostel Block A Warden",
            "Item #5: [Lost]  Student Identity Card        📍 Main Auditorium"
        ],
        [
            "(here is where all the campus items are listed)",
            "(users can filter items by campus landmark, category, and date)"
        ]
    )

    add_mock_card(
        "🛡️ ADMINISTRATIVE ADJUDICATION & AUDIT LOG PANEL",
        [
            "Total Items: 10  |  Active Lost: 5  |  Active Found: 5  |  Resolved: 0",
            "PENDING CLAIMS AWAITING VERIFICATION:",
            "Claim #104 | Item: Casio fx-991CW Calculator",
            "Claimant: Priya Sharma (21BCE2045) | Submitted: 2 hours ago",
            "Secret Question: 'What is written on the back battery cover?'",
            "Claimant Answer: 'Priya S. - Batch 2024'",
            "Actions: [ Approve & Issue Custody ]   [ ❌ Reject False Claim ]",
            "IMMUTABLE AUDIT LOG:",
            "[2026-10-24 14:15] Admin approved claim #102 for item #6 (Owner: Alex J.)"
        ],
        [
            "(this is the administrative moderation panel where claims are adjudicated)",
            "(approving a claim transitions item status to resolved and writes audit log)"
        ]
    )

    add_page_footer(12)
    
    doc.save(output_filename)
    print(f"Report document successfully saved to: {output_filename}")

if __name__ == '__main__':
    create_report()
