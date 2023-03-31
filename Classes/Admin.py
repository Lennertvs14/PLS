from Classes.Book import Book
from Classes.Member import Member
from Classes.Person import Person


class Admin(Person):
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
        "Restore backup"
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
            # TODO: add_list_of_members()
            6: lambda: print("Not implemented yet."),
            7: lambda: self.check_catalog(),
            8: lambda: self.add_book(),
            # TODO: edit_book()
            9: lambda: print("Not implemented yet."),
            # TODO: delete_book()
            10: lambda: print("Not implemented yet."),
            11: lambda: self.search_for_book(),
            # TODO: add_list_of_books()
            12: lambda: print("Not implemented yet."),
            13: lambda: self.check_library(),
            14: lambda: self.add_book_item(),
            # TODO: edit_book_item()
            15: lambda: print("Not implemented yet."),
            # TODO: delete_book_item()
            16: lambda: print("Not implemented yet."),
            17: lambda: self.search_for_book_item(),
            18: lambda: self.lend_book_item_to_member(),
            # TODO: Backup.make_backup()
            19: lambda: print("Not implemented yet."),
            # TODO: Backup.restore_backup()
            20: lambda: print("Not implemented yet.")
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

    def add_member(self):
        members = self.get_data("Data/Members.json")
        new_member = self.create_member_by_user_input()
        members.append(new_member)
        self.update_data("Data/Members.json", members)

    @staticmethod
    def create_member_by_user_input():
        empty_member_object = Member("", "", "", "", "", "", "", "", "")
        field_names = [attr for attr in dir(empty_member_object)
                       if not callable(getattr(empty_member_object, attr)) and not attr.startswith("__")]
        field_names.remove('id')
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
        member_to_delete = self.get_member_by_identity_input(sorted_members, True)
        sorted_members.remove(member_to_delete)
        self.update_data("Data/Members.json", sorted_members)

    def print_all_members(self, members=None):
        if members is None:
            members = self.get_data("Data/Members.json")
        for member in members:
            member_full_name = member['GivenName'] + " " + member['Surname']
            print(f"[{member['Number']}] {member_full_name}")

    def edit_member(self):
        member_to_edit = self.get_member_by_identity_input()
        member_to_edit_identity = member_to_edit['Number']
        member_to_edit.pop('Number')
        for key in member_to_edit:
            print(f"Would you like to edit the {key}?")
            yes_or_no = input("Enter 1, 2 or 3 to choose:\n [1] Yes\n [2] No\n [3] Exit\n-> ").strip()
            if yes_or_no == "1":
                value = input(f"Please enter the {key}: ")
                if value != "" and Member.validate_field(key, value):
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

    def get_member_by_identity_input(self, members=None, members_are_sorted=False):
        """
        Returns a member object based on their identity number.

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
                member = self.binary_search_for_member_by_identity(sorted_members, 0, len(sorted_members), member_id)
                return member
            else:
                raise ValueError
        except ValueError:
            print("Invalid member identity, please try again.")
            return self.get_member_by_identity_input(sorted_members, True)

    def binary_search_for_member_by_identity(self, data, low, high, value):
        if low > high:
            return None
        middle = (low + high) // 2
        member_id = int(data[middle]['Number'])
        if member_id > value:
            return self.binary_search_for_member_by_identity(data, low, middle - 1, value)
        elif member_id < value:
            return self.binary_search_for_member_by_identity(data, middle + 1, high, value)
        else:
            return data[middle]

    def add_book(self):
        new_book = Book.create_book_by_user_input()
        books = self.catalog.get_books()
        books.append(new_book)
        self.catalog.books.append(new_book)
        self.update_data("Data/Books.json", books)

    def add_book_item(self):
        self.check_catalog()
        book_item_id = input("Enter a digit for the book item you'd like to add: ").strip()
        quantity_to_add = input("Enter a digit for the amount of book items you'd like to add: ").strip()
        book_item_id_is_valid = book_item_id.isdigit() and -1 < int(book_item_id) <= len(self.library.book_items)
        if book_item_id_is_valid and quantity_to_add.isdigit():
            book_item = self.library.book_items[int(book_item_id) - 1]
            old_quantity = book_item['copies']
            book_item['copies'] += int(quantity_to_add)
            self.update_data("Data/BookItems.json", self.library.book_items)
            book_details = f"'{book_item['book']['title']}' by {book_item['book']['author']}"
            print(f"Done!"
                  f"\nThere used to be {old_quantity} paper copies, "
                  f"but there are now {book_item['copies']} paper copies available for {book_details}.")
        else:
            print("Invalid input, please try again.\n")
            return self.add_book_item()


    def check_book_item_status_for_member(self):
        # Get member to check for
        print("Choose the member:")
        member = self.__convert_member_from_dict_to_instance(self.get_member_by_identity_input())
        # Get the member's borrowed books
        borrowed_books = member.borrowed_books
        if borrowed_books is not None and len(borrowed_books) > 0:
            # Show book item status foreach borrowed book
            print("The member is borrowing these books:")
            for loan_item in borrowed_books:
                book_details = f"'{loan_item['book_item']['book']['title']}' by {loan_item['book_item']['book']['author']}"
                print("    " + book_details)
                if loan_item['return_date'] is not None:
                    status = "returned"
                else:
                    status = "not returned yet"
                loan_details = f"Loan date: {loan_item['loan_date']}\n    Status: {status}"
                print("    " + loan_details + "\n")
        else:
            print("    The member is currently not borrowing any books.")

    def __convert_member_from_dict_to_instance(self, member_dict):
        member_national_insurance_number = member_dict.pop('Number')
        member_instance = Member(**member_dict)
        member_instance.national_insurance_number = member_national_insurance_number
        return member_instance

    def lend_book_item_to_member(self):
        from Classes.LoanItem import LoanItem
        # Get user to loan with
        print("Choose the member:")
        get_member = self.get_member_by_identity_input()
        member = self.__convert_member_from_dict_to_instance(get_member)
        # Choose book item and loan it
        print("Choose the book to lend:")
        loan_item = member.borrow_book_item(True)
        if isinstance(loan_item, LoanItem):
            # Workaround to appropriately update the data files
            book_item_list_index = self.library.get_book_item_index_by_book_id(loan_item.book_item['book']['ISBN'])
            self.library.book_items[book_item_list_index]['copies'] -= 1
