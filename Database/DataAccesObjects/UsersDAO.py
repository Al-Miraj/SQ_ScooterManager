from Utils.security import hash_password, encrypt, decrypt
from Roles.ServiceEngineer import ServiceEngineer
from Roles.SystemAdmin import SystemAdmin
from Roles.SuperAdmin import SuperAdmin
import sqlite3


class UsersDAO:
    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection

    def updateUserPassword(self, username, newPassword):
        """newPassword should ALREADY be hashed"""
        cursor = self.conn.cursor()
        users = cursor.execute("SELECT * FROM users").fetchall()
        for user in users:
            if decrypt(user[0]) == username:
                cursor.execute("UPDATE users SET Password = ? WHERE Username = ?", [encrypt(newPassword), user[0]])
                self.conn.commit()
                cursor.close()
                return True
        
        cursor.close()
        return False
    
    def updateUserFirstName(self, username, newFirstName):
        cursor = self.conn.cursor()
        users = cursor.execute("SELECT * FROM users").fetchall()
        for user in users:
            if decrypt(user[0]) == username:
                cursor.execute("UPDATE users SET FirstName = ? WHERE Username = ?", [encrypt(newFirstName), user[0]])
                break
            
        self.conn.commit()
        if cursor.rowcount > 0:
            cursor.close()
            return True
        else:
            cursor.close()
            return False
        
                

    def updateUserLastName(self, username, newLastName):
        cursor = self.conn.cursor()
        users = cursor.execute("SELECT * FROM users").fetchall()
        for user in users:
            if decrypt(user[0]) == username:
                cursor.execute("UPDATE users SET LastName = ? WHERE Username = ?", [encrypt(newLastName), user[0]])
                break
            
        self.conn.commit()
        if cursor.rowcount > 0:
            cursor.close()
            return True
        else:
            cursor.close()
            return False



    def insertUsers(self, users: iter) -> bool:
        """expects password to NOT be hashed yet (might change later)"""
        cursor = self.conn.cursor()
        for user in users:
            insertUserQ = """INSERT OR IGNORE INTO users (Username, Password, FirstName, LastName, RegistrationDate, Role)
                            VALUES (?, ?, ?, ?, ?, ?)"""
            insertUsersValues = [encrypt(user.Username), 
                                 encrypt(hash_password(user.Password + user.Username)), 
                                 encrypt(user.FirstName), 
                                 encrypt(user.LastName), 
                                 encrypt(str(user.RegistrationDate)), 
                                 encrypt(user.Role)]
            cursor.execute(insertUserQ, insertUsersValues)
        self.conn.commit()
        if cursor.rowcount > 0:
            cursor.close()
            return True
        else:
            cursor.close()
            return False
    
    def getUserByUsername(self, username):
        """if found, it return user object in their respective type, otherwise None"""
        cursor = self.conn.cursor()
        users = cursor.execute("SELECT * FROM users").fetchall()

        user = None
        for u in users:
            if decrypt(u[0]) == username:
                username = decrypt(u[0])
                password = decrypt(u[1])
                firstName = decrypt(u[2])
                lastName = decrypt(u[3])
                registrationDate = decrypt(u[4])
                role = decrypt(u[5])

                if role == "ServiceEngineer":
                    serviceEngineer = ServiceEngineer(username, password, firstName, lastName, registrationDate)
                    user = serviceEngineer
                elif role == "SystemAdmin":
                    systemAdmin = SystemAdmin(username, password, firstName, lastName, registrationDate)
                    user = systemAdmin
                elif role == "SuperAdmin":
                    superAdmin = SuperAdmin(username, password, firstName, lastName, registrationDate)
                    user = superAdmin
                break
        
        cursor.close()
        return user

    def getAllUsers(self):
        """return list of user objects in their respective type"""
        cursor = self.conn.cursor()
        users = cursor.execute("SELECT * FROM users").fetchall()
        
        usersObjs = []
        for user in users:
            username = decrypt(user[0])
            password = decrypt(user[1])
            firstName = decrypt(user[2])
            lastName = decrypt(user[3])
            registrationDate = decrypt(user[4])
            role = decrypt(user[5])

            if role == "ServiceEngineer":
                serviceEngineer = ServiceEngineer(username, password, firstName, lastName, registrationDate)
                usersObjs.append(serviceEngineer)
            elif role == "SystemAdmin":
                systemAdmin = SystemAdmin(username, password, firstName, lastName, registrationDate)
                usersObjs.append(systemAdmin)
            elif role == "SuperAdmin":
                superAdmin = SuperAdmin(username, password, firstName, lastName, registrationDate)
                usersObjs.append(superAdmin)

        cursor.close()
        return usersObjs
    
    def DeleteUserByObject(self, user):
        cursor = self.conn.cursor()
        users = cursor.execute("SELECT * FROM users").fetchall()

        for u in users:
            if decrypt(u[0]) == user.Username:
                cursor.execute("DELETE FROM users WHERE Username = ?", [u[0]])
                self.conn.commit()
                if cursor.rowcount > 0:
                    cursor.close()
                    return True
                else:
                    break
        cursor.close()
        return False

