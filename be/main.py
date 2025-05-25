# main.py

from models import doctor, patient, appointment, medical_record, department, service, user, user_profile
from db.connection import get_connection

def is_username_taken(username):
    conn = get_connection()
    cursor = conn.cursor()
    sql_check = "SELECT COUNT(*) FROM User WHERE Username = %s"
    cursor.execute(sql_check, (username,))
    (count,) = cursor.fetchone()
    cursor.close()
    conn.close()
    return count > 0

def main_menu():
    print("\n==== Hospital Management ====")
    print("1. Manage Doctors")
    print("2. Manage Patients")
    print("3. Manage Appointments")
    print("4. Manage Medical Records")
    print("5. Manage Departments")
    print("6. Manage Services")
    print("7. Manage Users")
    print("8. Manage User Profiles")
    print("9. View data of all tables")
    print("0. Exit")
    return input("Select function: ")

def manage_doctor():
    while True:
        print("\n--- Manage Doctors ---")
        print("1. Add doctor")
        print("2. View list of doctors")
        print("3. Update doctor information")
        print("4. Delete doctor")
        print("0. Back")
        choice = input("Select function: ")
        if choice == '1':
            name = input("Doctor's name: ")
            spec = input("Specialization: ")
            dept_id = int(input("Department ID: "))
            doctor.create_doctor(name, spec, dept_id)
        elif choice == '2':
            doctors = doctor.read_doctors()
            if doctors:
                for d in doctors:
                    print(d)
            else:
                print("No doctors found.")
        elif choice == '3':
            doctor_id = int(input("ID of doctor to update: "))
            new_name = input("New name: ")
            new_spec = input("New specialization: ")
            new_dept_id = int(input("New department ID: "))
            doctor.update_doctor(doctor_id, new_name, new_spec, new_dept_id)
        elif choice == '4':
            doctor_id = int(input("ID of doctor to delete: "))
            doctor.delete_doctor(doctor_id)
        elif choice == '0':
            break
        else:
            print("Invalid function.")

def manage_patient():
    while True:
        print("\n--- Manage Patients ---")
        print("1. Add patient")
        print("2. View list of patients")
        print("3. Update patient information")
        print("4. Delete patient")
        print("0. Back")
        choice = input("Select function: ")
        if choice == '1':
            name = input("Patient's name: ")
            dob = input("Date of birth (YYYY-MM-DD): ")
            gender = input("Gender: ")
            contact = input("Contact: ")
            patient.create_patient(name, dob, gender, contact)
        elif choice == '2':
            patients = patient.read_patients()
            if patients:
                for p in patients:
                    print(p)
            else:
                print("No patients found.")
        elif choice == '3':
            patient_id = int(input("ID of patient to update: "))
            new_name = input("New name: ")
            new_dob = input("New date of birth (YYYY-MM-DD): ")
            new_gender = input("New gender: ")
            new_contact = input("New contact: ")
            patient.update_patient(patient_id, new_name, new_dob, new_gender, new_contact)
        elif choice == '4':
            patient_id = int(input("ID of patient to delete: "))
            patient.delete_patient(patient_id)
        elif choice == '0':
            break
        else:
            print("Invalid function.")

def manage_appointment():
    while True:
        print("\n--- Manage Appointments ---")
        print("1. Add appointment")
        print("2. View list of appointments")
        print("3. Update appointment")
        print("4. Delete appointment")
        print("0. Back")
        choice = input("Select function: ")
        if choice == '1':
            patient_id = int(input("Patient ID: "))
            doctor_id = int(input("Doctor ID: "))
            dt = input("Date and time (YYYY-MM-DD HH:MM:SS): ")
            status = input("Status: ")
            appointment.create_appointment(patient_id, doctor_id, dt, status)
        elif choice == '2':
            appointments = appointment.read_appointments()
            if appointments:
                for a in appointments:
                    print(a)
            else:
                print("No appointments found.")
        elif choice == '3':
            appointment_id = int(input("ID of appointment to update: "))
            patient_id = int(input("New Patient ID: "))
            doctor_id = int(input("New Doctor ID: "))
            dt = input("New Date and time (YYYY-MM-DD HH:MM:SS): ")
            status = input("New status: ")
            appointment.update_appointment(appointment_id, patient_id, doctor_id, dt, status)
        elif choice == '4':
            appointment_id = int(input("ID of appointment to delete: "))
            appointment.delete_appointment(appointment_id)
        elif choice == '0':
            break
        else:
            print("Invalid function.")

