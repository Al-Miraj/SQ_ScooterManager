from Database.MainDb import MainDb
from Models.User import User
from Utils.security import verify_password

class AuthHandler:

    __authenticated_user: "User | None" = None

    @classmethod
    def getCurrentUser(cls) -> User:
        return cls.__authenticated_user # type: ignore

    @classmethod
    def login(cls, username, password) -> bool:
        """ 
        Try to log in using a dictionary or list of users.
        user_db can be a dict {username: User} or list of User objects.
        """
        user = MainDb.users().getUserByUsername(username)
        if not user:
            return False
        
        if verify_password(password, user.Password):
            cls.__authenticated_user = user
            return True
        
        return False

    @classmethod
    def logout(cls):
        cls.__authenticated_user = None

    @classmethod
    def is_authenticated(cls):
        return cls.__authenticated_user is not None

    @classmethod
    def require_role(cls, *roles):
        """
        Returns True if the logged-in user has one of the specified roles.
        """
        if not cls.__authenticated_user:
            return False
        return cls.__authenticated_user.Role in roles