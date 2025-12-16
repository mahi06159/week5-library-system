# tests/test_library.py

import unittest
import os
# Adjust the imports based on your actual structure
from library_system.library import Library
from library_system.book import Book
from library_system.member import Member

# Define test file paths (must match paths in library.py)
TEST_BOOKS_FILE = 'data/test_books.json'
TEST_MEMBERS_FILE = 'data/test_members.json'

class TestLibrary(unittest.TestCase):
    """Tests the Library class methods, focusing on transactions and data management."""

    def setUp(self):
        """
        Set up a fresh, empty Library instance for each test.
        Uses temporary file paths to avoid corrupting real data.
        """
        # Temporarily override file paths for testing isolation
        Library.BOOKS_FILE = TEST_BOOKS_FILE
        Library.MEMBERS_FILE = TEST_MEMBERS_FILE
        
        self.library = Library()
        
        # Ensure temporary files are clean
        if os.path.exists(TEST_BOOKS_FILE):
            os.remove(TEST_BOOKS_FILE)
        if os.path.exists(TEST_MEMBERS_FILE):
            os.remove(TEST_MEMBERS_FILE)
            
        self.library.books = {}
        self.library.members = {}

        # Setup base objects
        self.book1 = Book("Python Intro", "G. Guido", "B001", 2000)
        self.book2 = Book("Web Dev", "H. Harvey", "B002", 2020)
        self.member1 = Member("John Doe", "M001")
        self.member2 = Member("Jane Smith", "M002")
        
        self.library.add_book(self.book1)
        self.library.register_member(self.member1)

    def tearDown(self):
        """Clean up test files after each test."""
        if os.path.exists(TEST_BOOKS_FILE):
            os.remove(TEST_BOOKS_FILE)
        if os.path.exists(TEST_MEMBERS_FILE):
            os.remove(TEST_MEMBERS_FILE)

    def test_add_and_find(self):
        """Test adding and finding books and members."""
        # Book tests
        self.assertIsNotNone(self.library.find_book("B001"))
        self.assertIsNone(self.library.find_book("B999"))
        # Member tests
        self.assertIsNotNone(self.library.find_member("M001"))
        self.assertIsNone(self.library.find_member("M999"))

    def test_borrow_success(self):
        """Test a successful borrowing transaction."""
        success, msg = self.library.borrow_book("B001", "M001")
        self.assertTrue(success)
        self.assertFalse(self.book1.available)
        self.assertIn("B001", self.member1.borrowed_books)
        self.assertEqual(len(self.member1.borrowed_books), 1)

    def test_borrow_limit_failure(self):
        """Test borrowing when the member is at their limit."""
        # Manually make the member borrow 5 books (the limit)
        self.member1.borrowed_books = ["1", "2", "3", "4", "5"] 
        self.library.add_book(self.book2)

        success, msg = self.library.borrow_book("B002", "M001")
        
        self.assertFalse(success)
        self.assertIn("Maximum book limit", msg)
        self.assertTrue(self.book2.available) # Book state must be reverted!

    def test_return_success(self):
        """Test a successful return transaction."""
        self.library.borrow_book("B001", "M001")
        
        success, msg = self.library.return_book("B001", "M001")
        self.assertTrue(success)
        self.assertTrue(self.book1.available)
        self.assertNotIn("B001", self.member1.borrowed_books)
        self.assertIn("returned successfully", msg)

    def test_persistence_save_load(self):
        """Test saving data to JSON and loading it back."""
        # 1. Perform transaction on the current library instance
        self.library.add_book(self.book2)
        self.library.register_member(self.member2)
        self.library.borrow_book("B001", "M001")
        
        # 2. Save data
        self.library.save_data()
        
        # 3. Create a NEW library instance to simulate restart
        new_library = Library()
        
        # 4. Verify data was loaded correctly
        self.assertEqual(len(new_library.books), 2)
        self.assertEqual(len(new_library.members), 2)
        
        loaded_book1 = new_library.find_book("B001")
        loaded_member1 = new_library.find_member("M001")

        self.assertFalse(loaded_book1.available) # State must be borrowed
        self.assertIn("B001", loaded_member1.borrowed_books) # Member list must be correct

if __name__ == '__main__':
    unittest.main()
