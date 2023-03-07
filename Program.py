from Classes.Admin import Admin
from Classes.Member import Member

def main():
    if isinstance(user, Admin):
        print("Hi Admin!")
    elif isinstance(user, Member):
        print(f"Hi {user.GivenName}!")
    else:
        print("Something went wrong, please try again.")
        return


def login():
    print("Welcome!\n")
    members = library_admin.get_members()
    attempts = 3
    while attempts > 0:
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()
        # Admin validation
        if username == "admin" and password == "admin123":
            return library_admin
        # Member validation
        for i in range(len(members)):
            if members[i]['Username'] == username and members[i]['Password'] == password:
                return members[i]
        attempts -= 1
        print(f"You have {attempts} attempts left.")
    return None


if __name__ == "__main__":
    library_admin = Admin()
    user = login()
    user_logged_in = user is not None
    if user_logged_in:
        main()
