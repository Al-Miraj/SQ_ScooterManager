import re
import datetime



CITIES = {
    "Amsterdam", 
    "Rotterdam", 
    "Roosendaal", 
    "Breda", 
    "Tilburg", 
    "Heerlen", 
    "Nijmegen",
    "Vienna",
    "Linköping"
    }




class InputHandler:

    @staticmethod
    def nullByteIsAbsent(value:str)->bool:
        return "\0" not in value
    
    
    @staticmethod
    def checkUsernameFormat(username:str) -> bool:
        if username == "super_admin": return True
        if InputHandler.nullByteIsAbsent(username):
            if (8 <= len(username) <= 10):
                if re.search(r'[a-z_]', username[0]):
                    if re.search(r'^[a-z0-9_\'\.]+$', username[1:]): 
                        return True
        return False


    @staticmethod
    def checkPasswordFormat(password:str)->bool: 
        if password == "Admin_123?": return True
        if InputHandler.nullByteIsAbsent(password):
            if (12 <= len(password) <= 30):
                if (re.search(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[\\~!@#$%&_\-+=`|\(){}[\]:;'<>,.?\/])[A-Z\\a-z0-9~!@#$%&_\-+=`|\(){}[\]:;'<>,.?\/]{12,30}$", password)):
                    return True
        return False


    @staticmethod
    def checkFirstName(firstName:str)->bool:
        if InputHandler.nullByteIsAbsent(firstName):
            if (1<= len(firstName) <= 25):
                if re.search(r"^[A-Za-z][A-Za-z'\- ]*[A-Za-z]$", firstName):
                    return True
        return False


    @staticmethod
    def checkLastName(lastName:str)->bool:
        if InputHandler.nullByteIsAbsent(lastName):
            if (1<= len(lastName) <= 25):
                if re.search(r"^[A-Za-z][A-Za-z'\- ]*[A-Za-z]$", lastName):
                    return True
        return False


    # note: allows double digits to start with zero,
    # but honestly thats fine in this usecase because
    # that will just be seen as a non option thingy in the ui layer
    @staticmethod
    def checkMenuChoice(choice:str)-> bool:
        if InputHandler.nullByteIsAbsent(choice):
            if 0 < len(choice) <= 2:
                if re.fullmatch(r'\d{1,2}', choice):
                    return True
        return False

    @staticmethod
    def checkScooterSerialNumber(serialNumber: str) -> bool:
        if InputHandler.nullByteIsAbsent(serialNumber):
            if re.fullmatch(r'[A-Za-z0-9]{10,17}', serialNumber):
                return True
        return False

    @staticmethod
    def checkConfirmChoice(confirm: str) -> bool:
        if InputHandler.nullByteIsAbsent(confirm):
            if confirm in {'y', 'n'}:
                return True
        return False

    @staticmethod
    def checkChargePercentage(chargePercentage: str) -> bool:
        if InputHandler.nullByteIsAbsent(chargePercentage) == True:
            if isinstance(re.fullmatch(r'\d{1,3}(\.\d{1,2})?', chargePercentage), re.Match) == True:
                try: # WRONG APPROACH - check for the range without casting to float. hint: split it at the decimal, if the string on the left of the decimal is 2 chars long, both just need to be 1-9. if it is three chars long it should be equal to the string  "100". on the left side both chars should be 1-9.
                    value = float(chargePercentage)
                    if 0 <= value <= 100:
                        return True
                except ValueError:
                    return False
        return False

    @staticmethod
    def checkCoordinate(coordinate: str) -> bool:
        if InputHandler.nullByteIsAbsent(coordinate):
            if re.fullmatch(r'\d{1,3}\.\d{1,5}', coordinate):
                try:
                    _ = float(coordinate)
                    return True
                except ValueError:
                    return False
        return False

    @staticmethod
    def checkCoordinateInRotterdam(latitude: str, longitude: str) -> bool:
        try:
            lat = float(latitude)
            lon = float(longitude)
            return 51.85000 <= lat <= 52.00000 and 4.40000 <= lon <= 4.60000
        except ValueError:
            return False

    @staticmethod
    def checkMileage(mileage: str) -> bool:
        if InputHandler.nullByteIsAbsent(mileage):
            if mileage.isdigit():
                try:
                    value = int(mileage)
                    if 0 <= value <=100000:
                        return True
                except ValueError:
                    return False
        return False

    @staticmethod
    def checkBrand(brand: str) -> bool:
        if InputHandler.nullByteIsAbsent(brand):
            if 1 <= len(brand) <= 25:
                if re.fullmatch(r'[A-Za-z0-9\- ]+', brand):
                    return True
        return False

    @staticmethod
    def checkModel(model: str) -> bool:
        if InputHandler.nullByteIsAbsent(model):
            if 1 <= len(model) <= 25:
                if re.fullmatch(r'[A-Za-z0-9\- ]+', model):
                    return True
        return False

    @staticmethod
    def checkTopSpeed(topSpeed: str) -> bool:
        if InputHandler.nullByteIsAbsent(topSpeed):
            try:
                '''
                000000000000000000000000000000000000050
                this should be invalid but is accepted by this check
                '''
                value = float(topSpeed)
                if 0 < value <= 150:
                    return True
            except ValueError:
                return False
        return False

    @staticmethod
    def checkBattaryCapacity(batteryCapacity: str) -> bool:
        if InputHandler.nullByteIsAbsent(batteryCapacity):
            try:
                value = float(batteryCapacity)
                if 250 < value <= 500: # how? without massaging input??
                    return True
            except ValueError:
                return False
        return False

    @staticmethod
    def isValidTravelerBirthday(birthday: str) -> bool:
        if InputHandler.nullByteIsAbsent(birthday):
            try:
                datetime.datetime.strptime(birthday, "%Y-%m-%dT%H:%M:%S")
                return True
            except ValueError:
                return False

    @staticmethod
    def isValidTravelerGender(gender: str) -> bool:
        if InputHandler.nullByteIsAbsent(gender):
            if len(gender) == 1:
                if gender == "M" or gender == "F":
                    return True
        return False

    @staticmethod
    def isValidTravelerStreetName(streetName: str) -> bool:
        if InputHandler.nullByteIsAbsent(streetName):
            if (2 <= len(streetName) <= 24):
                if re.search(r"^[A-Za-z][A-Za-z'\-. ]*[A-Za-z]$", streetName):
                    return True
        return False

    @staticmethod
    def isValidTravelerHouseNumber(houseNumber: str) -> bool:
        if InputHandler.nullByteIsAbsent(houseNumber):
            if 1 <= len(houseNumber) <= 6:
                if re.fullmatch(r'^[A-Za-z0-9]+$', houseNumber):
                    return True
        return False
    
    @staticmethod
    def isValidTravelerZipCode(zipCode: str) -> bool:
        if InputHandler.nullByteIsAbsent(zipCode):
            if len(zipCode) == 6:
                if re.search(r"^[0-9]*$", zipCode[:4]):
                    if re.search(r"^[A-Z]*$", zipCode[4:]): #isupper allows spaces
                        return True
        return False
    
    @staticmethod
    def isValidTravelerCity(city: str) -> bool:
        if InputHandler.nullByteIsAbsent(city):
            if city in CITIES:
                return True
        return False
    
#dh.-_--.sgkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkv_dhbf-.vfd (toegestaan bij microsoft)
# microsoft allows consecutive special characters like ____ ---- but no ....
# for now i wont allow any consecutive special characters 
    @staticmethod
    def isValidTravelerEmail(email: str) -> bool:
        if InputHandler.nullByteIsAbsent(email):
            if (5 <= len(email) <= 320):
                if re.search(r"^(?!\.)(?!.*\.\.)(?!.*--)(?!.*__)(?!.*_$)(?!.*-$)[A-Za-z0-9._-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,63}$", email):
                    return True
        return False
    
    @staticmethod
    def isValidTravelerPhoneNumber(phoneNumber: str) -> bool:
        if InputHandler.nullByteIsAbsent(phoneNumber):
            if (len(phoneNumber) == 14):
                if phoneNumber[:6] == "+31-6-":
                    if re.search(r"^[0-9]*$", phoneNumber[6:]):
                        return True
        return False

        
    
    @staticmethod
    def isValidTravelerDrivinLicenseNumber(drivingLicenseNumber: str) -> bool:
        if InputHandler.nullByteIsAbsent(drivingLicenseNumber):
            if len(drivingLicenseNumber) == 9:
                if drivingLicenseNumber[0].isupper(): #isupper doesn allow space with just 1 character string
                    if drivingLicenseNumber[1].isupper() or drivingLicenseNumber[1].isdigit():
                        if drivingLicenseNumber[2:].isdigit():
                            return True
        return False