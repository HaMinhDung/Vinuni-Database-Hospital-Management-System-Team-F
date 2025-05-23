from db.connection import get_connection
from models import user, patient, appointment, medical_record, user_profile, doctor  # Thêm import doctor

def check_user_credentials(username, password):
    """
    Kiểm tra đăng nhập bằng cách truy vấn bảng User với username và password_hash.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM User WHERE Username = %s AND PasswordHash = %s"
    cursor.execute(sql, (username, password))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def patient_menu(user_info):
    """
    Menu của bệnh nhân sau khi đăng nhập thành công.
    Dựa vào UserID, sử dụng hàm get_doctor_patient_ids để lấy list [DoctorID, PatientID].
    Nếu patient_id khác None thì hiện thị menu với các chức năng:
    - Chỉnh sửa hồ sơ bệnh nhân (dùng các hàm có trong patient.py)
    - Hiển thị danh sách appointment của bệnh nhân (dùng get_appointments_by_patient)
    - Hiển thị hồ sơ y tế (dùng get_appointment_ids_by_patient và get_medical_records_by_appointment_ids)
    - Xem hồ sơ bệnh nhân (chỉ hiển thị thông tin)
    - Xem danh sách thông tin các bác sĩ đã hẹn hoặc từng khám cho bạn
    """
    ids = user_profile.get_doctor_patient_ids(user_info["UserID"])
    doctor_id, patient_id = ids[0], ids[1]
    if patient_id is None:
        print("Tài khoản không phải bệnh nhân.")
        return

    while True:
        print("\n--- MENU BỆNH NHÂN ---")
        print("1. Chỉnh sửa hồ sơ bệnh nhân")
        print("2. Hiển thị danh sách appointment")
        print("3. Hiển thị hồ sơ y tế")
        print("4. Xem hồ sơ bệnh nhân")
        print("5. Xem danh sách các bác sĩ đã hẹn hoặc từng khám cho bạn")
        print("0. Đăng xuất")
        choice = input("Chọn chức năng: ")
        if choice == "1":
            # Lấy thông tin hiện tại của bệnh nhân để chỉnh sửa
            info = patient.get_patient(patient_id)
            if not info:
                print("Không tìm thấy thông tin bệnh nhân.")
            else:
                print("Thông tin hiện tại:")
                print(info)
                new_name = input(f"Nhập tên mới (Enter để giữ nguyên [{info.get('Name')}]): ").strip() or info.get('Name')
                new_dob = input(f"Nhập ngày sinh mới (YYYY-MM-DD) (Enter để giữ nguyên [{info.get('DOB')}]): ").strip() or info.get('DOB')
                new_gender = input(f"Nhập giới tính mới (Enter để giữ nguyên [{info.get('Gender')}]): ").strip() or info.get('Gender')
                new_contact = input(f"Nhập liên hệ mới (Enter để giữ nguyên [{info.get('Contact')}]): ").strip() or info.get('Contact')
                patient.update_patient(patient_id, new_name, new_dob, new_gender, new_contact)
        elif choice == "2":
            appointments = appointment.get_appointments_by_patient(patient_id)
            if not appointments:
                print("Bạn không có cuộc hẹn nào.")
            else:
                print("Danh sách cuộc hẹn của bạn:")
                for apt in appointments:
                    print(apt)
        elif choice == "3":
            apt_ids = appointment.get_appointment_ids_by_patient(patient_id)
            records = medical_record.get_medical_records_by_appointment_ids(apt_ids)
            if not records:
                print("Không có hồ sơ y tế nào.")
            else:
                print("Hồ sơ y tế của bạn:")
                for record in records:
                    # Hiển thị kết hợp thông tin medical record, DateTime và DoctorName
                    print(record)
        elif choice == "4":
            # Chức năng xem hồ sơ bệnh nhân (chỉ hiển thị thông tin)
            info = patient.get_patient(patient_id)
            if not info:
                print("Không tìm thấy hồ sơ bệnh nhân.")
            else:
                print("Hồ sơ bệnh nhân của bạn:")
                print(info)
        elif choice == "5":
            # Sử dụng hàm get_doctor_ids_by_patient và get_doctors_by_ids để lấy thông tin các bác sĩ đã hẹn
            doc_ids = appointment.get_doctor_ids_by_patient(patient_id)
            if not doc_ids:
                print("Không có bác sĩ nào hẹn hoặc từng khám cho bạn.")
            else:
                doctors_info = doctor.get_doctors_by_ids(doc_ids)
                if not doctors_info:
                    print("Không thể lấy được thông tin các bác sĩ.")
                else:
                    print("Danh sách các bác sĩ đã hẹn hoặc từng khám cho bạn:")
                    for d in doctors_info:
                        print(d)
        elif choice == "0":
            print("Đăng xuất.")
            break
        else:
            print("Lựa chọn không hợp lệ.")

def doctor_menu(user_info):
    """
    Menu của bác sĩ sau khi đăng nhập thành công.
    Các chức năng:
    1. Hiển thị hồ sơ bác sĩ (dựa vào DoctorID)
    2. Chỉnh sửa hồ sơ bác sĩ (dựa vào DoctorID)
    3. Hiển thị danh sách Appointments với bệnh nhân (dùng get_appointments_by_doctor)
    4. Hiển thị hồ sơ y tế bạn đã cung cấp (dùng get_appointment_ids_by_doctor và get_medical_records_with_appointment_info)
    5. Xem danh sách bệnh nhân của bạn (dùng get_patient_ids_by_doctor và get_patients_by_ids)
    6. Đặt lịch hẹn với bệnh nhân (sử dụng doctor_id của bạn)
    7. Chỉnh sửa lại lịch hẹn với bệnh nhân
    0. Đăng xuất
    """
    # Lấy thông tin DoctorID từ profile (nếu có) hoặc yêu cầu nhập thủ công.
    ids = user_profile.get_doctor_patient_ids(user_info["UserID"])
    doctor_id, _ = ids[0], ids[1]
    if doctor_id is None:
        try:
            doctor_id = int(input("Nhập ID bác sĩ của bạn: "))
        except ValueError:
            print("ID không hợp lệ.")
            return

    while True:
        print("\n--- MENU BÁC SĨ ---")
        print("1. Hiển thị hồ sơ bác sĩ")
        print("2. Chỉnh sửa hồ sơ bác sĩ")
        print("3. Hiển thị danh sách Appointment với bệnh nhân")
        print("4. Hiển thị hồ sơ y tế bạn đã cung cấp")
        print("5. Xem danh sách bệnh nhân của bạn")
        print("6. Đặt lịch hẹn với bệnh nhân")
        print("7. Chỉnh sửa lịch hẹn với bệnh nhân")
        print("8. Tạo hồ sơ y tế cho cuộc hẹn")
        print("0. Đăng xuất")
        choice = input("Chọn chức năng: ")
        
        if choice == "1":
            info = doctor.get_doctor(doctor_id)
            if info:
                print("Hồ sơ bác sĩ:")
                print(info)
            else:
                print("Không tìm thấy hồ sơ bác sĩ.")
                
        elif choice == "2":
            info = doctor.get_doctor(doctor_id)
            if not info:
                print("Không tìm thấy hồ sơ bác sĩ để cập nhật.")
            else:
                print("Thông tin hiện tại:")
                print(info)
                new_name = input(f"Nhập tên mới (Enter để giữ nguyên [{info.get('Name')}]): ").strip() or info.get('Name')
                new_spec = input(f"Nhập chuyên khoa mới (Enter để giữ nguyên [{info.get('Specialization')}]): ").strip() or info.get('Specialization')
                new_dept_input = input(f"Nhập ID khoa mới (Enter để giữ nguyên [{info.get('DepartmentID')}]): ").strip()
                new_dept = int(new_dept_input) if new_dept_input else info.get('DepartmentID')
                doctor.update_doctor(doctor_id, new_name, new_spec, new_dept)
                
        elif choice == "3":
            appointments = appointment.get_appointments_by_doctor(doctor_id)
            if not appointments:
                print("Không có cuộc hẹn nào.")
            else:
                print("Danh sách Appointment với bệnh nhân:")
                for apt in appointments:
                    print(apt)
                    
        elif choice == "4":
            apt_ids = appointment.get_appointment_ids_by_doctor(doctor_id)
            records = medical_record.get_medical_records_with_appointment_info(apt_ids)
            if not records:
                print("Không có hồ sơ y tế nào được cung cấp.")
            else:
                print("Hồ sơ y tế của bạn:")
                for rec in records:
                    print(rec)
                    
        elif choice == "5":
            patient_ids = appointment.get_patient_ids_by_doctor(doctor_id)
            if not patient_ids:
                print("Không có bệnh nhân nào.")
            else:
                patients_info = patient.get_patients_by_ids(patient_ids)
                if not patients_info:
                    print("Không thể lấy thông tin bệnh nhân.")
                else:
                    print("Danh sách bệnh nhân của bạn:")
                    for p in patients_info:
                        print(p)
                        
        elif choice == "6":
            # Chức năng đặt lịch cho bệnh nhân
            try:
                patient_id_input = input("Nhập ID bệnh nhân cần đặt lịch: ").strip()
                patient_id_val = int(patient_id_input)
            except ValueError:
                print("ID bệnh nhân không hợp lệ.")
                continue
            dt = input("Nhập ngày giờ cuộc hẹn (YYYY-MM-DD HH:MM:SS): ").strip()
            status = input("Nhập trạng thái cuộc hẹn (mặc định 'Scheduled'): ").strip() or "Scheduled"
            appointment.create_appointment(patient_id_val, doctor_id, dt, status)
            
        elif choice == "7":
            # Chức năng chỉnh sửa lịch hẹn của bệnh nhân
            try:
                appointment_id = int(input("Nhập ID cuộc hẹn cần chỉnh sửa: ").strip())
            except ValueError:
                print("ID cuộc hẹn không hợp lệ.")
                continue
            # Lấy thông tin cuộc hẹn hiện tại
            apt = appointment.get_appointment(appointment_id)
            if not apt:
                print("Không tìm thấy cuộc hẹn.")
                continue
            print("Thông tin cuộc hẹn hiện tại:", apt)
            new_patient_input = input(f"Nhập ID bệnh nhân mới (hiện tại: {apt['PatientID']}): ").strip()
            new_patient = int(new_patient_input) if new_patient_input else apt['PatientID']
            new_dt = input(f"Nhập ngày giờ mới (YYYY-MM-DD HH:MM:SS) (hiện tại: {apt['DateTime']}): ").strip() or apt['DateTime']
            new_status = input(f"Nhập trạng thái mới (hiện tại: {apt['Status']}): ").strip() or apt['Status']
            appointment.update_appointment(appointment_id, new_patient, doctor_id, new_dt, new_status)
            
        elif choice == "8":
            # Chức năng tạo hồ sơ y tế cho cuộc hẹn của bác sĩ và cập nhật trạng thái cuộc hẹn thành 'Completed'
            try:
                appointment_id = int(input("Nhập ID cuộc hẹn cần tạo hồ sơ y tế: ").strip())
            except ValueError:
                print("ID cuộc hẹn không hợp lệ.")
                continue
                
            # Lấy thông tin cuộc hẹn
            apt = appointment.get_appointment(appointment_id)
            if not apt:
                print("Không tìm thấy cuộc hẹn.")
                continue
            # Kiểm tra cuộc hẹn có thuộc về bác sĩ đang đăng nhập không
            if apt.get("DoctorID") != doctor_id:
                print("Cuộc hẹn không thuộc về bạn.")
                continue
            # Nhập thông tin hồ sơ y tế
            diagnosis = input("Nhập chẩn đoán: ").strip()
            treatment = input("Nhập phác đồ điều trị: ").strip()
            notes = input("Nhập ghi chú: ").strip()
            # Tạo hồ sơ y tế
            medical_record.create_medical_record(appointment_id, diagnosis, treatment, notes)
            # Cập nhật trạng thái cuộc hẹn thành 'Completed'
            updated_status = "Completed"
            appointment.update_appointment(appointment_id, apt.get("PatientID"), doctor_id, apt.get("DateTime"), updated_status)
            print("Hồ sơ y tế đã được tạo và trạng thái cuộc hẹn đã được cập nhật thành 'Completed'.")
            
        elif choice == "0":
            print("Đăng xuất.")
            break
        else:
            print("Lựa chọn không hợp lệ.")

def main():
    print("=== Hệ thống đăng nhập ===")
    username = input("Username: ")
    password = input("Password: ")
    user_info = check_user_credentials(username, password)
    if not user_info:
        print("Đăng nhập không thành công. Kiểm tra lại username hoặc password.")
        return

    # Lấy thông tin profile để xác định vai trò
    ids = user_profile.get_doctor_patient_ids(user_info["UserID"])
    doctor_id, patient_id = ids[0], ids[1]
    
    if doctor_id is not None:
        print("Đăng nhập thành công với vai trò: Bác sĩ")
        doctor_menu(user_info)
    elif patient_id is not None:
        print("Đăng nhập thành công với vai trò: Bệnh nhân")
        patient_menu(user_info)
    else:
        print("Không tìm thấy vai trò phù hợp cho user.")
        
if __name__ == "__main__":
    main()

