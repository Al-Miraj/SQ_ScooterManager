import datetime
import random

class Traveler:
    def __init__(self, firstName, lastName, birthday, gender, streetName, houseNumber, zipCode, city, email, phoneNumber, drivingLicenseNumber, registrationDate=None):
        self.CustomerID = self._generateCustomerID()
        self.FirstName = firstName
        self.LastName = lastName
        self.Birthday = birthday
        self.Gender = gender
        self.StreetName = streetName
        self.HouseNumber = houseNumber
        self.ZipCode = zipCode
        self.City = city
        self.Email = email
        self.PhoneNumber = phoneNumber
        self.DrivingLicenseNumber = drivingLicenseNumber
        self.RegistrationDate = datetime.datime.now() if registrationDate == None else registrationDate

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
