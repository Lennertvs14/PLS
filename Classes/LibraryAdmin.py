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

    def create_member_by_user_input(self):
        new_national_insurance_number = self.get_new_national_insurance_number()
        empty_member_object = LibraryMember(new_national_insurance_number, "", "", "", "", "", "", "", "", "")
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
        if member_to_delete:
            sorted_members.remove(member_to_delete)
            self.update_data("Data/Members.json", sorted_members)

    def print_all_members(self, members=None):
        if members is None:
            members = self.get_data("Data/Members.json")
        if members:
            for member in members:
                member_full_name = member['GivenName'] + " " + member['Surname']
                print(f"[{member['Number']}] {member_full_name}")
        else:
            print("There are no members registered to this library yet.")

    def edit_member(self):
        member_to_edit = self.get_member_by_national_insurance_number()
        if member_to_edit:
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

    def get_member_by_national_insurance_number(self, members=None, members_are_sorted=False, member_id=None):
        """
        Returns a member object based on their national insurance number.

        :param members: A list of member objects to search.
        :param members_are_sorted: A boolean flag indicating if the list is sorted.
        :param member_id: A national insurance number of the member to look for.
        :return: A member object if found, otherwise None.
        """
        # Get sorted member list and check the parameters
        if members is None:
            sorted_members = sorted(self.get_data("Data/Members.json"), key=lambda m: int(m["Number"]))
        elif not members_are_sorted:
            sorted_members = sorted(members, key=lambda m: int(m["Number"]))
        else:
            sorted_members = members
        if sorted_members:
            try:
                # Get member identity
                if member_id is None:
                    self.print_all_members(sorted_members)
                    member_id = int(input("\nGive the identity of the user you would like to move forward with: ").strip())
                else:
                    member_id = int(member_id)
                # Validate member identity
                if 0 < member_id <= sorted_members[-1]['Number']:
                    # Get & return member
                    member = self.binary_search_for_member_by_national_insurance_number(sorted_members, 0, len(sorted_members), member_id)
                    return member
                else:
                    raise ValueError
            except ValueError:
                print("Invalid member identity, please try again.")
                return self.get_member_by_national_insurance_number(sorted_members, True)
        else:
            print("There are no members registered to this library yet.")

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
        if books:
            for key in book_to_edit:
                print(f"\nWould you like to edit the {key}?")
                yes_or_no = input("Enter 1, 2 or 3 to choose:\n [1] Yes\n [2] No\n [3] Stop editing\n-> ").strip()
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
        else:
            # There are no books in this library catalog yet.
            pass

    def delete_book(self):
        book_to_delete = self.__get_book_by_user_input()
        books = self.catalog.books
        if books:
            books.remove(book_to_delete)
            self.update_data("Data/Books.json", books)
            print(book_to_delete["title"], "from", book_to_delete["author"], "has been removed from the catalog.")
        else:
            # There are no books in this library catalog yet.
            pass

    def __get_book_by_user_input(self):
        print("Available books:\n")
        self.catalog.print_all_books()
        if self.catalog.books:
            user_input = input("\nEnter a digit of the book you would like to move forward with: ").strip()
            if user_input.isdigit() and 0 < int(user_input) <= len(self.catalog.books):
                return self.catalog.books[int(user_input)-1]
            else:
                print("Invalid input, please try again.\n")
                return self.__get_book_by_user_input()
        else:
            # There are no books in this library catalog yet.
            pass

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
        """ Increase the count of available paper copies for a given book in the library's catalog. """
        from Classes.BookItem import BookItem
        self.explore_catalog()
        if self.catalog.books:
            book_item_id = input("Enter a digit for the book item you'd like to add: ").strip()
            quantity_to_add = input("Enter a digit for the amount of book items you'd like to add: ").strip()
            if book_item_id.isdigit() and quantity_to_add.isdigit():
                if int(book_item_id) <= len(self.library.book_items):
                    # add to a book that already has paper copies.
                    book_item = self.library.book_items[int(book_item_id) - 1]
                    old_quantity = book_item['printed_copies']
                    book_item['printed_copies'] += int(quantity_to_add)
                elif int(book_item_id) <= len(self.catalog.books):
                    # add to a book that does not have paper copies yet.
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
                      f"\nThere used to be {old_quantity} paper printed copies, "
                      f"but there are now {book_item['printed_copies']} paper printed copies available for {book_details}.")
            else:
                print("Invalid input, inputs must be digits and greater than zero, please try again.\n")
                return self.add_book_item()
        else:
            # There are no books in this library catalog yet.
            pass

    def edit_book_item(self):
        """ Allow users to modify the details or attributes of a physical copy (book item) of a loaned library' book. """
        print("This editing functionality allows only the metadata of a borrowed book to be modified.")
        if self.loan_items:
            loan_item_to_edit = self.__get_loan_item()
            if loan_item_to_edit:
                print(f"    {loan_item_to_edit}")
                editable_fields = ['loan_date', 'return_date']
                for key in editable_fields:
                    print(f"\nWould you like to edit the {key}?")
                    yes_or_no = input("Enter 1, 2 or 3 to choose:\n [1] Yes\n [2] No\n [3] Stop editing\n-> "). strip()
                    if yes_or_no == "1":
                        value = input(f"Please enter the {key}: ").strip()
                        if Book.validate_field(key, value):
                            loan_item_to_edit[key] = value
                        else:
                            print("Invalid input.")
                    if yes_or_no == "3":
                        break
                print(f"\n{loan_item_to_edit}")
                self.update_data("Data/LoanItems.json", self.loan_items)
                print(self.loan_items)
            else:
                # Unconventional case because the get loan items keeps iterating until one chooses a loan item.
                pass
        else:
            # No book items found
            print("No borrowed books were found, which means there is nothing to edit.")

    def __get_loan_item(self):
        self.__display_loan_items()
        book_item_id = input("Enter a digit to choose: ").strip()
        if book_item_id.isdigit() and 0 < int(book_item_id) <= len(self.loan_items):
            return self.loan_items[int(book_item_id)-1]
        else:
            print("Invalid input, please try again.\n")
            return self.edit_book_item()

    def __display_loan_items(self):
        print(f"{len(self.loan_items)} loaned books are found.")
        loan_details_strings = []
        count = 1
        for loan_item in self.loan_items:
            member = self.get_member_by_national_insurance_number(member_id=loan_item['borrower'])
            member_full_name = member['GivenName'] + " " + member['Surname']
            book_item = loan_item['book_item']
            title = book_item['title']
            author = book_item['author']
            loan_date = loan_item['loan_date']
            return_date = loan_item['return_date']
            loan_details = f"   [{count}] Member: {member_full_name} Title: {title}, Author: {author}, " \
                           f"Loan Date: {loan_date}, Return Date: {return_date}"
            loan_details_strings.append(loan_details)
            count += 1
        loan_entries_string = '\n'.join(loan_details_strings)
        print(loan_entries_string)

    def delete_book_item(self):
        """ Decrease the count of available paper copies for a given book in the library's catalog. """
        book_item = self.__get_book_item_by_user_input()
        if book_item:
            old_quantity = book_item['printed_copies']
            quantity_to_delete = input("Enter a digit for the amount of book items you'd like to delete: ").strip()
            if quantity_to_delete.isdigit():
                quantity_to_delete = int(quantity_to_delete)
                new_quantity = int(old_quantity) - quantity_to_delete
                if new_quantity >= 0:
                    book_item['printed_copies'] = new_quantity
                    self.update_data("Data/BookItems.json", self.library.book_items)
                    book_details = f"'{book_item['title']}' by {book_item['author']}"
                    print(f"Done!"
                          f"\nThere used to be {old_quantity} paper printed copies, "
                          f"but there are now {book_item['printed_copies']} paper printed copies available for {book_details}.")
                else:
                    print(f"Invalid input, "
                          f"you can't delete more than the existing {old_quantity} book items, "
                          f"please try again.\n")
                    return self.delete_book_item()
            else:
                print("Invalid input, enter a digit that is greater than zero, please try again.\n")
                return self.delete_book_item()
        else:
            # No book items found
            pass

    def __get_book_item_by_user_input(self):
        print("Available books:\n")
        self.library.print_all_book_items()
        if self.library.book_items:
            user_input = input("\nEnter a digit of the book you would like to move forward with: ").strip()
            if user_input.isdigit() and 0 < int(user_input) <= len(self.library.book_items):
                return self.library.book_items[int(user_input)-1]
            else:
                print("Invalid input, please try again.\n")
                return self.__get_book_by_user_input()
        else:
            # There are no book items
            pass

    def check_book_item_status_for_member(self):
        from Classes.LoanItem import LoanItem
        from datetime import datetime
        # Get member to check for
        member_obj = self.get_member_by_national_insurance_number()
        if member_obj:
            member = self.__convert_member_from_dict_to_instance(member_obj)
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
                        status = "The book borrower is overdue in returning the book."
                    else:
                        days_left_to_return = (datetime.strptime(loan_item['return_date'], "%Y-%m-%d") - datetime.now()).days
                        status = "The book is not returned yet."
                    loan_details = f"Loan date: {loan_item['loan_date']}" \
                                   f"\n    Status: {status}" \
                                   f"\n    Days left: {days_left_to_return}" \
                                   f"\n    Return date: {loan_item['return_date']}"
                    print("    " + loan_details + "\n")
            else:
                print("    The member is currently not borrowing any books.")
        else:
            # There are no members registered to this library yet
            pass

    def __convert_member_from_dict_to_instance(self, member_dict):
        member_instance = LibraryMember(**member_dict)
        return member_instance

    def lend_book_item_to_member(self):
        from Classes.LoanItem import LoanItem
        # Get user to loan with
        get_member = self.get_member_by_national_insurance_number()
        if get_member:
            member = self.__convert_member_from_dict_to_instance(get_member)
            # Choose book item and loan it
            print("Choose the book to lend:")
            loan_item = member.borrow_book_item(True)
            if isinstance(loan_item, LoanItem):
                # Workaround to appropriately update the data files
                book_item_list_index = self.library.get_book_item_index_by_book_id(loan_item.book_item['ISBN'])
                self.library.book_items[book_item_list_index]['printed_copies'] -= 1
                self.loan_items.append(vars(loan_item))
        else:
            # There are no members registered to this library yet
            pass

    def create_backup(self):
        from Classes.Backup import Backup
        backup_description = str(input("Give the backup a description or leave it empty: "))
        backup = Backup(backup_description)

    def restore_backup(self, delete_backup_after=False):
        from Classes.Backup import Backup
        Backup.restore_backup(delete_backup_after)
        self.library.initialize_book_items()
        self.catalog.books = self.get_data("Data/Books.json")
