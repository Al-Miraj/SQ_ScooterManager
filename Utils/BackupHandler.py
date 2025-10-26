from datetime import datetime
import hashlib
import os
from pathlib import Path
import secrets
import shutil
import string

from Database.MainDb import MainDb
from Models.Backup import Backup
from Models.BackupCode import BackupCode
from Utils.AuthHandler import AuthHandler
import Utils.logger as l


class BackupHandler:    

    @staticmethod
    def caclulate_hash(full_file_path: Path) -> str:
        hash_func = getattr(hashlib, "sha256")()

        with open(full_file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)

        return hash_func.hexdigest()

    @classmethod
    def find_project_root(cls, filename="um_members.py"):
        path = Path(__file__).resolve()
        for parent in path.parents:
            if (parent / filename).exists():
                return parent
        raise FileNotFoundError(f"{filename} not found in any parent folder")

    # create backup
    @classmethod
    def createBackup(cls):
        user = AuthHandler.getCurrentUser()
        root = cls.find_project_root()

        if user.Role not in ["SuperAdmin", "SystemAdmin"]:
            print("Unauthorized: Only SuperAdmin and SystemAdmin can create backups.")
            l.logEvent(user.Username, "Failed Backup creation attempt", suspicious=True)
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        target_file = f"Database/Backups/backup{timestamp}.sec"
        src_path = root / "Database/UrbanMobilityDB.db"
        backup_path = root / target_file
        
        try:
            shutil.copy2(src_path, backup_path)
            hash = cls.caclulate_hash(backup_path)
            backup = Backup(target_file,hash,user.Username)
            created = MainDb.backups().insertBackups([backup])

            if not created:
                print(f"Failed to save backup metadata")
                os.remove(backup_path)
            return
        
        except Exception as e:
            print(f"Failed to create backup: {str(e)}")

    @classmethod
    def __restore_backup_file(cls, filename):
        root = cls.find_project_root()
        src_path = root / filename
        dest_path = root / "Database/UrbanMobilityDB.db"

        if dest_path.exists() and src_path.exists():
            try:
                MainDb.disconnect()
                os.remove(dest_path)
            except Exception as e:
                print(f"Failed to remove existing database file: {str(e)}")
                l.logEvent(AuthHandler.getCurrentUser().Username, "Failed to remove existing database file during restore", suspicious=True)
            else:
                print("Existing database file removed successfully.")
                l.logEvent(AuthHandler.getCurrentUser().Username, "Existing database file removed successfully during restore")

        # copy the backup file to the database location
        shutil.copy2(src_path, dest_path)
        MainDb.initialize() # re-initialize the database connections
        AuthHandler.logout() # log out current user since the database has changed

    # restore backup (forced)
    @classmethod
    def restoreBackup(cls, filename):
        user = AuthHandler.getCurrentUser()
        if user.Role not in ["SuperAdmin"]:
            print("Unauthorized: Only SuperAdmin can force restore backups.")
            l.logEvent(user.Username, "Failed Backup restoration attempt", suspicious=True)
            return
        
        backup = MainDb.backups().getBackupByFilename(filename)
        if not backup:
            print(f"Backup not found: {filename}")
            return
        
        # restore the backup file
        cls.__restore_backup_file(filename)

        print(f"Backup {filename} restored successfully.")

    # restore backup code (single use, single user)
    @classmethod
    def restoreBackupCode(cls, backupCode):
        user = AuthHandler.getCurrentUser()
        if user.Role not in ["SystemAdmin"]:
            print("Unauthorized: Only SystemAdmin can restore backup codes.")
            l.logEvent(user.Username, "Failed Backup code restoration attempt", suspicious=True)
            return

        backup_code = MainDb.backupCodes().getBackupCodeByCode(backupCode)

        if not backup_code:
            print(f"Backup code not found: {backupCode}")
            return
        
        if user.Username != backup_code.username:
            print(f"Unauthorized: Backup code does not belong to the current user.")
            l.logEvent(user.Username, "Failed Backup code restoration attempt - wrong user", suspicious=True)
            return
        
        if backup_code.used is not None or backup_code.used != "":
            print(f"Backup code already used: {backupCode}")
            return
        
        # restore the backup file
        cls.__restore_backup_file(backup_code.filename)

        # mark backup code as used
        MainDb.backupCodes().updateCodeUsed(backup_code.code, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        # Restore the backup code (implementation depends on your specific requirements)
        print(f"Backup code {backupCode} restored successfully.")

    # create backup code
    @classmethod
    def __createBackupCode(cls):
        chars = string.ascii_letters + string.digits + string.punctuation
        backupCode = "".join(secrets.choice(chars) for _ in range(10))
        return backupCode
    
    @classmethod
    def createBackupCode(cls, username, filename):
        user = AuthHandler.getCurrentUser()
        root = cls.find_project_root()

        if user.Role not in ["SuperAdmin"]:
            print("Unauthorized: Only SuperAdmin can create backup codes.")
            l.logEvent(user.Username, "Failed Backup code creation attempt", suspicious=True)
            return
        
        backup = MainDb.backups().getBackupByFilename(filename)

        if not backup:
            print(f"Backup not found: {filename}")
            return

        backupCode = cls.__createBackupCode()
        print(f"Backup code created for {filename}: {backupCode}")
        created = MainDb.backupCodes().insertBackupCodes([BackupCode(filename, backup.hash, username, backupCode, None)])

        if not created:
            print(f"Failed to save backup code metadata")
            return
 
    # revoke backup code
    @classmethod
    def revokeBackupCode(cls):
        user = AuthHandler.getCurrentUser()
        if user.Role not in ["SuperAdmin"]:
            print("Unauthorized: Only SuperAdmin can revoke backup codes.")
            l.logEvent(user.Username, "Failed Backup code revocation attempt", suspicious=True)
            return

        code = input("Enter backup code to revoke: ")
        backup_code = MainDb.backupCodes().getBackupCodeByCode(code)

        if not backup_code:
            print(f"Backup code not found: {code}")
            return

        revoked = MainDb.backupCodes().deleteBackupCode(code)

        if revoked:
            print(f"Backup code {code} revoked successfully.")
        else:
            print(f"Failed to revoke backup code {code}.")

    # delete backup (and codes)
    @classmethod
    def deleteBackup(cls, filename):
        user = AuthHandler.getCurrentUser()
        if user.Role not in ["SuperAdmin"]:
            print("Unauthorized: Only SuperAdmin can delete backups.")
            l.logEvent(user.Username, "Failed Backup deletion attempt", suspicious=True)
            return
        
        deleted = MainDb.backups().deleteBackup(filename)
        MainDb.backupCodes().deleteCodesForBackup(filename)  # also delete associated backup codes

        if deleted:
            root = cls.find_project_root()
            backup_path = root / filename
            if backup_path.exists():
                try:
                    os.remove(backup_path)
                except Exception as e:
                    print(f"Failed to remove backup file: {str(e)}")
                    l.logEvent(user.Username, "Failed to remove backup file during deletion", suspicious=True)
                else:
                    print("Backup file removed successfully.")
                    l.logEvent(user.Username, "Backup file removed successfully during deletion")

            print(f"Backup {filename} deleted successfully.")
        else:
            print(f"Failed to delete backup {filename}.")

    # get list of backups for user (all for SuperAdmin)
    @classmethod
    def getBackupList(cls):
        user = AuthHandler.getCurrentUser()
        if user.Role == "SuperAdmin":
            return MainDb.backups().getAllBackups()
        elif user.Role == "SystemAdmin":
            # get all backups, filter where username is user.Username
            all_backups = MainDb.backups().getAllBackups()
            user_backups = {k: v for k, v in all_backups.items() if v.username == user.Username}
            return user_backups
        return {}

    # get list of backup codes for user (all for SuperAdmin)
    @classmethod
    def getBackupCodeList(cls):
        user = AuthHandler.getCurrentUser()
        if user.Role == "SuperAdmin":
            return MainDb.backupCodes().getAllBackupCodes()
        elif user.Role == "SystemAdmin":
            all_backup_codes = MainDb.backupCodes().getAllBackupCodes()
            user_backup_codes = {k: v for k, v in all_backup_codes.items() if v.username == user.Username}
            return user_backup_codes
        return {}
    
    @classmethod
    def getSystemAdmins(cls):
        user = AuthHandler.getCurrentUser()
        if user.Role == "SuperAdmin":
            all_system_admins = MainDb.users().getAllUsers()
            system_admins = {k: v for k, v in all_system_admins.items() if v.Role == "SystemAdmin"}
            return system_admins
        return {}