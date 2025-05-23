INSERT INTO Department (DepartmentID, Name, DepartmentHead) VALUES
(1, 'Cardiology', 'Dr. John Smitt'),
(2, 'Neurology', 'Dr. Alice Nguyen');

INSERT INTO Doctor (DoctorID, Name, Specialization, DepartmentID) VALUES
(1, 'Dr. John Smitt', 'Cardiologist', 1),
(2, 'Dr. Alice Nguyen', 'Neurologist', 2);

INSERT INTO Patient (PatientID, Name, DOB, Gender, Contact) VALUES
(1, 'Nguyen Van A', '1990-05-15', 'Male', '0123456789'),
(2, 'Tran Thi B', '1985-09-20', 'Female', '0987654321'),
(4, 'Veres Tanker', '1995-11-22', 'Male', '0983748532'),
(5, 'Ha', '2004-11-01', 'Male', '0983745842'),
(6, 'Ha Minh Dung', '2011-02-17', 'Male', '0987364953');

INSERT INTO Appointment (AppointmentID, PatientID, DoctorID, DateTime, Status) VALUES
(1, 1, 1, '2025-06-01 09:00:00', 'Scheduled'),
(2, 2, 2, '2025-06-01 10:00:00', 'Scheduled'),
(4, 1, 1, '2025-12-05 09:00:00', 'Scheduled'),
(5, 2, 1, '2025-08-05 09:00:00', 'Scheduled'),
(6, 1, 2, '2026-08-05 09:00:00', 'Scheduled'),
(7, 1, 2, '2026-11-01 10:00:00', 'Completed');

INSERT INTO MedicalRecord (RecordID, AppointmentID, Diagnosis, Treatment, Notes) VALUES
(1, 2, 'Migraine', 'Painkillers and rest', 'Patient responded well'),
(3, 7, 'Ung thu gan', 'thuoc tay giun', 'thuoc mua o goc pho, re hon 5k so voi benh vien'),
(4, 2, 'Nung', 'Kiem Nguoi yeu', 'Patient responded well'),
(5, 4, 'Nong', 'Coi bot ao ra', 'Patient responded well'),
(6, 5, 'Lanh', 'Mac them ao vao', 'Patient responded well');

INSERT INTO Service (ServiceID, Name, Cost) VALUES
(1, 'General Consultation', 500000.00),
(2, 'MRI Scan', 2500000.00);

INSERT INTO User (UserID, Username, PasswordHash, Role) VALUES
(1, 'Ad', 'Ad', 'Doctor'),
(2, 'drjohn', 'hash_john_pw', 'Doctor'),
(3, 'vana', 'hash_vana_pw', 'Patient'),
(5, 'Ha Dung', 'Tq41994034%', 'Patient'),
(7, 'Veres', 'Veres', 'Patient'),
(8, 'Adm', 'Adm', 'Patient'),
(9, 'Ha', 'ha', 'Patient'),
(10, 'HaMinhDung', 'HaMinhDung', 'Patient'),
(11, 'Admin', 'Admin', 'Admin');

INSERT INTO UserProfile (UserProfileID, UserID, DoctorID, PatientID) VALUES
(1, 2, 1, NULL),
(2, 3, NULL, 1),
(4, 1, 2, NULL),
(5, 5, NULL, 2),
(6, 7, NULL, 4),
(7, 9, NULL, 5),
(8, 10, NULL, 6),
(9, 11, NULL, NULL);

