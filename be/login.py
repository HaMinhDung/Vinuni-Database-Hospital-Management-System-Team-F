from db.connection import get_connection
from models import user, patient, appointment, medical_record, user_profile, doctor  

def check_user_credentials(username, password):
    """
    Check login by querying the User table with username and password_hash.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM User WHERE Username = %s AND PasswordHash = %s"
    cursor.execute(sql, (username, password))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def patient_menu(user_info):
    """
    Patient menu after successful login.
    Based on UserID, use the get_doctor_patient_ids function to get a list [DoctorID, PatientID].
    If patient_id is not None, display the menu with the following functions:
    - Edit patient profile (use functions in patient.py)
    - Display patient's appointment list (use get_appointments_by_patient)
    - Display medical records (use get_appointment_ids_by_patient and get_medical_records_by_appointment_ids)
    - View patient profile (only display information)
    - View list of doctors you have appointments with or have been examined by
    """
    ids = user_profile.get_doctor_patient_ids(user_info["UserID"])
    doctor_id, patient_id = ids[0], ids[1]
    if patient_id is None:
        print("Account is not a patient account.")
        return

    while True:
        print("\n--- PATIENT MENU ---")
        print("1. Edit patient profile")
        print("2. Display appointment list")
        print("3. Display medical records")
        print("4. View patient profile")
        print("5. View list of doctors you have appointments with or have been examined by")
        print("0. Log out")
        choice = input("Select function: ")
        if choice == "1":
            # Get current patient information to edit
            info = patient.get_patient(patient_id)
            if not info:
                print("Patient information not found.")
            else:
                print("Current information:")
                print(info)
                new_name = input(f"Enter new name (Press Enter to keep [{info.get('Name')}]): ").strip() or info.get('Name')
                new_dob = input(f"Enter new date of birth (YYYY-MM-DD) (Press Enter to keep [{info.get('DOB')}]): ").strip() or info.get('DOB')
                new_gender = input(f"Enter new gender (Press Enter to keep [{info.get('Gender')}]): ").strip() or info.get('Gender')
                new_contact = input(f"Enter new contact (Press Enter to keep [{info.get('Contact')}]): ").strip() or info.get('Contact')
                patient.update_patient(patient_id, new_name, new_dob, new_gender, new_contact)
        elif choice == "2":
            appointments = appointment.get_appointments_by_patient(patient_id)
            if not appointments:
                print("You have no appointments.")
            else:
                print("Your appointment list:")
                for apt in appointments:
                    print(apt)
        elif choice == "3":
            apt_ids = appointment.get_appointment_ids_by_patient(patient_id)
            records = medical_record.get_medical_records_by_appointment_ids(apt_ids)
            if not records:
                print("No medical records found.")
            else:
                print("Your medical records:")
                for record in records:
                    # Display combined medical record, DateTime and DoctorName information
                    print(record)
        elif choice == "4":
            # Function to view patient profile (only display information)
            info = patient.get_patient(patient_id)
            if not info:
                print("Patient profile not found.")
            else:
                print("Your patient profile:")
                print(info)
        elif choice == "5":
            # Use get_doctor_ids_by_patient and get_doctors_by_ids functions to get information of doctors with appointments
            doc_ids = appointment.get_doctor_ids_by_patient(patient_id)
            if not doc_ids:
                print("No doctors you have appointments with or have been examined by.")
            else:
                doctors_info = doctor.get_doctors_by_ids(doc_ids)
                if not doctors_info:
                    print("Could not retrieve doctor information.")
                else:
                    print("List of doctors you have appointments with or have been examined by:")
                    for d in doctors_info:
                        print(d)
        elif choice == "0":
            print("Logging out.")
            break
        else:
            print("Invalid choice.")

def doctor_menu(user_info):
    """
    Doctor menu after successful login.
    Functions:
    1. Display doctor profile (based on DoctorID)
    2. Edit doctor profile (based on DoctorID)
    3. Display list of Appointments with patients (use get_appointments_by_doctor)
    4. Display medical records you have provided (use get_appointment_ids_by_doctor and get_medical_records_with_appointment_info)
    5. View list of your patients (use get_patient_ids_by_doctor and get_patients_by_ids)
    6. Schedule appointment with patient (use your doctor_id)
    7. Edit appointment with patient
    0. Log out
    """
    # Lấy thông tin DoctorID từ profile (nếu có) hoặc yêu cầu nhập thủ công.
    ids = user_profile.get_doctor_patient_ids(user_info["UserID"])
    doctor_id, _ = ids[0], ids[1]
    if doctor_id is None:
        try:
            doctor_id = int(input("Enter your doctor ID: "))
        except ValueError:
            print("Invalid ID.")
            return

    while True:
        print("\n--- DOCTOR MENU ---")
        print("1. Display doctor profile")
        print("2. Edit doctor profile")
        print("3. Display list of Appointments with patients")
        print("4. Display medical records you have provided")
        print("5. View list of your patients")
        print("6. Schedule appointment with patient")
        print("7. Edit appointment with patient")
        print("8. Create medical record for appointment")
        print("0. Log out")
        choice = input("Select function: ")
        
        if choice == "1":
            info = doctor.get_doctor(doctor_id)
            if info:
                print("Doctor profile:")
                print(info)
            else:
                print("Doctor profile not found.")
                
        elif choice == "2":
            info = doctor.get_doctor(doctor_id)
            if not info:
                print("Doctor profile not found for update.")
            else:
                print("Current information:")
                print(info)
                new_name = input(f"Enter new name (Press Enter to keep [{info.get('Name')}]): ").strip() or info.get('Name')
                new_spec = input(f"Enter new specialization (Press Enter to keep [{info.get('Specialization')}]): ").strip() or info.get('Specialization')
                new_dept_input = input(f"Enter new department ID (Current: [{info.get('DepartmentID')}]): ").strip()
                new_dept = int(new_dept_input) if new_dept_input else info.get('DepartmentID')
                doctor.update_doctor(doctor_id, new_name, new_spec, new_dept)
                
        elif choice == "3":
            appointments = appointment.get_appointments_by_doctor(doctor_id)
            if not appointments:
                print("No appointments found.")
            else:
                print("List of Appointments with patients:")
                for apt in appointments:
                    print(apt)
                    
        elif choice == "4":
            apt_ids = appointment.get_appointment_ids_by_doctor(doctor_id)
            records = medical_record.get_medical_records_with_appointment_info(apt_ids)
            if not records:
                print("No medical records provided.")
            else:
                print("Your medical records:")
                for rec in records:
                    print(rec)
                    
        elif choice == "5":
            patient_ids = appointment.get_patient_ids_by_doctor(doctor_id)
            if not patient_ids:
                print("No patients found.")
            else:
                patients_info = patient.get_patients_by_ids(patient_ids)
                if not patients_info:
                    print("Could not retrieve patient information.")
                else:
                    print("List of your patients:")
                    for p in patients_info:
                        print(p)
                        
        elif choice == "6":
            # Function to schedule appointment for patient
            try:
                patient_id_input = input("Enter patient ID to schedule appointment: ").strip()
                patient_id_val = int(patient_id_input)
            except ValueError:
                print("Invalid patient ID.")
                continue
            dt = input("Enter appointment date and time (YYYY-MM-DD HH:MM:SS): ").strip()
            status = input("Enter appointment status (default 'Scheduled'): ").strip() or "Scheduled"
            appointment.create_appointment(patient_id_val, doctor_id, dt, status)
            
        elif choice == "7":
            # Function to edit patient's appointment
            try:
                appointment_id = int(input("Enter appointment ID to edit: ").strip())
            except ValueError:
                print("Invalid appointment ID.")
                continue
            # Get current appointment information
            apt = appointment.get_appointment(appointment_id)
            if not apt:
                print("Appointment not found.")
                continue
            print("Current appointment information:", apt)
            new_patient_input = input(f"Enter new patient ID (current: {apt['PatientID']}): ").strip()
            new_patient = int(new_patient_input) if new_patient_input else apt['PatientID']
            new_dt = input(f"Enter new date and time (YYYY-MM-DD HH:MM:SS) (current: {apt['DateTime']}): ").strip() or apt['DateTime']
            new_status = input(f"Enter new status (current: {apt['Status']}): ").strip() or apt['Status']
            appointment.update_appointment(appointment_id, new_patient, doctor_id, new_dt, new_status)
            
        elif choice == "8":
            # Function to create medical record for appointment and update appointment status to 'Completed'
            try:
                appointment_id = int(input("Enter appointment ID to create medical record for: ").strip())
            except ValueError:
                print("Invalid appointment ID.")
                continue
                
            # Get appointment information
            apt = appointment.get_appointment(appointment_id)
            if not apt:
                print("Appointment not found.")
                continue
            # Check if the appointment belongs to the logged-in doctor
            if apt.get("DoctorID") != doctor_id:
                print("Appointment does not belong to you.")
                continue
            # Enter medical record information
            diagnosis = input("Enter diagnosis: ").strip()
            treatment = input("Enter treatment plan: ").strip()
            notes = input("Enter notes: ").strip()
            # Create medical record
            medical_record.create_medical_record(appointment_id, diagnosis, treatment, notes)
            # Update appointment status to 'Completed'
            updated_status = "Completed"
            appointment.update_appointment(appointment_id, apt.get("PatientID"), doctor_id, apt.get("DateTime"), updated_status)
            print("Medical record created and appointment status updated to 'Completed'.")
            
        elif choice == "0":
            print("Logging out.")
            break
        else:
            print("Invalid choice.")

def main():
    print("=== Login System ===")
    username = input("Username: ")
    password = input("Password: ")
    user_info = check_user_credentials(username, password)
    if not user_info:
        print("Login failed. Check username or password.")
        return

    # Lấy thông tin profile để xác định vai trò
    ids = user_profile.get_doctor_patient_ids(user_info["UserID"])
    doctor_id, patient_id = ids[0], ids[1]
    
    if doctor_id is not None:
        print("Login successful with role: Doctor")
        doctor_menu(user_info)
    elif patient_id is not None:
        print("Login successful with role: Patient")
        patient_menu(user_info)
    else:
        print("No suitable role found for user.")
        
if __name__ == "__main__":
    main()

