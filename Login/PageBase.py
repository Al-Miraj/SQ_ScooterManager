from typing import Generic, TypeVar
from Models.User import User
from Utils.security import verify_password, hash_password
from Database.DBConfig import DBConfig

from Utils.InputValidator import InputHandler
import Utils.logger as l
import Utils.backupMaker as b

T = TypeVar("T", bound=User)

class PageBase(Generic[T]):
    def __init__(self, user: T):
        self.User = user
    
    def runUpdatePasswordUI(self):
        print("Update new password.\n")
        oldPassword = input("Enter current password: ")
        newPassword = input("Enter new password: ")
        newPasswordRepeat = input("Repeat new password: ")

        if InputHandler.checkPasswordFormat(oldPassword) and InputHandler.checkPasswordFormat(newPassword) and InputHandler.checkPasswordFormat(newPasswordRepeat):
            if verify_password(oldPassword + self.User.Username, self.User.Password):
                if newPassword != oldPassword:
                    if newPassword == newPasswordRepeat:
                        newPasswordHashed = hash_password(newPassword + self.User.Username)

                        result = DBConfig.usersDAO.updateUserPassword(self.User.Username, self.User.Password)
                        if result:
                            print("Password has been updated.")
                            l.logEvent(self.User.Username, "Updating password succesful")
                        else:
                            print("Something went wrong. Updating password Failed")
                            l.logEvent(self.User.Username, f"Failed DB update for updating password ({self.User.Username})", suspicious=True)
                else:
                    print("You must enter a new password. Updating Password failed.")
            else:
                print("Wrong password. Updating password failed")
                l.logEvent(self.User.Username, "Updating password failed due to wrong old password.", suspicious= True)
        else:
            print("Invalid input for one or more password inputs.")
    
    def runViewAllUsersUI(self):
        print("View all users.\n")
        users = DBConfig.usersDAO.getAllUsers()
        for user in users:
            print(user)
            print()

    def runAddNewUserUI(self, role: str):
        print(f"Add new {role}.\n")

        username = input("Username: ")
        password = input("Password: ")
        passwordRepeat = input("Repeat Password: ")
        firstName = input("First name: ")
        lastName = input("Last name: ")
        
        if InputHandler.checkUsernameFormat(username):
            if InputHandler.checkPasswordFormat(password):
                if InputHandler.checkPasswordFormat(passwordRepeat):
                    if InputHandler.checkFirstName(firstName):
                        if InputHandler.checkLastName(lastName):
                            login_user = DBConfig.usersDAO.getUserByUsername(username)
                            passwordIsConfirmed = password == passwordRepeat
                            usernameNotFound = login_user == None

                            if passwordIsConfirmed and usernameNotFound:
                                user = None
                                if role == "ServiceEngineer":
                                    user = User(username, password, firstName, lastName, "ServiceEngineer")
                                elif role == "SystemAdmin":
                                    user = User(username, password, firstName, lastName, "SystemAdmin")
                                else:
                                    print(f"Role of new user unclear. Adding {role} failed.")

                                if user != None:
                                    result = DBConfig.usersDAO.insertUsers([user])
                                    if result:
                                        print(f"{role} succesfully added:\n")
                                        print(user)
                                        l.logEvent(self.User.Username, f"Adding new {role} ({user.Username}) succesful")
                                    else:
                                        print(f"Something went wrong. Adding {role} failed.")
                                        l.logEvent(self.User.Username, f"Failed DB update for adding new user ({user.Username})", suspicious= True)
                                else:
                                    print(f"Unable to create new user. Adding {role} failed.")
                                    l.logEvent(self.User.Username, f"Adding new {role} ({username}) failed because current user has invalid role", suspicious= True)
                            else:
                                print(f"Something went wrong. Adding {role} failed.")
                        else:
                            print("Invalid input for last name.")
                    else:
                        print("Invalid input for first name")
                else:
                    print("Invalid input for retpeated password")
            else:
                print("Invalid input for password")
        else:
            print("Invalid input for username")



    def runDeleteUserUI(self, role: str):
        print(f"Delete {role}.\n")

        username = input(f"Enter the username of the {role} you want to delete: ")
        if InputHandler.checkUsernameFormat(username):
            user = DBConfig.usersDAO.getUserByUsername(username)
            if user != None and user.Role == role: # user found and is of role to delete
                print(user)
                print()
                confirmUser = input(f"Is this the correct {role}? (y/n)")
                if InputHandler.checkConfirmChoice(confirmUser):
                    if confirmUser == "y":
                        print("Deleting this account can NOT be undone. Confirm deletion by entering your password.")
                        password = input("Password: ")
                        if InputHandler.checkPasswordFormat(password):
                            if verify_password(password + self.User.Username, self.User.Password):
                                result = DBConfig.usersDAO.deleteUser(user.Username)
                                if result:
                                    print(f"{role} deleted succesfully")
                                    l.logEvent(self.User.Username, f"Deleting {role} ({user.Username}) succesful")
                                else:
                                    print(f"Deleting {role} failed")
                                    l.logEvent(self.User.Username, f"Failed DB update for deleting user ({user.Username}),", suspicious=True)
                            else:
                                print(f"Incorrect password. Deleting {role} canceled.")
                                l.logEvent(self.User.Username, f"Deleting {role} ({user.Username}) failed because of false password.", suspicious= True)
                        else: 
                            print(f"Invalid input for password")
                    else: # "n"
                        print(f"Deleting {role} canceled.")
                else:
                    print(f"Invalid input for confirm message")
            else:
                print(f"{role} not found. Deleting {role} failed.")
        else:
            print("invalid format for username")
    
    def runUpdateUserUI(self, role: str):
        print(f"Update {role}.\n")

        if role not in {"ServiceEngineer", "SystemAdmin"}:
            print(f"Role of the user you want to update is unclear. Updating {role} failed")
            l.logEvent(self.User.Username, f"Updating user method accessed by unauthorised user ({self.User.Username})", suspicious=True)
            return

        username = input(f"Enter the username of the {role} you want to update: ")
        if InputHandler.checkUsernameFormat(username):
            user = DBConfig.usersDAO.getUserByUsername(username)
            if user != None and user.Role == role:
                print(user)
                print()
                confirmUser = input(f"Is this the correct {role}? (y/n)")
                if confirmUser == "y":
                    print("What would you like to update?")
                    print("[1] First Name")
                    print("[2] Last Name")
                    print("[3] cancel")
                    choice = input("-> ")
                    if InputHandler.checkMenuChoice(choice):
                        if choice == "1": # is this allowed? would an attacker be able to change this value like with HTML server generated inputs thru a POST? should allowed values be stored else where?
                            if role == "ServiceEngineer":
                                self.updateServiceEngineerFN(user)
                            else:
                                self.updateSystemAdminFN(user)
                        elif choice == "2":
                            if role == "ServiceEngineer":
                                self.updateServiceEngineerLN(user)
                            else:
                                self.updateSystemAdminLN(user)
                        elif choice == "3":
                            return
                    else:
                        print(f"Input not valid. Updating {role} failed.")
                elif confirmUser == "n":
                    print(f"Updating {role} canceled.")
                else:
                    print(f"Input not recognised. Updating {role} failed.")
            else:
                print(f"{role} not found. Updating {role} failed.")
        else:
            print("invalid format for username")
    

    def updateServiceEngineerFN(self, serviceEngineer: User):
        newFirstName = input("Enter the new First Name: ")
        if InputHandler.checkFirstName(newFirstName):
            if newFirstName == serviceEngineer.FirstName:
                print("New First Name is identical to old First Name. Updating Service Engineer First Name canceled.")
            else:
                serviceEngineer.FirstName = newFirstName
                result = DBConfig.usersDAO.updateUserFirstName(serviceEngineer.Username, serviceEngineer.FirstName)
                if result:
                    print("Updated Service Engineer First Name succesfully.")
                    l.logEvent(self.User.Username, f"Updating ServiceEngineer ({serviceEngineer.Username}) first name succesful")
                else:
                    print("Updating Service Engineer First Name failed.")
                    l.logEvent(self.User.Username, f"Failed DB update for ServiceEngineer ({serviceEngineer.Username}) first name", suspicious=True)
        else:
            print("invalid format for first name")

    def updateServiceEngineerLN(self, serviceEngineer: User):
        newLastName = input("Enter the new Last Name: ")
        if InputHandler.checkLastName(newLastName):
            if newLastName == serviceEngineer.LastName:
                print("New Last Name is identical to old Last Name. Updating Service Engineer Last Name canceled.")
            else:
                serviceEngineer.LastName = newLastName
                result = DBConfig.usersDAO.updateUserLastName(serviceEngineer.Username, serviceEngineer.LastName)
                if result:
                    print("Updated Service Engineer Last Name succesfully.")
                    l.logEvent(self.User.Username, f"Updating ServiceEngineer ({serviceEngineer.Username}) last name succesful")
                else:
                    print("Updating Service Engineer Last Name failed.")
                    l.logEvent(self.User.Username, f"Failed DB update for ServiceEngineer ({serviceEngineer.Username}) last name", suspicious=True)
        else:
            print("invalid format for last name")


    def runResetUserPasswordUI(self, role: str):
        print(f"Reset {role} Password.\n")

        username = input(f"Enter the username of the {role} you want to reset the password of: ")
        if InputHandler.checkUsernameFormat(username):
            user = DBConfig.usersDAO.getUserByUsername(username)
            if user != None and user.Role == role:
                print(user)
                print()
                confirmUser = input(f"Is this the correct {role}? (y/n)")
                if InputHandler.checkConfirmChoice(confirmUser):
                    if confirmUser == "y":
                        print("Confirm action by entering your password.")
                        password = input("Password: ")
                        if InputHandler.checkPasswordFormat(password):
                            if verify_password(password + self.User.Username, self.User.Password):
                                result = DBConfig.usersDAO.updateUserPassword(username, hash_password("Temp123!" + username))
                                if result:
                                    print(f"Ressetted {role} password succesfully")
                                    l.logEvent(self.User.Username, f"Resetting {role} password ({user.Username}) succesful")
                                else:
                                    print(f"Resetting {role} password failed")
                                    l.logEvent(self.User.Username, f"Failed DB update for resetting {role} ({user.Username}) password", suspicious=True)
                            else:
                                print(f"Incorrect password. Deleting {role} canceled.")
                                l.logEvent(self.User.Username, f"Deleting {role} ({user.Username}) failed because of false password.", suspicious= True)
                        else:
                            print("Invalid format for password")
                    elif confirmUser == "n":
                        print(f"Resetting {role} password canceled.")
                else:
                    print(f"Input not valid. Resetting {role} password failed.")
            else:
                print(f"{role} not found. Resetting {role} password failed.")
        else:
            print("invalid format for username")

    def runUpdateOwnAccountUI(self):
        print("Update own account.\n")

        print(self.User)
        print()

        print("What would you like to update?")
        print("[1] First Name")
        print("[2] Last Name")
        print("[3] Password")
        print("[4] cancel")
        choice = input("-> ")
        if InputHandler.checkMenuChoice(choice):
            if choice == "1":
                self.updateSystemAdminFN(self.User)
            elif choice == "2":
                self.updateSystemAdminLN(self.User)
            elif choice == "3":
                self.runUpdatePasswordUI()
            elif choice == "4":
                return
        else:
            print("Input not valid. Updating Service Engineer failed.")

    def updateSystemAdminFN(self, systemAdmin: User):
        newFirstName = input("Enter the new First Name: ")
        if InputHandler.checkFirstName(newFirstName):
            if newFirstName == systemAdmin.FirstName:
                print("New First Name is identical to old First Name. Updating System Admin First Name canceled.")
            else:
                systemAdmin.FirstName = newFirstName
                result = DBConfig.usersDAO.updateUserFirstName(systemAdmin.Username, systemAdmin.FirstName)
                if result:
                    print("Updated System Admin First Name succesfully.")
                    l.logEvent(self.User.Username, f"Updating SystemAdmin ({systemAdmin.Username}) first name succesful")
                else:
                    print("Updating System Admin First Name failed.")
                    l.logEvent(self.User.Username, f"Failed DB update for SystemAdmin ({systemAdmin.Username}) first name", suspicious=True)
        else:
            print("invalid input for first name")


    def updateSystemAdminLN(self, systemAdmin: User):
        newLastName = input("Enter the new Last Name: ")
        if InputHandler.checkLastName(newLastName):
            if newLastName == systemAdmin.LastName:
                print("New Last Name is identical to old Last Name. Updating System Admin Last Name canceled.")
            else:
                systemAdmin.LastName = newLastName
                result = DBConfig.usersDAO.updateUserLastName(systemAdmin.Username, systemAdmin.LastName)
                if result:
                    print("Updated System Admin Last Name succesfully.")
                    l.logEvent(self.User.Username, f"Updating SystemAdmin ({systemAdmin.Username}) last name succesful")
                else:
                    print("Updating System Admin Last Name failed.")
                    l.logEvent(self.User.Username, f"Failed DB update for SystemAdmin ({systemAdmin.Username}) last name", suspicious=True)
        else:
            print("input for last name invalid")

    def runDeleteOwnAccountUI(self) -> bool:
        print("Delete own account.\n")

        if self.User.Role == "SystemAdmin":
            print(self.User)
            print()

            confirmDeletion = input("Are you sure you want to delete your account? This action can NOT be undone (y/n) ")
            if InputHandler.checkConfirmChoice(confirmDeletion):
                if confirmDeletion == "y":
                    print("you will be logged out after deletion. \nConfirm deletion by entering your password.")
                    password = input("Password: ")
                    if InputHandler.checkPasswordFormat(password):
                        if verify_password(password + self.User.Username, self.User.Password):
                            result = DBConfig.usersDAO.deleteUser(self.User.Username)
                            if result:
                                print("Your Account has been deleted succesfully")
                                l.logEvent(self.User.Username, f"Deleting own account succesful")
                                return True
                            else:
                                print("Deleting your account has failed")
                                l.logEvent(self.User.Username, f"Failed DB deletion for deleting own account", suspicious=True)
                        else:
                            print("Incorrect password. Deleting your account canceled.")
                            l.logEvent(self.User.Username, f"Deleting own account failed because of false password.", suspicious= True)
                    else:
                        print("invalid format for password")
                else: # "n"
                    print("Deleting this account canceled.")
            else:
                print("Invalid input for confirm. Deleting this account failed.")
        else:
            print("This user is not authorised to delete its own account.")
            l.logEvent(self.User.Username, f"Deleting own account method accessed by unauthorised user ({self.User.Username})", suspicious=True)
        
        return False


    def runUpdateScooterUI(self, role: str):
        print("Update Scooter Attributes.\n")

        if role not in {"ServiceEngineer", "SystemAdmin", "SuperAdmin"}:
            print(f"Role of current user unclear. Updating scooter failed")
            return

        serialNumber = input("Enter the Serial Number of the scooter you want to update: ")
        if InputHandler.checkScooterSerialNumber(serialNumber):
            scooter = DBConfig.scootersDAO.getScooterBySerialNumber(serialNumber)
            if scooter != None:
                print(scooter)
                print()
                confirmScooter = input("Is this the correct scooter? (y/n)")
                if InputHandler.checkConfirmChoice(confirmScooter):
                    if confirmScooter == "y":
                        if role in {"ServiceEngineer", "SystemAdmin", "SuperAdmin"}:
                            print("What would you like to update?")
                            print("[1] State of Charge")
                            print("[2] Target State of Charge")
                            print("[3] Location")
                            print("[4] Out of Service Status")
                            print("[5] Mileage")
                            print("[6] Last Maintenance Date")
                        if role == "SystemAdmin" or role == "SuperAdmin":
                            print("[7] Brand")
                            print("[8] Model")
                            print("[9] Top Speed")
                            print("[10] Battery Capacity")
                        print("[0] cancel")
                        choice = input("-> ")
                        if InputHandler.checkMenuChoice(choice):
                            if choice == "1":
                                self.updateScooterSoC(scooter)
                            elif choice == "2":
                                self.updateScooterTargetSoC(scooter)
                            elif choice == "3":
                                self.updateScooterLocation(scooter)
                            elif choice == "4":
                                self.updateScooterOutOfServiceStatus(scooter)
                            elif choice == "5":
                                self.updateScooterMileage(scooter)
                            elif choice == "6":
                                self.updateScooterLastMaintenanceDate(scooter)
                            elif choice == "7":
                                self.updateScooterBrand(scooter)
                            elif choice == "8":
                                self.updateScooterModel(scooter)
                            elif choice == "9":
                                self.updateScooterTopSpeed(scooter)
                            elif choice == "10":
                                self.updateScooterBatteryCapacity(scooter)
                            elif choice == "0":
                                return
                        else:
                            print("Input not valid for menu choice. Updating scooter failed.")
                    else: # "n"
                        print("Updating scooter canceled.")
                else:
                    print("Input not valid for confirm. Updating scooter failed.")
            else:
                print("Scooter not found. Updating scooter failed.")
        else:
            print("invalid format for serial number")

    def updateScooterSoC(self, scooter):
        print(f"Current State of Charge: {scooter.StateOfCharge}%")

        newSoC = input("Enter the new State of Charge: ")
        if InputHandler.checkChargePercentage(newSoC):
            newSoCFloat = float(newSoC)
            scooter.StateOfCharge = newSoCFloat
            result = DBConfig.scootersDAO.updateScooterStateOfCharge(scooter.SerialNumber, str(scooter.StateOfCharge))
            if result:
                print("Updated State of Charge succesfully.")
                l.logEvent(self.User.Username, f"Updating Scooter State of Charge ({scooter.SerialNumber}) succesful")
            else:
                print("Updating State of Charge failed.")
                l.logEvent(self.User.Username, f"Failed DB update for scooter State of Charge ({scooter.SerialNumber})", suspicious=True)
        else:
            print("Input whas not valid. Updating Scooter State of Charge failed.")


    def updateScooterTargetSoC(self, scooter):
        print(f"Current Target Range State of Charge: {scooter.TargetSoCMin}% - {scooter.TargetSoCMax}%")


        print("If you dont want to change one of the Range ends, just enter the same value.")
        newMin = input("Enter the new Minimum Range: ")
        newMax = input("Enter the new Maximum Range: ")

        if InputHandler.checkChargePercentage(newMin):
            if InputHandler.checkChargePercentage(newMax):
                newMinFloat = float(newMin)
                newMaxFloat = float(newMax)
                if newMinFloat <= newMaxFloat:
                    scooter.TargetSoCMin = newMinFloat
                    scooter.TargetSoCMax = newMaxFloat
                    result = DBConfig.scootersDAO.updateScooterTargetRangeSoC(scooter.SerialNumber, str(scooter.TargetSoCMin), str(scooter.TargetSoCMax))
                    if result:
                        print("Updated State of Charge succesfully.")
                        print(f"Current Target Range State of Charge: {scooter.TargetSoCMin}% - {scooter.TargetSoCMax}%")
                        l.logEvent(self.User.Username, f"Updating Scooter Target Range State of Charge ({scooter.SerialNumber}) succesful")
                    else:
                        print("Updating State of Charge failed.")
                        l.logEvent(self.User.Username, f"Failed DB update for scooter Target Range State of Charge ({scooter.SerialNumber})", suspicious=True)
            else:
                print("Input was not valid for maximum range. Updating Scooter State of Charge failed.")
        else:
            print("Input was not valid for minimum range. Updating Scooter State of Charge failed.")


    def updateScooterLocation(self, scooter):
        print("Updating scooter Location.\n")
        print(f"Current Location:")
        print(f"Latitude: {scooter.LocationLatitude}")
        print(f"Longitude: {scooter.LocationLongitude}")

        print("If you dont want to change one of the coordinates, just enter the same value.")
        newLat = input("Enter new Latitude (e.g., 51.92250): ")
        newLong = input("Enter new Longitude (e.g., 4.47917): ")

        if InputHandler.checkCoordinate(newLat):
            if InputHandler.checkCoordinate(newLong):
                if InputHandler.checkCoordinateInRotterdam(newLat, newLong):
                    newLatFloat = float(newLat)
                    newLongFloat = float(newLong)
                    scooter.LocationLatitude = newLatFloat
                    scooter.LocationLongitude = newLongFloat
                    result = DBConfig.scootersDAO.updateScooterLocation(scooter.SerialNumber, str(scooter.LocationLatitude), str(scooter.LocationLongitude))
                    if result:
                        print("Updated scooter Location successfully.")
                        l.logEvent(self.User.Username, f"Updating Scooter Location ({scooter.SerialNumber}) succesful")
                    else:
                        print("Updating scooter Location failed.")
                        l.logEvent(self.User.Username, f"Failed DB update for scooter Location ({scooter.SerialNumber})", suspicious=True)
                else:
                    print("New coordinates are outside of Rotterdam")
            else:
                print("Invalid longitude coordinate input. Updating scooter location failed.")
        else:
            print("Invalid latitude coordinate input. Updating scooter location failed.")


    def updateScooterOutOfServiceStatus(self, scooter):
        print("Updating Scooter Out Of Service Status.\n")
        print("If Status is '1' then it is Out of Service (unavailable). '0' means In Service (available)")
        print(f"Current Out Of Service Status: {scooter.OutOfServiceStatus}\n")
        confirmFlip = input(f"Would you like to flip the status from {scooter.OutOfServiceStatus} to {0 if scooter.OutOfServiceStatus == 1 else 1}? (y/n) ")
        if InputHandler.checkConfirmChoice(confirmFlip):
            if confirmFlip == "y":
                scooter.OutOfServiceStatus = 0 if scooter.OutOfServiceStatus == 1 else 1
                result = DBConfig.scootersDAO.updateScooterOutOfServiceStatus(scooter.SerialNumber, str(scooter.OutOfServiceStatus))
                if result:
                    print("Updated scooter Out of Service Status successfully.")
                    l.logEvent(self.User.Username, f"Updating Scooter Out of Service Status ({scooter.SerialNumber}) succesful")
                else:
                    print("Updating scooter Out of Service Status failed.")
                    l.logEvent(self.User.Username, f"Failed DB update for scooter Out of Service Status ({scooter.SerialNumber})", suspicious=True)
            else: # "n"
                print(f"Updating Out of Service Status canceled.")
        else:
            print(f"Input not valid for confirm. Updating Out of Service Status failed.")


    def updateScooterMileage(self, scooter):
        print(f"Current Mileage: {scooter.Mileage} km")

        newMileage = input("Enter the new Mileage: ")
        if InputHandler.checkMileage(newMileage):
            newMileageInt = int(newMileage)
            scooter.Mileage = newMileageInt
            result = DBConfig.scootersDAO.updateScooterMileage(scooter.SerialNumber, str(scooter.Mileage))
            if result:
                print("Updated Mileage succesfully.")
                l.logEvent(self.User.Username, f"Updating Scooter Mileage ({scooter.SerialNumber}) succesful")
            else:
                print("Updating Mileage failed.")
                l.logEvent(self.User.Username, f"Failed DB update for scooter Mileage ({scooter.SerialNumber})", suspicious=True)
        else:
            print("Input was not valid for mileage. Updating Scooter Mileage failed.")

    def updateScooterLastMaintenanceDate(self, scooter):
        print("updating last maintenance date feature currently out of order.")
    

    def updateScooterBrand(self, scooter):
        print(f"Current Brand: {scooter.Brand}")

        newBrand = input("Enter the new Brand: ")
        if InputHandler.checkBrand(newBrand):
            scooter.Brand = newBrand
            result = DBConfig.scootersDAO.updateScooterBrand(scooter.SerialNumber, scooter.Brand)
            if result:
                print("Updated Brand succesfully.")
                l.logEvent(self.User.Username, f"Updating Scooter Brand ({scooter.SerialNumber}) succesful")
            else:
                print("Updating Brand failed.")
                l.logEvent(self.User.Username, f"Failed DB update for scooter Brand ({scooter.SerialNumber})", suspicious=True)
        else:
            print("Input was not valid for brand. Updating Scooter Brand failed.")
    

    def updateScooterModel(self, scooter):
        print(f"Current Model: {scooter.Model}")

        newModel = input("Enter the new Model: ")
        if InputHandler.checkModel(newModel):
            scooter.Model = newModel
            result = DBConfig.scootersDAO.updateScooterModel(scooter.SerialNumber, scooter.Model)
            if result:
                print("Updated Model succesfully.")
                l.logEvent(self.User.Username, f"Updating Scooter Model ({scooter.SerialNumber}) succesful")
            else:
                print("Updating Model failed.")
                l.logEvent(self.User.Username, f"Failed DB update for scooter Model ({scooter.SerialNumber})", suspicious=True)
        else:
            print("Input was not valid for model. Updating Scooter Model failed.")
    

    def updateScooterTopSpeed(self, scooter):
        print(f"Current Top Speed: {scooter.TopSpeed} km/h")

        newTopSpeed = input("Enter the new Top Speed: ")
        if InputHandler.checkTopSpeed(newTopSpeed):
            newTopSpeedFloat = float(newTopSpeed)
            scooter.TopSpeed = newTopSpeedFloat
            result = DBConfig.scootersDAO.updateScooterTopSpeed(scooter.SerialNumber, str(scooter.TopSpeed))
            if result:
                print("Updated Top Speed succesfully.")
                l.logEvent(self.User.Username, f"Updating Scooter Top Speed ({scooter.SerialNumber}) succesful")
            else:
                print("Updating Top Speed failed.")
                l.logEvent(self.User.Username, f"Failed DB update for scooter Top Speedd ({scooter.SerialNumber})", suspicious=True)
        else:
            print("Input was not valid for top speed. Updating Scooter Top Speed failed.")
    

    def updateScooterBatteryCapacity(self, scooter):
        print(f"Current Battery Capacity: {scooter.BatteryCapacity} Wh")

        newBatteryCapacity = input("Enter the new Battery Capacity: ")
        if InputHandler.checkBattaryCapacity(newBatteryCapacity):
            newBatteryCapacityFloat = float(newBatteryCapacity)
            scooter.BatteryCapacity = newBatteryCapacityFloat
            result = DBConfig.scootersDAO.updateScooterBatteryCapacity(scooter.SerialNumber, str(scooter.BatteryCapacity))
            if result:
                print("Updated Battery Capacity succesfully.")
                l.logEvent(self.User.Username, f"Updating Scooter Battery Capacity ({scooter.SerialNumber}) succesful")
            else:
                print("Updating Battery Capacity failed.")
                l.logEvent(self.User.Username, f"Failed DB update for scooter Battery Capacity ({scooter.SerialNumber})", suspicious=True)
        else:
            print("Input was not valid for battery capacity. Updating Scooter Battery Capacity failed.")

    def runViewLogFilesUI(self):
        print("View Log Files.\n")
        logs = l.getLogs()

        if not logs:
            print("No logs found.\n")
            return

        print(f"{'No.':<4} {'Timestamp':<20} {'User':<15} {'Suspicious':<12} Description")
        print("-" * 80)

        for i, log in enumerate(logs, start=1):
            suspicious_tag = "YES" if log["suspicious"] else "NO"
            print(f"{i:<4} {log['timestamp']:<20} {log['username']:<15} {suspicious_tag:<12} {log['description']}")

        print("\n==================\n")

        l.markLogAsRead()
    

    def runMakeBackupUI(self):
        print("Make Backup.\n")
        b.makeBackup(self.User)
    
    def runRestoreBackupUI(self):
        print("Not implemented sorri :(")
