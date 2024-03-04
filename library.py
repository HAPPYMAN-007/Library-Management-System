import json
from book import Book
from patron import Patron
from transaction import Transaction

class Library:
    def __init__(self):
        self.books = self.load_books()
        self.patrons = self.load_patrons()
        self.transactions = []

    def load_books(self):
        try:
            with open('books.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_books(self):
        with open('books.json', 'w') as f:
            json.dump(self.books, f, indent=4)

    def load_patrons(self):
        try:
            with open('patrons.json', 'r') as f:
                patrons = json.load(f)
        except FileNotFoundError:
            patrons = {}

        # Check if the administrator exists, if not, create one
        admin_id = "admin-001"  # Sample user ID for the administrator
        if admin_id not in patrons:
            print(f"Creating default administrator account with ID: {admin_id}")
            # Adding a default administrator
            patrons[admin_id] = {
                "name": "Admin User",
                "patron_id": admin_id,
                "contact_info": "admin@example.com",
                "role": "administrator"
            }
            self.save_patrons(patrons)

        return patrons

    def save_patrons(self, patrons=None):
        if patrons is None:
            patrons = self.patrons
        with open('patrons.json', 'w') as f:
            json.dump(patrons, f, indent=4)


    def add_book(self, book, current_user_id):
        current_user = self.patrons.get(current_user_id)
        if current_user and current_user['role'] in ['librarian', 'administrator']:
            if book.isbn in self.books:
                print("Book already exists. Updating quantity.")
                self.books[book.isbn]['quantity'] += book.quantity
            else:
                self.books[book.isbn] = vars(book)
            self.save_books()
        else:
            print("You do not have permission to add books.")

    def remove_book(self, isbn, current_user_id):
        current_user = self.patrons.get(current_user_id)
        if current_user and current_user['role'] in ['librarian', 'administrator']:
            if isbn in self.books:
                del self.books[isbn]
                self.save_books()
                print(f"Book {isbn} removed.")
            else:
                print("Book not found.")
        else:
            print("You do not have permission to remove books.")

    def add_patron(self, patron, current_user_id):
        current_user = self.patrons.get(current_user_id)
        if current_user and current_user['role'] == 'administrator':
            self.patrons[patron.patron_id] = vars(patron)
            self.save_patrons()
        else:
            print("You do not have permission to add patrons.")

    def remove_patron(self, patron_id, current_user_id):
        current_user = self.patrons.get(current_user_id)
        if current_user and current_user['role'] == 'administrator':
            if patron_id in self.patrons:
                del self.patrons[patron_id]
                self.save_patrons()
                print(f"Patron {patron_id} removed.")
            else:
                print("Patron not found.")
        else:
            print("You do not have permission to remove patrons.")

    def set_user_role(self, patron_id, new_role, current_user_id):
        current_user = self.patrons.get(current_user_id)
        if current_user and current_user['role'] == 'administrator':
            if patron_id in self.patrons:
                self.patrons[patron_id]['role'] = new_role
                self.save_patrons()
                print(f"Updated role for {patron_id} to {new_role}.")
            else:
                print("Patron not found.")
        else:
            print("You do not have permission to change user roles.")

    def checkout_book(self, isbn, patron_id, current_user_id):
        current_user = self.patrons.get(current_user_id)
        # Verify current user is a registered patron (or higher role) for checkout.
        if not current_user or current_user['role'] not in ['patron', 'librarian', 'administrator']:
            print("You do not have permission to checkout books.")
            return

        if isbn not in self.books or self.books[isbn]['quantity'] <= 0:
            print("Book not available for checkout.")
            return

        self.books[isbn]['quantity'] -= 1
        self.save_books()
        # Assuming Transaction class exists and handles transaction details.
        transaction = Transaction(isbn, patron_id)
        self.transactions.append(vars(transaction))
        print(f"Book {isbn} checked out to patron {patron_id}.")

    def return_book(self, isbn, patron_id, current_user_id):
        current_user = self.patrons.get(current_user_id)
        # Verify current user is a registered patron (or higher role) for returns.
        if not current_user or current_user['role'] not in ['patron', 'librarian', 'administrator']:
            print("You do not have permission to return books.")
            return

        transaction_found = False
        for transaction in self.transactions:
            if transaction['book_isbn'] == isbn and transaction['patron_id'] == patron_id and not transaction['returned']:
                transaction['returned'] = True
                self.books[isbn]['quantity'] += 1
                self.save_books()
                print(f"Book {isbn} returned.")
                transaction_found = True
                break

        if not transaction_found:
            print("Transaction not found or book was not checked out.")


    def display_books(self):
        for isbn, book in self.books.items():
            print(f"ISBN: {isbn}, Title: {book['title']}, Author: {book['author']}, Quantity: {book['quantity']}")

    def display_patrons(self):
        for patron_id, patron in self.patrons.items():
            print(f"ID: {patron_id}, Name: {patron['name']}, Contact: {patron['contact_info']}, Role: {patron['role']}")
