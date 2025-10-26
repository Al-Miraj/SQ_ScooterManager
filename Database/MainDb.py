import sqlite3
import os

from Database.DataAccesObjects.BackupCodesDAO import BackupCodesDAO
from Database.DataAccesObjects.BackupsDAO import BackupsDAO
from Database.DataAccesObjects.UsersDAO import UsersDAO
from Database.DataAccesObjects.ScootersDAO import ScootersDAO
from Database.DataAccesObjects.TravelersDAO import TravelersDAO

class MainDb:
    databaseFile = "UrbanMobilityDB.db"
    databasePath = "Database\\UrbanMobilityDB.db"
    backupFile = "Backups.db"
    backupFilePath = "Database\\Backups.db"

    logFilePath = "Database\\Data\\SystemLogs.enc"
    backupPath = "Database\\Backups"
    mainConn = None
    backupConn = None
    __users = None
    __scooters = None
    __travelers = None
    __backupCodes = None
    __backups = None

    @classmethod
    def initialize(cls):
        cls.mainConn = cls.connect()
        cls.__users = UsersDAO(cls.mainConn)
        cls.__scooters = ScootersDAO(cls.mainConn)
        cls.__travelers = TravelersDAO(cls.mainConn)
        cls.__backupCodes = BackupCodesDAO(cls.mainConn)
        cls.__backups = BackupsDAO(cls.mainConn)

    @classmethod
    def users(cls) -> UsersDAO:
        return cls.__users # type: ignore

    @classmethod
    def scooters(cls) -> ScootersDAO:
        return cls.__scooters # type: ignore

    @classmethod
    def travelers(cls) -> TravelersDAO:
        return cls.__travelers # type: ignore

    @classmethod
    def backupCodes(cls) -> BackupCodesDAO:
        return cls.__backupCodes # type: ignore

    @classmethod
    def backups(cls) -> BackupsDAO:
        return cls.__backups # type: ignore

    @classmethod
    def connect(cls):
        return sqlite3.connect(os.path.join(os.path.dirname(__file__), cls.databaseFile))

    def disconnect(self):
        if self.mainConn:
            self.mainConn.close()
            self.mainConn = None
