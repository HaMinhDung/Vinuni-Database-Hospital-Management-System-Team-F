from db.connection import get_connection

def create_service(name, cost):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO Service (Name, Cost) VALUES (%s, %s)"
    cursor.execute(sql, (name, cost))
    conn.commit()
    print("Service created.")
    cursor.close()
    conn.close()

def read_services():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Service")
    services = cursor.fetchall()
    cursor.close()
    conn.close()
    return services

def update_service(service_id, name, cost):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Service SET Name = %s, Cost = %s WHERE ServiceID = %s", (name, cost, service_id))
    conn.commit()
    print("✅ Service updated.")
    cursor.close()
    conn.close()

def delete_service(service_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Service WHERE ServiceID = %s", (service_id,))
    conn.commit()
    print("🗑️ Service deleted.")
    cursor.close()
    conn.close()
