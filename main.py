from library import Library
from book import Book
from patron import Patron

def main():
    library = Library()
    print("Welcome to the Library Management System")
    current_user_id = input("Enter your user ID to login: ")
    current_user = library.patrons.get(current_user_id, None)

    if not current_user:
        print("User not found. Please contact an administrator.")
        return
    
    print(f"Logged in as: {current_user['name']} ({current_user['role']})")

    while True:
        print("\nAvailable Actions")
        print("1. Display Books")
        print("2. Display Patrons")
        actions = ["1", "2"]

        if current_user['role'] in ['librarian', 'administrator']:
            print("3. Add Book")
            print("4. Remove Book")
            print("5. Add Patron")
            print("6. Remove Patron")
            print("7. Checkout Book")
            print("8. Return Book")
            actions.extend(["3", "4", "5", "6", "7", "8"])

        if current_user['role'] == 'administrator':
            print("9. Set User Role")
            actions.append("9")

        print("0. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "0":
            actions.append("0")

        if choice not in actions:
            print("Invalid choice. Please try again.")
            continue

        if choice == "1":
            library.display_books()
        elif choice == "2":
            library.display_patrons()
        elif choice == "3" and current_user['role'] in ['librarian', 'administrator']:
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            isbn = input("Enter book ISBN: ")
            quantity = int(input("Enter quantity: "))
            book = Book(title, author, isbn, quantity)
            library.add_book(book, current_user_id)
        elif choice == "4" and current_user['role'] in ['librarian', 'administrator']:
            isbn = input("Enter book ISBN to remove: ")
            library.remove_book(isbn, current_user_id)
        elif choice == "5" and current_user['role'] in ['librarian', 'administrator']:
            name = input("Enter patron name: ")
            patron_id = input("Enter patron ID: ")
            contact_info = input("Enter contact info: ")
            role = input("Enter role (patron/librarian/administrator): ")
            patron = Patron(name, patron_id, contact_info, role)
            library.add_patron(patron, current_user_id)
        elif choice == "6" and current_user['role'] in ['librarian', 'administrator']:
            patron_id = input("Enter patron ID to remove: ")
            library.remove_patron(patron_id, current_user_id)
        elif choice == "7" and current_user['role'] in ['librarian', 'administrator']:
            isbn = input("Enter book ISBN to checkout: ")
            patron_id = input("Enter patron ID: ")
            library.checkout_book(isbn, patron_id, current_user_id)
        elif choice == "8" and current_user['role'] in ['librarian', 'administrator']:
            isbn = input("Enter book ISBN to return: ")
            patron_id = input("Enter patron ID: ")
            library.return_book(isbn, patron_id, current_user_id)
        elif choice == "9" and current_user['role'] == 'administrator':
            patron_id = input("Enter patron ID to change role: ")
            new_role = input("Enter new role (patron/librarian/administrator): ")
            library.set_user_role(patron_id, new_role, current_user_id)
        if choice == "0":
            print("Exiting the Library Management System. Goodbye!")
            break
if __name__ == "__main__":
    main()
