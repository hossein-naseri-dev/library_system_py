"""
Login Module for "Library System"
"""
from utils.config import set_current_user
from utils.database import login_query, create_user_query


def valid_input(inp, inp_is="username"):
    """Validates user input's"""

    if not inp:
        return valid_input(input(f"Please enter a valid {inp_is}: "),
                           inp_is)
    return inp


def login(username=None, password=None):
    """Check username/password combination in database
    if it exists, return username"""

    if username is None and password is None:
        username = valid_input(input("Please enter a username: "))
        password = valid_input(input("Please enter a password: "), "password")

    result = login_query(username, password)
    if result is None:
        return None
    elif result:
        set_current_user(username)
        return username


def create_user(username=None, password=None):
    """Create a new account in library system"""

    if username is None and password is None:
        username = valid_input(input("Please enter a username: "))
        password = valid_input(input("Please enter a password: "),"password")

    action = False
    result = create_user_query(username, password)
    if not result:
        print(f"username: '{username}' is exists in library.")
    elif result == 1:
        print(
            f"An account for '{username}' is created in library successfully."
        )
        set_current_user(username)
        return True
    elif result == -1:
        print(f"An account with username: '{username}' is already registered.")

    return action
