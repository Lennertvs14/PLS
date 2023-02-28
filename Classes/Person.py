import json


class Person:
    def __init__(self, username, password):
        self.id = Person.get_unique_identity()
        self.username = username
        self.password = password

    @staticmethod
    def get_unique_identity():
        file_path = "Data/Members.json"
        with open(file_path) as file:
            members = json.load(file)
        member_identities = {int(obj['Number'] for obj in members)}
        return max(member_identities) + 1

