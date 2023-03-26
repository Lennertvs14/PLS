class BookItem:
    def __init__(self, book_isbn, book, copies=5):
        self.ISBN = book_isbn
        self.book = book
        self.copies = copies

    @property
    def is_available(self):
        if self.copies > 0:
            return True
        else:
            return False
