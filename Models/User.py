
import datetime


#abstract class. you dont really create user objects.
class User():
    def __init__(self, Username, Password, FirstName, LastName, Role, RegistrationDate=None):
        self.Username = Username
        self.Password = Password
        self.FirstName = FirstName
        self.LastName = LastName
        self.RegistrationDate = datetime.datetime.now() if RegistrationDate == None else RegistrationDate
        self.Role = Role

    def __str__(self):
        return f"First name: {self.FirstName}\nLast name: {self.LastName}\nRegistrationDate: {self.RegistrationDate}"