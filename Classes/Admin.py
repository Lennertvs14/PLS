import json
from Classes.Person import Person
from Classes.Member import Member


class Admin(Person):
    def __init__(self):
        self.username = "admin"
        self.password = "admin123"

    def delete_member(self):
        members = self.get_members()
        self.print_all_member_names(members)
        try:
            member_id = int(input("Give the identity of the user you would like to delete: "))
            sorted_members = sorted(members, key = lambda m: int(m["Number"]))
            member_to_delete = self.binary_search_for_member_by_identity(sorted_members, 0, len(sorted_members), member_id)
            sorted_members.remove(member_to_delete)
            self.update_members(sorted_members)
        except:
            print("Invalid member identity, please try again.")
            self.delete_member()

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

    def add_member(self):
        members = self.get_members()
        new_member = self.create_member()
        members.append(new_member)
        self.update_members(members)

    @staticmethod
    def create_member():
        empty_member_object = Member("", "", "", "", "", "", "", "", "")
        field_names = [attr for attr in dir(empty_member_object)
                       if not callable(getattr(empty_member_object, attr)) and not attr.startswith("__")]
        field_names.remove('id')
        new_member = {'id': empty_member_object.id}

        for field_name in field_names:
            # TODO: Process optional/required attributes
            while True:
                value = input(f"Please enter the {field_name}: ")
                if empty_member_object.validate_field(field_name, value):
                    new_member[field_name] = value
                    break
                else:
                    print(f"Invalid {field_name} value, please try again.")

        return new_member

    def update_members(self, members):
        members_list_is_not_empty = len(members) > 0
        if members_list_is_not_empty:
            file_path = "Data/Members.json"
            with open(file_path, 'w') as file:
                json.dump(members, file, indent=2)
        else:
            print("There are no members to update.")

    def print_all_member_names(self, members = None):
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
