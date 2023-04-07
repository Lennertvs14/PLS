import csv
from Classes.Library import Library
from Classes.Catalog import Catalog
import json


class LibrarySystem:
    def __init__(self):
        self.library = Library()
        self.catalog = Catalog()

    def get_data(self, file_path):
        filepath_is_empty = file_path is None or file_path == "" or not isinstance(file_path, str)
        if not filepath_is_empty:
            with open(file_path) as file:
                loan_items = json.load(file)
            return loan_items
        else:
            print("Invalid file path.")

    def get_csv_data(self, file_path):
        filepath_is_empty = file_path is None or file_path == "" or not isinstance(file_path, str)
        if not filepath_is_empty:
            with open(file_path) as file:
                loan_items = csv.DictReader(file)
            return loan_items
        else:
            print("Invalid file path.")

    def update_data(self, file_path, data_dict):
        filepath_is_empty = file_path is None or file_path == "" or not isinstance(file_path, str)
        if not filepath_is_empty:
            with open(file_path, 'w') as file:
                json.dump(data_dict, file, indent=2)
        else:
            print("Invalid file path.")
