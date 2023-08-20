from Classes.BookItem import BookItem
import json


class Library:
    def __init__(self):
        self.book_items = []
        self.initialize_book_items()

    def initialize_book_items(self):
        """
        This method retrieves book items from a JSON file if it is not empty.
        Otherwise, it initializes book items based on the books in the library's catalog.
        """
        from Classes.Catalog import Catalog
        book_items = []
        try:
            book_items = self.get_book_items()
            self.book_items.extend(book_items)
        except Exception as e:
            catalog = Catalog()
            books = catalog.books
            for book in books:
                book_item = BookItem(book).get_book_item_data()
                book_items.append(book_item)
            self.update_book_items(book_items)
        self.book_items = book_items

    def get_book_items(self):
        file_path = "Data/BookItems.json"
        with open(file_path) as file:
            loan_items = json.load(file)
        return loan_items

    def update_book_items(self, book_items_dict):
        file_path = "Data/BookItems.json"
        with open(file_path, 'w') as file:
            json.dump(book_items_dict, file, indent=2)

    def get_book_item_by_user_input(self):
        sorted_book_items = self.print_all_book_items(should_sort=True, only_available_items=True)
        if sorted_book_items:
            book_id = int(input("\nGive the identity of the book you would like to move forward with: ").strip()) - 1
            if 0 <= book_id <= len(sorted_book_items):
                book_item = sorted_book_items[book_id]
                return book_item
            else:
                print(f"Your input ({book_id+1}) is invalid.")
                input("Press the enter key on your key board to try again.")
                return self.get_book_item_by_user_input()
        else:
            # There are no book items available
            pass

    def print_all_book_items(self, should_sort=False, only_available_items=False):
        """
        Prints information about all book items in the library.

        Arguments:
        should_sort -- If True, sorts the book items by book title (default False).
        only_available_items -- If True, only shows book items that are available (default False).
        """
        book_items = self.book_items
        if should_sort:
            book_items = sorted(book_items, key=lambda b: b['title'])
        if only_available_items:
            book_items = [b for b in book_items if b['printed_copies'] > 0]
        if book_items:
            print("")
            for count, book_item in enumerate(book_items, start=1):
                print(
                    f"    [{count}] {book_item['printed_copies']}x - {book_item['title']} by {book_item['author']}")
            if should_sort:
                return book_items
        else:
            print("There are no book items available.")
            return False

    def get_book_item_index_by_book_id(self, international_standard_book_number):
        index = -1
        book_items = self.book_items
        for i in range(len(book_items)):
            if book_items[i]['ISBN'] == international_standard_book_number:
                index = i
                break
        return index

