DELIMITER //

CREATE PROCEDURE GetPatientMedicalHistory(IN patient_id INT)
BEGIN
    SELECT 
        mr.RecordID,
        a.AppointmentID,
        a.DateTime AS AppointmentDate,
        d.Name AS DoctorName,
        d.Specialization,
        dept.Name AS DepartmentName,
        mr.Diagnosis,
        mr.Treatment,
        mr.Notes
    FROM 
        MedicalRecord mr
    JOIN 
        Appointment a ON mr.AppointmentID = a.AppointmentID
    JOIN 
        Doctor d ON a.DoctorID = d.DoctorID
    LEFT JOIN 
        Department dept ON d.DepartmentID = dept.DepartmentID
    WHERE 
        a.PatientID = patient_id
    ORDER BY 
        a.DateTime DESC;
END //

DELIMITER ; 