def manage_medical_record():
    while True:
        print("\n--- Manage Medical Records ---")
        print("1. Add medical record")
        print("2. View list of medical records")
        print("3. Update medical record (update notes only)")
        print("4. Delete medical record")
        print("0. Back")
        choice = input("Select function: ")
        if choice == '1':
            appointment_id = int(input("Appointment ID: "))
            diagnosis = input("Diagnosis: ")
            treatment = input("Treatment plan: ")
            notes = input("Notes: ")
            medical_record.create_medical_record(appointment_id, diagnosis, treatment, notes)
        elif choice == '2':
            records = medical_record.read_medical_records()
            if records:
                for r in records:
                    print(r)
            else:
                print("No medical records found.")
        elif choice == '3':
            record_id = int(input("ID of record to update: "))
            new_notes = input("New notes: ")
            medical_record.update_medical_record(record_id, new_notes)
        elif choice == '4':
            record_id = int(input("ID of record to delete: "))
            medical_record.delete_medical_record(record_id)
        elif choice == '0':
            break
        else:
            print("Invalid function.")

def manage_department():
    while True:
        print("\n--- Manage Departments ---")
        print("1. Add department")
        print("2. View list of departments")
        print("3. Update department name")
        print("4. Assign department head")
        print("5. Delete department")
        print("0. Back")
        choice = input("Select function: ")
        if choice == '1':
            name = input("Department name: ")
            department.create_department(name)
        elif choice == '2':
            departments = department.read_departments()
            if departments:
                for d in departments:
                    print(d)
            else:
                print("No departments found.")
        elif choice == '3':
            dept_id = int(input("ID of department to update: "))
            new_name = input("New department name: ")
            department.update_department(dept_id, new_name)
        elif choice == '4':
            dept_id = int(input("Department ID: "))
            doctor_id = int(input("ID of doctor to be department head: "))
            department.set_department_head(dept_id, doctor_id)
        elif choice == '5':
            dept_id = int(input("ID of department to delete: "))
            department.delete_department(dept_id)
        elif choice == '0':
            break
        else:
            print("Invalid function.")

def manage_service():
    while True:
        print("\n--- Manage Services ---")
        print("1. Add service")
        print("2. View list of services")
        print("3. Update service")
        print("4. Delete service")
        print("0. Back")
        choice = input("Select function: ")
        if choice == '1':
            name = input("Service name: ")
            cost = float(input("Cost: "))
            service.create_service(name, cost)
        elif choice == '2':
            services = service.read_services()
            if services:
                for s in services:
                    print(s)
            else:
                print("No services found.")
        elif choice == '3':
            service_id = int(input("ID of service to update: "))
            new_name = input("New name: ")
            new_cost = float(input("New cost: "))
            service.update_service(service_id, new_name, new_cost)
        elif choice == '4':
            service_id = int(input("ID of service to delete: "))
            service.delete_service(service_id)
        elif choice == '0':
            break
        else:
            print("Invalid function.")

