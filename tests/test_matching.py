"""
Unit Tests: Smart Matching Engine
=================================
Validates multi-factor similarity calculations, confidence tier classifications,
chronological constraints, and ranking heuristics.
"""

import unittest
from datetime import datetime, timedelta
from app.matching import evaluate_match, find_matches_for_item, clean_tokens, calculate_jaccard_similarity

class TestSmartMatching(unittest.TestCase):

    def test_clean_tokens(self):
        """Tokens should be lowercased and stripped of punctuation and stop words."""
        text = "I lost my blue Dell Inspiron laptop in the Library on Monday!"
        tokens = clean_tokens(text)
        self.assertIn("blue", tokens)
        self.assertIn("dell", tokens)
        self.assertIn("inspiron", tokens)
        self.assertIn("laptop", tokens)
        self.assertIn("library", tokens)
        self.assertNotIn("i", tokens)
        self.assertNotIn("my", tokens)
        self.assertNotIn("in", tokens)
        self.assertNotIn("the", tokens)

    def test_jaccard_similarity(self):
        """Verify standard Jaccard intersection over union."""
        set1 = {'dell', 'laptop', 'blue'}
        set2 = {'dell', 'laptop', 'silver'}
        # Intersection: 2 ('dell', 'laptop'), Union: 4 ('dell', 'laptop', 'blue', 'silver')
        self.assertAlmostEqual(calculate_jaccard_similarity(set1, set2), 2 / 4)
        self.assertEqual(calculate_jaccard_similarity(set(), set2), 0.0)

    def test_high_probability_match(self):
        """An identical item lost and found at the same place/time should yield High confidence."""
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)

        lost_item = {
            'id': 1,
            'title': 'Dell Inspiron 15 Silver Laptop',
            'category': 'Electronics & Gadgets',
            'description': 'Silver laptop with stickers left in reading room.',
            'location': 'Central Library',
            'item_date': yesterday.strftime("%Y-%m-%d")
        }

        found_item = {
            'id': 2,
            'title': 'Dell Inspiron Laptop Silver',
            'category': 'Electronics & Gadgets',
            'description': 'Found silver Dell laptop in library study room.',
            'location': 'Central Library',
            'item_date': today.strftime("%Y-%m-%d")
        }

        result = evaluate_match(lost_item, found_item)
        self.assertEqual(result['tier'], 'High')
        self.assertGreaterEqual(result['total_score'], 75.0)
        self.assertEqual(result['breakdown']['category']['earned'], 30.0)
        self.assertEqual(result['breakdown']['location']['earned'], 20.0)
        self.assertGreater(result['breakdown']['text']['earned'], 15.0)

    def test_category_mismatch_penalty(self):
        """Incompatible categories should receive zero category points."""
        lost = {
            'id': 10,
            'title': 'Casio Watch',
            'category': 'Clothing & Accessories',
            'description': 'Black wrist watch.',
            'location': 'Gym',
            'item_date': '2026-10-10'
        }
        found = {
            'id': 11,
            'title': 'Casio Watch',
            'category': 'Electronics & Gadgets',
            'description': 'Digital wrist watch.',
            'location': 'Gym',
            'item_date': '2026-10-11'
        }

        result = evaluate_match(lost, found)
        self.assertEqual(result['breakdown']['category']['earned'], 0.0)

    def test_chronological_sequence_penalty(self):
        """Item found significantly before it was reported lost is physically implausible."""
        lost = {
            'id': 20,
            'title': 'Lab Coat',
            'category': 'Clothing & Accessories',
            'description': 'White cotton lab coat.',
            'location': 'Engineering Workshop',
            'item_date': '2026-10-20'
        }
        found = {
            'id': 21,
            'title': 'Lab Coat',
            'category': 'Clothing & Accessories',
            'description': 'White cotton lab coat.',
            'location': 'Engineering Workshop',
            'item_date': '2026-10-05'  # 15 days before it was reported lost!
        }

        result = evaluate_match(lost, found)
        self.assertEqual(result['breakdown']['date']['earned'], 0.0)
        self.assertIn("implausible", result['breakdown']['date']['reason'].lower())

    def test_ranking_candidates(self):
        """Rank multiple candidates and verify descending order."""
        lost = {
            'id': 1,
            'type': 'lost',
            'title': 'Apple AirPods Pro 2',
            'category': 'Electronics & Gadgets',
            'description': 'White case with initials AJ.',
            'location': 'Student Activity Center (SAC)',
            'item_date': '2026-10-15'
        }

        candidates = [
            # Poor match: water bottle
            {
                'id': 2,
                'type': 'found',
                'title': 'Red Water Bottle',
                'category': 'Bottles & Tumblers',
                'description': 'Plastic bottle.',
                'location': 'Parking Area',
                'item_date': '2026-10-16'
            },
            # Strong match: AirPods
            {
                'id': 3,
                'type': 'found',
                'title': 'AirPods Pro with White Case',
                'category': 'Electronics & Gadgets',
                'description': 'Found in SAC lounge.',
                'location': 'Student Activity Center (SAC)',
                'item_date': '2026-10-16'
            }
        ]

        matches = find_matches_for_item(lost, candidates, min_score=30.0)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]['found_item_id'], 3)
        self.assertGreaterEqual(matches[0]['total_score'], 70.0)

    def test_missing_and_malformed_fields_handled_safely(self):
        """Engine handles None fields, malformed dates, and empty tokens gracefully."""
        lost = {
            'id': 99,
            'title': '',
            'category': None,
            'description': None,
            'location': None,
            'item_date': 'invalid-date-format'
        }
        found = {
            'id': 100,
            'title': None,
            'category': 'Unknown Category',
            'description': 'Some description',
            'location': 'Unknown Location',
            'item_date': None
        }

        # Must not raise an unhandled exception
        result = evaluate_match(lost, found)
        self.assertIsNotNone(result)
        self.assertEqual(result['tier'], 'Low')
        self.assertLess(result['total_score'], 30.0)

if __name__ == '__main__':
    unittest.main()
