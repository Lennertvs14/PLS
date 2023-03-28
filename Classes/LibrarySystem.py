from Classes.Library import Library
from Classes.Catalog import Catalog
from Classes.LoanItem import LoanItem


class LibrarySystem:
    def __init__(self):
        self.library = Library()
        self.catalog = Catalog()

    def borrow_book_item(self, member, book_item):
        # Create loan_item instance.
        loan_item = LoanItem(member, book_item)
        # Update the library's book items.
        book_item_list_index = self.library.get_book_item_index_by_ISBN(book_item['book']['ISBN'])
        self.library.book_items[book_item_list_index]['copies'] -= 1
        # Update the corresponding json data storage file.
        self.library.update_book_items(self.library.book_items)
        # Give user a success notification.
        print("")
        print(f"You successfully loaned '{book_item['book']['title']}' by {book_item['book']['author']}.")
        print(f"We expect you to return it before {loan_item.due_date}.")
