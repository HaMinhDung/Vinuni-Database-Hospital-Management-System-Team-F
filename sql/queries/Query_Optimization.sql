-- Query Optimization Demonstration
-- This file shows how to optimize queries using indexes

-- 1. Complex query before optimization
-- This query joins multiple tables to get appointment details with patient and doctor info

-- First, let's analyze the query BEFORE adding indexes
EXPLAIN
SELECT 
    a.AppointmentID,
    a.DateTime,
    a.Status,
    p.PatientID,
    p.Name AS PatientName,
    d.DoctorID,
    d.Name AS DoctorName,
    d.Specialization,
    dept.Name AS DepartmentName
FROM 
    Appointment a
JOIN 
    Patient p ON a.PatientID = p.PatientID
JOIN 
    Doctor d ON a.DoctorID = d.DoctorID
LEFT JOIN 
    Department dept ON d.DepartmentID = dept.DepartmentID
WHERE 
    a.Status = 'Scheduled'
    AND a.DateTime BETWEEN '2023-01-01' AND '2023-12-31'
ORDER BY 
    a.DateTime;

-- 2. Adding indexes to improve performance
-- Let's add indexes on the frequently queried columns

-- Index on Appointment.Status (for filtering)
CREATE INDEX idx_appointment_status ON Appointment(Status);

-- Index on Appointment.DateTime (for range queries and sorting)
CREATE INDEX idx_appointment_datetime ON Appointment(DateTime);

-- Composite index on Appointment for foreign keys (for joins)
CREATE INDEX idx_appointment_patient_doctor ON Appointment(PatientID, DoctorID);

-- 3. Analyze the SAME query AFTER adding indexes
EXPLAIN
SELECT 
    a.AppointmentID,
    a.DateTime,
    a.Status,
    p.PatientID,
    p.Name AS PatientName,
    d.DoctorID,
    d.Name AS DoctorName,
    d.Specialization,
    dept.Name AS DepartmentName
FROM 
    Appointment a
JOIN 
    Patient p ON a.PatientID = p.PatientID
JOIN 
    Doctor d ON a.DoctorID = d.DoctorID
LEFT JOIN 
    Department dept ON d.DepartmentID = dept.DepartmentID
WHERE 
    a.Status = 'Scheduled'
    AND a.DateTime BETWEEN '2023-01-01' AND '2023-12-31'
ORDER BY 
    a.DateTime;

-- 4. Performance measurement query
-- Run this query to measure execution time before and after indexing
-- Example output: "Query took 0.23 seconds"

-- Before indexing (you'd run this and note the time):
SET profiling = 1;
SELECT 
    COUNT(*) 
FROM 
    Appointment a
JOIN 
    Patient p ON a.PatientID = p.PatientID
JOIN 
    Doctor d ON a.DoctorID = d.DoctorID
WHERE 
    a.Status = 'Scheduled'
    AND a.DateTime BETWEEN '2023-01-01' AND '2023-12-31';
SHOW PROFILES;

-- After indexing (you'd run this and note the improved time):
SET profiling = 1;
SELECT 
    COUNT(*) 
FROM 
    Appointment a
JOIN 
    Patient p ON a.PatientID = p.PatientID
JOIN 
    Doctor d ON a.DoctorID = d.DoctorID
WHERE 
    a.Status = 'Scheduled'
    AND a.DateTime BETWEEN '2023-01-01' AND '2023-12-31';
SHOW PROFILES; 