from Classes.Person import Person
import re
import json


class Member(Person):
    member_options = [
        "Explore catalog",
        "Search catalog"
    ]

    def __init__(self, GivenName, Surname, StreetAddress, ZipCode, City, EmailAddress, Username, Password, TelephoneNumber):
        super().__init__(Username, Password)
        self.GivenName = GivenName
        self.Surname = Surname
        self.StreetAddress = StreetAddress
        self.ZipCode = ZipCode
        self.City = City
        self.EmailAddress = EmailAddress
        self.Username = Username
        self.Password = Password
        self.TelephoneNumber = TelephoneNumber

    def show_interface(self):
        switcher = {
            1 : lambda: self.Catalog.print_all_books(),
            2 : lambda: self.Catalog.search_book()
        }
        # Print user's options
        print("What would you like to do?")
        for i in range(len(self.member_options)):
            print(f" [{i+1}] {self.member_options[i]}")
        user_input = input("Enter a digit to choose: ").strip()
        # Validate input
        if user_input.isdigit() and 0 < int(user_input) < len(switcher):
            # Execute
            get_user_choice = switcher.get(user_input)
            print("")
            user_choice = get_user_choice()
        else:
            print("Invalid input, please try again.")
            return self.show_interface()


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
                return Member.validate_username(input_value)
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
        zip_regex = r'^\d{4}\s?[A-Z]{2}$'
        return re.match(zip_regex, zip_code) is not None

    @staticmethod
    def validate_username(username):
        username_is_lowercase = username == username.lower()
        all_usernames = Member.__get_member_usernames()
        username_is_unique = username not in all_usernames
        if username_is_lowercase and username_is_unique:
            return True
        else:
            return False

    @staticmethod
    def __get_member_usernames():
        file_path = "Data/Members.json"
        with open(file_path) as file:
            members = json.load(file)
        usernames = [member["Username"] for member in members]
        return usernames
