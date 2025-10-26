from .User import User


class ServiceEngineer(User):
    def __init__(self, username, password, firstName, lastName, registrationDate=None):
        super().__init__(username, password, firstName, lastName, registrationDate)

    # update their own password
    def UpdateOwnPassword(self, newPasswordHashed) -> bool:
        """expects password to be hashed"""
        self.Password = newPasswordHashed
        

    # update some attributes of a scooter
        # State of Charge
        # target State of Charge
        # Location
        # Out of Service Status
        # Mileage
        # Last Maintenence date
    # search and retrieve info of a scooter
    pass