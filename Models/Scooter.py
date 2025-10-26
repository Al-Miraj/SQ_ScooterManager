import datetime

class Scooter:
    def __init__(self, serialNumber, brand, model, topSpeed, batteryCapacity,
                 stateOfCharge, targetSoCMin, targetSoCMax,
                 locationLatitude, locationLongitude, outOfServiceStatus,
                 mileage, lastMaintenanceDate, inServiceDate = None):
        self.SerialNumber = serialNumber
        self.Brand = brand
        self.Model = model
        self.TopSpeed = topSpeed
        self.BatteryCapacity = batteryCapacity
        self.StateOfCharge = stateOfCharge
        self.TargetSoCMin = targetSoCMin
        self.TargetSoCMax = targetSoCMax
        self.LocationLatitude = locationLatitude
        self.LocationLongitude = locationLongitude
        self.OutOfServiceStatus = outOfServiceStatus
        self.Mileage = mileage
        self.LastMaintenanceDate = lastMaintenanceDate
        self.InServiceDate = datetime.datetime.now() if inServiceDate == None else inServiceDate
    
    def __str__(self):
        return (
            f"Serial Number      : {self.SerialNumber}\n"
            f"Brand              : {self.Brand}\n"
            f"Model              : {self.Model}\n"
            f"Top Speed          : {self.TopSpeed} km/h\n"
            f"Battery Capacity   : {self.BatteryCapacity} kWh\n"
            f"State of Charge    : {self.StateOfCharge}%\n"
            f"Target SoC Range   : {self.TargetSoCMin}% - {self.TargetSoCMax}%\n"
            f"Location           : ({self.LocationLatitude}, {self.LocationLongitude})\n"
            f"Out of Service     : {'Yes' if self.OutOfServiceStatus else 'No'}\n"
            f"Mileage            : {self.Mileage} km\n"
            f"Last Maintenance   : {self.LastMaintenanceDate}\n"
        )



'''
    {
        "SerialNumber": "SN98765ZXCVB",
        "Brand": "Segway",
        "Model": "Ninebot Max",
        "TopSpeed": 30.0,
        "BatteryCapacity": 350.0,
        "StateOfCharge": 60.0,
        "TargetSoCMin": 25.0,
        "TargetSoCMax": 90.0,
        "LocationLatitude": 51.9230,
        "LocationLongitude": 4.48123,
        "OutOfServiceStatus": 0,
        "Mileage": 800,
        "LastMaintenanceDate": "2024-04-15T10:05:00"
    },

'''