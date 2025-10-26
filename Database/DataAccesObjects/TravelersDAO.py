from Utils.security import encrypt, decrypt
from Models.Traveler import Traveler
import sqlite3

class TravelersDAO:
    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
    
    def insertTravelers(self, travelers: iter) -> bool:
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
        self.conn.commit()
        if cursor.rowcount > 0: # note: uhh this will still pass if not all were inserted correctly.. i think
            cursor.close()
            return True
        else:
            cursor.close()
            return False
        
    
    def updateTravelerResidence(self, CustomerID: str, streetName: str, houseNumber: str, zipCode: str, city: str) -> bool:
        """Arguments are expected to be plaintext!"""
        cursor = self.conn.cursor()
        travelers = cursor.execute("SELECT * FROM travelers").fetchall()
        for t in travelers:
            if (decrypt(t[0]) == CustomerID):
                cursor.execute("UPDATE travelers SET StreetName = ?, HouseNumber = ?, ZipCode = ?, City = ? WHERE CustomerID = ?",
                               [encrypt(streetName), encrypt(houseNumber), encrypt(zipCode), encrypt(city), t[0]])
                break

        self.conn.commit()
        if cursor.rowcount > 0:
            cursor.close()
            return True
        else:
            cursor.close()
            return False


    def updateTravelerEmail(self, CustomerID: str, email: str) -> bool:
        """Arguments are expected to be plaintext!"""
        cursor = self.conn.cursor()
        travelers = cursor.execute("SELECT * FROM travelers").fetchall()
        for t in travelers:
            if (decrypt(t[0]) == CustomerID):
                cursor.execute("UPDATE travelers SET Email = ? WHERE CustomerID = ?", [encrypt(email), t[0]])
                break
        
        self.conn.commit()
        if cursor.rowcount > 0:
            cursor.close()
            return True
        else:
            cursor.close()
            return False


    def updateTravelerPhoneNumber(self, CustomerID: str, phoneNumber: str) -> bool:
        """Arguments are expected to be plaintext!"""
        cursor = self.conn.cursor()
        travelers = cursor.execute("SELECT * FROM travelers").fetchall()
        for t in travelers:
            if (decrypt(t[0]) == CustomerID):
                cursor.execute("UPDATE travelers SET PhoneNumber = ? WHERE CustomerID = ?", [encrypt(phoneNumber), t[0]])
                break
        
        self.conn.commit()
        if cursor.rowcount > 0:
            cursor.close()
            return True
        else:
            cursor.close()
            return False


    def DeleteTravelerByObject(self, traveler):
        cursor = self.conn.cursor()
        travelers = cursor.execute("SELECT * FROM travelers").fetchall()

        for t in travelers:
            if decrypt(t[0]) == traveler.CustomerID:
                cursor.execute("DELETE FROM travelers WHERE CustoomerID = ?", [t[0]])
                break

        self.conn.commit()
        if cursor.rowcount > 0:
            cursor.close()
            return True
        else:
            cursor.close()
            return False
                
