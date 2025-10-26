from Models.User import User
from Utils.security import hash_password, encrypt, decrypt
import sqlite3


class UsersDAO:
    cache : dict[str, User] = {}

    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self.cache : dict[str, User] = self.getAllUsers()

    # Create methods

    def insertUsers(self, users: iter) -> bool: # type: ignore
        """expects password to NOT be hashed yet (might change later)"""
        cursor = self.conn.cursor()
        for user in users:
            user.Password = hash_password(user.Password)

            insertUserQ = """INSERT OR IGNORE INTO users (Username, Password, FirstName, LastName, RegistrationDate, Role)
                            VALUES (?, ?, ?, ?, ?, ?)"""
            insertUsersValues = [encrypt(user.Username), 
                                 encrypt(user.Password), 
                                 encrypt(user.FirstName), 
                                 encrypt(user.LastName), 
                                 encrypt(str(user.RegistrationDate)), 
                                 encrypt(user.Role)]
            cursor.execute(insertUserQ, insertUsersValues)
            self.cache[user.Username] = user
        self.conn.commit()
        if cursor.rowcount > 0:
            cursor.close()
            return True
        else:
            cursor.close()
            return False
        
    # read methods

    def search(self, searchTerm: str) -> dict[str, User]:
        """return dict of user objects whose username contains the search term"""
        result : dict[str, User] = {}
        for username, user in self.getAllUsers().items():
            for value in {**user.__dict__}.values():
                if searchTerm in str(value).lower():
                    result[username] = user
                    break
        return result

    def getAllUsers(self) -> dict[str, User]:
        """return dict of user objects from db if cache is empty, otherwise from cache"""
        if not self.cache:
            cursor = self.conn.cursor()
            users = cursor.execute("SELECT * FROM users").fetchall()

            for u in users:
                username = decrypt(u[0])
                password = decrypt(u[1])
                firstName = decrypt(u[2])
                lastName = decrypt(u[3])
                registrationDate = decrypt(u[4])
                role = decrypt(u[5])

                user = User(username, password, firstName, lastName, role, registrationDate)
                self.cache[username] = user
            
            cursor.close()

        return self.cache
    
    
    def getUserByUsername(self, username):
        """if found, it return user object in their respective type, otherwise None"""
        return self.cache.get(username, None)
    
    # update methods

    def updateUserPassword(self, username, newPassword):
        """newPassword should ALREADY be hashed"""
        return self.updateField(username, "Password", newPassword)
    
    
    def updateUserFirstName(self, username, newFirstName):
        return self.updateField(username, "FirstName", newFirstName)        
                

    def updateUserLastName(self, username, newLastName):
        return self.updateField(username, "LastName", newLastName)
    
    
    def updateField(self, username: str, fieldName: str, newValue: str) -> bool:
        """Generic update method for any field. Update database then cache."""
        cursor = self.conn.cursor()
        users = cursor.execute("SELECT * FROM users").fetchall()
        for u in users:
            if decrypt(u[0]) == username:
                cursor.execute(f"UPDATE users SET {fieldName} = ? WHERE Username = ?", [encrypt(newValue), u[0]])
                break
        
        self.conn.commit()
        if cursor.rowcount > 0:
            cursor.close()
            if username in self.cache:
                setattr(self.cache[username], fieldName, newValue)
            return True
        else:
            cursor.close()
            return False
    
    # delete methods
    
    def deleteUser(self, username: str) -> bool:
        cursor = self.conn.cursor()
        users = cursor.execute("SELECT * FROM users").fetchall()

        for u in users:
            if decrypt(u[0]) == username:
                cursor.execute("DELETE FROM users WHERE Username = ?", [u[0]])
                break

        self.conn.commit()
        if cursor.rowcount > 0:
            cursor.close()
            if username in self.cache:
                del self.cache[username]
            return True
        else:
            cursor.close()
            return False
    

    def deleteAllUsers(self) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM users")
        self.conn.commit()
        
        if cursor.rowcount > 0:
            cursor.close()
            self.cache.clear()
            return True
        else:
            cursor.close()
            return False