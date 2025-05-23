from db.connection import get_connection

def create_patient(name, dob, gender, contact):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO Patient (Name, DOB, Gender, Contact) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (name, dob, gender, contact))
    conn.commit()
    print("Patient added.")
    cursor.close()
    conn.close()

def read_patients():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Patient")
    patients = cursor.fetchall()
    cursor.close()
    conn.close()
    return patients

def get_patient(patient_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM Patient WHERE PatientID = %s"
    cursor.execute(sql, (patient_id,))
    patient_info = cursor.fetchone()
    cursor.close()
    conn.close()
    return patient_info

# Cập nhật lại hàm update_patient để nhận thêm các thông tin nếu cần
def update_patient(patient_id, name, dob=None, gender=None, contact=None):
    conn = get_connection()
    cursor = conn.cursor()
    # Giả sử cập nhật được tất cả các trường nếu chúng không None
    sql = "UPDATE Patient SET Name = %s, DOB = %s, Gender = %s, Contact = %s WHERE PatientID = %s"
    cursor.execute(sql, (name, dob, gender, contact, patient_id))
    conn.commit()
    print("✅ Patient updated.")
    cursor.close()
    conn.close()

def delete_patient(patient_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Patient WHERE PatientID = %s", (patient_id,))
    conn.commit()
    print("🗑️ Patient deleted.")
    cursor.close()
    conn.close()

def get_patients_by_ids(patient_ids):
    if not patient_ids:
        return []
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    placeholders = ', '.join(['%s'] * len(patient_ids))
    sql = f"SELECT * FROM Patient WHERE PatientID IN ({placeholders})"
    cursor.execute(sql, tuple(patient_ids))
    patients = cursor.fetchall()
    cursor.close()
    conn.close()
    return patients

def get_patient_name(patient_id):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT Name FROM Patient WHERE PatientID = %s"
    cursor.execute(sql, (patient_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        # row[0] chứa tên bệnh nhân
        return row[0]
    else:
        return None

def get_latest_patient_id():
    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT MAX(PatientID) FROM Patient"
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result and result[0] is not None else None


