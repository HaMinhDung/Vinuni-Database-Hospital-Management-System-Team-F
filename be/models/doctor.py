# models/doctor.py

from db.connection import get_connection

def create_doctor(name, specialization, department_id):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO Doctor (Name, Specialization, DepartmentID) VALUES (%s, %s, %s)"
    cursor.execute(sql, (name, specialization, department_id))
    conn.commit()
    print("Doctor added successfully.")
    cursor.close()
    conn.close()

def read_doctors():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Doctor")
    doctors = cursor.fetchall()
    cursor.close()
    conn.close()
    return doctors

def update_doctor(doctor_id, name, specialization, department_id):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "UPDATE Doctor SET Name = %s, Specialization = %s, DepartmentID = %s WHERE DoctorID = %s"
    cursor.execute(sql, (name, specialization, department_id, doctor_id))
    conn.commit()
    print("✅ Doctor infomation updated.")
    cursor.close()
    conn.close()

def delete_doctor(doctor_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Doctor WHERE DoctorID = %s", (doctor_id,))
    conn.commit()
    print("🗑️ Deleted.")
    cursor.close()
    conn.close()
    
def get_doctor(doctor_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM Doctor WHERE DoctorID = %s"
    cursor.execute(sql, (doctor_id,))
    doctor_info = cursor.fetchone()
    cursor.close()
    conn.close()
    return doctor_info

def get_doctors_by_ids(doctor_ids):
    if not doctor_ids:
        return []
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    placeholders = ', '.join(['%s'] * len(doctor_ids))
    sql = f"SELECT * FROM Doctor WHERE DoctorID IN ({placeholders})"
    cursor.execute(sql, tuple(doctor_ids))
    doctors = cursor.fetchall()
    cursor.close()
    conn.close()
    return doctors

def get_doctor_name(doctor_id):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT Name FROM Doctor WHERE DoctorID = %s"
    cursor.execute(sql, (doctor_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return row[0]
    else:
        return None