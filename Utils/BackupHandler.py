

from datetime import datetime
import os
from pathlib import Path
import secrets
import string
import sys

from Utils.AuthHandler import AuthHandler
import Utils.logger as l


class BackupHandler:
    @classmethod
    def get_full_path(cls, file_path: str) -> Path:
        """Get the full path of a file."""
        base = getattr(
            sys, "_MEIPASS", Path(os.path.dirname(os.path.abspath(__file__)))
        )
        return base / file_path

    # create backup
    @classmethod
    def createBackup(cls):
        user = AuthHandler.getCurrentUser()

        if user.Role not in ["SuperAdmin", "SystemAdmin"]:
            print("Unauthorized: Only SuperAdmin and SystemAdmin can create backups.")
            l.logEvent(user.Username, "Failed Backup creation attempt", suspicious=True)
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        target_file = f"Backups/backup_{timestamp}.sec"
        src_path = cls.get_full_path("./Database/urban_mobility.db")
        backup_path = cls.get_full_path(target_file)

    # restore backup (forced)
    @classmethod
    def restoreBackup(cls):
        pass

    # create backup code
    @classmethod
    def createBackupCode(cls):
        chars = string.ascii_letters + string.digits + string.punctuation
        backupCode = "".join(secrets.choice(chars) for _ in range(10))
        return backupCode

    # restore backup code (single use, single user)
    @classmethod
    def restoreBackupCode(cls):
        pass
 
    # revoke backup code
    @classmethod
    def revokeBackupCode(cls):
        pass

    # delete backup (and codes)
    @classmethod
    def deleteBackup(cls):
        pass

    # get list of backups for user (all for SuperAdmin)
    @classmethod
    def getBackupList(cls):
        pass

    # get list of backup codes for user (all for SuperAdmin)
    @classmethod
    def getBackupCodeList(cls):
        pass