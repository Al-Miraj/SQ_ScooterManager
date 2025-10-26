# this is the main file. 
# starting the application should be done by running this file
from Database.MainDb import MainDb

from Models.Traveler import Traveler
from Models.Scooter import Scooter
from Models.User import User
from Utils.AuthHandler import AuthHandler
from Utils.InputValidator import InputHandler

#////////////
from Login.PageServiceEngineer import PageServiceEngineer
from Login.PageSystemAdmin import PageSystemAdmin
from Login.PageSuperAdmin import PageSuperAdmin

from Utils.BackupHandler import BackupHandler
import Utils.logger as l


# FEEDBACK
# type casting considered massaging the input. the format is just string
# authorisation not complete after changing. session control after changing critical operations that make the session invalid


def reset_db():
    MainDb.scooters().deleteAllScooters()
    MainDb.users().deleteAllUsers()
    MainDb.travelers().deleteAllTravelers()

    # check if db is empty
    if (len(MainDb.scooters().getAllScooters()) != 0) or \
       (len(MainDb.users().getAllUsers()) != 0) or \
       (len(MainDb.travelers().getAllTravelers()) != 0):
        print("Database reset unsuccessful, aborting...")
        return

    # read seed data from json files
    import json
    with open("Database/Data/scooters.json", "r") as f:
        # load from json then map to scooter objects
        scooters_data = json.load(f)
        scooters = [Scooter(**data) for data in scooters_data]
    with open("Database/Data/users.json", "r") as f:
        users_data = json.load(f)
        users = [User(**data) for data in users_data]
    with open("Database/Data/travelers.json", "r") as f:
        travelers_data = json.load(f)
        travelers = [Traveler(**data) for data in travelers_data]

    # Insert seed data through DAOs
    MainDb.scooters().insertScooters(scooters)
    MainDb.users().insertUsers(users)
    MainDb.travelers().insertTravelers(travelers)

    print("dbconfig scooters:", MainDb.scooters().getAllScooters())
    print("dbconfig users:", MainDb.users().getAllUsers())
    print("dbconfig travelers:", MainDb.travelers().getAllTravelers())
    print("Database reset successful.")


if __name__ == "__main__":
    MainDb.initialize()
    # reset_db()

    # passed = AuthHandler.login("super_admin", "Admin_123?")
    # 
    # BackupHandler.createBackup()
    # backups = BackupHandler.getBackupList()
    # for b in backups.values():
    #     BackupHandler.restoreBackup(b.filename)
    #     passed = AuthHandler.login("super_admin", "Admin_123?")
    # 
    # backups = BackupHandler.getBackupList()
    # for b in list(backups.values()):
    #     BackupHandler.deleteBackup(b.filename)
    # 
    # BackupHandler.createBackup()
    # sysAdmins = BackupHandler.getSystemAdmins()
    # for b in backups.values():
    #     sa = list(sysAdmins.values())[0]
    #     BackupHandler.createBackupCode(sa.Username, b.filename)
    #     codes = BackupHandler.getBackupCodeList()
    #     for c in codes.values():
    #         BackupHandler.restoreBackupCode(c.code)
    #         passed = AuthHandler.login("super_admin", "Admin_123?")
# 
    # for c in codes.values():
    #     print(c.code, c.username, c.filename, c.used)

    print("--start--\n\n")

    print("Welcome to the Urban Mobility backend system.\n\n")
    username = input("username: ")
    password = input("password: ")
    if InputHandler.checkUsernameFormat(username) and InputHandler.checkPasswordFormat(password):
        if (not AuthHandler.login(username, password)):
            print("Log in attempt failed")
            l.logEvent(username, "Failed Login attempt by wrong username or password", suspicious= True)
            exit()
        
        page = None
        role = AuthHandler.getCurrentUser().Role

        if role not in ["ServiceEngineer", "SystemAdmin", "SuperAdmin"]:
            print("User found without defined role. logging out.")
            exit()

        l.logEvent(AuthHandler.getCurrentUser().Username, "Succesful Login")

        firstName = AuthHandler.getCurrentUser().FirstName
        if role == "ServiceEngineer":
            print("Welcome Service Engineer " + firstName)
            page = PageServiceEngineer()
        elif role == "SystemAdmin":
            print("Welcome System Admin " + firstName)
            page = PageSystemAdmin()
        elif role == "SuperAdmin":
            print("Welcome Super Admin " + firstName)
            page = PageSuperAdmin()

        if page != None:
            page.Run()
    else:
        print("Invalid input for username or password")

