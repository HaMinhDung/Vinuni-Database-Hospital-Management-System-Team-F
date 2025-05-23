# main.py

from models import doctor, patient, appointment, medical_record, department, service, user, user_profile
from db.connection import get_connection

def is_username_taken(username):
    conn = get_connection()
    cursor = conn.cursor()
    sql_check = "SELECT COUNT(*) FROM User WHERE Username = %s"
    cursor.execute(sql_check, (username,))
    (count,) = cursor.fetchone()
    cursor.close()
    conn.close()
    return count > 0

def main_menu():
    print("\n==== Quản lý Bệnh viện ====")
    print("1. Quản lý Bác sĩ")
    print("2. Quản lý Bệnh nhân")
    print("3. Quản lý Cuộc hẹn")
    print("4. Quản lý Hồ sơ y tế")
    print("5. Quản lý Khoa")
    print("6. Quản lý Dịch vụ")
    print("7. Quản lý Người dùng")
    print("8. Quản lý Hồ sơ người dùng")
    print("9. Xem dữ liệu tất cả các bảng")
    print("0. Thoát")
    return input("Chọn chức năng: ")

def manage_doctor():
    while True:
        print("\n--- Quản lý Bác sĩ ---")
        print("1. Thêm bác sĩ")
        print("2. Xem danh sách bác sĩ")
        print("3. Cập nhật thông tin bác sĩ")
        print("4. Xóa bác sĩ")
        print("0. Quay lại")
        choice = input("Chọn chức năng: ")
        if choice == '1':
            name = input("Tên bác sĩ: ")
            spec = input("Chuyên khoa: ")
            dept_id = int(input("ID khoa: "))
            doctor.create_doctor(name, spec, dept_id)
        elif choice == '2':
            doctors = doctor.read_doctors()
            if doctors:
                for d in doctors:
                    print(d)
            else:
                print("Không có bác sĩ nào.")
        elif choice == '3':
            doctor_id = int(input("ID bác sĩ cần cập nhật: "))
            new_name = input("Tên mới: ")
            new_spec = input("Chuyên khoa mới: ")
            new_dept_id = int(input("ID khoa mới: "))
            doctor.update_doctor(doctor_id, new_name, new_spec, new_dept_id)
        elif choice == '4':
            doctor_id = int(input("ID bác sĩ cần xóa: "))
            doctor.delete_doctor(doctor_id)
        elif choice == '0':
            break
        else:
            print("Chức năng không hợp lệ.")

def manage_patient():
    while True:
        print("\n--- Quản lý Bệnh nhân ---")
        print("1. Thêm bệnh nhân")
        print("2. Xem danh sách bệnh nhân")
        print("3. Cập nhật thông tin bệnh nhân")
        print("4. Xóa bệnh nhân")
        print("0. Quay lại")
        choice = input("Chọn chức năng: ")
        if choice == '1':
            name = input("Tên bệnh nhân: ")
            dob = input("Ngày sinh (YYYY-MM-DD): ")
            gender = input("Giới tính: ")
            contact = input("Liên hệ: ")
            patient.create_patient(name, dob, gender, contact)
        elif choice == '2':
            patients = patient.read_patients()
            if patients:
                for p in patients:
                    print(p)
            else:
                print("Không có bệnh nhân nào.")
        elif choice == '3':
            patient_id = int(input("ID bệnh nhân cần cập nhật: "))
            new_name = input("Tên mới: ")
            new_dob = input("Ngày sinh mới (YYYY-MM-DD): ")
            new_gender = input("Giới tính mới: ")
            new_contact = input("Liên hệ mới: ")
            patient.update_patient(patient_id, new_name, new_dob, new_gender, new_contact)
        elif choice == '4':
            patient_id = int(input("ID bệnh nhân cần xóa: "))
            patient.delete_patient(patient_id)
        elif choice == '0':
            break
        else:
            print("Chức năng không hợp lệ.")

def manage_appointment():
    while True:
        print("\n--- Quản lý Cuộc hẹn ---")
        print("1. Thêm cuộc hẹn")
        print("2. Xem danh sách cuộc hẹn")
        print("3. Cập nhật cuộc hẹn")
        print("4. Xóa cuộc hẹn")
        print("0. Quay lại")
        choice = input("Chọn chức năng: ")
        if choice == '1':
            patient_id = int(input("ID bệnh nhân: "))
            doctor_id = int(input("ID bác sĩ: "))
            dt = input("Ngày giờ (YYYY-MM-DD HH:MM:SS): ")
            status = input("Trạng thái: ")
            appointment.create_appointment(patient_id, doctor_id, dt, status)
        elif choice == '2':
            appointments = appointment.read_appointments()
            if appointments:
                for a in appointments:
                    print(a)
            else:
                print("Không có cuộc hẹn nào.")
        elif choice == '3':
            appointment_id = int(input("ID cuộc hẹn cần cập nhật: "))
            patient_id = int(input("ID bệnh nhân mới: "))
            doctor_id = int(input("ID bác sĩ mới: "))
            dt = input("Ngày giờ mới (YYYY-MM-DD HH:MM:SS): ")
            status = input("Trạng thái mới: ")
            appointment.update_appointment(appointment_id, patient_id, doctor_id, dt, status)
        elif choice == '4':
            appointment_id = int(input("ID cuộc hẹn cần xóa: "))
            appointment.delete_appointment(appointment_id)
        elif choice == '0':
            break
        else:
            print("Chức năng không hợp lệ.")

