import json
from Classes.Person import Person
from Classes.Member import Member


class Admin(Person):
    admin_options = [
        "Explore members",
        "Add member",
        "Edit member",
        "Delete member",
        "Explore catalog",
        "Search catalog",
        "Add book",
    ]

    def __init__(self):
        self.username = "admin"
        self.password = "admin123"
        super().__init__(self.username, self.password)

    def show_interface(self):
        switcher = {
            1 : lambda: self.print_all_members(),
            2 : lambda: self.add_member(),
            3 : lambda: self.edit_member(),
            4 : lambda: self.delete_member(),
            5 : lambda: self.Catalog.print_all_books(),
            6 : lambda: self.Catalog.search_for_book()
            8 : lambda: self.Catalog.edit_book(),
            8 : lambda: self.Catalog.delete_book()
        }
        # Print user's options
        print("\nWhat would you like to do?")
        for i in range(len(self.admin_options)):
            print(f" [{i+1}] {self.admin_options[i]}")
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
        members = self.get_members()
        new_member = self.create_member_by_user_input()
        members.append(new_member)
        self.update_members(members)

    @staticmethod
    def create_member_by_user_input():
        empty_member_object = Member("", "", "", "", "", "", "", "", "")
        field_names = [attr for attr in dir(empty_member_object)
                       if not callable(getattr(empty_member_object, attr)) and not attr.startswith("__")]
        field_names.remove('id')
        new_member = {'Number': empty_member_object.id}
        for field_name in field_names:
            while True:
                value = input(f"Please enter the {field_name}: ")
                if empty_member_object.validate_field(field_name, value):
                    new_member[field_name] = value
                    break
                else:
                    print(f"Invalid {field_name} value, please try again.")
        return new_member

    def delete_member(self):
        sorted_members = sorted(self.get_members(), key = lambda m: int(m["Number"]))
        member_to_delete = self.get_member_by_identity_input(sorted_members, True)
        sorted_members.remove(member_to_delete)
        self.update_members(sorted_members)

    def update_members(self, members):
        file_path = "Data/Members.json"
        with open(file_path, 'w') as file:
            json.dump(members, file, indent=2)

    def print_all_members(self, members = None):
        if members is None:
            members = self.get_members()
        for member in members:
            member_full_name = member['GivenName'] + " " + member['Surname']
            print(f"[{member['Number']}] {member_full_name}")

    def get_members(self):
        file_path = "Data/Members.json"
        with open(file_path) as file:
            members = json.load(file)
        return members

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
        members = self.get_members()
        for i, member in enumerate(members):
            if member["Number"] == member_to_edit["Number"]:
                members[i] = member_to_edit
                self.update_members(members)
                break

    def get_member_by_identity_input(self, members = None, members_are_sorted = False):
        """
        Returns a member object based on their identity number.

        :param members: A list of member objects to search.
        :param members_are_sorted: A boolean flag indicating if the list is sorted.
        :return: A member object if found, otherwise None.
        """
        if members is None:
            sorted_members = sorted(self.get_members(), key=lambda m: int(m["Number"]))
        elif not members_are_sorted:
            sorted_members = sorted(members, key = lambda m: int(m["Number"]))
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
        middle = (low+high)//2
        member_id = int(data[middle]['Number'])
        if member_id > value:
            return self.binary_search_for_member_by_identity(data, low, middle - 1, value)
        elif member_id < value:
            return self.binary_search_for_member_by_identity(data, middle + 1, high, value)
        else:
            return data[middle]
