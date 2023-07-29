class NoUserForIdException(Exception):
    """Raised when a user with the given id does not exist in users table"""


class NoUserForUsernameException(Exception):
    """Raised when a user with the given username does not exist in users table"""