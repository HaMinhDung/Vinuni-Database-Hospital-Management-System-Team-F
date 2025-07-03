-- Query to analyze appointment trends by month
-- Uses MONTH() and YEAR() date functions with GROUP BY

SELECT 
    YEAR(a.DateTime) AS Year,
    MONTH(a.DateTime) AS Month,
    MONTHNAME(a.DateTime) AS MonthName,
    COUNT(a.AppointmentID) AS TotalAppointments,
    COUNT(DISTINCT a.PatientID) AS UniquePatients,
    AVG(CASE WHEN mr.RecordID IS NOT NULL THEN 1 ELSE 0 END) * 100 AS CompletionRate
FROM 
    Appointment a
LEFT JOIN 
    MedicalRecord mr ON a.AppointmentID = mr.AppointmentID
GROUP BY 
    YEAR(a.DateTime), MONTH(a.DateTime), MONTHNAME(a.DateTime)
ORDER BY 
    Year, Month; 