from Utils.security import encrypt, decrypt
from Models.Traveler import Traveler
import sqlite3

class TravelersDAO:
    cache : dict[str, Traveler] = {}

    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self.cache : dict[str, Traveler] = self.getAllTravelers()
    
    # Create methods

    def insertTravelers(self, travelers: iter) -> bool: # type: ignore
        cursor = self.conn.cursor()
        for traveler in travelers:
            insertTravelerQ = """INSERT OR IGNORE INTO travelers (CustomerID, FirstName, LastName,
                                 Birthday, Gender, StreetName, HouseNumber, ZipCode, City, Email,
                                 PhoneNumber, DrivingLicenseNumber, RegistrationDate)
                                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            insertTravelerV = [encrypt(traveler.CustomerID),
                               encrypt(traveler.FirstName),
                               encrypt(traveler.LastName),
                               encrypt(traveler.Birthday),
                               encrypt(traveler.Gender),
                               encrypt(traveler.StreetName),
                               encrypt(traveler.HouseNumber),
                               encrypt(traveler.ZipCode),
                               encrypt(traveler.City),
                               encrypt(traveler.Email),
                               encrypt(traveler.PhoneNumber),
                               encrypt(traveler.DrivingLicenseNumber),
                               encrypt(traveler.RegistrationDate)]
            cursor.execute(insertTravelerQ, insertTravelerV)
            self.cache[traveler.CustomerID] = traveler
        self.conn.commit()
        if cursor.rowcount > 0: # note: uhh this will still pass if not all were inserted correctly.. i think
            cursor.close()
            return True
        else:
            cursor.close()
            return False
    
    # Read methods
    
    def search(self, searchTerm: str) -> dict[str, Traveler]:
        """return dict of traveler objects whose attributes contain the search term"""
        result : dict[str, Traveler] = {}
        for customerID, traveler in self.getAllTravelers().items():
            for value in {**traveler.__dict__}.values():
                if searchTerm in str(value).lower():
                    result[customerID] = traveler
                    break
        return result

    def getAllTravelers(self) -> dict[str, Traveler]:
        """return dict of traveler objects from db if cache is empty, otherwise from cache"""
        if not self.cache:
            cursor = self.conn.cursor()
            travelers = cursor.execute("SELECT * FROM travelers").fetchall()

            for t in travelers:
                customerID = decrypt(t[0])
                firstName = decrypt(t[1])
                lastName = decrypt(t[2])
                birthday = decrypt(t[3])
                gender = decrypt(t[4])
                streetName = decrypt(t[5])
                houseNumber = decrypt(t[6])
                zipCode = decrypt(t[7])
                city = decrypt(t[8])
                email = decrypt(t[9])
                phoneNumber = decrypt(t[10])
                drivingLicenseNumber = decrypt(t[11])
                registrationDate = decrypt(t[12])

                traveler = Traveler(firstName, lastName, birthday, gender, streetName,
                                    houseNumber, zipCode, city, email, phoneNumber,
                                    drivingLicenseNumber, registrationDate, customerID)

                self.cache[customerID] = traveler

            cursor.close()

        return self.cache
    
    def getTravelerByCustomerID(self, customerID: str):
        """If found, it returns traveler object, otherwise None"""
        return self.cache.get(customerID, None)

    # update methods
    
    def updateTravelerResidence(self, CustomerID: str, streetName: str, houseNumber: str, zipCode: str, city: str) -> bool:
        """Arguments are expected to be plaintext!"""
        success1 = self.updateField(CustomerID, "StreetName", streetName)
        success2 = self.updateField(CustomerID, "HouseNumber", houseNumber)
        success3 = self.updateField(CustomerID, "ZipCode", zipCode)
        success4 = self.updateField(CustomerID, "City", city)
        return success1 and success2 and success3 and success4


    def updateTravelerEmail(self, CustomerID: str, email: str) -> bool:
        """Arguments are expected to be plaintext!"""
        return self.updateField(CustomerID, "Email", email)


    def updateTravelerPhoneNumber(self, CustomerID: str, phoneNumber: str) -> bool:
        """Arguments are expected to be plaintext!"""
        return self.updateField(CustomerID, "PhoneNumber", phoneNumber)


    def updateField(self, serialNumber: str, fieldName: str, newValue: str) -> bool:
        """Generic update method for any field. Update database then cache."""
        cursor = self.conn.cursor()
        travelers = cursor.execute("SELECT * FROM travelers").fetchall()
        for t in travelers:
            if decrypt(t[0]) == serialNumber:
                cursor.execute(f"UPDATE travelers SET {fieldName} = ? WHERE CustomerID = ?", [encrypt(newValue), t[0]])
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

    # delete methods

    def deleteTraveler(self, customerID: str) -> bool:
        cursor = self.conn.cursor()
        travelers = cursor.execute("SELECT * FROM travelers").fetchall()

        for t in travelers:
            if decrypt(t[0]) == customerID:
                cursor.execute("DELETE FROM travelers WHERE CustomerID = ?", [t[0]])
                break

        self.conn.commit()
        if cursor.rowcount > 0:
            cursor.close()
            return True
        else:
            cursor.close()
            return False
                

    def deleteAllTravelers(self) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM travelers")
        self.conn.commit()

        if cursor.rowcount > 0:
            cursor.close()
            self.cache.clear()
            return True
        else:
            cursor.close()
            return False