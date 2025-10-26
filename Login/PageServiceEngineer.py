from Login.PageBase import PageBase

from Models.User import User
from Utils.InputValidator import InputHandler


class PageServiceEngineer(PageBase[User]):

    def Run(self):
        while True:
            self.printMenu()
            action = input()
            if InputHandler.checkMenuChoice(action):
                if action == "1":
                    self.runUpdatePasswordUI()
                elif action == "2":
                    self.runUpdateScooterUI("ServiceEngineer")
                elif action == "3":
                    print("you chose 3")
                elif action == "4":
                    print("logging out...")
                    break
            else:
                print("Invalid menu option.")
            

    
    def printMenu(self):
        print('''
        
            Choose your action:
            [1] Update own password
            [2] Update scooter attributes
            [3] Search and retrieve scooter information
            [4] Log Out
            '''
        )
    
