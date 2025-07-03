DELIMITER //

CREATE TRIGGER before_doctor_delete
BEFORE DELETE ON Doctor
FOR EACH ROW
BEGIN
    -- If the doctor being deleted is a department head, set DepartmentHeadID to NULL
    UPDATE Department 
    SET DepartmentHeadID = NULL 
    WHERE DepartmentHeadID = OLD.DoctorID;
    
    -- Also delete any appointments associated with this doctor
    DELETE FROM Appointment
    WHERE DoctorID = OLD.DoctorID;
    
    -- Also delete any user profiles associated with this doctor
    DELETE FROM UserProfile
    WHERE DoctorID = OLD.DoctorID;
END //

DELIMITER ; 