from Classes.LibrarySystem import LibrarySystem
import json


class Person(LibrarySystem):
    def __init__(self):
        super().__init__()
        self.national_insurance_number = self.get_new_national_insurance_number()

    def get_new_national_insurance_number(self):
        """ This function leverages the fact that only administrators add users,
        and thus that member numbers are sequentially ordered. """
        member_identities = self.__get_members_national_insurance_numbers()
        return max(member_identities) + 1

    def __get_members_national_insurance_numbers(self):
        file_path = "Data/Members.json"
        with open(file_path) as file:
            members = json.load(file)
        member_identities = {obj['Number'] for obj in members}
        return member_identities

    def explore_catalog(self):
        """ This function shows all the books from the catalog. """
        self.catalog.print_all_books()

    def search_for_book(self):
        """ This search function is based on user input and accepts a book title or author as search key. """
        search_term = input("Enter book title or author: ").lower()
        matching_books = []
        for book in self.catalog.books:
            if search_term in book["author"].lower() or search_term in book["title"].lower():
                matching_books.append(book)
        if matching_books:
            print(f"    Found {len(matching_books)} matching book(s):")
            for book in matching_books:
                print(f"    {book['title']} by {book['author']}")
        else:
            print("     No matching books found.")

    def explore_library(self):
        """ This function shows all the book items from the library."""
        self.library.print_all_book_items()

    def search_for_book_item(self):
        """ This search function is based on user input and accepts a book title or author as search key. """
        search_term = input("Enter book title or author: ").lower()
        matching_books = []
        for book_item in self.library.book_items:
            if search_term in book_item["author"].lower() or search_term in book_item["title"].lower():
                matching_books.append(book_item)
        if len(matching_books) > 0:
            for book_item in matching_books:
                print(f"    [{book_item['printed_copies']}x] {book_item['title']} by {book_item['author']}")
        else:
            print("    No matching book item found.")
