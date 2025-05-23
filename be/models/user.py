from db.connection import get_connection

def create_user(username, password_hash, role):
    conn = get_connection()
    cursor = conn.cursor()
    # Kiểm tra xem username đã tồn tại hay chưa
    sql_check = "SELECT COUNT(*) FROM User WHERE Username = %s"
    cursor.execute(sql_check, (username,))
    (count,) = cursor.fetchone()
    if count > 0:
        print("Username đã được sử dụng. Vui lòng chọn tên khác.")
    else:
        sql = "INSERT INTO User (Username, PasswordHash, Role) VALUES (%s, %s, %s)"
        cursor.execute(sql, (username, password_hash, role))
        conn.commit()
        print("User created.")
    cursor.close()
    conn.close()

def read_users():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM User")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users

# Hàm này cập nhật toàn bộ thông tin của user: username, password và role
def update_user_full(user_id, new_username, new_password_hash, new_role):
    conn = get_connection()
    cursor = conn.cursor()
    # Kiểm tra nếu new_username đã thuộc về user khác
    sql_check = "SELECT COUNT(*) FROM User WHERE Username = %s AND UserID != %s"
    cursor.execute(sql_check, (new_username, user_id))
    (count,) = cursor.fetchone()
    if count > 0:
        print("Username đã tồn tại cho một user khác. Vui lòng chọn tên khác.")
    else:
        sql = "UPDATE User SET Username = %s, PasswordHash = %s, Role = %s WHERE UserID = %s"
        cursor.execute(sql, (new_username, new_password_hash, new_role, user_id))
        conn.commit()
        print("✅ User info (bao gồm mật khẩu) updated.")
    cursor.close()
    conn.close()

def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM User WHERE UserID = %s", (user_id,))
    conn.commit()
    print("🗑️ User deleted.")
    cursor.close()
    conn.close()

def get_user_profile(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM UserProfile WHERE UserID = %s"
    cursor.execute(sql, (user_id,))
    profile = cursor.fetchone()
    cursor.close()
    conn.close()
    return profile

def is_admin(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT Role FROM User WHERE UserID = %s"
    cursor.execute(sql, (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result and result['Role'] == 'Admin':
        return True
    return False