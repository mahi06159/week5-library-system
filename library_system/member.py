# library_system/member.py

class Member:
    """Represents a library member, capable of borrowing books."""
    
    MAX_BOOKS = 5  # Class Variable: Maximum number of books a member can borrow

    def __init__(self, name, member_id):
        """
        Initializes a new Member object.
        member_id should be unique (e.g., 'MEM001').
        """
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []  # Instance Variable: Stores a list of book ISBNs
        
    def can_borrow(self):
        """Checks if the member is eligible to borrow another book."""
        return len(self.borrowed_books) < self.MAX_BOOKS

    def borrow_book(self, isbn):
        """Adds a book (by ISBN) to the member's list of borrowed books."""
        if not self.can_borrow():
            return False, f"Maximum book limit ({self.MAX_BOOKS}) reached."
        
        self.borrowed_books.append(isbn)
        return True, f"Book (ISBN: {isbn}) successfully borrowed."

    def return_book(self, isbn):
        """Removes a book (by ISBN) from the member's list of borrowed books."""
        if isbn in self.borrowed_books:
            self.borrowed_books.remove(isbn)
            return True, f"Book (ISBN: {isbn}) successfully returned."
        
        return False, f"Error: Member {self.member_id} did not borrow book with ISBN: {isbn}."

    def to_dict(self):
        """Converts the member object to a dictionary for JSON serialization."""
        return {
            'name': self.name,
            'member_id': self.member_id,
            'borrowed_books': self.borrowed_books,
        }
    
    @classmethod
    def from_dict(cls, data):
        """Creates a Member instance from a dictionary loaded from JSON."""
        member = cls(
            name=data['name'],
            member_id=data['member_id']
        )
        member.borrowed_books = data.get('borrowed_books', [])
        return member
    
    def __str__(self):
        return f"Member ID: {self.member_id}, Name: {self.name}, Books Borrowed: {len(self.borrowed_books)}"
