from Models.Backup import Backup
from Utils.security import hash_password, encrypt, decrypt
import sqlite3


class BackupsDAO:
    cache : dict[str, Backup] = {}

    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self.cache : dict[str, Backup] = self.getAllBackups()

    # Create methods

    def insertBackups(self, backups: iter) -> bool: # type: ignore
        cursor = self.conn.cursor()
        for backup in backups:
            backup.hash = hash_password(backup.hash)

            insertBackupQ = """INSERT OR IGNORE INTO backups (filename, hash, username)
                            VALUES (?, ?, ?)"""
            insertBackupValues = [encrypt(backup.filename), 
                                  encrypt(backup.hash), 
                                  encrypt(backup.username)]
            cursor.execute(insertBackupQ, insertBackupValues)
            self.cache[backup.id] = backup
        self.conn.commit()
        if cursor.rowcount > 0:
            cursor.close()
            return True
        else:
            cursor.close()
            return False

    # read methods

    def search(self, searchTerm: str) -> dict[str, Backup]:
        """return dict of backup objects whose attributes contain the search term"""
        result : dict[str, Backup] = {}
        for filename, backup in self.getAllBackups().items():
            for value in {**backup.__dict__}.values():
                if searchTerm in str(value).lower():
                    result[filename] = backup
                    break
        return result

    def getAllBackups(self) -> dict[str, Backup]:
        """return dict of backup objects from db if cache is empty, otherwise from cache"""
        if not self.cache:
            cursor = self.conn.cursor()
            backups = cursor.execute("SELECT * FROM backups").fetchall()

            for b in backups:
                filename = decrypt(b[0])
                hash = decrypt(b[1])
                username = decrypt(b[2])

                backup = Backup(filename, hash, username)
                self.cache[backup.filename] = backup

            cursor.close()
        return self.cache

    def getBackupByFilename(self, filename):
        """if found, it return backup object in their respective type, otherwise None"""
        return self.cache.get(filename, None)

    # delete methods

    def deleteBackup(self, filename: str) -> bool:
        cursor = self.conn.cursor()
        backups = cursor.execute("SELECT * FROM backups").fetchall()

        for b in backups:
            if b[3] == filename:
                cursor.execute("DELETE FROM backups WHERE filename = ?", [b[3]])
                break

        self.conn.commit()
        if cursor.rowcount > 0:
            cursor.close()
            if filename in self.cache:
                del self.cache[filename]
            return True
        else:
            cursor.close()
            return False
    

    def deleteAllBackups(self) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM backups")
        self.conn.commit()
        
        if cursor.rowcount > 0:
            cursor.close()
            self.cache.clear()
            return True
        else:
            cursor.close()
            return False