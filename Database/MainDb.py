import sqlite3
import os

from Database.DataAccesObjects.UsersDAO import UsersDAO
from Database.DataAccesObjects.ScootersDAO import ScootersDAO
from Database.DataAccesObjects.TravelersDAO import TravelersDAO

class MainDb:
    databaseName = "UrbanMobilityDB"
    databaseFile = "UrbanMobilityDB.db"
    databasePath = "Database\\UrbanMobilityDB.db"
    logFilePath = "Database\\Data\\SystemLogs.enc"
    backupPath = "Database\\Backups"
    conn = None
    __users = None
    __scooters = None
    __travelers = None

    @classmethod
    def initialize(cls):
        cls.conn = cls.connect()
        cls.__users = UsersDAO(cls.conn)
        cls.__scooters = ScootersDAO(cls.conn)
        cls.__travelers = TravelersDAO(cls.conn)

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
    def connect(cls):
        return sqlite3.connect(os.path.join(os.path.dirname(__file__), cls.databaseFile))

    def disconnect(self):
        if self.conn:
            self.conn.close()
            self.conn = None
