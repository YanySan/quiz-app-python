import string
from QuizQuestions import questions_set, play_quiz, show_ranking

# Class representing a user in the system
class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role


# Load all users from the Users.txt file
def load_users():
    users = []
    with open("Users.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line:
                username, password, role = line.split(":")
                users.append(User(username, password, role))
    return users


# Handles login attempts for a user
def login(users):
    attempts = 0
    while attempts < 3:
        name = input("Enter your name: ")
        password = input("Enter your password: ")
        role = input("Enter your role: ")

        for user in users:
            if name == user.username and password == user.password and role == user.role:
                print(f"Welcome {name}! Your role is {role}!")
                return user

        attempts += 1
        print(f"Login unsuccessful. Attempts left: {3 - attempts}")

    print("You have exceeded maximum login attempts.")
    return None


# Display user menu based on role
def user_menu(user, users):
    if user.role == "admin":
        while True:
            print("\nAdmin Menu:")
            print("1. Add new user")
            print("2. Delete user")
            print("3. Choose an active set of questions")
            print("4. Log out")
            choice = input("Enter your choice: ").strip()
            if choice == "1":
                add_new_user(users)
            elif choice == "2":
                delete_user(user, users)
            elif choice == "3":
                questions_set()
            elif choice == "4":
                print("Logging out...\n")
                break
            else:
                print("Invalid input, try again.\n")
    else:
        while True:
            print("\nContestant Menu:")
            print("1. Play quiz")
            print("2. Check the rank list")
            print("3. Log out")
            choice = input("Enter your choice: ").strip()
            if choice == "1":
                play_quiz(user)
            elif choice == "2":
                show_ranking()
            elif choice == "3":
                print("Logging out...\n")
                break
            else:
                print("Invalid input, try again.\n")


# Add a new user with validations for username, password, and role
def add_new_user(users):

    # Validate username
    while True:
        new_username = input("Enter username: ")

        if not new_username:
            print("Username cannot be empty.")
            continue

        if new_username[0].isdigit():
            print("Username must not start with digit")
            continue

        if not new_username.isalnum():
            print("Username must not contain special character, only alphanumeric characters are allowed.")
            continue

        if any(u.username == new_username for u in users):
            print("Username already exists")
            continue

        break

    # Validate password
    while True:
        new_password = input("Enter password: ")
        if (
            any(c.isupper() for c in new_password) and
            any(c.islower() for c in new_password) and
            any(c.isdigit() for c in new_password) and
            any(c in string.punctuation for c in new_password) and
            len(new_password) > 6
        ):
            break

        else:
            print("Password must contain upper, lower, digit, and special character. Please try again!")

    while True:
        new_role = input("Enter role(admin/contestant): ")
        if new_role in ["admin", "contestant"]:
            break
        else:
            print("Invalid input, please try again by entering  'admin' or 'contestant'.")

    # Create user object and save to file
    new_user = User(new_username, new_password, new_role)
    users.append(new_user)

    with open("Users.txt", "a") as f:
        f.write(f"{new_username}:{new_password}:{new_role}\n")

    print(f"User {new_username } is successfully added!")


# Delete a user with admin restrictions
def delete_user(current_user,users):
    while True:
        deleted_username = input("Enter username of the user you want to delete: ")

        # Find the user object to delete
        user_to_delete = None
        for u in users:
            if u.username == deleted_username:
                user_to_delete = u
                break


        if not user_to_delete:
            print("User not found")
            continue

        #Admin can't delete THEMSELVES!
        if user_to_delete.username == current_user.username:
            print("You cannot delete yourself!")
            return

        # Prevent deleting last admin
        if user_to_delete.role == "admin":
            admin_count = 0

            for u in users:
                if u.role == "admin":
                    admin_count += 1

            if admin_count <=1:
                print("You cannot delete last admin!")
                return

        # Remove user from list and rewrite Users.txt
        users.remove(user_to_delete)

        with open("Users.txt", "w") as f:
            for u in users:
                f.write(f"{u.username}:{u.password}:{u.role}\n")

        print(f"User {deleted_username} is successfully deleted!")
        return