from Classes.Person import Person
import re
import json


class Member(Person):
    def __init__(self, given_name, surname, street_address, zip_code, city, email_address, username, password, telephone_number):
        super().__init__(username, password)
        self.GivenName = given_name
        self.Surname = surname
        self.StreetAddress = street_address
        self.ZipCode = zip_code
        self.City = city
        self.EmailAddress = email_address
        self.Username = username
        self.Password = password
        self.TelephoneNumber = telephone_number

    @staticmethod
    def validate_field(field_name, input_value):
        input_value = input_value.strip()
        special_validation_fields = ['EmailAddress', 'ZipCode', 'Username']
        field_is_string = isinstance(field_name, str)

        if field_is_string:
            input_is_correct = isinstance(input_value, str) and 0 < len(input_value) < 100
            if field_name not in special_validation_fields:
                return input_is_correct
            elif input_is_correct and field_name == 'EmailAddress':
                return Member.validate_email(input_value)
            elif input_is_correct and field_name == 'ZipCode':
                return Member.validate_zip_code(input_value)
            elif input_is_correct and field_name == 'Username':
                return Member.validate_credentials(field_name, input_value)
            else:
                return False
        else:
            # There are no integer fields to validate yet.
            return True

    @staticmethod
    def validate_email(email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None

    @staticmethod
    def validate_zip_code(zip_code):
        # TODO: Make optional
        zip_regex = r'^\d{4}\s?[A-Z]{2}$'
        return re.match(zip_regex, zip_code) is not None

    @staticmethod
    def validate_credentials(field, credential):
        validation = credential == credential.lower()
        if validation and field == 'Username':
            member_usernames = Member.__get_member_usernames()
            if credential in member_usernames:
                validation = False
        return validation

    @staticmethod
    def __get_member_usernames():
        file_path = "Data/Members.json"
        with open(file_path) as file:
            members = json.load(file)
        usernames = [member["Username"] for member in members]
        return usernames