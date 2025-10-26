from .SystemAdmin import SystemAdmin

class SuperAdmin(SystemAdmin):
    def __init__(self, username, password, firstName, lastName, registrationDate=None):
        super().__init__(username, password, firstName, lastName, registrationDate)

    # add new syster admin
    # modify or update system admin account and profile
    # delete system admin
    # reset system admin password  (temporary password)
    # make back up 
    # restore backup
    # allow systemadmin to manage backup with one time use only code that refers to a specific backup
    # revoke restore code 