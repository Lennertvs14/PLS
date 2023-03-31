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

    def return_book_item(self, book_item_to_return, member_id):
        # Get library book item instance
        library_book_item = None
        for book_item in self.library.book_items:
            if book_item_to_return['ISBN'] == book_item['ISBN']:
                library_book_item = book_item
        # Update the library
        if library_book_item is not None:
            library_book_item['copies'] += 1
            self.library.update_book_items(self.library.book_items)
            # Update the loan items' data storage file.
            loan_items = self.__get_all_loan_items()
            for loan_item in loan_items:
                members_are_equal = str(loan_item['borrower']) == str(member_id)
                international_standard_book_numbers_are_equal = str(loan_item['book_item']['ISBN']) == str(library_book_item['ISBN'])
                if members_are_equal and international_standard_book_numbers_are_equal:
                    loan_items.remove(loan_item)
            self.__update_loan_items(loan_items)
        else:
            raise ValueError("This library did not loan this book to you.")

    def __get_all_loan_items(self):
        import json
        file_path = "Data/LoanItems.json"
        with open(file_path) as file:
            loan_items = json.load(file)
        return loan_items

    def __update_loan_items(self, loan_items_dict):
        import json
        file_path = "Data/LoanItems.json"
        with open(file_path, 'w') as file:
            json.dump(loan_items_dict, file, indent=2)
