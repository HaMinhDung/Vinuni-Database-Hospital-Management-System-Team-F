-- Query to rank doctors by number of appointments
-- Uses RANK() window function

SELECT 
    d.DoctorID,
    d.Name AS DoctorName,
    d.Specialization,
    dept.Name AS Department,
    COUNT(a.AppointmentID) AS TotalAppointments,
    RANK() OVER (ORDER BY COUNT(a.AppointmentID) DESC) AS AppointmentRank
FROM 
    Doctor d
LEFT JOIN 
    Department dept ON d.DepartmentID = dept.DepartmentID
LEFT JOIN 
    Appointment a ON d.DoctorID = a.DoctorID
GROUP BY 
    d.DoctorID, d.Name, d.Specialization, dept.Name
ORDER BY 
    AppointmentRank; 