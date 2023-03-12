import json
from Classes.Book import Book

class Catalog:
    def __init__(self):
        self.books = self.__get_books()

    @staticmethod
    def __get_books():
        file_path = "Data/Books.json"
        with open(file_path) as file:
            books = json.load(file)
        return books

    def print_all_books(self):
        count = 0
        for book in self.books:
            print(f"[{count+1}] {book['title']} by {book['author']}")
            count += 1

    def search_for_book(self):
        """ This search function accepts a book title or author as search key. """
        search_term = input("Enter search term: ").lower()
        matching_books = []
        for book in self.books:
            if search_term in book["author"].lower() or search_term in book["title"].lower():
                matching_books.append(book)
        if matching_books:
            print(f"Found {len(matching_books)} matching book(s):")
            for book in matching_books:
                print(f"    {book['title']} by {book['author']}")
        else:
            print("No matching books found.")

    def add_book(self):
        new_book = self.create_book_by_user_input()
        new_book = Book(**new_book)
        self.books.append(new_book)
        self.update_books(books)

    def create_book_by_user_input(self):
        empty_book_object = Book("", "", "", "", "", 0, "", "", "")
        field_names = [attr for attr in dir(empty_book_object)
                       if not callable(getattr(empty_book_object, attr)) and not attr.startswith("__")]
        new_book = {}
        for field_name in field_names:
            while True:
                value = input(f"Please enter the {field_name}: ")
                if empty_book_object.validate_field(field_name, value):
                    new_book[field_name] = value
                    break
                else:
                    print(f"Invalid {field_name} value, please try again.")
        return new_book

    def update_books(self, books):
        