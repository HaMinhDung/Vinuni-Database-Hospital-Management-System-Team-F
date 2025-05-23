Drop database HospitalDB;
CREATE DATABASE HospitalDB;
USE HospitalDB;



-- Bảng Doctor trước để dùng làm khóa ngoại cho Department
CREATE TABLE Doctor ( 
  DoctorID INT PRIMARY KEY AUTO_INCREMENT, 
  Name VARCHAR(100) NOT NULL, 
  Specialization VARCHAR(100), 
  DepartmentID INT 
);

-- Bảng Department (sau Doctor) với liên kết DepartmentHeadID
CREATE TABLE Department ( 
  DepartmentID INT PRIMARY KEY AUTO_INCREMENT, 
  Name VARCHAR(100) NOT NULL, 
  DepartmentHeadID INT,
  FOREIGN KEY (DepartmentHeadID) REFERENCES Doctor(DoctorID) 
);

-- Thêm khóa ngoại từ Doctor về Department (sau khi Department đã tồn tại)
ALTER TABLE Doctor 
ADD CONSTRAINT FK_Doctor_Department 
FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID);

-- Bảng Patient
CREATE TABLE Patient ( 
  PatientID INT PRIMARY KEY AUTO_INCREMENT, 
  Name VARCHAR(100) NOT NULL, 
  DOB DATE, 
  Gender ENUM('Male', 'Female', 'Other'), 
  Contact VARCHAR(100) 
);

-- Bảng User
CREATE TABLE User ( 
  UserID INT PRIMARY KEY AUTO_INCREMENT, 
  Username VARCHAR(100) UNIQUE NOT NULL, 
  PasswordHash VARCHAR(255) NOT NULL, 
  Role ENUM('Admin', 'Doctor', 'Patient') NOT NULL
);

-- Bảng UserProfile
CREATE TABLE UserProfile (
  UserProfileID INT PRIMARY KEY AUTO_INCREMENT,
  UserID INT UNIQUE,
  DoctorID INT NULL,
  PatientID INT NULL,
  FOREIGN KEY (UserID) REFERENCES User(UserID),
  FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID),
  FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
);

-- Bảng Appointment
CREATE TABLE Appointment ( 
  AppointmentID INT PRIMARY KEY AUTO_INCREMENT, 
  PatientID INT, 
  DoctorID INT, 
  DateTime DATETIME, 
  Status ENUM('Scheduled', 'Completed', 'Cancelled'), 
  FOREIGN KEY (PatientID) REFERENCES Patient(PatientID), 
  FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID)
);

-- Bảng MedicalRecord
CREATE TABLE MedicalRecord ( 
  RecordID INT PRIMARY KEY AUTO_INCREMENT, 
  AppointmentID INT, 
  Diagnosis TEXT, 
  Treatment TEXT, 
  Notes TEXT, 
  FOREIGN KEY (AppointmentID) REFERENCES Appointment(AppointmentID)
);

-- Bảng Service
CREATE TABLE Service ( 
  ServiceID INT PRIMARY KEY AUTO_INCREMENT, 
  Name VARCHAR(100), 
  Cost DECIMAL(10,2) 
);
