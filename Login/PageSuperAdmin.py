from Login.PageBase import PageBase

from Models.User import User
from Utils.InputValidator import InputHandler




class PageSuperAdmin(PageBase[User]):
    def Run(self):
        while True:
            self.printMenu()
            action = input()
            if InputHandler.checkMenuChoice(action):
                if action == "1":
                    self.runUpdateScooterUI("SuperAdmin")
                elif action == "2":
                    print("you chose 2")
                elif action == "3":
                    self.runViewAllUsersUI()
                elif action == "4":
                    self.runAddNewUserUI("ServiceEngineer")
                elif action == "5":
                    self.runUpdateUserUI("ServiceEngineer")
                elif action == "6":
                    self.runDeleteUserUI("ServiceEngineer")
                elif action == "7":
                    self.runResetUserPasswordUI("ServiceEngineer")
                elif action == "8":
                    self.runViewLogFilesUI()
                elif action == "9":
                    print("you chose 9")
                elif action == "10":
                    print("you chose 10")
                elif action == "11":
                    print("you chose 11")
                elif action == "12":
                    print("you chose 12")
                elif action == "13":
                    print("you chose 13")
                elif action == "14":
                    print("you chose 14")
                elif action == "15":
                    print("you chose 15")
                elif action == "16":
                    self.runAddNewUserUI("SystemAdmin")
                elif action == "17":
                    self.runUpdateUserUI("SystemAdmin")
                elif action == "18":
                    self.runDeleteUserUI("SystemAdmin")
                elif action == "19":
                    self.runResetUserPasswordUI("SystemAdmin")
                elif action == "20":
                    print("you chose 20")
                elif action == "21":
                    print("you chose 21")
                elif action == "22":
                    print("you chose 22")
                elif action == "23":
                    print("you chose 23")
                elif action == "24":
                    print("logging out..")
                    break
            else:
                print("Invalid menu option.")
    

    def printMenu(self):
        print('''
        
            Choose your action:
            [1] Update scooter attributes
            [2] Search and retrieve scooter information
            [3] View all users
            [4] Add new Service Engineer
            [5] Update Service Engineer
            [6] Delete Service Engineer
            [7] Reset Service Engineer Password
            [8] View Log files
            [9] Add new Traveler
            [10] Update Traveler Information
            [11] Delete Traveler
            [12] Add new Scooter
            [13] Update Scooter information
            [14] Delete Scooter
            [15] Search Traveler info
            [16] Add new System Admin
            [17] Update System Admin
            [18] Delete System Admin
            [19] Reset System Admin Password
            [20] Make System Backup
            [21] Restore System Backup
            [22] Authorise System Admin for backup restoration
            [23] Revoke System Admin backup restoration authorisation
            [24] Log Out
            '''
            )