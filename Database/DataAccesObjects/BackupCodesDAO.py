from Models.BackupCode import BackupCode
from Utils.security import hash_password, encrypt, decrypt
import sqlite3


class BackupCodesDAO:
    cache : dict[str, BackupCode] = {}

    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self.cache : dict[str, BackupCode] = self.getAllBackupCodes()

    # Create methods

    def insertBackupCodes(self, backupCodes: iter) -> bool: # type: ignore
        cursor = self.conn.cursor()
        for backupCode in backupCodes:
            backupCode.hash = hash_password(backupCode.hash)

            insertBackupQ = """INSERT OR IGNORE INTO backupCodes (code, filename, hash, username, used)
                            VALUES (?, ?, ?, ?, ?)"""
            insertBackupValues = [encrypt(backupCode.code), 
                                  encrypt(backupCode.filename), 
                                  encrypt(backupCode.hash), 
                                  encrypt(backupCode.username),
                                  backupCode.used]
            cursor.execute(insertBackupQ, insertBackupValues)
            self.cache[backupCode.code] = backupCode
        self.conn.commit()
        if cursor.rowcount > 0:
            cursor.close()
            return True
        else:
            cursor.close()
            return False

    # read methods
    
    def search(self, searchTerm: str) -> dict[str, BackupCode]:
        """return dict of user objects whose username contains the search term"""
        result : dict[str, BackupCode] = {}
        for code, backupCode in self.getAllBackupCodes().items():
            for value in {**backupCode.__dict__}.values():
                if searchTerm in str(value).lower():
                    result[code] = backupCode
                    break
        return result

    def getAllBackupCodes(self) -> dict[str, BackupCode]:
        """return dict of backup code objects from db if cache is empty, otherwise from cache"""
        if not self.cache:
            cursor = self.conn.cursor()
            backupCodes = cursor.execute("SELECT * FROM backupCodes").fetchall()

            for b in backupCodes:
                code = decrypt(b[0])
                userID = decrypt(b[1])
                filename = decrypt(b[2])
                hash = decrypt(b[3])
                username = decrypt(b[4])
                used = b[5]

                backupCode = BackupCode(filename, hash, username, code, used)
                self.cache[code] = backupCode

            cursor.close()
        return self.cache

    def getBackupCodeByCode(self, code):
        """if found, it return backup code object in their respective type, otherwise None"""
        return self.cache.get(code, None)

    # update methods

    def updateCodeUsed(self, code, used):
        """newPassword should ALREADY be hashed"""
        return self.updateField(code, "Used", used)


    def updateField(self, code: str, fieldName: str, newValue: str) -> bool:
        """Generic update method for any field. Update database then cache."""
        cursor = self.conn.cursor()
        backupCodes = cursor.execute("SELECT * FROM backupCodes").fetchall()
        for b in backupCodes:
            if decrypt(b[0]) == code:
                cursor.execute(f"UPDATE backupCodes SET {fieldName} = ? WHERE Code = ?", [encrypt(newValue), b[0]])
                break
        
        self.conn.commit()
        if cursor.rowcount > 0:
            cursor.close()
            if code in self.cache:
                setattr(self.cache[code], fieldName, newValue)
            return True
        else:
            cursor.close()
            return False
    
    # delete methods

    def deleteBackupCode(self, code: str) -> bool:
        cursor = self.conn.cursor()
        backupCodes = cursor.execute("SELECT * FROM backupCodes").fetchall()

        for b in backupCodes:
            if decrypt(b[0]) == code:
                cursor.execute("DELETE FROM backupCodes WHERE Code = ?", [b[0]])
                break

        self.conn.commit()
        if cursor.rowcount > 0:
            cursor.close()
            if code in self.cache:
                del self.cache[code]
            return True
        else:
            cursor.close()
            return False
    

    def deleteAllBackupCodes(self) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM backupCodes")
        self.conn.commit()
        
        if cursor.rowcount > 0:
            cursor.close()
            self.cache.clear()
            return True
        else:
            cursor.close()
            return False