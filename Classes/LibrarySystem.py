import csv
import json
from Classes.Library import Library
from Classes.Catalog import Catalog


class LibrarySystem:
    # TODO: Library system should hold a list of loan items as well, for the generic logic and class diagram.
    def __init__(self):
        self.library = Library()
        self.catalog = Catalog()
        self.loan_items = self.get_data("Data/LoanItems.json")

    def get_data(self, file_path):
        try:
            with open(file_path) as file:
                data = json.load(file)
            return data
        except Exception as e:
            return []

    def get_csv_data(self, file_path):
        filepath_is_empty = file_path is None or file_path == "" or not isinstance(file_path, str)
        if not filepath_is_empty:
            with open(file_path) as file:
                items = list(csv.DictReader(file, delimiter=";"))
            
            for item in items:
                for row in item:
                    if row == "Number":
                        item[row] = int(item[row].strip())
            return items
        else:
            print("Invalid file path.")
    
    def update_data(self, file_path, data_dict):
        filepath_is_empty = file_path is None or file_path == "" or not isinstance(file_path, str)
        if not filepath_is_empty:
            with open(file_path, 'w') as file:
                json.dump(data_dict, file, indent=2)
        else:
            print("Invalid file path.")
