from db.connection import get_connection

# Patients
def admin_get_all_patients():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM Patient"
    cursor.execute(sql)
    patients = cursor.fetchall()
    cursor.close()
    conn.close()
    return patients

def admin_get_patient(patient_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM Patient WHERE PatientID = %s"
    cursor.execute(sql, (patient_id,))
    patient_info = cursor.fetchone()
    cursor.close()
    conn.close()
    return patient_info if patient_info else None

def admin_create_patient(name, dob, gender, contact):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO Patient (Name, DOB, Gender, Contact) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (name, dob, gender, contact))
    conn.commit()
    patient_id = cursor.lastrowid
    cursor.close()
    conn.close()
    print("Patient added with ID:", patient_id)
    return patient_id

def admin_delete_patient(patient_id):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "DELETE FROM Patient WHERE PatientID = %s"
    cursor.execute(sql, (patient_id,))
    conn.commit()
    cursor.close()
    conn.close()
    print("Patient deleted with ID:", patient_id)

# Doctors
def admin_get_all_doctors():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM Doctor"
    cursor.execute(sql)
    doctors = cursor.fetchall()
    cursor.close()
    conn.close()
    return doctors

def admin_get_doctor(doctor_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM Doctor WHERE DoctorID = %s"
    cursor.execute(sql, (doctor_id,))
    doctor_info = cursor.fetchone()
    cursor.close()
    conn.close()
    return doctor_info if doctor_info else None

def admin_create_doctor(name, specialization, department_id):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO Doctor (Name, Specialization, DepartmentID) VALUES (%s, %s, %s)"
    cursor.execute(sql, (name, specialization, department_id))
    conn.commit()
    doctor_id = cursor.lastrowid
    cursor.close()
    conn.close()
    print("Doctor added with ID:", doctor_id)
    return doctor_id

def admin_delete_doctor(doctor_id):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "DELETE FROM Doctor WHERE DoctorID = %s"
    cursor.execute(sql, (doctor_id,))
    conn.commit()
    cursor.close()
    conn.close()
    print("Doctor deleted with ID:", doctor_id)

# Appointments
def admin_get_all_appointments():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM Appointment"
    cursor.execute(sql)
    appointments = cursor.fetchall()
    cursor.close()
    conn.close()
    return appointments

def admin_get_appointment(appointment_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM Appointment WHERE AppointmentID = %s"
    cursor.execute(sql, (appointment_id,))
    appointment_info = cursor.fetchone()
    cursor.close()
    conn.close()
    return appointment_info if appointment_info else None

# Departments
def admin_get_all_departments():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM Department"
    cursor.execute(sql)
    departments = cursor.fetchall()
    cursor.close()
    conn.close()
    return departments

def admin_delete_department(department_id):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "DELETE FROM Department WHERE DepartmentID = %s"
    cursor.execute(sql, (department_id,))
    conn.commit()
    cursor.close()
    conn.close()
    print("Department deleted with ID:", department_id)

def admin_create_department(name):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO Department (Name) VALUES (%s)"
    cursor.execute(sql, (name,))
    conn.commit()
    department_id = cursor.lastrowid
    cursor.close()
    conn.close()
    print("Department added with ID:", department_id)
    return department_id

# Medical Records
def admin_get_all_medical_records():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM MedicalRecord"
    cursor.execute(sql)
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records

# Services
def admin_get_all_services():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM Service"
    cursor.execute(sql)
    services = cursor.fetchall()
    cursor.close()
    conn.close()
    return services

def admin_get_service(service_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM Service WHERE ServiceID = %s"
    cursor.execute(sql, (service_id,))
    service_info = cursor.fetchone()
    cursor.close()
    conn.close()
    return service_info if service_info else None

def admin_create_service(name, cost):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO Service (Name, Cost) VALUES (%s, %s)"
    cursor.execute(sql, (name, cost))
    conn.commit()
    service_id = cursor.lastrowid
    cursor.close()
    conn.close()
    print("Service created with ID:", service_id)
    return service_id

def admin_delete_service(service_id):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "DELETE FROM Service WHERE ServiceID = %s"
    cursor.execute(sql, (service_id,))
    conn.commit()
    cursor.close()
    conn.close()
    print("Service deleted with ID:", service_id)

def admin_update_service(service_id, name, cost):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "UPDATE Service SET Name = %s, Cost = %s WHERE ServiceID = %s"
    cursor.execute(sql, (name, cost, service_id))
    conn.commit()
    cursor.close()
    conn.close()
    print("Service updated with ID:", service_id)