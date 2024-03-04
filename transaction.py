from datetime import datetime, timedelta

class Transaction:
    def __init__(self, book_isbn, patron_id, check_out_date=None, due_date=None, returned=False):
        self.book_isbn = book_isbn
        self.patron_id = patron_id
        self.check_out_date = check_out_date if check_out_date else datetime.now()
        self.due_date = due_date if due_date else self.check_out_date + timedelta(days=14)  # Assuming 2 weeks loan period
        self.returned = returned

    def mark_as_returned(self):
        self.returned = True