def manage_user():
    while True:
        print("\n--- Manage Users ---")
        print("1. Add user")
        print("2. View list of users")
        print("3. Update all user information (Name, Password, Role)")
        print("4. Delete user")
        print("0. Back")
        choice = input("Select function: ")
        if choice == '1':
            while True:
                username = input("Username: ")
                if is_username_taken(username):
                    print("Username is already in use. Please enter again.")
                else:
                    break
            password_hash = input("Password hash: ")
            role = input("Role: ")
            user.create_user(username, password_hash, role)
        elif choice == '2':
            users = user.read_users()
            if users:
                for u in users:
                    print(u)
            else:
                print("No users found.")
        elif choice == '3':
            user_id = int(input("ID of user to update: "))
            new_username = input("New username: ")
            new_password_hash = input("New password hash: ")
            new_role = input("New role: ")
            user.update_user_full(user_id, new_username, new_password_hash, new_role)
        elif choice == '4':
            user_id = int(input("ID of user to delete: "))
            user.delete_user(user_id)
        elif choice == '0':
            break
        else:
            print("Invalid function.")

def manage_user_profile():
    while True:
        print("\n--- Manage User Profiles ---")
        print("1. Add user profile")
        print("2. View list of user profiles")
        print("3. Update user profile")
        print("4. Delete user profile")
        print("0. Back")
        choice = input("Select function: ")
        if choice == '1':
            user_id = int(input("User ID: "))
            doctor_id = input("Doctor ID (leave blank if none): ")
            patient_id = input("Patient ID (leave blank if none): ")
            doctor_id = int(doctor_id) if doctor_id.strip() != "" else None
            patient_id = int(patient_id) if patient_id.strip() != "" else None
            user_profile.create_user_profile(user_id, doctor_id, patient_id)
        elif choice == '2':
            profiles = user_profile.read_user_profiles()
            if profiles:
                for p in profiles:
                    print(p)
            else:
                print("No user profiles found.")
        elif choice == '3':
            profile_id = int(input("ID of profile to update: "))
            doctor_id = input("Doctor ID (leave blank if none): ")
            patient_id = input("Patient ID (leave blank if none): ")
            doctor_id = int(doctor_id) if doctor_id.strip() != "" else None
            patient_id = int(patient_id) if patient_id.strip() != "" else None
            user_profile.update_user_profile(profile_id, doctor_id, patient_id)
        elif choice == '4':
            profile_id = int(input("ID of profile to delete: "))
            user_profile.delete_user_profile(profile_id)
        elif choice == '0':
            break
        else:
            print("Invalid function.")

def view_all_data():
    print("\n--- Doctors ---")
    doctors = doctor.read_doctors()
    if doctors:
        for d in doctors:
            print(d)
    else:
        print("No doctors found.")
    print("\n--- Patients ---")
    patients = patient.read_patients()
    if patients:
        for p in patients:
            print(p)
    else:
        print("No patients found.")
    print("\n--- Appointments ---")
    appointments = appointment.read_appointments()
    if appointments:
        for a in appointments:
            print(a)
    else:
        print("No appointments found.")
    print("\n--- Medical Records ---")
    records = medical_record.read_medical_records()
    if records:
        for r in records:
            print(r)
    else:
        print("No medical records found.")
    print("\n--- Departments ---")
    departments = department.read_departments()
    if departments:
        for d in departments:
            print(d)
    else:
        print("No departments found.")
    print("\n--- Services ---")
    services = service.read_services()
    if services:
        for s in services:
            print(s)
    else:
        print("No services found.")
    print("\n--- Users ---")
    users = user.read_users()
    if users:
        for u in users:
            print(u)
    else:
        print("No users found.")
    print("\n--- User Profiles ---")
    profiles = user_profile.read_user_profiles()
    if profiles:
        for p in profiles:
            print(p)
    else:
        print("No user profiles found.")

if __name__ == "__main__":
    while True:
        choice = main_menu()
        if choice == '1':
            manage_doctor()
        elif choice == '2':
            manage_patient()
        elif choice == '3':
            manage_appointment()
        elif choice == '4':
            manage_medical_record()
        elif choice == '5':
            manage_department()
        elif choice == '6':
            manage_service()
        elif choice == '7':
            manage_user()
        elif choice == '8':
            manage_user_profile()
        elif choice == '9':
            view_all_data()
        elif choice == '0':
            exit()
        else:
            print("Invalid function. Please select again.")
