import json


class Catalog:
    def __init__(self):
        self.books = self.__get_books()

    def __get_books(self):
        try:
            file_path = "Data/Books.json"
            with open(file_path) as file:
                books = json.load(file)
            return books
        except:
            return []

    def print_all_books(self):
        if self.books:
            count = 0
            for book in self.books:
                print(f"[{count + 1}] {book['title']} by {book['author']}")
                count += 1
        else:
            print("There are no books in this library catalog yet.")
