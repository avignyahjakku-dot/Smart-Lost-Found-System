"""
CampusFind - Modern Tech Deck Generator
=======================================
Generates a sleek, high-impact, modern 11-slide presentation for classroom demo.
- Dark Mode Aesthetic (Deep Slate / Midnight Navy)
- Electric Cyan & Crimson Accents
- Only 2 clean, punchy comparison tables
- Floating feature cards, big stats, and bullet-free punchy visuals
"""

import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_crazy_deck(output_filename="CampusFind_Presentation.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Sleek Modern Dark Palette
    C_BG = RGBColor(15, 23, 42)          # Deep Midnight Slate (bg)
    C_CARD = RGBColor(30, 41, 59)        # Card Background
    C_CARD_BORDER = RGBColor(51, 65, 85) # Subtle Border
    C_CYAN = RGBColor(56, 189, 248)      # Electric Sky/Cyan
    C_CORAL = RGBColor(244, 63, 94)      # Vivid Coral/Crimson
    C_EMERALD = RGBColor(52, 211, 153)   # Mint Emerald
    C_WHITE = RGBColor(255, 255, 255)
    C_TEXT_SUB = RGBColor(148, 163, 184) # Muted text
    C_TEXT_MUTED = RGBColor(100, 116, 139)
    C_TABLE_HEADER = RGBColor(2, 132, 199)# Blue header
    C_TABLE_ROW_ALT = RGBColor(24, 34, 53)

    def set_slide_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG
        bg.line.color.rgb = C_BG
        return bg

    def add_top_bar(slide, title_text, tag_text="CAMPUSFIND • DATA STRUCTURES PROJECT"):
        # Top pill tag
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.4), Inches(4.5), Inches(0.35))
        pill.fill.solid()
        pill.fill.fore_color.rgb = C_CARD
        pill.line.color.rgb = C_CYAN
        pill.line.width = Pt(1)
        p = pill.text_frame.paragraphs[0]
        p.text = tag_text.upper()
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = C_CYAN
        p.alignment = PP_ALIGN.CENTER

        # Title
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.733), Inches(0.8))
        tf = tb.text_frame
        p_t = tf.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = C_WHITE

        # Footer branding
        fb = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.3))
        ft = fb.text_frame
        p_f = ft.paragraphs[0]
        p_f.text = "CampusFind  |  Avignyah Jakku (25070721024) & Meghana (25070721002)  |  SIT Hyderabad"
        p_f.font.size = Pt(9)
        p_f.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 1: HERO TITLE SLIDE (Modern Keynote Style)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1)

    # Glowing subtle banner
    glow = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(0.06))
    glow.fill.solid()
    glow.fill.fore_color.rgb = C_CYAN
    glow.line.color.rgb = C_CYAN

    # Big Tag
    tag = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.3), Inches(4.0), Inches(0.45))
    tag.fill.solid()
    tag.fill.fore_color.rgb = C_CARD
    tag.line.color.rgb = C_CYAN
    p_tag = tag.text_frame.paragraphs[0]
    p_tag.text = "BTech CSE Capstone  •  Data Structures Lab"
    p_tag.font.size = Pt(10)
    p_tag.font.bold = True
    p_tag.font.color.rgb = C_CYAN
    p_tag.alignment = PP_ALIGN.CENTER

    # Massive Title
    tb_title = s1.shapes.add_textbox(Inches(0.8), Inches(1.85), Inches(11.733), Inches(2.3))
    tf_t = tb_title.text_frame
    tf_t.word_wrap = True
    p1 = tf_t.paragraphs[0]
    p1.text = "🔍 CampusFind"
    p1.font.size = Pt(40)
    p1.font.bold = True
    p1.font.color.rgb = C_WHITE

    p2 = tf_t.add_paragraph()
    p2.text = "Smart University Lost & Found System"
    p2.font.size = Pt(28)
    p2.font.bold = True
    p2.font.color.rgb = C_CYAN

    p3 = tf_t.add_paragraph()
    p3.text = "Reuniting Campuses with In-Memory Binary Search Trees & Heuristic Matching"
    p3.font.size = Pt(14)
    p3.font.color.rgb = C_TEXT_SUB

    # Presenter Card (Avignyah & Meghana)
    card_p = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.4), Inches(6.8), Inches(2.2))
    card_p.fill.solid()
    card_p.fill.fore_color.rgb = C_CARD
    card_p.line.color.rgb = C_CARD_BORDER
    card_p.line.width = Pt(1.5)
    tf_p = card_p.text_frame
    tf_p.margin_left = Inches(0.3)
    tf_p.margin_top = Inches(0.2)
    p_ph = tf_p.paragraphs[0]
    p_ph.text = "PRESENTED BY:"
    p_ph.font.size = Pt(11)
    p_ph.font.bold = True
    p_ph.font.color.rgb = C_CORAL

    p_m1 = tf_p.add_paragraph()
    p_m1.text = "👨‍💻 Avignyah Jakku   (PRN: 25070721024)"
    p_m1.font.size = Pt(13)
    p_m1.font.bold = True
    p_m1.font.color.rgb = C_WHITE

    p_m2 = tf_p.add_paragraph()
    p_m2.text = "👩‍💻 Meghana                  (PRN: 25070721002)"
    p_m2.font.size = Pt(13)
    p_m2.font.bold = True
    p_m2.font.color.rgb = C_WHITE

    p_inst = tf_p.add_paragraph()
    p_inst.text = "Symbiosis Institute of Technology, Hyderabad (SIT-H)"
    p_inst.font.size = Pt(10.5)
    p_inst.font.color.rgb = C_TEXT_SUB

    # Mentor Card
    card_m = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.9), Inches(4.4), Inches(4.633), Inches(2.2))
    card_m.fill.solid()
    card_m.fill.fore_color.rgb = C_CARD
    card_m.line.color.rgb = C_CARD_BORDER
    card_m.line.width = Pt(1.5)
    tf_m = card_m.text_frame
    tf_m.margin_left = Inches(0.3)
    tf_m.margin_top = Inches(0.2)
    p_mh = tf_m.paragraphs[0]
    p_mh.text = "GUIDANCE & MENTORSHIP:"
    p_mh.font.size = Pt(11)
    p_mh.font.bold = True
    p_mh.font.color.rgb = C_EMERALD

    p_g1 = tf_m.add_paragraph()
    p_g1.text = "Dr. Rakesh Salakapuri"
    p_g1.font.size = Pt(13)
    p_g1.font.bold = True
    p_g1.font.color.rgb = C_WHITE

    p_g2 = tf_m.add_paragraph()
    p_g2.text = "Professor & Project Guide, Dept. of CSE"
    p_g2.font.size = Pt(10.5)
    p_g2.font.color.rgb = C_TEXT_SUB

    p_g3 = tf_m.add_paragraph()
    p_g3.text = "Under the Directorate of Dr. Rajinikanth Aluvalu"
    p_g3.font.size = Pt(10)
    p_g3.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 2: THE REAL-LIFE PROBLEM (Visual & Punchy)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s2)
    add_top_bar(s2, "The Problem: Losing Things on Campus Sucks")

    problems = [
        ("📱 The WhatsApp Spam Chaos", 
         "Messages get buried under 500 unread group chats within 2 hours.", 
         "Zero searchability. Zero filters. Pure frustration.", C_CORAL),
        ("🕵️‍♂️ The Fake Claim Hazard", 
         "Public posts show every detail (laptop stickers, scratches, colors).", 
         "Anyone can pretend it's theirs and steal it without proof.", C_CYAN),
        ("📁 The Forgotten Paper Register", 
         "Found items sit in dusty security guard drawers for an entire semester.", 
         "Students never know which of the 6 security gates to visit.", C_EMERALD)
    ]

    for idx, (title, line1, line2, accent) in enumerate(problems):
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + idx * 4.0), Inches(1.8), Inches(3.733), Inches(4.8))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD
        card.line.color.rgb = accent
        card.line.width = Pt(2)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.3)
        tf.margin_top = Inches(0.35)

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

        p_line = tf.add_paragraph()
        p_line.text = "\n" + line1
        p_line.font.size = Pt(12)
        p_line.font.color.rgb = C_TEXT_SUB

        p_line2 = tf.add_paragraph()
        p_line2.text = "\n❌ " + line2
        p_line2.font.size = Pt(12)
        p_line2.font.bold = True
        p_line2.font.color.rgb = accent

    # =========================================================================
    # SLIDE 3: ENTER CAMPUSFIND (The Solution)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s3)
    add_top_bar(s3, "Enter CampusFind: One Smart Platform. Zero Chaos.")

    pillars = [
        ("⚡ 1. Lightning Fast DSA Search",
         "In-Memory Binary Search Tree (BST) indexes all items directly in RAM.",
         "Lookups execute in O(log n) time — sub-millisecond response!"),
        ("🔒 2. Anti-Theft Verification",
         "The owner sets a private secret question when reporting.",
         "Claimants must answer the secret hint before admin approves handover!"),
        ("🧠 3. Smart Matching Algorithm",
         "Heuristic engine automatically scores candidate pairings.",
         "Evaluates Category, Keywords, Campus Landmark & Date causality.")
    ]

    for idx, (title, line1, line2) in enumerate(pillars):
        top_y = Inches(1.8 + idx * 1.6)
        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_y, Inches(11.733), Inches(1.35))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD
        card.line.color.rgb = C_CYAN if idx == 0 else (C_CORAL if idx == 1 else C_EMERALD)
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.margin_left = Inches(0.35)
        tf.margin_top = Inches(0.18)

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

        p_sub = tf.add_paragraph()
        p_sub.text = line1 + "   •   " + line2
        p_sub.font.size = Pt(11.5)
        p_sub.font.color.rgb = C_TEXT_SUB

    # =========================================================================
    # SLIDE 4: THE BIG COMPARISON (TABLE 1 - Only 1 of 2 tables!)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s4)
    add_top_bar(s4, "The Showdown: Old School vs. CampusFind")

    # High-contrast table
    t_shape = s4.shapes.add_table(6, 3, Inches(0.8), Inches(1.8), Inches(11.733), Inches(4.8))
    table = t_shape.table
    table.columns[0].width = Inches(2.7)
    table.columns[1].width = Inches(4.5)
    table.columns[2].width = Inches(4.533)

    t_headers = ["Dimension", "Traditional Way ❌", "CampusFind Way 🚀"]
    for col_idx, h_text in enumerate(t_headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_TABLE_HEADER
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = C_WHITE

    t_rows = [
        ["Where to search?", "10 WhatsApp groups + security gates", "1 Centralized Searchable Web App"],
        ["How items match?", "Students scrolling endlessly for days", "Algorithm pairs them in 0.01 seconds"],
        ["Fraud prevention?", "None. First person to claim gets it", "2-Factor Secret Challenge Question"],
        ["Search Speed & DSA?", "O(n) linear scan through paper records", "O(log n) In-Memory Binary Search Tree"],
        ["Custody Tracking?", "Items rot forgotten in drawer boxes", "Tracked holding desk (Gate 1, Library)"]
    ]

    for row_idx, r_data in enumerate(t_rows):
        is_alt = (row_idx % 2 == 1)
        for col_idx, text in enumerate(r_data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_TABLE_ROW_ALT if is_alt else C_CARD
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(11)
            p.font.color.rgb = C_CYAN if col_idx == 2 else (C_CORAL if col_idx == 1 else C_WHITE)

    # =========================================================================
    # SLIDE 5: USER WORKFLOW IN 4 STEPS
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s5)
    add_top_bar(s5, "How It Works: 4-Step Recovery Journey")

    steps = [
        ("1️⃣ Log Item", "Report lost or found with title, photo, location, and set secret hint.", C_CYAN),
        ("2️⃣ BST Insert", "Item ID is instantly inserted into RAM Binary Search Tree in O(log n).", C_EMERALD),
        ("3️⃣ Auto-Match", "Multi-factor algorithm calculates score (>75% = High Confidence).", C_CORAL),
        ("4️⃣ Claim & Verify", "Claimant answers secret hint; Admin verifies & approves physical handover.", C_CYAN)
    ]

    for idx, (s_title, s_desc, accent) in enumerate(steps):
        card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + idx * 3.0), Inches(2.2), Inches(2.75), Inches(4.2))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD
        card.line.color.rgb = accent
        card.line.width = Pt(2)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_top = Inches(0.3)

        p = tf.paragraphs[0]
        p.text = s_title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = accent

        p_desc = tf.add_paragraph()
        p_desc.text = "\n" + s_desc
        p_desc.font.size = Pt(12)
        p_desc.font.color.rgb = C_TEXT_SUB

    # =========================================================================
    # SLIDE 6: THE DSA BRAIN: BINARY SEARCH TREE
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s6)
    add_top_bar(s6, "The DSA Brain: Pure Python Binary Search Tree")

    # Left card: Why BST?
    c_left = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.8))
    c_left.fill.solid()
    c_left.fill.fore_color.rgb = C_CARD
    c_left.line.color.rgb = C_CYAN
    tf_l = c_left.text_frame
    tf_l.margin_left = Inches(0.3)
    tf_l.margin_top = Inches(0.3)

    p = tf_l.paragraphs[0]
    p.text = "🌳 WHY AN IN-MEMORY BST?"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_CYAN

    points_bst = [
        ("⚡ O(log n) Search Speed", "Cuts search space in half at every step. Lightning fast in RAM."),
        ("🗺️ Real-Time Path Tracing", "Exposes exact traversal: [Root ➔ Right ➔ Left ➔ Found!]."),
        ("🔄 In-Order Traversal", "Visiting Left-Root-Right gives sorted item keys in O(n) time."),
        ("✂️ 3-Case Node Deletion", "Removes claimed items cleanly (leaf, 1 child, or 2 children successor).")
    ]
    for h, d in points_bst:
        p_h = tf_l.add_paragraph()
        p_h.text = "\n• " + h
        p_h.font.size = Pt(12)
        p_h.font.bold = True
        p_h.font.color.rgb = C_WHITE
        p_d = tf_l.add_paragraph()
        p_d.text = "   " + d
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = C_TEXT_SUB

    # Right card: Code & Invariant
    c_right = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.733), Inches(4.8))
    c_right.fill.solid()
    c_right.fill.fore_color.rgb = C_CARD
    c_right.line.color.rgb = C_CARD_BORDER
    tf_r = c_right.text_frame
    tf_r.margin_left = Inches(0.3)
    tf_r.margin_top = Inches(0.3)

    p = tf_r.paragraphs[0]
    p.text = "📐 THE BST INVARIANT"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD

    p_inv = tf_r.add_paragraph()
    p_inv.text = "\nFor every Node N:\n• Left Subtree Keys  <  Node Key\n• Right Subtree Keys >  Node Key\n"
    p_inv.font.size = Pt(12)
    p_inv.font.color.rgb = C_WHITE

    p_code = tf_r.add_paragraph()
    p_code.text = "```python\nclass BSTNode:\n    def __init__(self, key, data):\n        self.key = key       # Item ID\n        self.data = data     # Item info\n        self.left = None\n        self.right = None\n```\n\n🎯 Dual Engine Advantage:\nMySQL saves to disk permanently.\nBST caches in RAM for instant visual search."
    p_code.font.size = Pt(10.5)
    p_code.font.color.rgb = C_CYAN

    # =========================================================================
    # SLIDE 7: MATCHING ALGORITHM (TABLE 2 - The 2nd table!)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s7)
    add_top_bar(s7, "How It Thinks: Multi-Factor Heuristic Matching")

    # Formula banner
    fb = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.733), Inches(0.75))
    fb.fill.solid()
    fb.fill.fore_color.rgb = C_CARD
    fb.line.color.rgb = C_CORAL
    p_f = fb.text_frame.paragraphs[0]
    p_f.text = "🎯 Matching Formula:  Score = 30% Category + 35% Keywords + 20% Location + 15% Date"
    p_f.font.size = Pt(13)
    p_f.font.bold = True
    p_f.font.color.rgb = C_WHITE
    p_f.alignment = PP_ALIGN.CENTER

    # Table 2
    t2_shape = s7.shapes.add_table(5, 3, Inches(0.8), Inches(2.55), Inches(11.733), Inches(4.3))
    t2 = t2_shape.table
    t2.columns[0].width = Inches(2.5)
    t2.columns[1].width = Inches(1.8)
    t2.columns[2].width = Inches(7.433)

    h2 = ["Dimension", "Weight", "How It Calculates"]
    for col_idx, h_text in enumerate(h2):
        cell = t2.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_TABLE_HEADER
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = C_WHITE

    r2 = [
        ["🏷️ Category Match", "30%", "Exact category check: 30 pts for exact match, 0 for mismatch (e.g. Electronics vs Bottle)."],
        ["📝 Keyword Overlap", "35%", "Jaccard similarity on tokens after stripping stop words ('dell', 'laptop', 'silver') + title boost."],
        ["📍 Campus Location", "20%", "Proximity scoring: 20 pts for exact landmark (e.g. Central Library), 15 pts for shared zone."],
        ["⏱️ Date Causality", "15%", "Chronological plausibility: 15 pts if found on same day; 0 pts if found before reported lost!"]
    ]

    for row_idx, r_data in enumerate(r2):
        is_alt = (row_idx % 2 == 1)
        for col_idx, text in enumerate(r_data):
            cell = t2.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_TABLE_ROW_ALT if is_alt else C_CARD
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(11)
            p.font.color.rgb = C_CORAL if col_idx == 1 else (C_CYAN if col_idx == 0 else C_TEXT_SUB)

    # =========================================================================
    # SLIDE 8: WHAT WE WILL DEMO LIVE (Exciting features)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s8)
    add_top_bar(s8, "What You'll See in the Live Demo")

    demos = [
        ("🌳 1. BST Visualizer", 
         "Watch nodes animate into the tree.", 
         "Type an item ID and watch the green laser trace the search path step-by-step!", C_CYAN),
        ("🎯 2. Smart Matches Hub", 
         "See real candidate rankings.", 
         "Items automatically paired with 84.5% confidence and transparent factor breakdown!", C_CORAL),
        ("🔒 3. Anti-Theft Secret Hint", 
         "File a lost report with a secret question.", 
         "Watch how the public cannot see the answer, but the claimant must answer it!", C_EMERALD),
        ("🛡️ 4. Admin Control Center", 
         "The security officer portal.", 
         "Review pending claims, inspect claimant answers, and approve custody handover!", C_CYAN)
    ]

    for idx, (title, line1, line2, accent) in enumerate(demos):
        card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + idx * 3.0), Inches(2.0), Inches(2.75), Inches(4.5))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD
        card.line.color.rgb = accent
        card.line.width = Pt(2)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_top = Inches(0.3)

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = accent

        p1 = tf.add_paragraph()
        p1.text = "\n" + line1
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = C_WHITE

        p2 = tf.add_paragraph()
        p2.text = "\n" + line2
        p2.font.size = Pt(11)
        p2.font.color.rgb = C_TEXT_SUB

    # =========================================================================
    # SLIDE 9: TECH STACK & SYSTEM SPECS
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s9)
    add_top_bar(s9, "Under the Hood: Tech Stack & Architecture")

    techs = [
        ("🐍 Python Flask", "Lightweight WSGI backend with modular blueprints."),
        ("🌳 Pure-Python BST", "In-memory tree engine with full path tracing & 3-case deletion."),
        ("🗄️ MySQL 8.0 & SQLite", "Dual database engine: Production MySQL with zero-config SQLite failover."),
        ("🎨 Vanilla CSS3 & SVG", "Fast, responsive UI with real-time vector canvas rendering."),
        ("🔒 Werkzeug Security", "scrypt password hashing, session guards, and CSRF protection."),
        ("🧪 51/51 Tests Passing", "100% automated test coverage across models, routes & BST.")
    ]

    for idx, (title, desc) in enumerate(techs):
        row = idx // 3
        col = idx % 3
        x = Inches(0.8 + col * 4.0)
        y = Inches(2.0 + row * 2.3)

        card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(3.733), Inches(2.0))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD
        card.line.color.rgb = C_CARD_BORDER

        tf = card.text_frame
        tf.margin_left = Inches(0.3)
        tf.margin_top = Inches(0.25)

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = C_CYAN

        p_d = tf.add_paragraph()
        p_d.text = "\n" + desc
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = C_TEXT_SUB

    # =========================================================================
    # SLIDE 10: WHAT'S NEXT? (Future Scope)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s10)
    add_top_bar(s10, "What's Next: CampusFind 2.0 Roadmap")

    futures = [
        ("👁️ AI Computer Vision", 
         "Snap a photo of a found water bottle.", 
         "OpenAI CLIP embeddings match items visually even if descriptions differ completely!", C_CYAN),
        ("🪪 Smart ID Card OCR", 
         "Found a student ID on the grass?", 
         "Camera extracts PRN/Roll Number and automatically alerts the student directly!", C_CORAL),
        ("📡 Campus BLE Beacons", 
         "Lost your keys in the library?", 
         "Bluetooth beacons detect when you walk near the desk where they were handed in!", C_EMERALD)
    ]

    for idx, (title, line1, line2, accent) in enumerate(futures):
        card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + idx * 4.0), Inches(2.0), Inches(3.733), Inches(4.5))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD
        card.line.color.rgb = accent
        card.line.width = Pt(2)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.3)
        tf.margin_top = Inches(0.35)

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = accent

        p1 = tf.add_paragraph()
        p1.text = "\n" + line1
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = C_WHITE

        p2 = tf.add_paragraph()
        p2.text = "\n💡 " + line2
        p2.font.size = Pt(11.5)
        p2.font.color.rgb = C_TEXT_SUB

    # =========================================================================
    # SLIDE 11: WRAP-UP & LIVE DEMO TIME!
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s11)

    # Hero wrap-up card
    box = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(1.2), Inches(10.333), Inches(5.1))
    box.fill.solid()
    box.fill.fore_color.rgb = C_CARD
    box.line.color.rgb = C_CYAN
    box.line.width = Pt(2.5)

    tf_c = box.text_frame
    tf_c.margin_left = Inches(0.5)
    tf_c.margin_top = Inches(0.6)

    p1 = tf_c.paragraphs[0]
    p1.text = "🚀 Time for the Live Demo!"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = C_WHITE
    p1.alignment = PP_ALIGN.CENTER

    p2 = tf_c.add_paragraph()
    p2.text = "Let's test an item search and see the In-Memory BST in action."
    p2.font.size = Pt(16)
    p2.font.color.rgb = C_CYAN
    p2.alignment = PP_ALIGN.CENTER

    p3 = tf_c.add_paragraph()
    p3.text = "\n\nAvignyah Jakku (25070721024)   &   Meghana (25070721002)"
    p3.font.size = Pt(14)
    p3.font.bold = True
    p3.font.color.rgb = C_CORAL
    p3.alignment = PP_ALIGN.CENTER

    p4 = tf_c.add_paragraph()
    p4.text = "Department of Computer Science & Engineering  |  SIT Hyderabad"
    p4.font.size = Pt(11)
    p4.font.color.rgb = C_TEXT_MUTED
    p4.alignment = PP_ALIGN.CENTER

    p5 = tf_c.add_paragraph()
    p5.text = "\n🔥 Questions? Fire away!"
    p5.font.size = Pt(18)
    p5.font.bold = True
    p5.font.color.rgb = C_EMERALD
    p5.alignment = PP_ALIGN.CENTER

    prs.save(output_filename)
    print(f"Presentation saved successfully to: {output_filename}")

if __name__ == '__main__':
    create_crazy_deck()
