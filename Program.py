from Classes.LibraryAdmin import LibraryAdmin
from Classes.LibraryMember import LibraryMember


def main():
    try:
        if isinstance(user, LibraryAdmin):
            user.show_interface()
        else:
            # Convert the user (dictionary) to a member (instance)
            if 'Number' in user:
                user.pop('Number')
            member = LibraryMember(**user)
            member.show_interface()
        return main()
    except Exception as exception:
        print("")
        print(f"The following error occurred:\n {exception}")
        print("Please get in touch with a library admin to solve the issue.")


def login():
    print("Welcome!\n")
    members = library_admin.get_data("Data/Members.json")
    attempts = 3
    while attempts > 0:
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()
        # LibraryAdmin validation
        if username == "admin" and password == "admin123":
            return library_admin
        # LibraryMember validation
        for i in range(len(members)):
            if members[i]['Username'] == username and members[i]['Password'] == password:
                return members[i]
        attempts -= 1
        print(f"You have {attempts} attempt(s) left.")
    return None


if __name__ == "__main__":
    library_admin = LibraryAdmin()
    user = login()
    user_is_logged_in = user is not None
    if user_is_logged_in:
        main()
