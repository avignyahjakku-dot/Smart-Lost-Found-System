"""
CampusFind - Automated Test Suite Runner
========================================
Discovers and executes all unit and integration tests across:
- Binary Search Tree (BST) algorithms and operations
- Multi-factor smart similarity matching
- User authentication and role-based permissions
- Lost and found item reporting and filtering
- Claim submissions and administrator moderation
"""

import sys
import unittest
import os

def run_all_tests():
    print("=" * 70)
    print(" CampusFind (Smart Lost & Found System) — Automated Test Suite")
    print("=" * 70)

    # Set testing environment
    os.environ['FLASK_ENV'] = 'testing'

    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.dirname(__file__), 'tests')
    suite = loader.discover(start_dir, pattern='test_*.py')

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 70)
    print(f" Tests Run: {result.testsRun}")
    print(f" Errors:    {len(result.errors)}")
    print(f" Failures:  {len(result.failures)}")
    print("=" * 70)

    if result.wasSuccessful():
        print("[SUCCESS] ALL TESTS PASSED SUCCESSFULLY!")
        return 0
    else:
        print("[FAILED] SOME TESTS ENCOUNTERED ERRORS OR FAILURES.")
        return 1

if __name__ == '__main__':
    exit_code = run_all_tests()
    sys.exit(exit_code)
