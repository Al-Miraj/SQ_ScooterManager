import os
import zipfile
from datetime import datetime
import Utils.logger as l
from Database.DBConfig import DBConfig


def makeBackup(user):
    dbPath = DBConfig.DBPath
    backupPath = DBConfig.backupPath
    os.makedirs(backupPath, exist_ok=True)

    # Generate backup filename
    date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backupFilename = f"backup_{date}.zip"
    backupPath = os.path.join(backupPath, backupFilename)

    try:
        with zipfile.ZipFile(backupPath, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
            backup_zip.write(dbPath, arcname=os.path.basename(dbPath))

        print(f"Backup created: {backupFilename}")
        l.logEvent(user.Username, f"Created system backup: {backupFilename}")

    except Exception as e:
        print("Backup failed:", e)
        l.logEvent(user.Username, "Creating Backup failed: " + str(e), suspicious=True)