def manage_medical_record():
    while True:
        print("\n--- Quản lý Hồ sơ y tế ---")
        print("1. Thêm hồ sơ y tế")
        print("2. Xem danh sách hồ sơ y tế")
        print("3. Cập nhật hồ sơ y tế (chỉ cập nhật ghi chú)")
        print("4. Xóa hồ sơ y tế")
        print("0. Quay lại")
        choice = input("Chọn chức năng: ")
        if choice == '1':
            appointment_id = int(input("ID cuộc hẹn: "))
            diagnosis = input("Chẩn đoán: ")
            treatment = input("Phác đồ điều trị: ")
            notes = input("Ghi chú: ")
            medical_record.create_medical_record(appointment_id, diagnosis, treatment, notes)
        elif choice == '2':
            records = medical_record.read_medical_records()
            if records:
                for r in records:
                    print(r)
            else:
                print("Không có hồ sơ y tế nào.")
        elif choice == '3':
            record_id = int(input("ID hồ sơ cần cập nhật: "))
            new_notes = input("Ghi chú mới: ")
            medical_record.update_medical_record(record_id, new_notes)
        elif choice == '4':
            record_id = int(input("ID hồ sơ cần xóa: "))
            medical_record.delete_medical_record(record_id)
        elif choice == '0':
            break
        else:
            print("Chức năng không hợp lệ.")

def manage_department():
    while True:
        print("\n--- Quản lý Khoa ---")
        print("1. Thêm khoa")
        print("2. Xem danh sách khoa")
        print("3. Cập nhật tên khoa")
        print("4. Chỉ định trưởng khoa")
        print("5. Xóa khoa")
        print("0. Quay lại")
        choice = input("Chọn chức năng: ")
        if choice == '1':
            name = input("Tên khoa: ")
            department.create_department(name)
        elif choice == '2':
            departments = department.read_departments()
            if departments:
                for d in departments:
                    print(d)
            else:
                print("Không có khoa nào.")
        elif choice == '3':
            dept_id = int(input("ID khoa cần cập nhật: "))
            new_name = input("Tên khoa mới: ")
            department.update_department(dept_id, new_name)
        elif choice == '4':
            dept_id = int(input("ID khoa: "))
            doctor_id = int(input("ID bác sĩ làm trưởng khoa: "))
            department.set_department_head(dept_id, doctor_id)
        elif choice == '5':
            dept_id = int(input("ID khoa cần xóa: "))
            department.delete_department(dept_id)
        elif choice == '0':
            break
        else:
            print("Chức năng không hợp lệ.")

def manage_service():
    while True:
        print("\n--- Quản lý Dịch vụ ---")
        print("1. Thêm dịch vụ")
        print("2. Xem danh sách dịch vụ")
        print("3. Cập nhật dịch vụ")
        print("4. Xóa dịch vụ")
        print("0. Quay lại")
        choice = input("Chọn chức năng: ")
        if choice == '1':
            name = input("Tên dịch vụ: ")
            cost = float(input("Chi phí: "))
            service.create_service(name, cost)
        elif choice == '2':
            services = service.read_services()
            if services:
                for s in services:
                    print(s)
            else:
                print("Không có dịch vụ nào.")
        elif choice == '3':
            service_id = int(input("ID dịch vụ cần cập nhật: "))
            new_name = input("Tên mới: ")
            new_cost = float(input("Chi phí mới: "))
            service.update_service(service_id, new_name, new_cost)
        elif choice == '4':
            service_id = int(input("ID dịch vụ cần xóa: "))
            service.delete_service(service_id)
        elif choice == '0':
            break
        else:
            print("Chức năng không hợp lệ.")

