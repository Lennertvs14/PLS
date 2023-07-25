from datetime import datetime, timedelta
import json


class LoanItem:
    def __init__(self, member_national_insurance_number, book_item):
        self.borrower = member_national_insurance_number
        self.book_item = book_item
        self.loan_date = datetime.now().strftime("%Y-%m-%d")
        self.return_date = (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d")
        self.store_loan_item()

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

    @staticmethod
    def is_overdue(return_date):
        due_date = datetime.strptime(return_date, "%Y-%m-%d")
        return datetime.now() > due_date

