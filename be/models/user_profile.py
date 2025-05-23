from db.connection import get_connection

def create_user_profile(user_id, doctor_id=None, patient_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO UserProfile (UserID, DoctorID, PatientID) VALUES (%s, %s, %s)"
    cursor.execute(sql, (user_id, doctor_id, patient_id))
    conn.commit()
    print("User profile created.")
    cursor.close()
    conn.close()

def read_user_profiles():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM UserProfile")
    profiles = cursor.fetchall()
    cursor.close()
    conn.close()
    return profiles

def update_user_profile(user_profile_id, doctor_id=None, patient_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE UserProfile SET DoctorID = %s, PatientID = %s WHERE UserProfileID = %s",
                   (doctor_id, patient_id, user_profile_id))
    conn.commit()
    print("✅ User profile updated.")
    cursor.close()
    conn.close()

def delete_user_profile(user_profile_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM UserProfile WHERE UserProfileID = %s", (user_profile_id,))
    conn.commit()
    print("🗑️ User profile deleted.")
    cursor.close()
    conn.close()

# Get doctor and patient IDs from user profile
def get_doctor_patient_ids(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT DoctorID, PatientID FROM UserProfile WHERE UserID = %s"
    cursor.execute(sql, (user_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return [row.get("DoctorID"), row.get("PatientID")]
    else:
        return [None, None]


