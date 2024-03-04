class Patron:
    def __init__(self, name, patron_id, contact_info):
        self.name = name
        self.patron_id = patron_id
        self.contact_info = contact_info

    def display(self):
        print(f"Name: {self.name}, ID: {self.patron_id}, Contact: {self.contact_info}")
