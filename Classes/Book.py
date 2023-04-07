import re


class Book:
    def __init__(self, author, country, imageLink, language, link, pages, title, ISBN, year):
        self.author = author,
        self.country = country,
        self.imageLink = imageLink,
        self.language = language,
        self.link = link,
        self.pages = pages,
        self.title = title,
        self.ISBN = ISBN,
        self.year = year

    @staticmethod
    def create_book_by_user_input():
        empty_book_object = Book("", "", "", "", "", 0, "", "", 0)
        field_names = [attr for attr in dir(empty_book_object)
                       if not callable(getattr(empty_book_object, attr)) and not attr.startswith("__")]
        new_book = {}
        for field_name in field_names:
            while True:
                value = input(f"Please enter the {field_name}: ").strip()
                if empty_book_object.validate_field(field_name, value):
                    if value.isdigit() and field_name != 'ISBN':
                        new_book[field_name] = int(value)
                    else:
                        new_book[field_name] = value
                    break
                else:
                    print(f"Invalid {field_name} value, please try again.")
        return new_book

    @staticmethod
    def get_book_by_user_input():
        pass

    @staticmethod
    def validate_field(field_name, input_value):
        special_validation_fields = ['ISBN', 'link']
        integer_validation_fields = ['pages', 'year']
        if field_name in special_validation_fields:
            if field_name == 'ISBN':
                return Book.validate_isbn_13(input_value)
            else:
                return Book.validate_link(input_value)
        elif field_name in integer_validation_fields:
            return input_value.isdigit()
        else:
            return True

    @staticmethod
    def validate_isbn_13(isbn):
        # Remove any non-digit characters
        isbn = re.sub('[^0-9X]', '', isbn)
        isbn_has_valid_length = len(isbn) == 13
        if not isbn_has_valid_length:
            print(len(isbn))
            return False
        # Calculate the checksum
        factors = [1, 3] * 6
        digits = [int(digit) for digit in isbn]
        checksum = 10 - (sum([factor * digit for factor, digit in zip(factors, digits)]) % 10)
        checksum = checksum % 10 if checksum < 10 else 0
        # Compare the calculated checksum with the last digit of the ISBN
        return checksum == digits[-1]

    @staticmethod
    def validate_link(url):
        url_pattern = re.compile(r"^(?:http|ftp)s?://"
                                 # domain name
                                 r"(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+"
                                 # top-level domain
                                 r"(?:[a-zA-Z]{2,})(?:/?|[/?]\S+)$")
        return url_pattern.match(url)


