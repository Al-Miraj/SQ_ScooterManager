from Login.PageBase import PageBase

from Utils.InputValidator import InputHandler



        
class PageSystemAdmin(PageBase):


    def Run(self):
        while True:
            self.printMenu()
            action = input()
            if InputHandler.checkMenuChoice(action):
                if action == "1":
                    self.runUpdatePasswordUI()
                elif action == "2":
                    self.runUpdateScooterUI("SystemAdmin")
                elif action == "3":
                    print("you chose 3")
                elif action == "4":
                    self.runViewAllUsersUI()
                elif action == "5":
                    self.runAddNewUserUI("ServiceEngineer")
                elif action == "6":
                    self.runUpdateUserUI("ServiceEngineer")
                elif action == "7":
                    self.runDeleteUserUI("ServiceEngineer")
                elif action == "8":
                    self.runResetUserPasswordUI("ServiceEngineer")
                elif action == "9":
                    self.runUpdateOwnAccountUI()
                elif action == "10":
                    result = self.runDeleteOwnAccountUI()
                    if result:
                        print("logging out..")
                        break
                elif action == "11":
                    self.runMakeBackupUI()
                elif action == "12":
                    print("you chose 12")
                elif action == "13":
                    self.runViewLogFilesUI()
                elif action == "14":
                    print("you chose 14")
                elif action == "15":
                    print("you chose 15")
                elif action == "16":
                    print("you chose 16")
                elif action == "17":
                    print("you chose 17")
                elif action == "18":
                    self.runUpdateScooterUI("SystemAdmin")
                elif action == "19":
                    print("you chose 19")
                elif action == "20":
                    print("you chose 20")
                elif action == "21":
                    print("logging out..")
                    break
            else:
                print("Invalid menu option.")


    
    def printMenu(self):
        print('''
        
            Choose your action:
            [1] Update own password
            [2] Update scooter attributes
            [3] Search and retrieve scooter information
            [4] View all users
            [5] Add new Service Engineer
            [6] Update Service Engineer
            [7] Delete Service Engineer
            [8] Reset Service Engineer Password
            [9] Update own account
            [10] Delete own account
            [11] Make System Backup
            [12] Restore System Backup
            [13] View Log files
            [14] Add new Traveler
            [15] Update Traveler Information
            [16] Delete Traveler
            [17] Add new Scooter
            [18] Update Scooter information
            [19] Delete Scooter
            [20] Search Traveler info
            [21] Log Out
            '''
            )