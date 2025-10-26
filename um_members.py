# this is the main file. 
# starting the application should be done by running this file
from Database.DBConfig import DBConfig

from Models.Traveler import Traveler
from Models.Scooter import Scooter
from Models.User import User
from Utils.security import verify_password
from Utils.InputValidator import InputHandler

#////////////
from Login.PageServiceEngineer import PageServiceEngineer
from Login.PageSystemAdmin import PageSystemAdmin
from Login.PageSuperAdmin import PageSuperAdmin

import Utils.logger as l


# FEEDBACK
# type casting considered massaging the input. the format is just string
# authorisation not complete after changing. session control after changing critical operations that make the session invalid


def reset_db():
    DBConfig.scootersDAO.deleteAllScooters()
    DBConfig.usersDAO.deleteAllUsers()
    DBConfig.travelersDAO.deleteAllTravelers()

    # check if db is empty
    if (len(DBConfig.scootersDAO.getAllScooters()) != 0) or \
       (len(DBConfig.usersDAO.getAllUsers()) != 0) or \
       (len(DBConfig.travelersDAO.getAllTravelers()) != 0):
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
    DBConfig.scootersDAO.insertScooters(scooters)
    DBConfig.usersDAO.insertUsers(users)
    DBConfig.travelersDAO.insertTravelers(travelers)

    print("dbconfig scooters:", DBConfig.scootersDAO.getAllScooters())
    print("dbconfig users:", DBConfig.usersDAO.getAllUsers())
    print("dbconfig travelers:", DBConfig.travelersDAO.getAllTravelers())
    print("Database reset successful.")


if __name__ == "__main__":
    reset_db()

    print("--start--\n\n")

    print("Welcome to the Urban Mobility backend system.\n\n")
    username = input("username: ")
    password = input("password: ")
    if InputHandler.checkUsernameFormat(username) and InputHandler.checkPasswordFormat(password):
        loginUser = DBConfig.usersDAO.getUserByUsername(username)
        if loginUser != None:
            result = verify_password(password, loginUser.Password)
            if result:
                page = None

                if loginUser.Role != "ServiceEngineer" and loginUser.Role != "SystemAdmin" and loginUser.Role != "SuperAdmin":
                    print("User found without defined role. logging out.")
                    exit()

                username_ = loginUser.Username
                password_ = loginUser.Password
                firstName = loginUser.FirstName
                lastName = loginUser.LastName
                registrationDate = loginUser.RegistrationDate
                user = User(username_, password_, firstName, lastName, registrationDate)
                l.logEvent(user.Username, "Succesful Login")

                if loginUser.Role == "ServiceEngineer":
                    print("Welcome Service Engineer " + loginUser.FirstName)
                    page = PageServiceEngineer(user)
                elif loginUser.Role == "SystemAdmin":
                    print("Welcome System Admin " + loginUser.FirstName)
                    page = PageSystemAdmin(user)
                elif loginUser.Role == "SuperAdmin":
                    print("Welcome Super Admin " + loginUser.FirstName + " " + loginUser.LastName)
                    page = PageSuperAdmin(user)
                
                if page != None:
                    page.Run()
            else:
                print("Log in attempt failed")
                l.logEvent(username, "Failed Login attempt by wrong password", suspicious= True)
        else:
            print("Log in attempt failed.")
            l.logEvent(username, "Failed Login attempt by username not found", suspicious= True)
    else:
        print("Invalid input for username or password")

