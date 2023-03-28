from datetime import datetime, timedelta
import json


class LoanItem:
    def __init__(self, member, book_item):
        self.borrower = member.id
        self.book_item = book_item
        self.loan_date = datetime.now().strftime("%Y-%m-%d")
        self.return_date = None
        self.store_loan_item()

    @property
    def due_date(self):
        return (datetime.strptime(self.loan_date, "%Y-%m-%d") + timedelta(days=60)).strftime("%Y-%m-%d")

    def store_loan_item(self):
        if self.book_item is not None:
            file_path = "Data/LoanItems.json"
            loan_items = []
            try:
                with open(file_path) as file:
                    loan_items = json.load(file)
            except Exception as e:
                print("")
            finally:
                loan_items.append(self.__dict__)
                with open(file_path, 'w') as file:
                    json.dump(loan_items, file, indent=2)
        else:
            raise ValueError("There's no valid book item to loan.")

    def is_overdue(self):
        due_date = datetime.strptime(self.due_date, "%Y-%m-%d")
        return datetime.now() > due_date

