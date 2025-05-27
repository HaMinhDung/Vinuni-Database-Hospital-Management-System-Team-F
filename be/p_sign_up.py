from db.connection import get_connection
import getpass

def is_username_taken(username):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT COUNT(*) FROM User WHERE Username = %s"
    cursor.execute(sql, (username,))
    (count,) = cursor.fetchone()
    cursor.close()
    conn.close()
    return count > 0

def create_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO User (Username, PasswordHash, Role) VALUES (%s, %s, %s)"
    role = "Patient"  # Assign role Patient
    cursor.execute(sql, (username, password, role))
    conn.commit()
    user_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return user_id

def create_patient_record(name, dob, gender, contact):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO Patient (Name, DOB, Gender, Contact) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (name, dob, gender, contact))
    conn.commit()
    patient_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return patient_id

def create_user_profile_entry(user_id, patient_id):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO UserProfile (UserID, DoctorID, PatientID) VALUES (%s, %s, %s)"
    cursor.execute(sql, (user_id, None, patient_id))
    conn.commit()
    cursor.close()
    conn.close()

def create_patient_account():
    print("=== Create Patient Account ===")
    while True:
        username = input("Enter username: ").strip()
        if is_username_taken(username):
            print("Username already exists. Please choose another username.")
        else:
            break
    password = getpass.getpass("Enter password: ").strip()
    print("Enter personal information:")
    name = input("Full name: ").strip()
    dob = input("Date of birth (YYYY-MM-DD): ").strip()
    gender = input("Gender: ").strip()
    contact = input("Contact: ").strip()
    
    user_id = create_user(username, password) # Pass plain password string
    patient_id = create_patient_record(name, dob, gender, contact)
    create_user_profile_entry(user_id, patient_id)
    print("Patient account created successfully.")

if __name__ == "__main__":
    create_patient_account()