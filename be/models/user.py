from db.connection import get_connection
import bcrypt

def create_user(username, password, role):
    conn = get_connection()
    cursor = conn.cursor()
    # Kiểm tra xem username đã tồn tại hay chưa
    sql_check = "SELECT COUNT(*) FROM User WHERE Username = %s"
    cursor.execute(sql_check, (username,))
    (count,) = cursor.fetchone()
    if count > 0:
        print("Username is already in use. Please choose another username.")
        user_id = None # Indicate failure to create user
    else:
        # Hash the password before storing
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        sql = "INSERT INTO User (Username, PasswordHash, Role) VALUES (%s, %s, %s)"
        cursor.execute(sql, (username, hashed_password, role))
        conn.commit()
        user_id = cursor.lastrowid
        print("User created.")
    cursor.close()
    conn.close()
    return user_id

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

def change_password(user_id, old_password, new_password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Get the current password hash from the database
    sql_get_hash = "SELECT PasswordHash FROM User WHERE UserID = %s"
    cursor.execute(sql_get_hash, (user_id,))
    result = cursor.fetchone()
    if not result:
        cursor.close()
        conn.close()
        return False, "User not found"

    stored_hash = result['PasswordHash']

    # Verify the old password
    if not bcrypt.checkpw(old_password.encode('utf-8'), stored_hash.encode('utf-8')):
        cursor.close()
        conn.close()
        return False, "Incorrect old password"

    # Hash the new password
    new_password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Update the password hash in the database
    sql_update_password = "UPDATE User SET PasswordHash = %s WHERE UserID = %s"
    cursor.execute(sql_update_password, (new_password_hash, user_id))
    conn.commit()

    cursor.close()
    conn.close()
    return True, "Password changed successfully"