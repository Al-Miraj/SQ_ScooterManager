import datetime

class Scooter:
    def __init__(self, SerialNumber, Brand, Model, TopSpeed, BatteryCapacity,
                 StateOfCharge, TargetSoCMin, TargetSoCMax,
                 LocationLatitude, LocationLongitude, OutOfServiceStatus,
                 Mileage, LastMaintenanceDate, InServiceDate = None):
        self.SerialNumber = SerialNumber
        self.Brand = Brand
        self.Model = Model
        self.TopSpeed = TopSpeed
        self.BatteryCapacity = BatteryCapacity
        self.StateOfCharge = StateOfCharge
        self.TargetSoCMin = TargetSoCMin
        self.TargetSoCMax = TargetSoCMax
        self.LocationLatitude = LocationLatitude
        self.LocationLongitude = LocationLongitude
        self.OutOfServiceStatus = OutOfServiceStatus
        self.Mileage = Mileage
        self.LastMaintenanceDate = LastMaintenanceDate
        self.InServiceDate = datetime.datetime.now() if InServiceDate == None else InServiceDate

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