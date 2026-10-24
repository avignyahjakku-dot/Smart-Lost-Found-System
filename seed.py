"""
CampusFind - Seed Data Script
=============================
Populates realistic campus sample users, lost & found items, and claims
for testing, demonstration, and algorithmic evaluation.
"""

import sys
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from app import create_app
from app.db import execute_db, query_db

def seed_database(reset=False):
    app = create_app('development')
    with app.app_context():
        if reset:
            print("Clearing existing records...")
            execute_db("DELETE FROM activity_logs")
            execute_db("DELETE FROM claims")
            execute_db("DELETE FROM items")
            execute_db("DELETE FROM users WHERE email != %s", (app.config['DEFAULT_ADMIN_EMAIL'],))

        print("Checking/seeding campus users...")
        users = [
            ("Alex Johnson", "alex@campusfind.edu", "21BCE1024", "+91 9876543210", "student"),
            ("Priya Sharma", "priya@campusfind.edu", "21BCE2045", "+91 9876543211", "student"),
            ("Dr. Robert Vance", "vance@campusfind.edu", "FAC-CSE-042", "+91 9876543212", "staff"),
            ("Security Desk Officer", "security@campusfind.edu", "SEC-007", "+91 9876543213", "staff"),
        ]

        user_ids = {}
        for name, email, roll, phone, role in users:
            existing = query_db("SELECT id FROM users WHERE email = %s", (email,), one=True)
            if not existing:
                uid = execute_db(
                    "INSERT INTO users (full_name, email, student_id, phone, password_hash, role) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (name, email, roll, phone, generate_password_hash("Student@123"), role),
                    return_id=True
                )
                user_ids[email] = uid
                print(f"Created user: {email} (ID: {uid})")
            else:
                user_ids[email] = existing['id']

        admin_user = query_db("SELECT id FROM users WHERE role = 'admin' LIMIT 1", one=True)
        admin_id = admin_user['id'] if admin_user else list(user_ids.values())[0]

        print("Seeding campus lost and found item reports...")
        today = datetime.now().date()
        one_day_ago = today - timedelta(days=1)
        two_days_ago = today - timedelta(days=2)
        three_days_ago = today - timedelta(days=3)
        four_days_ago = today - timedelta(days=4)

        sample_items = [
            # High Match Pair 1: Laptop
            {
                'user_id': user_ids.get('alex@campusfind.edu', 1),
                'type': 'lost',
                'title': 'Dell Inspiron 15 Silver Laptop',
                'category': 'Electronics & Gadgets',
                'description': 'Left silver Dell Inspiron laptop on second floor study table near the north window. Has a GitHub Octocat sticker on the lid.',
                'location': 'Central Library',
                'item_date': two_days_ago.strftime("%Y-%m-%d"),
                'secret_hint': 'What brand sticker is next to the GitHub sticker?',
                'storage_location': None,
                'status': 'open'
            },
            {
                'user_id': user_ids.get('security@campusfind.edu', 1),
                'type': 'found',
                'title': 'Silver Dell Laptop with Tech Stickers',
                'category': 'Electronics & Gadgets',
                'description': 'Discovered on 2nd floor reading area study desk. Silver Dell Inspiron laptop in protective sleeve.',
                'location': 'Central Library',
                'item_date': one_day_ago.strftime("%Y-%m-%d"),
                'secret_hint': None,
                'storage_location': 'Central Library Front Circulation Desk (Librarian Desk A)',
                'status': 'open'
            },

            # High Match Pair 2: Student ID Card
            {
                'user_id': user_ids.get('priya@campusfind.edu', 1),
                'type': 'lost',
                'title': 'University Student Identity Card - Priya Sharma',
                'category': 'Student IDs & Cards',
                'description': 'Lost my university RFID student ID card in a blue lanyard. Department of CSE.',
                'location': 'Cafeteria / Food Court',
                'item_date': one_day_ago.strftime("%Y-%m-%d"),
                'secret_hint': 'What is the color of the clip attached to the lanyard?',
                'storage_location': None,
                'status': 'open'
            },
            {
                'user_id': user_ids.get('vance@campusfind.edu', 1),
                'type': 'found',
                'title': 'Student ID Card (Priya Sharma - CSE)',
                'category': 'Student IDs & Cards',
                'description': 'Found student ID card lying on food court table near the coffee counter.',
                'location': 'Cafeteria / Food Court',
                'item_date': today.strftime("%Y-%m-%d"),
                'secret_hint': None,
                'storage_location': 'Student Activity Center (SAC) Information Office',
                'status': 'open'
            },

            # High Match Pair 3: Casio Calculator
            {
                'user_id': user_ids.get('alex@campusfind.edu', 1),
                'type': 'lost',
                'title': 'Casio Scientific Calculator FX-991EX',
                'category': 'Electronics & Gadgets',
                'description': 'Black and white Casio FX-991EX Classwiz scientific calculator. Has my initials "AJ" engraved lightly on the back battery cover.',
                'location': 'Computer Science Department',
                'item_date': three_days_ago.strftime("%Y-%m-%d"),
                'secret_hint': 'What initials are engraved on the back cover?',
                'storage_location': None,
                'status': 'open'
            },
            {
                'user_id': user_ids.get('security@campusfind.edu', 1),
                'type': 'found',
                'title': 'Casio FX-991EX Scientific Calculator',
                'category': 'Electronics & Gadgets',
                'description': 'Found in Computer Science Lab 3 after afternoon lab session. Good condition.',
                'location': 'Computer Science Department',
                'item_date': two_days_ago.strftime("%Y-%m-%d"),
                'secret_hint': None,
                'storage_location': 'CS Department Main Office Room 204',
                'status': 'open'
            },

            # Moderate Match: Keys
            {
                'user_id': user_ids.get('priya@campusfind.edu', 1),
                'type': 'lost',
                'title': 'Hostel Room Keys with Iron Man Keychain',
                'category': 'Keys & Badges',
                'description': 'Set of two Yale keys with a red metallic Iron Man mask keychain and bike key.',
                'location': 'Hostel Block A',
                'item_date': four_days_ago.strftime("%Y-%m-%d"),
                'secret_hint': 'What is written on the small white tag attached?',
                'storage_location': None,
                'status': 'open'
            },
            {
                'user_id': user_ids.get('security@campusfind.edu', 1),
                'type': 'found',
                'title': 'Keyring with Superhero Keychain',
                'category': 'Keys & Badges',
                'description': 'Keys found on lawn pathway between Hostel Block A and Mess hall.',
                'location': 'Hostel Block A',
                'item_date': (four_days_ago + timedelta(days=1)).strftime("%Y-%m-%d"),
                'secret_hint': None,
                'storage_location': 'Hostel Block A Warden Office',
                'status': 'open'
            },

            # Unmatched Items
            {
                'user_id': user_ids.get('alex@campusfind.edu', 1),
                'type': 'lost',
                'title': 'Blue Hydro Flask Water Bottle 1L',
                'category': 'Bottles & Tumblers',
                'description': 'Cobalt blue 32oz vacuum insulated bottle with minor dent on bottom rim.',
                'location': 'Sports Ground / Gym',
                'item_date': one_day_ago.strftime("%Y-%m-%d"),
                'secret_hint': None,
                'storage_location': None,
                'status': 'open'
            },
            {
                'user_id': user_ids.get('vance@campusfind.edu', 1),
                'type': 'found',
                'title': 'Black Ray-Ban Eyeglasses in Case',
                'category': 'Eyewear & Glasses',
                'description': 'Found on 3rd row auditorium seat during morning faculty seminar.',
                'location': 'Main Auditorium',
                'item_date': today.strftime("%Y-%m-%d"),
                'secret_hint': None,
                'storage_location': 'Main Security Gate 1 Lost & Found Box',
                'status': 'open'
            }
        ]

        inserted_items = []
        for item in sample_items:
            # Check duplicate by title and type
            dup = query_db(
                "SELECT id FROM items WHERE title = %s AND type = %s",
                (item['title'], item['type']),
                one=True
            )
            if not dup:
                iid = execute_db(
                    "INSERT INTO items (user_id, type, title, category, description, location, item_date, secret_hint, storage_location, status) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (
                        item['user_id'], item['type'], item['title'], item['category'],
                        item['description'], item['location'], item['item_date'],
                        item['secret_hint'], item['storage_location'], item['status']
                    ),
                    return_id=True
                )
                inserted_items.append((iid, item['title']))
                print(f"Inserted item #{iid}: {item['title']} ({item['type']})")

        # Seed sample claim
        found_laptop = query_db("SELECT id FROM items WHERE title LIKE '%Silver Dell Laptop%'", one=True)
        alex = query_db("SELECT id FROM users WHERE email = 'alex@campusfind.edu'", one=True)
        if found_laptop and alex:
            existing_claim = query_db(
                "SELECT id FROM claims WHERE item_id = %s AND claimant_id = %s",
                (found_laptop['id'], alex['id']),
                one=True
            )
            if not existing_claim:
                execute_db(
                    "INSERT INTO claims (item_id, claimant_id, proof_details, secret_answer, contact_phone, status) "
                    "VALUES (%s, %s, %s, %s, %s, 'pending')",
                    (
                        found_laptop['id'], alex['id'],
                        "The laptop is a Dell Inspiron 15 with service tag #DL98234. Has a sticker of Python logo beside GitHub Octocat. Inside wallpaper is a photo of mountains.",
                        "Python logo sticker",
                        "+91 9876543210"
                    )
                )
                print(f"Created sample pending claim for Item #{found_laptop['id']}")

        print("Seeding completed successfully!")

if __name__ == '__main__':
    reset_flag = '--reset' in sys.argv
    seed_database(reset=reset_flag)
