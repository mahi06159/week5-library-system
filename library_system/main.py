# library_system/main.py

from .library import Library
from .book import Book
from .member import Member
# Note: You'd also need a separate utils.py for safe input handling,
# but we'll use simple input() for this draft.

def display_menu():
    """Prints the main application menu."""
    print("\n" + "="*32)
    print("    LIBRARY MANAGEMENT SYSTEM")
    print("="*32)
    print("1. Add New Book")
    print("2. Register New Member")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. Search Books")
    print("6. View Library Statistics")
    print("7. View Overdue Books")
    print("9. Save & Exit")
    print("0. Exit Without Saving")
    print("="*32)

def handle_add_book(library):
    print("\n--- Add New Book ---")
    title = input("Enter Title: ")
    author = input("Enter Author: ")
    isbn = input("Enter ISBN (Unique ID): ")
    # Basic validation for ISBN uniqueness will be handled by Library class
    
    try:
        new_book = Book(title, author, isbn)
        success, message = library.add_book(new_book)
        print(message)
    except Exception as e:
        print(f"Operation failed: {e}")

def handle_register_member(library):
    print("\n--- Register New Member ---")
    name = input("Enter Member Name: ")
    # Simple ID generation/input for demonstration
    member_id = input("Enter Unique Member ID (e.g., MEM001): ") 

    try:
        new_member = Member(name, member_id)
        success, message = library.register_member(new_member)
        print(message)
    except Exception as e:
        print(f"Operation failed: {e}")

def handle_borrow_book(library):
    print("\n--- Borrow Book ---")
    isbn = input("Enter ISBN of the book to borrow: ")
    member_id = input("Enter Member ID: ")
    
    success, message = library.borrow_book(isbn, member_id)
    print(message)

def handle_return_book(library):
    print("\n--- Return Book ---")
    isbn = input("Enter ISBN of the book to return: ")
    member_id = input("Enter Member ID: ")
    
    success, message = library.return_book(isbn, member_id)
    print(message)

def handle_view_stats(library):
    print("\n--- Library Statistics ---")
    stats = library.get_stats()
    print("-" * 25)
    for key, value in stats.items():
        print(f"- {key}: {value}")
    print("-" * 25)

def handle_overdue_books(library):
    print("\n--- Overdue Books ---")
    overdue_list = library.get_overdue_books()
    if not overdue_list:
        print("No books are currently overdue.")
        return
        
    for book in overdue_list:
        member = library.find_member(book.borrowed_by)
        days = book.days_overdue()
        print(f"* '{book.title}' by {book.author}")
        print(f"  Borrowed by: {member.name if member else 'Unknown'}")
        print(f"  Due Date: {book.due_date}, Overdue by: {days} days.")
    
def main():
    """Main function to run the application loop."""
    library = Library()
    
    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            handle_add_book(library)
        elif choice == '2':
            handle_register_member(library)
        elif choice == '3':
            handle_borrow_book(library)
        elif choice == '4':
            handle_return_book(library)
        elif choice == '6':
            handle_view_stats(library)
        elif choice == '7':
            handle_overdue_books(library)
        elif choice == '9':
            # Save and Exit
            library.save_data()
            print("Exiting application. Goodbye!")
            break
        elif choice == '0':
            # Exit Without Saving
            print("Exiting without saving data. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    # This is typically where you would call main() if running main.py directly
    # For a package structure, the run.py (or main entry point) calls this.
    main()
