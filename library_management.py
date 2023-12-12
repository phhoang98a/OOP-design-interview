from abc import ABC
from enum import Enum
from datetime import datetime

class BookStatus(Enum):
    AVAILABLE, RESERVED, LOANED, LOST = 1, 2, 3, 4

class AccountStatus(Enum):
    ACTIVE, CLOSED, CANCELED, BLACKLISTED, NONE = 1, 2, 3, 4, 5

class Constants:
    def __init__(self):
        self.MAX_BOOKS_ISSUED_TO_A_USER = 5
        self.MAX_LENDING_DAY = 10
        
class Book():
    def __init__(self, id, tittle, author, status, fee):
        self.id = id
        self.tittle = tittle
        self.author = author
        self.status = status
        self.borrow_by = None
        self.fee = fee
        self.due_date = None

    def update_status(self, status):
        self.status = status

    def update_borrow_by(self, memberID):
        self.borrow_by = memberID

    def reset_due_date(self):
        self.due_date = None
    
    def update_due_date(self):
        today = datetime.date.today()
        self.due_date = today + datetime.timedelta(days=Constants.MAX_LENDING_DAY)

class Account(ABC):
    def __init__(self, id, password, name, email, status=AccountStatus.ACTIVE):
        self.id = id
        self.password = password
        self.name = name
        self.email =email
        self.status = status

class Librarian(Account):
    def __init__(self, id, password, name, email, status=AccountStatus.ACTIVE):
        super().__init__(id, password, name, email, status)

class Member(Account):
    def __init__(self, id, password, name, email, status=AccountStatus.ACTIVE):
        super().__init__(id, password, name, email, status)
        self.total_books_borrowed = 0
        self.borrowed_fee = 0
    
    def increase_total_books_borrowed(self):
        self.total_books_borrowed +=1
    
    def decrease_total_books_borrowed(self):
        self.total_books_borrowed +=1

    def update_borrowed_fee(self, fee_of_book):
        self.borrowed_fee += fee_of_book

    # check-out books
    def checkout_books(self, books):
        if len(books)>= Constants.MAX_BOOKS_ISSUED_TO_A_USER:
            print("The member has borrowed over the allowed number of books")
            return
        for book in books:
            if book.status == BookStatus.RESERVED:
                continue
            book.update_status(BookStatus.LOANED)
            book.update_borrow_by(self.id)
            book.update_due_date()
            self.increase_total_books_borrowed()
            self.update_due_date()
            self.update_borrowed_fee(book.fee)
    
    def calculateFineFee(self):
        None
            
    # return a book
    def return_books(self, book):
        if book.borrow_by != self.id:
            print("This book did not borrowed by the member")
            return
        today = datetime.date.today()
        diff = today - book.due_date
        if diff.days >= Constants.MAX_LENDING_DAY:
            self.borrowed_fee += self.calculateFineFee()
 
        book.update_status(BookStatus.AVAILABLE)
        book.update_borrow_by(None)
        book.reset_due_date()
        self.decrease_total_books_borrowed()
        

