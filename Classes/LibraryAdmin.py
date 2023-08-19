from Classes.Book import Book
from Classes.LibraryMember import LibraryMember
from Classes.Person import Person


class LibraryAdmin(Person):
    admin_options = [
        "Explore members",
        "Add member",
        "Edit member",
        "Delete member",
        "Check book item status for member",
        "Add list of members",
        "Explore catalog",
        "Add book",
        "Edit book",
        "Delete book",
        "Search catalog",
        "Add list of books",
        "Explore book items",
        "Add book item",
        "Edit book item",
        "Delete book item",
        "Search book item",
        "Lend book item to member",
        "Make backup",
        "Restore backup",
        "Restore and remove backup"
    ]

    def __init__(self):
        super().__init__()
        self.username = "admin"
        self.password = "admin123"

    def show_interface(self):
        switcher = {
            1: lambda: self.print_all_members(),
            2: lambda: self.add_member(),
            3: lambda: self.edit_member(),
            4: lambda: self.delete_member(),
            5: lambda: self.check_book_item_status_for_member(),
            6: lambda: self.add_list_of_members(),
            7: lambda: self.explore_catalog(),
            8: lambda: self.add_book(),
            9: lambda: self.edit_book(),
            10: lambda: self.delete_book(),
            11: lambda: self.search_for_book(),
            12: lambda: self.add_list_of_books(),
            13: lambda: self.explore_library(),
            14: lambda: self.add_book_item(),
            15: lambda: self.edit_book_item(),
            16: lambda: self.delete_book_item(),
            17: lambda: self.search_for_book_item(),
            18: lambda: self.lend_book_item_to_member(),
            19: lambda: self.create_backup(),
            20: lambda: self.restore_backup(),
            21: lambda: self.restore_backup(True)
        }
        # Print user's options
        print("\nWhat would you like to do?")
        for i in range(len(self.admin_options)):
            print(f" [{i + 1}] {self.admin_options[i]}")
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

    def add_member(self, new_member=None):
        members = self.get_data("Data/Members.json")
        if new_member is None:
            new_member = self.create_member_by_user_input()
        members.append(new_member)
        self.update_data("Data/Members.json", members)

    @staticmethod
    def create_member_by_user_input():
        empty_member_object = LibraryMember("", "", "", "", "", "", "", "", "")
        field_names = [attr for attr in dir(empty_member_object)
                       if not callable(getattr(empty_member_object, attr)) and not attr.startswith("__")]
        fields_to_exclude = \
            ['national_insurance_number', 'borrowed_books', 'catalog', 'library', 'loan_items', 'member_options']
        for field in fields_to_exclude:
            field_names.remove(field)
        new_member = {'Number': empty_member_object.national_insurance_number}
        for field_name in field_names:
            while True:
                value = input(f"Please enter the {field_name}: ").strip()
                if empty_member_object.validate_field(field_name, value):
                    new_member[field_name] = value
                    break
                else:
                    print(f"Invalid {field_name} value, please try again.")
        return new_member

    def delete_member(self):
        sorted_members = sorted(self.get_data("Data/Members.json"), key=lambda m: int(m["Number"]))
        member_to_delete = self.get_member_by_national_insurance_number(sorted_members, True)
        sorted_members.remove(member_to_delete)
        self.update_data("Data/Members.json", sorted_members)

    def print_all_members(self, members=None):
        if members is None:
            members = self.get_data("Data/Members.json")
        for member in members:
            member_full_name = member['GivenName'] + " " + member['Surname']
            print(f"[{member['Number']}] {member_full_name}")

    def edit_member(self):
        member_to_edit = self.get_member_by_national_insurance_number()
        member_to_edit_identity = member_to_edit['Number']
        member_to_edit.pop('Number')
        for key in member_to_edit:
            print(f"Would you like to edit the {key}?")
            yes_or_no = input("Enter 1, 2 or 3 to choose:\n [1] Yes\n [2] No\n [3] Exit\n-> ").strip()
            if yes_or_no == "1":
                value = input(f"Please enter the {key}: ")
                if LibraryMember.validate_field(key, value):
                    member_to_edit[key] = value
                else:
                    print("Invalid input.")
            if yes_or_no == "3":
                break
        member_to_edit['Number'] = member_to_edit_identity
        print(f"\n{member_to_edit}")
        members = self.get_data("Data/Members.json")
        for i, member in enumerate(members):
            if member["Number"] == member_to_edit["Number"]:
                members[i] = member_to_edit
                self.update_data("Data/Members.json", members)
                break

    def get_member_by_national_insurance_number(self, members=None, members_are_sorted=False):
        """
        Returns a member object based on their national insurance number.

        :param members: A list of member objects to search.
        :param members_are_sorted: A boolean flag indicating if the list is sorted.
        :return: A member object if found, otherwise None.
        """
        if members is None:
            sorted_members = sorted(self.get_data("Data/Members.json"), key=lambda m: int(m["Number"]))
        elif not members_are_sorted:
            sorted_members = sorted(members, key=lambda m: int(m["Number"]))
        else:
            sorted_members = members
        self.print_all_members(sorted_members)
        try:
            member_id = int(input("Give the identity of the user you would like to move forward with: ").strip())
            if 0 < member_id <= sorted_members[-1]['Number']:
                member = self.binary_search_for_member_by_national_insurance_number(sorted_members, 0, len(sorted_members), member_id)
                return member
            else:
                raise ValueError
        except ValueError:
            print("Invalid member identity, please try again.")
            return self.get_member_by_national_insurance_number(sorted_members, True)

    def binary_search_for_member_by_national_insurance_number(self, data, low, high, value):
        if low > high:
            return None
        middle = (low + high) // 2
        member_id = int(data[middle]['Number'])
        if member_id > value:
            return self.binary_search_for_member_by_national_insurance_number(data, low, middle - 1, value)
        elif member_id < value:
            return self.binary_search_for_member_by_national_insurance_number(data, middle + 1, high, value)
        else:
            return data[middle]

    def add_list_of_members(self):
        """This method will load and add a list of members to the system, all at once using a csv file."""
        instructions = "\n1. Put your csv file in the Import folder."
        print(instructions)
        file_to_import = input("2. Enter the name of the file you want to import: ").strip()
        file_type = file_to_import[-4:]
        if file_type != ".csv":
            file_to_import += ".csv"
        new_members = self.__get_data_from_csv_file("Import/" + file_to_import)
        if new_members is not None and len(new_members) > 0:
            for member in new_members:
                if LibraryMember.validate_username(member['Username']):
                    member.pop('Number')
                    member['Number'] = self.get_new_national_insurance_number()
                    self.add_member(new_member=member)
                else:
                    print(f"    [WARNING] '{member['GivenName']}' is not added to the library system.")
        else:
            print(f"Invalid file '{file_to_import}', no data found.")
            return
        print("Done!")

    def __get_data_from_csv_file(self, file_path):
        import csv
        try:
            with open(file_path) as file:
                items = list(csv.DictReader(file, delimiter=";"))
            return items
        except Exception as e:
            print(f"Invalid file path {file_path}.")

    def add_book(self, new_book=None):
        if new_book is None:
            book_to_add = Book.create_book_by_user_input()
        else:
            book_to_add = new_book
        book_is_unique = True
        duplicate_book = None
        for book in self.catalog.books:
            if book_to_add['ISBN'] == book['ISBN']:
                book_is_unique = False
                duplicate_book = book
        if book_is_unique:
            self.catalog.books.append(book_to_add)
            self.update_data("Data/Books.json", self.catalog.books)
        else:
            print(f"\nThis book is not unique, the ISBN already exist:\n    {book_to_add}\nPlease try again.\n")
            if new_book is None:
                return self.add_book()

    def edit_book(self):
        book_to_edit = self.__get_book_by_user_input()
        books = self.catalog.books
        for key in book_to_edit:
            print(f"\nWould you like to edit the {key}?")
            yes_or_no = input("Enter 1, 2 or 3 to choose:\n [1] Yes\n [2] No\n [3] Exit\n-> ").strip()
            if yes_or_no == "1":
                value = input(f"Please enter the {key}: ").strip()
                if Book.validate_field(key, value):
                    book_to_edit[key] = value
                else:
                    print("Invalid input.")
            if yes_or_no == "3":
                break
        print(f"\n{book_to_edit}")
        self.update_data("Data/Books.json", books)
        print("\nBook successfully edited!")

    def delete_book(self):
        book_to_delete = self.__get_book_by_user_input()
        books = self.catalog.books
        books.remove(book_to_delete)
        self.update_data("Data/Books.json", books)
        print(book_to_delete["title"], "from", book_to_delete["author"], "has been removed from the catalog.")

    def __get_book_by_user_input(self):
        print("Available books:\n")
        self.catalog.print_all_books()
        user_input = input("\nEnter a digit of the book you would like to move forward with: ").strip()
        if user_input.isdigit() and 0 < int(user_input) <= len(self.catalog.books):
            return self.catalog.books[int(user_input)-1]
        else:
            print("Invalid input, please try again.\n")
            return self.__get_book_by_user_input()

    def add_list_of_books(self):
        """This method will load and add a list of books to the system, all at once using a json file."""
        instructions = "\n1. Put your json file in the Import folder."
        print(instructions)
        file_to_import = input("2. Enter the name of the file you want to import: ").strip()
        file_type = file_to_import[-5:]
        if file_type != ".json":
            file_to_import += ".json"
        new_books = self.get_data("Import/" + file_to_import)
        if new_books is not None and len(new_books) > 0:
            for book in new_books:
                self.add_book(new_book=book)
        else:
            print(f"Invalid file '{file_to_import}', no data found.")
            return
        print("Done!")

    def add_book_item(self):
        from Classes.BookItem import BookItem
        self.explore_catalog()
        book_item_id = input("Enter a digit for the book item you'd like to add: ").strip()
        quantity_to_add = input("Enter a digit for the amount of book items you'd like to add: ").strip()
        book_item_id_is_digit = book_item_id.isdigit() and int(book_item_id) > -1
        if book_item_id_is_digit:
            if int(book_item_id) <= len(self.library.book_items):
                book_item = self.library.book_items[int(book_item_id) - 1]
                old_quantity = book_item['printed_copies']
                book_item['printed_copies'] += int(quantity_to_add)
            elif int(book_item_id) <= len(self.catalog.books):
                book_item = BookItem(self.catalog.books[int(book_item_id) - 1], int(quantity_to_add))
                old_quantity = 0
                self.library.book_items.append(book_item.get_book_item_data())
                book_item = book_item.__dict__
            else:
                print("Invalid input, please try again.\n")
                return self.add_book_item()
            self.update_data("Data/BookItems.json", self.library.book_items)
            book_details = f"'{book_item['title']}' by {book_item['author']}"
            print(f"Done!"
                  f"\nThere used to be {old_quantity} paper printed_copies, "
                  f"but there are now {book_item['printed_copies']} paper printed_copies available for {book_details}.")
        else:
            print("Invalid input, please try again.\n")
            return self.add_book_item()

    def edit_book_item(self):
        book_item_to_edit = self.__get_book_item_by_user_input()
        print(f"\nWould you like to edit the printed copies?")
        yes_or_no = input("Enter 1, 2 or 3 to choose:\n [1] Yes\n [2] No\n [3] Exit\n-> ").strip()
        if yes_or_no == "1":
            value = input(f"Please enter the new amount of printed copies: ").strip()
            if value.isdigit() and int(value) > 0:
                book_item_to_edit['printed_copies'] = int(value)
                self.update_data("Data/BookItems.json", self.library.book_items)
                print("\nBook's printed copies are successfully edited!")
            else:
                print("Invalid input, the amount of copies must be a positive digit, please try again.")
                return self.edit_book_item()
        else:
            print("There are no other details to edit at a book item, maybe you're looking to alter the book it self?")

    def delete_book_item(self):
        book_item_to_delete = self.__get_book_item_by_user_input()
        book_items = self.library.book_items
        book_items.remove(book_item_to_delete)
        self.update_data("Data/BookItems.json", book_items)
        print(book_item_to_delete["title"], "from", book_item_to_delete["author"],
              "has been removed from the catalog.")

    def __get_book_item_by_user_input(self):
        print("Available books:\n")
        self.library.print_all_book_items()
        user_input = input("\nEnter a digit of the book you would like to move forward with: ").strip()
        if user_input.isdigit() and 0 < int(user_input) <= len(self.library.book_items):
            return self.library.book_items[int(user_input)-1]
        else:
            print("Invalid input, please try again.\n")
            return self.__get_book_by_user_input()

    def check_book_item_status_for_member(self):
        from Classes.LoanItem import LoanItem
        from datetime import datetime
        # Get member to check for
        print("Choose the member:")
        member = self.__convert_member_from_dict_to_instance(self.get_member_by_national_insurance_number())
        # Get the member's borrowed books
        borrowed_books = member.borrowed_books
        if borrowed_books is not None and len(borrowed_books) > 0:
            # Show book item status foreach borrowed book
            print("The member is borrowing these books:")
            for loan_item in borrowed_books:
                book_details = f"'{loan_item['book_item']['title']}' by {loan_item['book_item']['author']}"
                print("    " + book_details)
                if LoanItem.is_overdue(loan_item['return_date']):
                    days_left_to_return = 0
                else:
                    days_left_to_return = (datetime.strptime(loan_item['return_date'], "%Y-%m-%d") - datetime.now()).days
                status = "not returned yet"
                loan_details = f"Loan date: {loan_item['loan_date']}" \
                               f"\n    Status: {status}" \
                               f"\n    Days left: {days_left_to_return}"
                print("    " + loan_details + "\n")
        else:
            print("    The member is currently not borrowing any books.")

    def __convert_member_from_dict_to_instance(self, member_dict):
        member_instance = LibraryMember(**member_dict)
        return member_instance

    def lend_book_item_to_member(self):
        from Classes.LoanItem import LoanItem
        # Get user to loan with
        print("Choose the member:")
        get_member = self.get_member_by_national_insurance_number()
        member = self.__convert_member_from_dict_to_instance(get_member)
        # Choose book item and loan it
        print("Choose the book to lend:")
        loan_item = member.borrow_book_item(True)
        if isinstance(loan_item, LoanItem):
            # Workaround to appropriately update the data files
            book_item_list_index = self.library.get_book_item_index_by_book_id(loan_item.book_item['ISBN'])
            self.library.book_items[book_item_list_index]['printed_copies'] -= 1

    def create_backup(self):
        from Classes.Backup import Backup
        backup_description = str(input("Give the backup a description or leave it empty: "))
        create_backup = Backup(backup_description)

    def restore_backup(self, delete_backup_after=False):
        from Classes.Backup import Backup
        Backup.restore_backup(delete_backup_after)
        self.library.initialize_book_items()
        self.catalog.books = self.get_data("Data/Books.json")
