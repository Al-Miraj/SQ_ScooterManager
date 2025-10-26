from Utils.security import encrypt, decrypt
from Models.Scooter import Scooter
import sqlite3


class ScootersDAO:
    cache : dict[str, Scooter] = {}

    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self.cache : dict[str, Scooter] = self.getAllScooters()

    # Create methods
    
    def insertScooters(self, scooters: iter) -> bool: # type: ignore
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
            self.cache[scooter.SerialNumber] = scooter
        self.conn.commit()
        if cursor.rowcount > 0: # note: uhh this will still pass if not all were inserted correctly.. i think
            cursor.close()
            return True
        else:
            cursor.close()
            return False
        
    # Read methods
    
    def search(self, searchTerm: str) -> dict[str, Scooter]:
        """return dict of user objects whose username contains the search term"""
        result : dict[str, Scooter] = {}
        for serialNumber, scooter in self.getAllScooters().items():
            for value in {**scooter.__dict__}.values():
                if searchTerm in str(value).lower():
                    result[serialNumber] = scooter
                    break
        return result

    def getAllScooters(self) -> dict[str, Scooter]:
        """return dict of scooter objects from db if cache is empty, otherwise from cache"""
        if not self.cache:
            cursor = self.conn.cursor()
            scooters = cursor.execute("SELECT * FROM scooters").fetchall()

            for s in scooters:
                serialNumber = decrypt(s[0])
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

                scooter = Scooter(serialNumber, brand, model, topSpeed, batteryCapacity, stateOfCharge,
                                  targetSoCMin, targetSoCMax, locationLatitude, locationLongitude,
                                  outOfServiceStatus, mileage, lastMaintenanceDate, inServiceDate)

                self.cache[serialNumber] = scooter

            cursor.close()

        return self.cache


    def getScooterBySerialNumber(self, serialNumber: str):
        """If found, it returns scooter object, otherwise None"""
        return self.cache.get(serialNumber, None)
    
    # update methods

    def updateScooterStateOfCharge(self, serialNumber: str, newSoC: str) -> bool:
        return self.updateField(serialNumber, "StateOfCharge", newSoC)  # update db
    

    def updateScooterTargetRangeSoC(self, serialNumber: str, targetSoCMin: str, targetSoCMax: str):
        return self.updateField(serialNumber, "TargetSoCMin", targetSoCMin) and self.updateField(serialNumber, "TargetSoCMax", targetSoCMax)
    

    def updateScooterLocation(self, serialNumber: str, locationLat: str, locationLong: str) -> bool:
        return self.updateField(serialNumber, "LocationLatitude", locationLat) and self.updateField(serialNumber, "LocationLongitude", locationLong)


    def updateScooterOutOfServiceStatus(self, serialNumber: str, status: str) -> bool:
        return self.updateField(serialNumber, "OutOfServiceStatus", status)  # update db

        
    def updateScooterMileage(self, serialNumber: str, mileage: str) -> bool:
        return self.updateField(serialNumber, "Mileage", mileage)  # update db


    def updateScooterBrand(self, serialNumber: str, brand: str) -> bool:
        return self.updateField(serialNumber, "Brand", brand)  # update db


    def updateScooterModel(self, serialNumber: str, model: str) -> bool:
        return self.updateField(serialNumber, "Model", model)  # update db
    

    def updateScooterTopSpeed(self, serialNumber: str, topSpeed: str) -> bool:
        return self.updateField(serialNumber, "TopSpeed", topSpeed)  # update db


    def updateScooterBatteryCapacity(self, serialNumber: str, batteryCapacity: str) -> bool:
        return self.updateField(serialNumber, "BatteryCapacity", batteryCapacity)  # update db
    

    def updateField(self, serialNumber: str, fieldName: str, newValue: str) -> bool:
        """Generic update method for any field. Update database then cache."""
        cursor = self.conn.cursor()
        scooters = cursor.execute("SELECT * FROM scooters").fetchall()
        for s in scooters:
            if decrypt(s[0]) == serialNumber:
                cursor.execute(f"UPDATE scooters SET {fieldName} = ? WHERE SerialNumber = ?", [encrypt(newValue), s[0]])
                break
        
        self.conn.commit()
        if cursor.rowcount > 0:
            cursor.close()
            # Update cache
            if serialNumber in self.cache:
                scooter = self.cache[serialNumber]
                setattr(scooter, fieldName, newValue)
            return True
        else:
            cursor.close()
            return False

    # Delete methods

    def deleteScooter(self, serialNumber: str) -> bool:
        cursor = self.conn.cursor()
        scooters = cursor.execute("SELECT * FROM scooters").fetchall()

        for s in scooters:
            if decrypt(s[0]) == serialNumber:
                cursor.execute("DELETE FROM scooters WHERE SerialNumber = ?", [s[0]])
                break

        self.conn.commit()
        if cursor.rowcount > 0:
            cursor.close()
            if serialNumber in self.cache:
                del self.cache[serialNumber]
            return True
        else:
            cursor.close()
            return False
         

    def deleteAllScooters(self) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM scooters")
        self.conn.commit()
        
        if cursor.rowcount > 0:
            cursor.close()
            self.cache.clear()
            return True
        else:
            cursor.close()
            return False