# library_system/library.py

import json
import os
from .book import Book # Assuming book.py is in the same package
from .member import Member

class Library:
    """Manages the collection of books and members, and handles all transactions."""

    BOOKS_FILE = 'data/books.json'
    MEMBERS_FILE = 'data/members.json'

    def __init__(self):
        """Initializes the library with empty collections and loads data."""
        # Dictionaries map unique IDs (ISBN, member_id) to objects
        self.books = {}    # Key: ISBN, Value: Book object
        self.members = {}  # Key: member_id, Value: Member object
        self.load_data()
        
    # --- Data Persistence Methods ---

    def _get_file_path(self, filename):
        """Helper to construct absolute path for data files."""
        # Adjusting for the 'data' directory relative to the project root
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_dir, filename)

    def load_data(self):
        """Loads books and members from JSON files."""
        # Load Books
        books_path = self._get_file_path(self.BOOKS_FILE)
        if os.path.exists(books_path):
            with open(books_path, 'r') as f:
                data = json.load(f)
                for isbn, book_data in data.items():
                    self.books[isbn] = Book.from_dict(book_data)
        
        # Load Members
        members_path = self._get_file_path(self.MEMBERS_FILE)
        if os.path.exists(members_path):
            with open(members_path, 'r') as f:
                data = json.load(f)
                for member_id, member_data in data.items():
                    self.members[member_id] = Member.from_dict(member_data)
        
        print(f"\nLoaded {len(self.books)} books and {len(self.members)} members from file.")

    def save_data(self):
        """Saves books and members data to JSON files."""
        # Ensure data directory exists
        data_dir = os.path.dirname(self._get_file_path(self.BOOKS_FILE))
        os.makedirs(data_dir, exist_ok=True)

        # Save Books
        books_data = {isbn: book.to_dict() for isbn, book in self.books.items()}
        with open(self._get_file_path(self.BOOKS_FILE), 'w') as f:
            json.dump(books_data, f, indent=4)
            
        # Save Members
        members_data = {mid: member.to_dict() for mid, member in self.members.items()}
        with open(self._get_file_path(self.MEMBERS_FILE), 'w') as f:
            json.dump(members_data, f, indent=4)
            
        print("\nData saved successfully.")
        
    # --- Book Management Methods ---

    def add_book(self, book):
        """Adds a new Book object to the library collection."""
        if book.isbn in self.books:
            return False, "Error: Book with this ISBN already exists."
        self.books[book.isbn] = book
        return True, f"Book '{book.title}' added successfully."

    def find_book(self, isbn):
        """Returns a Book object given its ISBN, or None."""
        return self.books.get(isbn)

    # --- Member Management Methods ---
    
    def register_member(self, member):
        """Registers a new Member object."""
        if member.member_id in self.members:
            return False, "Error: Member ID already registered."
        self.members[member.member_id] = member
        return True, f"Member '{member.name}' registered with ID {member.member_id}."

    def find_member(self, member_id):
        """Returns a Member object given its ID, or None."""
        return self.members.get(member_id)

    # --- Core Transaction Methods ---

    def borrow_book(self, isbn, member_id):
        """Handles the book borrowing transaction."""
        book = self.find_book(isbn)
        member = self.find_member(member_id)

        if not book:
            return False, "Book not found."
        if not member:
            return False, "Member not found."

        # 1. Check if the book is available and update book state
        success_book, msg_book = book.check_out(member_id)
        if not success_book:
            return False, msg_book

        # 2. Check member limit and update member state
        success_member, msg_member = member.borrow_book(isbn)
        if not success_member:
            # If member failed, revert book state to avoid inconsistency
            book.return_book() 
            return False, msg_member
            
        return True, f"SUCCESS: Book '{book.title}' borrowed by {member.name}. Due: {book.due_date}"

    def return_book(self, isbn, member_id):
        """Handles the book return transaction."""
        book = self.find_book(isbn)
        member = self.find_member(member_id)

        if not book:
            return False, "Book not found."
        if not member:
            return False, "Member not found."
        
        # Double check consistency
        if book.borrowed_by != member_id or isbn not in member.borrowed_books:
            return False, "Error: Borrow records are inconsistent. Check book status."

        # 1. Update book state and check for overdue
        success_book, msg_book = book.return_book()

        # 2. Update member state
        success_member, msg_member = member.return_book(isbn)
        
        # 3. Handle potential fine calculation (simplified for now)
        fine_msg = ""
        if "was overdue" in msg_book:
            days = book.days_overdue()
            # Simple fine calculation: $0.50 per day overdue
            fine = days * 0.50
            fine_msg = f" Note: Book was overdue by {days} days. Fine: ${fine:.2f}"
            
        return True, f"SUCCESS: Book returned. {msg_book}.{fine_msg}"
        
    # --- Reporting Methods (Example) ---
    
    def get_overdue_books(self):
        """Returns a list of all currently overdue Book objects."""
        overdue_books = []
        for book in self.books.values():
            if book.is_overdue():
                overdue_books.append(book)
        return overdue_books
        
    def get_stats(self):
        """Returns basic library statistics."""
        available = sum(1 for book in self.books.values() if book.available)
        borrowed = len(self.books) - available
        overdue = len(self.get_overdue_books())
        
        return {
            "Total Books": len(self.books),
            "Available Books": available,
            "Total Members": len(self.members),
            "Books Borrowed": borrowed,
            "Overdue Books": overdue
        }
