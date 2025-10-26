from .ServiceEngineer import ServiceEngineer

class SystemAdmin(ServiceEngineer):
    def __init__(self, username, password, firstName, lastName, registrationDate=None):
        super().__init__(username, password, firstName, lastName, registrationDate)




    # Check all users + roles
    # add new service engineer
    # update service engineer account + profile
    # delete service engineer
    # reset srvice engineer password (temp password)
    # update own account and profile (such as?)
    # delete own account
    # make system backup
    # restore system backup (For this purpose, the SuperAdministrator has generated a specific ‘one-use only’ code to restore a specific backup.)
    # see log files
    # add new traveler
    # update traveler information
    # delete traveler
    # add scooter
    # update scooter info
        # all info
    # delete scooter
    # search info of traveler
