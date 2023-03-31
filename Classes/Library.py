import json
from Classes.Catalog import Catalog
from Classes.BookItem import BookItem


class Library:
    def __init__(self):
        self.catalog = Catalog()
        self.book_items = []
        self.get_book_items()

    def get_book_items(self):
        """ This method retrieves book items from a JSON file if it is not empty.
        Otherwise, it initializes book items based on the books in the library's catalog."""
        file_path = "Data/BookItems.json"
        book_items = []
        try:
            with open(file_path) as file:
                book_items = json.load(file)
                self.book_items.extend(book_items)
        except Exception as e:
            books = self.catalog.get_books()
            for book in books:
                book_item = BookItem(book['ISBN'], book).__dict__
                book_items.append(book_item)
            self.update_book_items(book_items)
        self.book_items = book_items

    def update_book_items(self, book_items):
        file_path = "Data/BookItems.json"
        with open(file_path, 'w') as file:
            json.dump(book_items, file, indent=2)

    def get_book_item_by_user_input(self):
        sorted_book_items = self.print_all_book_items(should_sort=True, only_available_items=True)
        book_id = int(input("\nGive the identity of the book you would like to move forward with: ").strip()) - 1
        if 0 <= book_id <= len(sorted_book_items):
            book_item = sorted_book_items[book_id]
            return book_item
        else:
            raise ValueError(f"Your input ({book_id}) is invalid.")

    def print_all_book_items(self, should_sort=False, only_available_items=False):
        """
        Prints information about all book items in the library.

        Arguments:
        should_sort -- If True, sorts the book items by book title (default False).
        only_available_items -- If True, only shows book items that are available (default False).
        """
        print("")
        book_items = self.book_items
        if should_sort:
            book_items = sorted(book_items, key=lambda b: b['book']['title'])
        if only_available_items:
            book_items = [b for b in book_items if b['copies'] > 0]
        for count, book_item in enumerate(book_items, start=1):
            print(
                f"    [{count}] {book_item['copies']}x - {book_item['book']['title']} by {book_item['book']['author']}")
        if should_sort:
            return book_items

    def get_book_item_index_by_ISBN(self, ISBN):
        index = -1
        book_items = self.book_items
        for i in range(len(book_items)):
            if book_items[i]['book']['ISBN'] == ISBN:
                index = i
                break
        return index

