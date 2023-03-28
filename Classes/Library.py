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
        sorted_book_items = self.print_all_book_items(should_sort=True)
        book_id = int(input("\nGive the identity of the book you would like to move forward with: ").strip()) - 1
        if 0 <= book_id <= len(sorted_book_items):
            book_item = sorted_book_items[book_id]
            return book_item
        else:
            raise ValueError("The chosen book item does not exist after all")

    def print_all_book_items(self, should_sort=False):
        print("")
        book_items = self.book_items
        if should_sort:
            book_items = sorted(book_items, key=lambda b: b['book']['title'])
        for count, book_item in enumerate(book_items, start=1):
            print(
                f"    [{count}] {book_item['copies']}x - {book_item['book']['title']} by {book_item['book']['author']}")
        if should_sort:
            return book_items

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

    def get_book_item_index_by_ISBN(self, ISBN):
        index = -1
        book_items = self.book_items
        for i in range(len(book_items)):
            if book_items[i]['book']['ISBN'] == ISBN:
                index = i
                break
        return index

