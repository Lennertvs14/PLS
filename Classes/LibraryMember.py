from Classes.Person import Person
import json
import re


class LibraryMember(Person):
    member_options = [
        "Explore catalog",
        "Search catalog",
        "Explore book items",
        "Search book items",
        "Loan book item",
        "Return book item"
    ]

    def __init__(self, Number, GivenName, Surname, StreetAddress, ZipCode, City,EmailAddress,Username,Password,TelephoneNumber):
        super().__init__()
        self.national_insurance_number = Number
        self.GivenName = GivenName
        self.Surname = Surname
        self.StreetAddress = StreetAddress
        self.ZipCode = ZipCode
        self.City = City
        self.EmailAddress = EmailAddress
        self.Username = Username
        self.Password = Password
        self.TelephoneNumber = TelephoneNumber

    @property
    def borrowed_books(self):
        file_path = "Data/LoanItems.json"
        loan_items_for_member = []
        try:
            with open(file_path) as file:
                loan_items = json.load(file)
                for item in loan_items:
                    if self.national_insurance_number == item['borrower']:
                        loan_items_for_member.append(item)
                return loan_items_for_member
        except Exception as e:
            return None

    def show_interface(self):
        switcher = {
            1: lambda: self.explore_catalog(),
            2: lambda: self.search_for_book(),
            3: lambda: self.explore_library(),
            4: lambda: self.search_for_book_item(),
            5: lambda: self.borrow_book_item(),
            6: lambda: self.return_book_item()
        }
        # Print user's options
        print("\nWhat would you like to do?")
        for i in range(len(self.member_options)):
            print(f" [{i + 1}] {self.member_options[i]}")
        user_input = input("Enter a digit to choose: ").strip()
        # Validate input
        if user_input.isdigit() and 0 < int(user_input) <= len(switcher):
            # Execute
            get_user_choice = switcher.get(int(user_input))
            print("")
            user_choice = get_user_choice()
        else:
            print("Invalid input, please try again.")
            return self.show_interface()

    def borrow_book_item(self, retrieve_loan_item=False):
        """
        Borrow a book item from the library.
        Args:
            retrieve_loan_item (bool): If True, the function will return the loan item object.
        Returns:
            LoanItem or None: If retrieve_loan_item is True, returns the loan item object;
            otherwise, returns None.
        """
        from Classes.LoanItem import LoanItem
        borrowed_books = self.borrowed_books
        max_amount_of_books_to_have = 3
        if borrowed_books is None or len(borrowed_books) < max_amount_of_books_to_have:
            book_item_to_loan = self.library.get_book_item_by_user_input()
            if borrowed_books is not None:
                if self.user_already_borrows_book_item(book_item_to_loan):
                    print("You are already borrowing this book.")
                    return
            if book_item_to_loan:
                loan_item = LoanItem(self.national_insurance_number, book_item_to_loan)
                # Update the library's book items.
                book_item_list_index = self.library.get_book_item_index_by_book_id(book_item_to_loan['ISBN'])
                self.library.book_items[book_item_list_index]['printed_copies'] -= 1
                # Update the corresponding json data storage file.
                self.update_data("Data/BookItems.json", self.library.book_items)
                # Give user a success notification.
                print(f"You successfully loaned '{book_item_to_loan['title']}' "
                      f"by {book_item_to_loan['author']}.")
                print(f"We expect you to return it before {loan_item.return_date}.")
            else:
                # No book item to loan
                return
        else:
            print("You are not allowed to borrow more than 3 books, simultaneously.")
            input("Press the enter key on your key board to continue.")
        if retrieve_loan_item is True:
            return loan_item

    def user_already_borrows_book_item(self, book_item):
        for loan_item in self.borrowed_books:
            if loan_item['book_item']['ISBN'] == book_item["ISBN"]:
                return True
        return False

    def return_book_item(self):
        borrowed_books = self.borrowed_books
        if borrowed_books is not None and len(borrowed_books) > 0:
            loan_item = self.__get_loan_item_to_return_by_user_input()
            book_item_to_return = loan_item['book_item']
            # Update the library's book items.
            library_book_item_index = self.library.get_book_item_index_by_book_id(book_item_to_return['ISBN'])
            if library_book_item_index != -1:
                self.library.book_items[library_book_item_index]['printed_copies'] += 1
                self.library.update_book_items(self.library.book_items)
                # Update the loan items' data storage file.
                loan_items = self.loan_items
                for loan_item in loan_items:
                    members_are_equal = str(loan_item['borrower']) == str(self.national_insurance_number)
                    international_standard_book_numbers_are_equal = \
                        str(loan_item['book_item']['ISBN']) == str(book_item_to_return['ISBN'])
                    if members_are_equal and international_standard_book_numbers_are_equal:
                        loan_items.remove(loan_item)
                self.update_data("Data/LoanItems.json", loan_items)
                print(f"You successfully returned '{book_item_to_return['title']}' "
                      f"by {book_item_to_return['author']}.")
            else:
                raise ValueError("This library did not loan this book to you.")
        else:
            print("You have no book to return.")

    def __get_loan_item_to_return_by_user_input(self):
        loan_items = self.borrowed_books
        self.__print_all_borrowed_book_items(loan_items)
        loan_item_id = int(input("Give the identity of the book you would like to move forward with: ").strip()) - 1
        if 0 <= loan_item_id < len(loan_items):
            return loan_items[loan_item_id]
        else:
            raise ValueError(f"Your input ({loan_item_id}) is invalid.")

    def __print_all_borrowed_book_items(self, loan_items=None):
        print("Your borrowed books:")
        if loan_items is None:
            loan_items = self.borrowed_books
        count = 1
        for loan_item in loan_items:
            print(f"   [{count}] '{loan_item['book_item']['title']}' by {loan_item['book_item']['author']}.")
            count += 1

    @staticmethod
    def validate_field(field_name, input_value):
        special_validation_fields = ['EmailAddress', 'Username']
        # There are no integer fields to validate yet.
        input_is_correct = 0 < len(input_value) < 100
        if input_is_correct:
            if field_name in special_validation_fields:
                if field_name == 'EmailAddress':
                    return LibraryMember.validate_email(input_value)
                else:
                    return LibraryMember.validate_username(input_value)
            else:
                return True
        return False

    @staticmethod
    def validate_email(email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None

    @staticmethod
    def validate_username(username):
        username_is_lowercase = username == username.lower()
        all_usernames = LibraryMember.__get_member_usernames()
        username_is_unique = username not in all_usernames
        if username_is_lowercase and username_is_unique:
            return True
        else:
            print("    - Username must be lowercase and unique!")
            return False

    @staticmethod
    def __get_member_usernames():
        try:
            file_path = "Data/Members.json"
            with open(file_path) as file:
                members = json.load(file)
            usernames = [member["Username"] for member in members]
            return usernames
        except:
            return []
