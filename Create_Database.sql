DROP DATABASE IF EXISTS HospitalDB;
CREATE DATABASE HospitalDB;
USE HospitalDB;



CREATE TABLE Doctor ( 
  DoctorID INT PRIMARY KEY AUTO_INCREMENT, 
  Name VARCHAR(100) NOT NULL, 
  Specialization VARCHAR(100), 
  DepartmentID INT 
);

CREATE TABLE Department ( 
  DepartmentID INT PRIMARY KEY AUTO_INCREMENT, 
  Name VARCHAR(100) NOT NULL, 
  DepartmentHeadID INT,
  FOREIGN KEY (DepartmentHeadID) REFERENCES Doctor(DoctorID) 
);

ALTER TABLE Doctor 
ADD CONSTRAINT FK_Doctor_Department 
FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID);

CREATE TABLE Patient ( 
  PatientID INT PRIMARY KEY AUTO_INCREMENT, 
  Name VARCHAR(100) NOT NULL, 
  DOB DATE, 
  Gender ENUM('Male', 'Female', 'Other'), 
  Contact VARCHAR(100) 
);

CREATE TABLE User ( 
  UserID INT PRIMARY KEY AUTO_INCREMENT, 
  Username VARCHAR(100) UNIQUE NOT NULL, 
  PasswordHash VARCHAR(255) NOT NULL, 
  Role ENUM('Admin', 'Doctor', 'Patient') NOT NULL
);

CREATE TABLE UserProfile (
  UserProfileID INT PRIMARY KEY AUTO_INCREMENT,
  UserID INT UNIQUE,
  DoctorID INT NULL,
  PatientID INT NULL,
  FOREIGN KEY (UserID) REFERENCES User(UserID),
  FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID),
  FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
);

CREATE TABLE Appointment ( 
  AppointmentID INT PRIMARY KEY AUTO_INCREMENT, 
  PatientID INT, 
  DoctorID INT, 
  DateTime DATETIME, 
  Status ENUM('Scheduled', 'Completed', 'Cancelled'), 
  FOREIGN KEY (PatientID) REFERENCES Patient(PatientID), 
  FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID)
);

CREATE TABLE MedicalRecord ( 
  RecordID INT PRIMARY KEY AUTO_INCREMENT, 
  AppointmentID INT, 
  Diagnosis TEXT, 
  Treatment TEXT, 
  Notes TEXT, 
  FOREIGN KEY (AppointmentID) REFERENCES Appointment(AppointmentID)
);

CREATE TABLE Service ( 
  ServiceID INT PRIMARY KEY AUTO_INCREMENT, 
  Name VARCHAR(100), 
  Cost DECIMAL(10,2) 
);
