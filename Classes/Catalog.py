import json
from Classes.Book import Book

class Catalog:
    def __init__(self):
        self.books = self.get_books()

    @staticmethod
    def get_books():
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