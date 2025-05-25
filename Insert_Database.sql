use hospitaldb;
INSERT INTO Doctor (Name, Specialization)
VALUES
  ('John Smith',       'Cardiology'),
  ('Jane Doe',         'Neurology'),
  ('Alan Turing',      'General Medicine'),
  ('Clara Oswald',     'Pediatrics'),
  ('Gregory House',    'Oncology'),
  ('Meredith Grey',    'Dermatology'),
  ('Leonard McCoy',    'Radiology'),
  ('Dana Scully',      'Psychiatry'),
  ('Stephen Strange', 'Orthopedics');

-- 2.2 Create exactly 5 departments, head = first 5 doctors
INSERT INTO Department (Name, DepartmentHeadID)
VALUES
  ('Cardiology',       1),
  ('Neurology',        2),
  ('General Medicine', 3),
  ('Pediatrics',       4),
  ('Oncology',         5);

-- 2.3 Assign each doctor to one of these 5 departments
UPDATE Doctor SET DepartmentID = 1 WHERE DoctorID IN (1,6);
UPDATE Doctor SET DepartmentID = 2 WHERE DoctorID IN (2,7);
UPDATE Doctor SET DepartmentID = 3 WHERE DoctorID IN (3,8);
UPDATE Doctor SET DepartmentID = 4 WHERE DoctorID IN (4,9);
UPDATE Doctor SET DepartmentID = 5 WHERE DoctorID = 5;

-- 2.4 Insert 15 patients
INSERT INTO Patient (Name, DOB, Gender, Contact)
VALUES
  ('Alice Brown',    '1980-05-12','Female','alice.brown@example.com'),
  ('Bob Green',      '1975-11-30','Male',  'bob.green@example.com'),
  ('Charlie Black',  '1990-02-20','Male',  'charlie.black@example.com'),
  ('Diana White',    '1985-07-08','Female','diana.white@example.com'),
  ('Eve Adams',      '1992-03-15','Female','eve.adams@example.com'),
  ('Frank Wright',   '1978-09-22','Male',  'frank.wright@example.com'),
  ('Grace Hopper',   '1986-12-09','Female','grace.hopper@example.com'),
  ('Heidi Klum',     '1991-04-02','Female','heidi.klum@example.com'),
  ('Ivan Petrov',    '1983-01-18','Male',  'ivan.petrov@example.com'),
  ('Judy Garland',   '1979-10-29','Female','judy.garland@example.com'),
  ('Karl Marx',      '1968-05-05','Male',  'karl.marx@example.com'),
  ('Lara Croft',     '1993-08-12','Female','lara.croft@example.com'),
  ('Mike Tyson',     '1970-06-30','Male',  'mike.tyson@example.com'),
  ('Nina Simone',    '1982-11-21','Female','nina.simone@example.com'),
  ('Oliver Twist',   '1995-02-14','Male',  'oliver.twist@example.com');

