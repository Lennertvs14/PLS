from Classes.Person import Person
import re


class Member(Person):
    def __init__(self, given_name, surname, street_address, zip_code, city, email_address, username, password, telephone_number):
        super().__init__(username, password)
        self.given_name = given_name
        self.surname = surname
        self.street_address = street_address
        self.zip_code = zip_code
        self.city = city
        self.email_address = email_address
        self.username = username
        self.password = password
        self.telephone_number = telephone_number

    @staticmethod
    def validate_field(field_name, input_value):
        input_value = input_value.strip()
        special_validation_fields = ['email_address', 'zip_code', 'username', 'password']
        field_is_string = isinstance(field_name, str)

        if field_is_string:
            input_is_correct = isinstance(input_value, str) and 0 < len(input_value) < 100
            if field_name not in special_validation_fields:
                return input_is_correct
            elif input_is_correct and field_name == 'email_address':
                return Member.validate_email(input_value)
            elif input_is_correct and field_name == 'zip_code':
                return Member.validate_zip_code(input_value)
            elif input_is_correct and field_name == 'username' or field_name == 'password':
                return Member.validate_credentials(input_value)
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
    def validate_credentials(credential):
        credential_lowercase = credential.lower()
        credential_is_lowercase = credential == credential_lowercase
        return credential_is_lowercase

