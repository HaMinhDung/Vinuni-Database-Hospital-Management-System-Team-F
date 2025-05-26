from db.connection import get_connection
from models import doctor  # để sử dụng hàm get_doctor_name
from models import appointment  # nếu cần thao tác liên quan đến Appointment
from models import patient  # để sử dụng get_patient_name

def create_medical_record(appointment_id, diagnosis, treatment, notes):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO MedicalRecord (AppointmentID, Diagnosis, Treatment, Notes) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (appointment_id, diagnosis, treatment, notes))
    conn.commit()
    print("Medical record created.")
    cursor.close()
    conn.close()

def read_medical_records():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM MedicalRecord")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records

def update_medical_record(record_id, diagnosis=None, treatment=None, notes=None):
    conn = get_connection()
    cursor = conn.cursor()
    updates = []
    values = []

    if diagnosis is not None:
        updates.append("Diagnosis = %s")
        values.append(diagnosis)
    if treatment is not None:
        updates.append("Treatment = %s")
        values.append(treatment)
    if notes is not None:
        updates.append("Notes = %s")
        values.append(notes)

    if not updates:
        print("No fields to update for medical record ID", record_id)
        cursor.close()
        conn.close()
        return # No updates to perform

    sql = "UPDATE MedicalRecord SET " + ", ".join(updates) + " WHERE RecordID = %s"
    values.append(record_id) # Add record_id to the end of values

    cursor.execute(sql, tuple(values))

    conn.commit()
    print("✅ Medical record updated.")
    cursor.close()
    conn.close()

def delete_medical_record(record_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM MedicalRecord WHERE RecordID = %s", (record_id,))
    conn.commit()
    print("🗑️ Medical record deleted.")
    cursor.close()
    conn.close()

def get_medical_records_by_appointment_ids(appointment_ids):
    if not appointment_ids:
        return []
    # Lấy thông tin medical record
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    placeholders = ', '.join(['%s'] * len(appointment_ids))
    sql = f"SELECT * FROM MedicalRecord WHERE AppointmentID IN ({placeholders})"
    cursor.execute(sql, tuple(appointment_ids))
    records = cursor.fetchall()
    cursor.close()
    conn.close()

    # Lấy thông tin Appointment (DateTime và DoctorID) cho các appointment_id
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    placeholders = ', '.join(['%s'] * len(appointment_ids))
    sql2 = f"SELECT AppointmentID, DateTime, DoctorID FROM Appointment WHERE AppointmentID IN ({placeholders})"
    cursor.execute(sql2, tuple(appointment_ids))
    appointments = cursor.fetchall()
    cursor.close()
    conn.close()

    # Tạo mapping từ AppointmentID sang thông tin appointment
    apt_mapping = {apt["AppointmentID"]: apt for apt in appointments}

    # Với mỗi medical record, thêm DateTime, DoctorID và DoctorName dựa vào thông tin appointment
    for rec in records:
        apt_id = rec.get("AppointmentID")
        apt_info = apt_mapping.get(apt_id)
        if apt_info:
            rec["DateTime"] = apt_info.get("DateTime")
            rec["DoctorID"] = apt_info.get("DoctorID")
            rec["DoctorName"] = doctor.get_doctor_name(apt_info.get("DoctorID"))
        else:
            rec["DateTime"] = None
            rec["DoctorID"] = None
            rec["DoctorName"] = None
    return records

def get_medical_records_with_appointment_info(appointment_ids):
    if not appointment_ids:
        return []
    # Lấy thông tin MedicalRecord cho các appointment_id
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    placeholders = ', '.join(['%s'] * len(appointment_ids))
    sql = f"SELECT * FROM MedicalRecord WHERE AppointmentID IN ({placeholders})"
    cursor.execute(sql, tuple(appointment_ids))
    records = cursor.fetchall()
    cursor.close()
    conn.close()

    # Lấy thông tin Appointment (DateTime và PatientID) cho các appointment_id
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql2 = f"SELECT AppointmentID, DateTime, PatientID FROM Appointment WHERE AppointmentID IN ({placeholders})"
    cursor.execute(sql2, tuple(appointment_ids))
    appointments = cursor.fetchall()
    cursor.close()
    conn.close()

    # Tạo mapping từ AppointmentID sang thông tin Appointment
    apt_mapping = {apt["AppointmentID"]: apt for apt in appointments}

    # Với mỗi MedicalRecord, thêm các thông tin bổ sung
    for rec in records:
        apt_id = rec.get("AppointmentID")
        apt_info = apt_mapping.get(apt_id)
        if apt_info:
            rec["DateTime"] = apt_info.get("DateTime")
            rec["PatientID"] = apt_info.get("PatientID")
            rec["PatientName"] = patient.get_patient_name(apt_info.get("PatientID"))
        else:
            rec["DateTime"] = None
            rec["PatientID"] = None
            rec["PatientName"] = None
    return records