-- 2.5 Insert users: 1 admin + 9 doctors + 15 patients
INSERT INTO `User` (Username, PasswordHash, Role)
VALUES
  -- admin
  ('admin',           'bcrypt_hash_for_admin',   'Admin'),
  -- doctors (UserID 2–10)
  ('john_smith',      'bcrypt_hash_john',        'Doctor'),
  ('jane_doe',        'bcrypt_hash_jane',        'Doctor'),
  ('alan_turing',     'bcrypt_hash_alan',        'Doctor'),
  ('clara_oswald',    'bcrypt_hash_clara',       'Doctor'),
  ('greg_house',      'bcrypt_hash_greg',        'Doctor'),
  ('meredith_grey',   'bcrypt_hash_meredith',    'Doctor'),
  ('leonard_mccoy',   'bcrypt_hash_leonard',     'Doctor'),
  ('dana_scully',     'bcrypt_hash_dana',        'Doctor'),
  ('stephen_strange','bcrypt_hash_stephen',     'Doctor'),
  -- patients (UserID 11–25)
  ('alice_brown',     'bcrypt_hash_alice',       'Patient'),
  ('bob_green',       'bcrypt_hash_bob',         'Patient'),
  ('charlie_black',   'bcrypt_hash_charlie',     'Patient'),
  ('diana_white',     'bcrypt_hash_diana',       'Patient'),
  ('eve_adams',       'bcrypt_hash_eve',         'Patient'),
  ('frank_wright',    'bcrypt_hash_frank',       'Patient'),
  ('grace_hopper',    'bcrypt_hash_grace',       'Patient'),
  ('heidi_klum',      'bcrypt_hash_heidi',       'Patient'),
  ('ivan_petrov',     'bcrypt_hash_ivan',        'Patient'),
  ('judy_garland',    'bcrypt_hash_judy',        'Patient'),
  ('karl_marx',       'bcrypt_hash_karl',        'Patient'),
  ('lara_croft',      'bcrypt_hash_lara',        'Patient'),
  ('mike_tyson',      'bcrypt_hash_mike',        'Patient'),
  ('nina_simone',     'bcrypt_hash_nina',        'Patient'),
  ('oliver_twist',    'bcrypt_hash_oliver',      'Patient');

-- 2.6 Link Users ↔ Doctors/Patients
INSERT INTO UserProfile (UserID, DoctorID)
VALUES
  (2,1),(3,2),(4,3),(5,4),(6,5),(7,6),(8,7),(9,8),(10,9);

INSERT INTO UserProfile (UserID, PatientID)
VALUES
  (11,1),(12,2),(13,3),(14,4),(15,5),
  (16,6),(17,7),(18,8),(19,9),(20,10),
  (21,11),(22,12),(23,13),(24,14),(25,15);

-- 2.7 Insert 10 appointments
INSERT INTO Appointment (PatientID, DoctorID, DateTime, Status)
VALUES
  (1, 2, '2025-06-01 09:00:00', 'Scheduled'),
  (2, 3, '2025-06-02 10:30:00', 'Completed'),
  (3, 1, '2025-06-03 11:00:00', 'Cancelled'),
  (4, 4, '2025-06-04 14:00:00', 'Completed'),
  (5, 5, '2025-06-05 15:30:00', 'Scheduled'),
  (6, 6, '2025-06-06 08:00:00', 'Completed'),
  (7, 7, '2025-06-07 13:45:00', 'Completed'),
  (8, 8, '2025-06-08 16:00:00', 'Scheduled'),
  (9, 9, '2025-06-09 10:15:00', 'Cancelled'),
  (10,1,'2025-06-10 09:30:00','Completed');

-- 2.8 Five medical records for completed appointments
INSERT INTO MedicalRecord (AppointmentID, Diagnosis, Treatment, Notes)
VALUES
  (2, 'Migraine',       'Painkillers',      'Follow up in one week'),
  (4, 'Fractured Arm',  'Cast Application', 'Rest for 6 weeks'),
  (6, 'Seasonal Flu',   'Rest & Fluids',    'Return if no improvement'),
  (7, 'Allergy',        'Antihistamines',   'Seasonal reaction'),
  (10,'Hypertension',   'Lifestyle changes','Monitor BP daily');

-- 2.9 Ten services
INSERT INTO Service (Name, Cost)
VALUES
  ('Consultation',   50.00),
  ('X-Ray',         100.00),
  ('Blood Test',    150.00),
  ('MRI Scan',      800.00),
  ('Ultrasound',    200.00),
  ('ECG',           120.00),
  ('Vaccination',    30.00),
  ('Physiotherapy',  60.00),
  ('Surgery',      5000.00),
  ('Dental Cleaning',80.00);

-- =================================================================================
-- Done! You now have:
--  • 9 Doctors across 5 Departments
--  • 15 Patients
--  • 25 Users (1 Admin, 9 Doctors, 15 Patients) with profiles
--  • 10 Appointments
--  •  5 MedicalRecords
--  • 10 Services
-- =================================================================================