def manage_user():
    while True:
        print("\n--- Quản lý Người dùng ---")
        print("1. Thêm người dùng")
        print("2. Xem danh sách người dùng")
        print("3. Cập nhật toàn bộ thông tin người dùng (Tên, Mật khẩu, Vai trò)")
        print("4. Xóa người dùng")
        print("0. Quay lại")
        choice = input("Chọn chức năng: ")
        if choice == '1':
            while True:
                username = input("Tên người dùng: ")
                if is_username_taken(username):
                    print("Username đã được sử dụng. Hãy nhập lại.")
                else:
                    break
            password_hash = input("Mã băm mật khẩu: ")
            role = input("Vai trò: ")
            user.create_user(username, password_hash, role)
        elif choice == '2':
            users = user.read_users()
            if users:
                for u in users:
                    print(u)
            else:
                print("Không có người dùng nào.")
        elif choice == '3':
            user_id = int(input("ID người dùng cần cập nhật: "))
            new_username = input("Tên người dùng mới: ")
            new_password_hash = input("Mã băm mật khẩu mới: ")
            new_role = input("Vai trò mới: ")
            user.update_user_full(user_id, new_username, new_password_hash, new_role)
        elif choice == '4':
            user_id = int(input("ID người dùng cần xóa: "))
            user.delete_user(user_id)
        elif choice == '0':
            break
        else:
            print("Chức năng không hợp lệ.")

def manage_user_profile():
    while True:
        print("\n--- Quản lý Hồ sơ người dùng ---")
        print("1. Thêm hồ sơ người dùng")
        print("2. Xem danh sách hồ sơ người dùng")
        print("3. Cập nhật hồ sơ người dùng")
        print("4. Xóa hồ sơ người dùng")
        print("0. Quay lại")
        choice = input("Chọn chức năng: ")
        if choice == '1':
            user_id = int(input("ID người dùng: "))
            doctor_id = input("ID bác sĩ (để trống nếu không): ")
            patient_id = input("ID bệnh nhân (để trống nếu không): ")
            doctor_id = int(doctor_id) if doctor_id.strip() != "" else None
            patient_id = int(patient_id) if patient_id.strip() != "" else None
            user_profile.create_user_profile(user_id, doctor_id, patient_id)
        elif choice == '2':
            profiles = user_profile.read_user_profiles()
            if profiles:
                for p in profiles:
                    print(p)
            else:
                print("Không có hồ sơ người dùng nào.")
        elif choice == '3':
            profile_id = int(input("ID hồ sơ cần cập nhật: "))
            doctor_id = input("ID bác sĩ (để trống nếu không): ")
            patient_id = input("ID bệnh nhân (để trống nếu không): ")
            doctor_id = int(doctor_id) if doctor_id.strip() != "" else None
            patient_id = int(patient_id) if patient_id.strip() != "" else None
            user_profile.update_user_profile(profile_id, doctor_id, patient_id)
        elif choice == '4':
            profile_id = int(input("ID hồ sơ cần xóa: "))
            user_profile.delete_user_profile(profile_id)
        elif choice == '0':
            break
        else:
            print("Chức năng không hợp lệ.")

def view_all_data():
    print("\n--- Bác sĩ ---")
    doctors = doctor.read_doctors()
    if doctors:
        for d in doctors:
            print(d)
    else:
        print("Không có bác sĩ nào.")
    print("\n--- Bệnh nhân ---")
    patients = patient.read_patients()
    if patients:
        for p in patients:
            print(p)
    else:
        print("Không có bệnh nhân nào.")
    print("\n--- Cuộc hẹn ---")
    appointments = appointment.read_appointments()
    if appointments:
        for a in appointments:
            print(a)
    else:
        print("Không có cuộc hẹn nào.")
    print("\n--- Hồ sơ y tế ---")
    records = medical_record.read_medical_records()
    if records:
        for r in records:
            print(r)
    else:
        print("Không có hồ sơ y tế nào.")
    print("\n--- Khoa ---")
    departments = department.read_departments()
    if departments:
        for d in departments:
            print(d)
    else:
        print("Không có khoa nào.")
    print("\n--- Dịch vụ ---")
    services = service.read_services()
    if services:
        for s in services:
            print(s)
    else:
        print("Không có dịch vụ nào.")
    print("\n--- Người dùng ---")
    users = user.read_users()
    if users:
        for u in users:
            print(u)
    else:
        print("Không có người dùng nào.")
    print("\n--- Hồ sơ người dùng ---")
    profiles = user_profile.read_user_profiles()
    if profiles:
        for p in profiles:
            print(p)
    else:
        print("Không có hồ sơ người dùng nào.")

if __name__ == "__main__":
    while True:
        choice = main_menu()
        if choice == '1':
            manage_doctor()
        elif choice == '2':
            manage_patient()
        elif choice == '3':
            manage_appointment()
        elif choice == '4':
            manage_medical_record()
        elif choice == '5':
            manage_department()
        elif choice == '6':
            manage_service()
        elif choice == '7':
            manage_user()
        elif choice == '8':
            manage_user_profile()
        elif choice == '9':
            view_all_data()
        elif choice == '0':
            exit()
        else:
            print("Chức năng không hợp lệ. Vui lòng chọn lại.")
