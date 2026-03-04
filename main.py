from Users import *

# Main entry point of the Quiz App
def main():
    print("Welcome to the Quiz App! ")

    # Load all users from Users.txt
    users = load_users()

    while True:  # Main menu loop
        print("\nMain Menu:")
        print("1. Log in")
        print("2. Exit")
        choice = input("Enter your choice: ").strip().lower()

        if choice == "1":
            current_user = login(users)
            if current_user:
                # Display role-specific menu after successful login
                user_menu(current_user, users)
                print("\nReturning to main menu...\n")
            else:
                print("Login failed. Returning to main menu.\n")

        elif choice == "2" or choice == "exit":
            print("Exiting program...")
            break  # Leaving main loop and exiting program

        else:

            # Handle invalid input
            print("Invalid input, please try again.\n")

#Run the program
if __name__ == '__main__':
    main()







