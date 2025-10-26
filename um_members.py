# this is the main file. 
# starting the application should be done by running this file
from Database.DBConfig import DBConfig
from Roles.ServiceEngineer import ServiceEngineer
from Roles.SystemAdmin import SystemAdmin
from Roles.SuperAdmin import SuperAdmin
from Models.Scooter import Scooter

from Utils.security import encrypt, decrypt, verify_password, hash_password
from Utils.InputValidator import InputHandler

#////////////
from Login.PageServiceEngineer import PageServiceEngineer
from Login.PageSystemAdmin import PageSystemAdmin
from Login.PageSuperAdmin import PageSuperAdmin

import Utils.logger as l


# FEEDBACK
# type casting considered massaging the input. the format is just string
# authorisation not complete after changing. session control after changing critical operations that make the session invalid


t = [
    {
        "CustomerID": "2521030014",
        "FirstName": "Xiaomi",
        "LastName": "King",
        "Birthday": "2004-05-10T14:23:00",
        "Gender": "M",
        "StreetName": "Pink Avenue",
        "HouseNumber": "576",
        "ZipCode": "3697WR",
        "City": "Roosendaal",
        "Email": "xiaomi@outlook.com",
        "PhoneNumber": "+31-6-12345678",
        "DrivingLicenseNumber": "AB1234567",
        "RegistrationDate": "2024-05-10T14:23:00"
    },
    {
        "CustomerID": "2588503102",
        "FirstName": "Hannah",
        "LastName": "Pet",
        "Birthday": "1994-10-11T14:23:00",
        "Gender": "F",
        "StreetName": "Bouwgaarweg",
        "HouseNumber": "12A",
        "ZipCode": "2586QE",
        "City": "Rotterdam",
        "Email": "hannah@outlook.com",
        "PhoneNumber": "+31-6-87654321",
        "DrivingLicenseNumber": "CD7654321",
        "RegistrationDate": "2024-05-10T14:23:00"
    },
    {
        "CustomerID": "2537698886",
        "FirstName": "Chorouk",
        "LastName": "Cherry",
        "Birthday": "2003-02-07T14:23:00",
        "Gender": "F",
        "StreetName": "KittyLane",
        "HouseNumber": "777",
        "ZipCode": "1475PO",
        "City": "Nijmegen",
        "Email": "cherry@outlook.com",
        "PhoneNumber": "+31-6-11223344",
        "DrivingLicenseNumber": "E98765432",
        "RegistrationDate": "2024-05-10T14:23:00"
    },
    {
        "CustomerID": "2512938707",
        "FirstName": "Dilara",
        "LastName": "Azul",
        "Birthday": "2001-08-08T14:23:00",
        "Gender": "F",
        "StreetName": "Lightningbaan",
        "HouseNumber": "918",
        "ZipCode": "0274AZ",
        "City": "Vienna",
        "Email": "dilara@outlook.com",
        "PhoneNumber": "+31-6-92735548",
        "DrivingLicenseNumber": "D92735548",
        "RegistrationDate": "2024-05-10T14:23:00"
    },
    {
        "CustomerID": "2550075059",
        "FirstName": "Lucy",
        "LastName": "Daisy",
        "Birthday": "2003-11-11T14:23:00",
        "Gender": "F",
        "StreetName": "DuckDuck Lane",
        "HouseNumber": "111",
        "ZipCode": "1111LU",
        "City": "Linköping",
        "Email": "lucy@outlook.com",
        "PhoneNumber": "+31-6-00001111",
        "DrivingLicenseNumber": "LU1029384",
        "RegistrationDate": "2024-05-10T14:23:00"
    }
]

if __name__ == "__main__":

    # for tr in t:
    #     print(f"{tr['FirstName']} => {InputHandler.checkFirstName(tr['FirstName'])}")
    #     print(f"{tr['LastName']} => {InputHandler.checkLastName(tr['LastName'])}")
    #     print(f"{tr['Birthday']} => {InputHandler.isValidTravelerBirthday(tr['Birthday'])}")
    #     print(f"{tr['Gender']} => {InputHandler.isValidTravelerGender(tr['Gender'])}")
    #     print(f"{tr['StreetName']} => {InputHandler.isValidTravelerStreetName(tr['StreetName'])}")
    #     print(f"{tr['HouseNumber']} => {InputHandler.isValidTravelerHouseNumber(tr['HouseNumber'])}")
    #     print(f"{tr['ZipCode']} => {InputHandler.isValidTravelerZipCode(tr['ZipCode'])}")
    #     print(f"{tr['City']} => {InputHandler.isValidTravelerCity(tr['City'])}")
    #     print(f"{tr['Email']} => {InputHandler.isValidTravelerEmail(tr['Email'])}")
    #     print(f"{tr['PhoneNumber']} => {InputHandler.isValidTravelerPhoneNumber(tr['PhoneNumber'])}")
    #     print(f"{tr['DrivingLicenseNumber']} => {InputHandler.isValidTravelerDrivinLicenseNumber(tr['DrivingLicenseNumber'])}")
    #     print()



    conn = DBConfig.dcm.conn
    cursor = conn.cursor()
    



    print("--start--\n\n")

    print("Welcome to the Urban Mobility backend system.\n\n")
    username = input("username: ")
    password = input("password: ")
    if InputHandler.checkUsernameFormat(username) and InputHandler.checkPasswordFormat(password):
        loginUser = DBConfig.usersDAO.getUserByUsername(username)
        if loginUser != None:
            result = verify_password(password + username, loginUser.Password)
            if result:
                if loginUser.Role == "ServiceEngineer":
                    print("Welcome Service Engineer " + loginUser.FirstName)
                    username_ = loginUser.Username
                    password_ = loginUser.Password
                    firstName = loginUser.FirstName
                    lastName = loginUser.LastName
                    registrationDate = loginUser.RegistrationDate
                    user = ServiceEngineer(username_, password_, firstName, lastName, registrationDate)
                    l.logEvent(user.Username, "Succesful Login")

                    page = PageServiceEngineer(user)
                    page.Run()
                elif loginUser.Role == "SystemAdmin":
                    print("Welcome System Admin " + loginUser.FirstName)
                    username_ = loginUser.Username
                    password_ = loginUser.Password
                    firstName = loginUser.FirstName
                    lastName = loginUser.LastName
                    registrationDate = loginUser.RegistrationDate
                    user = SystemAdmin(username_, password_, firstName, lastName, registrationDate)
                    l.logEvent(user.Username, "Succesful Login")

                    page = PageSystemAdmin(user)
                    page.Run()
                elif loginUser.Role == "SuperAdmin":
                    print("Welcome Super Admin " + loginUser.FirstName + " " + loginUser.LastName)
                    username_ = loginUser.Username
                    password_ = loginUser.Password
                    firstName = loginUser.FirstName
                    lastName = loginUser.LastName
                    registrationDate = loginUser.RegistrationDate
                    user = SuperAdmin(username_, password_, firstName, lastName, registrationDate)
                    l.logEvent(user.Username, "Succesful Login")

                    page = PageSuperAdmin(user)
                    page.Run()
                else:
                    print("User found without defined role. logging out.")
            else:
                print("Log in attempt failed")
                l.logEvent(username, "Failed Login attempt by wrong password", suspicious= True)
        else:
            print("Log in attempt failed.")
            l.logEvent(username, "Failed Login attempt by username not found", suspicious= True)
    else:
        print("Invalid input for username or password")

