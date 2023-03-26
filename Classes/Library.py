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
            self.update_members(book_items)
        self.book_items = book_items

    def update_members(self, book_items):
        file_path = "Data/BookItems.json"
        with open(file_path, 'w') as file:
            json.dump(book_items, file, indent=2)

    def print_all_book_items(self):
        for book_item in self.book_items:
            print(f"    [{book_item['copies']}x] {book_item['book']['title']} by {book_item['book']['author']}")

    def search_for_book_item(self):
        """ This search function accepts a book title or author as search key. """
        search_term = input("Enter search term: ").lower()
        matching_books = []
        for book_item in self.book_items:
            if search_term in book_item['book']["author"].lower() or search_term in book_item['book']["title"].lower():
                matching_books.append(book_item)
        if len(matching_books) > 0:
            for book_item in matching_books:
                print(f"    [{book_item['copies']}x] {book_item['book']['title']} by {book_item['book']['author']}")
        else:
            print("    No matching book item found.")
