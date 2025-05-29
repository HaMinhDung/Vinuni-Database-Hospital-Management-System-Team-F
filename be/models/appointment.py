from db.connection import get_connection

def create_appointment(patient_id, doctor_id, datetime_str, status):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO Appointment (PatientID, DoctorID, DateTime, Status) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (patient_id, doctor_id, datetime_str, status))
    conn.commit()
    print("Appointment created.")
    cursor.close()
    conn.close()

def read_appointments():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Appointment")
    appointments = cursor.fetchall()
    cursor.close()
    conn.close()
    return appointments

def update_appointment(appointment_id, patient_id, doctor_id, datetime_str, status):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "UPDATE Appointment SET PatientID = %s, DoctorID = %s, DateTime = %s, Status = %s WHERE AppointmentID = %s"
    cursor.execute(sql, (patient_id, doctor_id, datetime_str, status, appointment_id))
    conn.commit()
    print("✅ Appointment updated.")
    cursor.close()
    conn.close()

def delete_appointment(appointment_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Appointment WHERE AppointmentID = %s", (appointment_id,))
    conn.commit()
    print("🗑️ Appointment deleted.")
    cursor.close()
    conn.close()

def get_appointments_by_doctor(doctor_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT A.*, P.Name AS PatientName FROM Appointment A JOIN Patient P ON A.PatientID = P.PatientID WHERE A.DoctorID = %s"
    cursor.execute(sql, (doctor_id,))
    appointments = cursor.fetchall()
    cursor.close()
    conn.close()
    return appointments

def get_appointment(appointment_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM Appointment WHERE AppointmentID = %s"
    cursor.execute(sql, (appointment_id,))
    appointment_info = cursor.fetchone()
    cursor.close()
    conn.close()
    return appointment_info

def get_appointments_by_patient(patient_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT A.*, D.Name AS DoctorName FROM Appointment A JOIN Doctor D ON A.DoctorID = D.DoctorID WHERE A.PatientID = %s"
    cursor.execute(sql, (patient_id,))
    appointments = cursor.fetchall()
    cursor.close()
    conn.close()
    return appointments

def get_appointment_ids_by_patient(patient_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT AppointmentID FROM Appointment WHERE PatientID = %s"
    cursor.execute(sql, (patient_id,))
    rows = cursor.fetchall()
    appointment_ids = [row["AppointmentID"] for row in rows]
    cursor.close()
    conn.close()
    return appointment_ids

def get_doctor_ids_by_patient(patient_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT DISTINCT DoctorID FROM Appointment WHERE PatientID = %s"
    cursor.execute(sql, (patient_id,))
    rows = cursor.fetchall()
    doctor_ids = [row["DoctorID"] for row in rows]
    cursor.close()
    conn.close()
    return doctor_ids

def get_patient_ids_by_doctor(doctor_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT DISTINCT PatientID FROM Appointment WHERE DoctorID = %s"
    cursor.execute(sql, (doctor_id,))
    rows = cursor.fetchall()
    patient_ids = [row["PatientID"] for row in rows]
    cursor.close()
    conn.close()
    return patient_ids

def get_appointment_ids_by_doctor(doctor_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT AppointmentID FROM Appointment WHERE DoctorID = %s"
    cursor.execute(sql, (doctor_id,))
    rows = cursor.fetchall()
    appointment_ids = [row["AppointmentID"] for row in rows]
    cursor.close()
    conn.close()
    return appointment_ids

