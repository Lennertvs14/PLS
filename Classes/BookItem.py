class BookItem:
    # TODO: Make a BookItem inherit from book and leave the book object out of the attributes, if that's possible.
    #  This will also fix the double ISBN data issue.
    def __init__(self, book_isbn, book, copies=5):
        self.ISBN = book_isbn
        self.book = book
        self.copies = copies # TODO: copies -> hard_copies

    @property
    def is_available(self):
        if self.copies > 0:
            return True
        else:
            return False
