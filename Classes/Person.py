import json


class Person:
    def __init__(self, username, password):
        self.id = Person.get_unique_identity()
        self.username = username
        self.password = password

    @staticmethod
    def get_unique_identity():
        member_identities = Person.get_member_identities()
        return max(member_identities) + 1

    @staticmethod
    def get_member_identities():
        file_path = "Data/Members.json"
        with open(file_path) as file:
            members = json.load(file)
        member_identities = {int(obj['Number'] for obj in members)}
        return member_identities


