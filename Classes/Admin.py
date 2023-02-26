import json
from Classes.Person import Person
from Classes.Member import Member


class Admin(Person):
    def __init__(self):
        self.username = "admin"
        self.password = "admin123"

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


    def print_all_member_names(self):
        members = self.get_members()
        for member in members:
            member_full_name = member['GivenName'] + " " + member['Surname']
            print(member_full_name)

    def get_members(self):
        file_path = "Data/Members.json"
        with open(file_path) as file:
            members = json.load(file)
        return members
