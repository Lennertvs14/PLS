from Classes.LibrarySystem import LibrarySystem
import json


class Person(LibrarySystem):
    def __init__(self):
        super().__init__()
        self.national_insurance_number = Person.get_new_national_insurance_number()

    @staticmethod
    def get_new_national_insurance_number():
        member_identities = Person.__get_members_national_insurance_numbers()
        return max(member_identities) + 1

    @staticmethod
    def __get_members_national_insurance_numbers():
        file_path = "Data/Members.json"
        with open(file_path) as file:
            members = json.load(file)
        member_identities = {obj['Number'] for obj in members}
        return member_identities
