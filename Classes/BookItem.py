from Classes.Book import Book


class BookItem(Book):
    def __init__(self, book, printed_copies=5):
        super().__init__(book['author'], book['country'], book['imageLink'], book['language'], book['link'],
                         book['pages'], book['title'], book['ISBN'], book['year'])
        self.printed_copies = printed_copies

    @property
    def is_available(self):
        if self.printed_copies > 0:
            return True
        else:
            return False

    def get_book_item_data(self):
        """ Get the book item's ISBN and printed copies formatted as a dictionary. """
        return {
            'title': self.title[0],
            'author': self.author[0],
            'ISBN': self.ISBN[0],
            'printed_copies': self.printed_copies
        }

