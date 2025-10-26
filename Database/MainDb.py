import sqlite3
import os

from Database.DataAccesObjects.BackupCodesDAO import BackupCodesDAO
from Database.DataAccesObjects.BackupsDAO import BackupsDAO
from Database.DataAccesObjects.UsersDAO import UsersDAO
from Database.DataAccesObjects.ScootersDAO import ScootersDAO
from Database.DataAccesObjects.TravelersDAO import TravelersDAO

class MainDb:
    mainConn = None
    databaseFile = "UrbanMobilityDB.db"
    databasePath = "Database/UrbanMobilityDB.db"
    
    backupConn = None
    backupFile = "Backups.db"
    backupFilePath = "Database/Backups.db"

    logFilePath = "Database/Data/SystemLogs.enc"

    __users = None
    __scooters = None
    __travelers = None
    __backupCodes = None
    __backups = None

    @classmethod
    def initialize(cls):
        cls.mainConn = cls.connect(cls.databaseFile)
        cls.__users = UsersDAO(cls.mainConn)
        cls.__scooters = ScootersDAO(cls.mainConn)
        cls.__travelers = TravelersDAO(cls.mainConn)

        cls.backupConn = cls.connect(cls.backupFile)
        cls.__backupCodes = BackupCodesDAO(cls.backupConn)
        cls.__backups = BackupsDAO(cls.backupConn)

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
    def connect(cls, file):
        return sqlite3.connect(os.path.join(os.path.dirname(__file__), file))

    @classmethod
    def disconnect(cls):
        if cls.mainConn:
            cls.mainConn.close()
            cls.mainConn = None
        if cls.backupConn:
            cls.backupConn.close()
            cls.backupConn = None
