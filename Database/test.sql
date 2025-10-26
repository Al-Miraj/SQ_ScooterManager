-- database: UrbanMobilityDB.db

CREATE TABLE IF NOT EXISTS users (
    Username TEXT NOT NULL,
    Password TEXT NOT NULL,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    RegistrationDate TEXT,
    Role TEXT
);

DROP TABLE IF EXISTS scooters;


CREATE TABLE IF NOT EXISTS scooters (
    SerialNumber TEXT NOT NULL UNIQUE, 
    Brand TEXT NOT NULL,
    Model TEXT NOT NULL,
    TopSpeed REAL NOT NULL,
    BatteryCapacity REAL NOT NULL,
    StateOfCharge REAL NOT NULL,
    TargetSoCMin REAL NOT NULL,
    TargetSoCMax REAL NOT NULL,
    LocationLatitude REAL NOT NULL,
    LocationLongitude REAL NOT NULL,
    OutOfServiceStatus INTEGER NOT NULL,
    Mileage INTEGER NOT NULL,
    LastMaintenanceDate TEXT NOT NULL,
    InServiceDate TEXT NOT NULL
);



CREATE TABLE IF NOT EXISTS travelers (
    CustomerID TEXT NOT NULL UNIQUE,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    Birthday TEXT NOT NULL,
    Gender TEXT NOT NULL,
    StreetName TEXT NOT NULL,
    HouseNumber TEXT NOT NULL,
    ZipCode TEXT NOT NULL,
    City TEXT NOT NULL,
    Email TEXT NOT NULL,
    PhoneNumber TEXT NOT NULL,
    DrivingLicenseNumber TEXT NOT NULL,
    RegistrationDate TEXT NOT NULL
);