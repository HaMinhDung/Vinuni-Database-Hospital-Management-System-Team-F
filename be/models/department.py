# models/department.py

from db.connection import get_connection

def create_department(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Department (Name) VALUES (%s)", (name,))
    conn.commit()
    print("Department added.")
    cursor.close()
    conn.close()

def read_departments():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Department")
    departments = cursor.fetchall()
    cursor.close()
    conn.close()
    return departments

def update_department(department_id, name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Department SET Name = %s WHERE DepartmentID = %s", (name, department_id))
    conn.commit()
    print("✅ Department updated.")
    cursor.close()
    conn.close()

def set_department_head(department_id, doctor_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Department SET DepartmentHeadID = %s WHERE DepartmentID = %s", (doctor_id, department_id))
    conn.commit()
    print("👨‍⚕️ Department head set.")
    cursor.close()
    conn.close()

def delete_department(department_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Department WHERE DepartmentID = %s", (department_id,))
    conn.commit()
    print("🗑️ Department deleted.")
    cursor.close()
    conn.close()
