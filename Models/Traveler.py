import datetime
import random

class Traveler:
    def __init__(self, FirstName, LastName, Birthday, Gender, StreetName, HouseNumber, ZipCode, City, Email, PhoneNumber, DrivingLicenseNumber, RegistrationDate=None, CustomerID=None):
        self.CustomerID = self._generateCustomerID() if CustomerID is None else CustomerID
        self.FirstName = FirstName
        self.LastName = LastName
        self.Birthday = Birthday
        self.Gender = Gender
        self.StreetName = StreetName
        self.HouseNumber = HouseNumber
        self.ZipCode = ZipCode
        self.City = City
        self.Email = Email
        self.PhoneNumber = PhoneNumber
        self.DrivingLicenseNumber = DrivingLicenseNumber
        self.RegistrationDate = datetime.datetime.now() if RegistrationDate == None else RegistrationDate

    def _generateCustomerID(self):
        today = datetime.datetime.now()

        currentYear = str(today.year)
        yearDigits = currentYear[2:]

        randseq = ""
        for i in range(7):
            randseq += f"{random.randint(0, 9)}"

        sum = 0
        for char in yearDigits + randseq:
            sum += int(char)
        checksum = str(sum % 10)

        return yearDigits + randseq + checksum
