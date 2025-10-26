from Utils.security import encrypt, decrypt
from Models.Scooter import Scooter
import sqlite3


class ScootersDAO:
    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
    
    def insertScooters(self, scooters: iter) -> bool:
        cursor = self.conn.cursor()
        for scooter in scooters:
            insertScooterQ = """INSERT OR IGNORE INTO scooters (SerialNumber, Brand, Model, TopSpeed, BatteryCapacity, StateOfCharge, 
                                TargetSoCMin, TargetSoCMax, LocationLatitude, LocationLongitude, 
                                OutOfServiceStatus, Mileage, LastMaintenanceDate, InServiceDate) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            insertScooterV = [encrypt(scooter.SerialNumber),
                              encrypt(scooter.Brand),
                              encrypt(scooter.Model),
                              encrypt(str(scooter.TopSpeed)),
                              encrypt(str(scooter.BatteryCapacity)),
                              encrypt(str(scooter.StateOfCharge)),
                              encrypt(str(scooter.TargetSoCMin)),
                              encrypt(str(scooter.TargetSoCMax)),
                              encrypt(str(scooter.LocationLatitude)),
                              encrypt(str(scooter.LocationLongitude)),
                              encrypt(str(scooter.OutOfServiceStatus)),
                              encrypt(str(scooter.Mileage)),
                              encrypt(str(scooter.LastMaintenanceDate)),
                              encrypt(str(scooter.InServiceDate))
                              ]
            cursor.execute(insertScooterQ, insertScooterV)
        self.conn.commit()
        if cursor.rowcount > 0: # note: uhh this will still pass if not all were inserted correctly.. i think
            cursor.close()
            return True
        else:
            cursor.close()
            return False
    

    def getScooterBySerialNumber(self, serialNumber: str):
        """If found, it returns scooter object, otherwise None"""
        cursor = self.conn.cursor()
        scooters = cursor.execute("SELECT * FROM scooters")

        scooter = None
        for s in scooters:
            if decrypt(s[0]) == serialNumber:
                serialNumber_ = decrypt(s[0])
                brand = decrypt(s[1])
                model = decrypt(s[2])
                topSpeed = float(decrypt(s[3]))
                batteryCapacity = float(decrypt(s[4]))
                stateOfCharge = float(decrypt(s[5]))
                targetSoCMin = float(decrypt(s[6]))
                targetSoCMax = float(decrypt(s[7]))
                locationLatitude = float(decrypt(s[8]))
                locationLongitude = float(decrypt(s[9]))
                outOfServiceStatus = int(decrypt(s[10]))
                mileage = int(decrypt(s[11]))
                lastMaintenanceDate = decrypt(s[12])
                inServiceDate = decrypt(s[13])

                scooter = Scooter(serialNumber_, brand, model, topSpeed, batteryCapacity, stateOfCharge, 
                             targetSoCMin, targetSoCMax, locationLatitude, locationLongitude,
                             outOfServiceStatus, mileage, lastMaintenanceDate, inServiceDate)

                break
        
        cursor.close()
        return scooter


    def updateScooterStateOfCharge(self, serialNumber: str, newSoC: str) -> bool:
        cursor = self.conn.cursor()
        scooters = cursor.execute("SELECT * FROM scooters").fetchall()
        for s in scooters:
            if decrypt(s[0]) == serialNumber:
                cursor.execute("UPDATE scooters SET StateOfCharge = ? WHERE SerialNumber = ?", [encrypt(newSoC), s[0]])
                break
        
        self.conn.commit()
        if cursor.rowcount > 0:
            cursor.close()
            return True
        else:
            cursor.close()
            return False
    

    def updateScooterTargetRangeSoC(self, serialNumber: str, targetSoCMin: str, targetSoCMax: str):
        cursor = self.conn.cursor()
        scooters = cursor.execute("SELECT * FROM scooters").fetchall()
        for s in scooters:
            if decrypt(s[0]) == serialNumber:
                cursor.execute("UPDATE scooters SET TargetSoCMin = ?, TargetSoCMax = ? WHERE SerialNumber = ?", [encrypt(targetSoCMin), encrypt(targetSoCMax), s[0]])
                break
        
        self.conn.commit()
        if cursor.rowcount > 0:
            cursor.close()
            return True
        else:
            cursor.close()
            return False
    
    def updateScooterLocation(self, serialNumber: str, locationLat: str, locationLong: str) -> bool:
        cursor = self.conn.cursor()
        scooters = cursor.execute("SELECT * FROM scooters").fetchall()
        for s in scooters:
            if decrypt(s[0]) == serialNumber:
                cursor.execute("UPDATE scooters SET LocationLatitude = ?, LocationLongitude = ? WHERE SerialNumber = ?", [encrypt(locationLat), encrypt(locationLong), s[0]])
                break
        
        self.conn.commit()
        if cursor.rowcount > 0:
            cursor.close()
            return True
        else:
            cursor.close()
            return False


    def updateScooterOutOfServiceStatus(self, serialNumber: str, status: str) -> bool:
        cursor = self.conn.cursor()
        scooters = cursor.execute("SELECT * FROM scooters").fetchall()
        for s in scooters:
            if decrypt(s[0]) == serialNumber:
                cursor.execute("UPDATE scooters SET OutOfServiceStatus = ? WHERE SerialNumber = ?", [encrypt(status), s[0]])
                break
        
        self.conn.commit()
        if cursor.rowcount > 0:
            cursor.close()
            return True
        else:
            cursor.close()
            return False

        
    def updateScooterMileage(self, serialNumber: str, mileage: str) -> bool:
        cursor = self.conn.cursor()
        scooters = cursor.execute("SELECT * FROM scooters").fetchall()
        for s in scooters:
            if decrypt(s[0]) == serialNumber:
                cursor.execute("UPDATE scooters SET Mileage = ? WHERE SerialNumber = ?", [encrypt(mileage), s[0]])
                break
        
        self.conn.commit()
        if cursor.rowcount > 0:
            cursor.close()
            return True
        else:
            cursor.close()
            return False


    def updateScooterBrand(self, serialNumber: str, brand: str) -> bool:
        cursor = self.conn.cursor()
        scooters = cursor.execute("SELECT * FROM scooters").fetchall()
        for s in scooters:
            if decrypt(s[0]) == serialNumber:
                cursor.execute("UPDATE scooters SET Brand = ? WHERE SerialNumber = ?", [encrypt(brand), s[0]])
                break
        
        self.conn.commit()
        if cursor.rowcount > 0:
            cursor.close()
            return True
        else:
            cursor.close()
            return False


    def updateScooterModel(self, serialNumber: str, model: str) -> bool:
        cursor = self.conn.cursor()
        scooters = cursor.execute("SELECT * FROM scooters").fetchall()
        for s in scooters:
            if decrypt(s[0]) == serialNumber:
                cursor.execute("UPDATE scooters SET Model = ? WHERE SerialNumber = ?", [encrypt(model), s[0]])
                break
        
        self.conn.commit()
        if cursor.rowcount > 0:
            cursor.close()
            return True
        else:
            cursor.close()
            return False
    

    def updateScooterTopSpeed(self, serialNumber: str, topSpeed: str) -> bool:
        cursor = self.conn.cursor()
        scooters = cursor.execute("SELECT * FROM scooters").fetchall()
        for s in scooters:
            if decrypt(s[0]) == serialNumber:
                cursor.execute("UPDATE scooters SET TopSpeed = ? WHERE SerialNumber = ?", [encrypt(topSpeed), s[0]])
                break
        
        self.conn.commit()
        if cursor.rowcount > 0:
            cursor.close()
            return True
        else:
            cursor.close()
            return False


    def updateScooterBatteryCapacity(self, serialNumber: str, batteryCapacity: str) -> bool:
        cursor = self.conn.cursor()
        scooters = cursor.execute("SELECT * FROM scooters").fetchall()
        for s in scooters:
            if decrypt(s[0]) == serialNumber:
                cursor.execute("UPDATE scooters SET BatteryCapacity = ? WHERE SerialNumber = ?", [encrypt(batteryCapacity), s[0]])
                break
        
        self.conn.commit()
        if cursor.rowcount > 0:
            cursor.close()
            return True
        else:
            cursor.close()
            return False