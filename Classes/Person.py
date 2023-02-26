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
        # TODO: Improve time complexity
        member_identities = [obj['Number'] for obj in members]
        member_identities = [int(identity) for identity in member_identities]
        member_identities_sorted = sorted(member_identities)
        return member_identities_sorted[-1] + 1

