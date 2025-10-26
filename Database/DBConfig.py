from .DCM import DCM
from .DataAccesObjects.UsersDAO import UsersDAO
from .DataAccesObjects.ScootersDAO import ScootersDAO

class DBConfig:
    DBName = "UrbanMobilityDB"
    DBFile = "UrbanMobilityDB.db"
    DBPath = "Database\\UrbanMobilityDB.db" #"src\\Database\\UrbanMobilityDB.db"
    travelersJsonPath = "Database\\Data\\travelers.json"
    usersJsonPath = "Database\\Data\\users.json"
    scootersJsonPath = "Database\\Data\\scooters.json"
    logFilePath = "Database\\Data\\SystemLogs.enc"
    backupPath = "Database\\Backups"
    dcm = DCM(DBFile)
    dcm.connect()
    usersDAO = UsersDAO(dcm.conn)
    scootersDAO = ScootersDAO(dcm.conn)
