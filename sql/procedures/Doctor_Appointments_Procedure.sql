DELIMITER //

CREATE PROCEDURE GetDoctorAppointments(IN doctor_id INT)
BEGIN
    SELECT 
        a.AppointmentID,
        a.DateTime,
        a.Status,
        p.PatientID,
        p.Name AS PatientName,
        p.DOB,
        p.Gender,
        p.Contact
    FROM 
        Appointment a
    JOIN 
        Patient p ON a.PatientID = p.PatientID
    WHERE 
        a.DoctorID = doctor_id
    ORDER BY 
        a.DateTime;
END //

DELIMITER ; 