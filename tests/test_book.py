# tests/test_book.py

import unittest
from datetime import datetime, timedelta
# Adjust the import based on your actual structure (e.g., from library_system.book import Book)
from library_system.book import Book 

class TestBook(unittest.TestCase):
    """Tests the core functionalities and state management of the Book class."""

    def setUp(self):
        """Set up a fresh Book object before each test."""
        self.test_book = Book("The Test Book", "A. Tester", "1234567890", 2023)
        self.member_id = "MEM001"
        
    def test_initial_state(self):
        """Verify the book is correctly initialized as available."""
        self.assertTrue(self.test_book.available)
        self.assertIsNone(self.test_book.borrowed_by)
        self.assertIsNone(self.test_book.due_date)

    def test_check_out_success(self):
        """Test successful checkout and state change."""
        success, msg = self.test_book.check_out(self.member_id, loan_period=1) # 1 day loan for easy testing
        self.assertTrue(success)
        self.assertFalse(self.test_book.available)
        self.assertEqual(self.test_book.borrowed_by, self.member_id)
        self.assertIsNotNone(self.test_book.due_date)

    def test_check_out_already_borrowed(self):
        """Test failure when attempting to check out an already borrowed book."""
        self.test_book.check_out(self.member_id)
        success, msg = self.test_book.check_out("MEM002")
        self.assertFalse(success)
        self.assertIn("already checked out", msg)
        self.assertEqual(self.test_book.borrowed_by, self.member_id) # Should still be MEM001

    def test_return_book_success(self):
        """Test successful return of a book."""
        self.test_book.check_out(self.member_id)
        success, msg = self.test_book.return_book()
        self.assertTrue(success)
        self.assertTrue(self.test_book.available)
        self.assertIsNone(self.test_book.borrowed_by)
        self.assertIn("returned successfully", msg)
        
    def test_return_book_already_available(self):
        """Test failure when attempting to return an available book."""
        success, msg = self.test_book.return_book()
        self.assertFalse(success)
        self.assertIn("already available", msg)

    def test_is_overdue_logic(self):
        """Test if the overdue calculation works correctly."""
        # 1. Check out with a due date in the past (e.g., 5 days ago)
        past_due_date = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')
        
        # Manually set the state for testing overdue
        self.test_book.available = False
        self.test_book.borrowed_by = self.member_id
        self.test_book.due_date = past_due_date
        
        self.assertTrue(self.test_book.is_overdue())
        self.assertEqual(self.test_book.days_overdue(), 5) # Should calculate 5 days overdue

if __name__ == '__main__':
    unittest.main()
