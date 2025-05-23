from flask import Flask, request, jsonify
from flask_cors import CORS
from db.connection import get_connection
from models import user, patient, appointment, medical_record, user_profile, doctor

app = Flask(__name__)
CORS(app)

def check_user_credentials(username, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM User WHERE Username = %s AND PasswordHash = %s"
    cursor.execute(sql, (username, password))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

###############################################
# Endpoint đăng nhập và xác định vai trò user #
###############################################
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or ('username' not in data) or ('password' not in data):
        return jsonify({'error': 'Missing username or password'}), 400

    username = data['username']
    password = data['password']
    user_info = check_user_credentials(username, password)
    if not user_info:
        return jsonify({'error': 'Invalid credentials'}), 401

    ids = user_profile.get_doctor_patient_ids(user_info["UserID"])
    doctor_id, patient_id = ids[0], ids[1]
    if doctor_id is not None:
        role = "Doctor"
    elif patient_id is not None:
        role = "Patient"
    else:
        role = "Unknown"
    user_info["Role"] = role

    return jsonify({
        'message': 'Login successful',
        'user_info': user_info,
        'doctor_id': doctor_id,
        'patient_id': patient_id
    })

##############################
# Các endpoint cho BỆNH NHÂN #
##############################
# Cập nhật hồ sơ bệnh nhân
@app.route('/patient/update_profile', methods=['PUT'])
def update_patient_profile():
    data = request.get_json()
    for field in ["patient_id", "new_name", "new_dob", "new_gender", "new_contact"]:
        if field not in data:
            return jsonify({'error': f'Missing {field}'}), 400
    try:
        patient.update_patient(
            data["patient_id"],
            data["new_name"],
            data["new_dob"],
            data["new_gender"],
            data["new_contact"]
        )
        return jsonify({'message': 'Patient profile updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Lấy danh sách appointment của bệnh nhân
@app.route('/patient/appointments', methods=['GET'])
def get_patient_appointments():
    patient_id = request.args.get('patient_id')
    if not patient_id:
        return jsonify({'error': 'Missing patient_id'}), 400
    try:
        appointments = appointment.get_appointments_by_patient(int(patient_id))
        return jsonify({'appointments': appointments})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Lấy hồ sơ y tế của bệnh nhân
@app.route('/patient/medical_records', methods=['GET'])
def get_patient_medical_records():
    patient_id = request.args.get('patient_id')
    if not patient_id:
        return jsonify({'error': 'Missing patient_id'}), 400
    try:
        apt_ids = appointment.get_appointment_ids_by_patient(int(patient_id))
        records = medical_record.get_medical_records_by_appointment_ids(apt_ids)
        return jsonify({'medical_records': records})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Xem thông tin hồ sơ bệnh nhân
@app.route('/patient/profile', methods=['GET'])
def get_patient_profile():
    patient_id = request.args.get('patient_id')
    if not patient_id:
        return jsonify({'error': 'Missing patient_id'}), 400
    try:
        info = patient.get_patient(int(patient_id))
        if not info:
            return jsonify({'error': 'Patient not found'}), 404
        return jsonify({'patient_profile': info})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Lấy danh sách bác sĩ đã hẹn/từng khám
@app.route('/patient/doctors', methods=['GET'])
def get_patient_doctors():
    patient_id = request.args.get('patient_id')
    if not patient_id:
        return jsonify({'error': 'Missing patient_id'}), 400
    try:
        doc_ids = appointment.get_doctor_ids_by_patient(int(patient_id))
        if not doc_ids:
            return jsonify({'message': 'No doctor found'}), 200
        doctors_info = doctor.get_doctors_by_ids(doc_ids)
        return jsonify({'doctors': doctors_info})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#########################
# Các endpoint cho BÁC SĨ #
#########################
# Xem hồ sơ bác sĩ
@app.route('/doctor/profile', methods=['GET'])
def get_doctor_profile():
    doctor_id = request.args.get('doctor_id')
    if not doctor_id:
        return jsonify({'error': 'Missing doctor_id'}), 400
    try:
        info = doctor.get_doctor(int(doctor_id))
        if not info:
            return jsonify({'error': 'Doctor not found'}), 404
        return jsonify({'doctor_profile': info})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Cập nhật hồ sơ bác sĩ
@app.route('/doctor/update_profile', methods=['PUT'])
def update_doctor_profile():
    data = request.get_json()
    for field in ["doctor_id", "new_name", "new_spec", "new_dept"]:
        if field not in data:
            return jsonify({'error': f'Missing {field}'}), 400
    try:
        doctor.update_doctor(
            data["doctor_id"],
            data["new_name"],
            data["new_spec"],
            int(data["new_dept"])
        )
        return jsonify({'message': 'Doctor profile updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Lấy danh sách appointment của bác sĩ
@app.route('/doctor/appointments', methods=['GET'])
def get_doctor_appointments():
    doctor_id = request.args.get('doctor_id')
    if not doctor_id:
        return jsonify({'error': 'Missing doctor_id'}), 400
    try:
        appointments = appointment.get_appointments_by_doctor(int(doctor_id))
        return jsonify({'appointments': appointments})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Lấy hồ sơ y tế bác sĩ đã cung cấp (có thêm thông tin DateTime, PatientID)
@app.route('/doctor/medical_records', methods=['GET'])
def get_doctor_medical_records():
    doctor_id = request.args.get('doctor_id')
    if not doctor_id:
        return jsonify({'error': 'Missing doctor_id'}), 400
    try:
        apt_ids = appointment.get_appointment_ids_by_doctor(int(doctor_id))
        records = medical_record.get_medical_records_with_appointment_info(apt_ids)
        return jsonify({'medical_records': records})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Lấy danh sách bệnh nhân của bác sĩ
@app.route('/doctor/patients', methods=['GET'])
def get_doctor_patients():
    doctor_id = request.args.get('doctor_id')
    if not doctor_id:
        return jsonify({'error': 'Missing doctor_id'}), 400
    try:
        patient_ids = appointment.get_patient_ids_by_doctor(int(doctor_id))
        if not patient_ids:
            return jsonify({'message': 'No patients found'}), 200
        patients_info = patient.get_patients_by_ids(patient_ids)
        return jsonify({'patients': patients_info})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Đặt lịch hẹn cho bệnh nhân (Bác sĩ)
@app.route('/doctor/appointments', methods=['POST'])
def create_appointment():
    data = request.get_json()
    for field in ["patient_id", "doctor_id", "datetime_str"]:
        if field not in data:
            return jsonify({'error': f'Missing {field}'}), 400
    status = data.get("status", "Scheduled")
    try:
        appointment.create_appointment(
            int(data["patient_id"]),
            int(data["doctor_id"]),
            data["datetime_str"],
            status
        )
        return jsonify({'message': 'Appointment created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Cập nhật lịch hẹn của bệnh nhân (Bác sĩ)
@app.route('/doctor/appointments', methods=['PUT'])
def update_appointment():
    data = request.get_json()
    for field in ["appointment_id", "patient_id", "doctor_id", "datetime_str", "status"]:
        if field not in data:
            return jsonify({'error': f'Missing {field}'}), 400
    try:
        appointment.update_appointment(
            int(data["appointment_id"]),
            int(data["patient_id"]),
            int(data["doctor_id"]),
            data["datetime_str"],
            data["status"]
        )
        return jsonify({'message': 'Appointment updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Tạo hồ sơ y tế cho appointment và cập nhật trạng thái cuộc hẹn thành 'Completed'
@app.route('/doctor/medical_record', methods=['POST'])
def create_medical_record():
    data = request.get_json()
    for field in ["appointment_id", "diagnosis", "treatment", "notes"]:
        if field not in data:
            return jsonify({'error': f'Missing {field}'}), 400
    try:
        # Kiểm tra xem appointment có hợp lệ và thuộc về bác sĩ không
        apt = appointment.get_appointment(int(data["appointment_id"]))
        if not apt:
            return jsonify({'error': 'Appointment not found'}), 404
        # Tạo hồ sơ y tế
        medical_record.create_medical_record(
            int(data["appointment_id"]),
            data["diagnosis"],
            data["treatment"],
            data["notes"]
        )
        # Cập nhật trạng thái appointment thành Completed
        appointment.update_appointment(
            int(data["appointment_id"]),
            apt.get("PatientID"),
            apt.get("DoctorID"),
            apt.get("DateTime"),
            "Completed"
        )
        return jsonify({'message': 'Medical record created and appointment completed'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint đăng kí tài khoản bệnh nhân (Sign Up)
@app.route('/patient/sign_up', methods=['POST'])
def sign_up_patient():
    data = request.get_json()
    required_fields = ['username', 'password', 'name', 'dob', 'gender', 'contact']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"Missing {field}"}), 400
    try:
        # Sử dụng code đăng kí từ p_sign_up.py
        from p_sign_up import is_username_taken, create_user, create_patient_record, create_user_profile_entry
        if is_username_taken(data["username"]):
            return jsonify({"error": "Username already exists"}), 400

        user_id = create_user(data["username"], data["password"])
        patient_id = create_patient_record(data["name"], data["dob"], data["gender"], data["contact"])
        create_user_profile_entry(user_id, patient_id)
        return jsonify({
            "message": "Patient account created successfully",
            "user_id": user_id,
            "patient_id": patient_id
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

##############################################
# Các endpoint ADMIN (quản lý toàn bộ database)
##############################################

# Lấy toàn bộ dữ liệu của tất cả các bảng
@app.route('/admin/all_data', methods=['GET'])
def admin_all_data():
    try:
        all_data = {
            'doctors': doctor.read_doctors(),
            'patients': patient.read_patients(),
            'appointments': appointment.read_appointments(),
            'medical_records': medical_record.read_medical_records(),
            'departments': __import__('models.department', fromlist=['read_departments']).read_departments(),
            'services': __import__('models.service', fromlist=['read_services']).read_services(),
            'users': user.read_users(),
            'user_profiles': user_profile.read_user_profiles()
        }
        return jsonify(all_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

##############################################
# Các endpoint cho Bác sĩ
##############################################
@app.route('/admin/doctor', methods=['GET'])
def admin_get_doctors():
    try:
        docs = doctor.read_doctors()
        return jsonify({'doctors': docs})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/doctor', methods=['POST'])
def admin_create_doctor():
    data = request.get_json()
    required_fields = ['name', 'specialization', 'department_id']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f"Missing {field}"}), 400
    try:
        doctor.create_doctor(data['name'], data['specialization'], int(data['department_id']))
        return jsonify({'message': 'Doctor created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/doctor', methods=['PUT'])
def admin_update_doctor():
    data = request.get_json()
    required_fields = ['doctor_id', 'new_name', 'new_spec', 'new_dept']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f"Missing {field}"}), 400
    try:
        doctor.update_doctor(data['doctor_id'], data['new_name'], data['new_spec'], int(data['new_dept']))
        return jsonify({'message': 'Doctor updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/doctor', methods=['DELETE'])
def admin_delete_doctor():
    data = request.get_json()
    if 'doctor_id' not in data or not data['doctor_id']:
        return jsonify({'error': 'Missing doctor_id'}), 400
    try:
        doctor.delete_doctor(data['doctor_id'])
        return jsonify({'message': 'Doctor deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

##############################################
# Các endpoint cho Bệnh nhân
##############################################
@app.route('/admin/patient', methods=['GET'])
def admin_get_patients():
    try:
        pts = patient.read_patients()
        return jsonify({'patients': pts})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/patient', methods=['POST'])
def admin_create_patient():
    data = request.get_json()
    required_fields = ['name', 'dob', 'gender', 'contact']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f"Missing {field}"}), 400
    try:
        patient.create_patient(data['name'], data['dob'], data['gender'], data['contact'])
        return jsonify({'message': 'Patient created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/patient', methods=['PUT'])
def admin_update_patient():
    data = request.get_json()
    required_fields = ['patient_id', 'new_name', 'new_dob', 'new_gender', 'new_contact']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f"Missing {field}"}), 400
    try:
        patient.update_patient(data['patient_id'], data['new_name'], data['new_dob'], data['new_gender'], data['new_contact'])
        return jsonify({'message': 'Patient updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/patient', methods=['DELETE'])
def admin_delete_patient():
    data = request.get_json()
    if 'patient_id' not in data or not data['patient_id']:
        return jsonify({'error': 'Missing patient_id'}), 400
    try:
        patient.delete_patient(data['patient_id'])
        return jsonify({'message': 'Patient deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

##############################################
# Các endpoint cho Cuộc hẹn
##############################################
@app.route('/admin/appointment', methods=['GET'])
def admin_get_appointments():
    try:
        appts = appointment.read_appointments()
        return jsonify({'appointments': appts})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/appointment', methods=['POST'])
def admin_create_appointment():
    data = request.get_json()
    required_fields = ['patient_id', 'doctor_id', 'datetime_str', 'status']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f"Missing {field}"}), 400
    try:
        appointment.create_appointment(int(data['patient_id']), int(data['doctor_id']), data['datetime_str'], data['status'])
        return jsonify({'message': 'Appointment created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/appointment', methods=['PUT'])
def admin_update_appointment():
    data = request.get_json()
    required_fields = ['appointment_id', 'patient_id', 'doctor_id', 'datetime_str', 'status']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f"Missing {field}"}), 400
    try:
        appointment.update_appointment(int(data['appointment_id']), int(data['patient_id']), int(data['doctor_id']), data['datetime_str'], data['status'])
        return jsonify({'message': 'Appointment updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/appointment', methods=['DELETE'])
def admin_delete_appointment():
    data = request.get_json()
    if 'appointment_id' not in data or not data['appointment_id']:
        return jsonify({'error': 'Missing appointment_id'}), 400
    try:
        # Nếu hàm delete_appointment chưa được định nghĩa, có thể trả về thông báo Not implemented.
        if hasattr(appointment, 'delete_appointment'):
            appointment.delete_appointment(int(data['appointment_id']))
            return jsonify({'message': 'Appointment deleted successfully'})
        else:
            return jsonify({'error': 'Delete appointment not implemented'}), 501
    except Exception as e:
        return jsonify({'error': str(e)}), 500

##############################################
# Các endpoint cho Hồ sơ y tế
##############################################
@app.route('/admin/medical_record', methods=['GET'])
def admin_get_medical_records():
    try:
        records = medical_record.read_medical_records()
        return jsonify({'medical_records': records})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/medical_record', methods=['POST'])
def admin_create_medical_record():
    data = request.get_json()
    required_fields = ['appointment_id', 'diagnosis', 'treatment', 'notes']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f"Missing {field}"}), 400
    try:
        medical_record.create_medical_record(int(data['appointment_id']), data['diagnosis'], data['treatment'], data['notes'])
        return jsonify({'message': 'Medical record created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/medical_record', methods=['PUT'])
def admin_update_medical_record():
    data = request.get_json()
    required_fields = ['record_id', 'notes']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f"Missing {field}"}), 400
    try:
        medical_record.update_medical_record(int(data['record_id']), data['notes'])
        return jsonify({'message': 'Medical record updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/medical_record', methods=['DELETE'])
def admin_delete_medical_record():
    data = request.get_json()
    if 'record_id' not in data or not data['record_id']:
        return jsonify({'error': 'Missing record_id'}), 400
    try:
        medical_record.delete_medical_record(int(data['record_id']))
        return jsonify({'message': 'Medical record deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

##############################################
# Các endpoint cho Khoa
##############################################
@app.route('/admin/department', methods=['GET'])
def admin_get_departments():
    try:
        depts = __import__('models.department', fromlist=['read_departments']).read_departments()
        return jsonify({'departments': depts})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/department', methods=['POST'])
def admin_create_department():
    data = request.get_json()
    if 'name' not in data or not data['name']:
        return jsonify({'error': 'Missing name'}), 400
    try:
        __import__('models.department', fromlist=['create_department']).create_department(data['name'])
        return jsonify({'message': 'Department created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/department', methods=['PUT'])
def admin_update_department():
    data = request.get_json()
    if 'department_id' not in data or 'new_name' not in data or not data['new_name']:
        return jsonify({'error': 'Missing department_id or new_name'}), 400
    try:
        __import__('models.department', fromlist=['update_department']).update_department(data['department_id'], data['new_name'])
        return jsonify({'message': 'Department updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/department', methods=['DELETE'])
def admin_delete_department():
    data = request.get_json()
    if 'department_id' not in data or not data['department_id']:
        return jsonify({'error': 'Missing department_id'}), 400
    try:
        __import__('models.department', fromlist=['delete_department']).delete_department(data['department_id'])
        return jsonify({'message': 'Department deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

##############################################
# Các endpoint cho Dịch vụ
##############################################
@app.route('/admin/service', methods=['GET'])
def admin_get_services():
    try:
        svcs = __import__('models.service', fromlist=['read_services']).read_services()
        return jsonify({'services': svcs})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/service', methods=['POST'])
def admin_create_service():
    data = request.get_json()
    required_fields = ['name', 'cost']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f"Missing {field}"}), 400
    try:
        __import__('models.service', fromlist=['create_service']).create_service(data['name'], data['cost'])
        return jsonify({'message': 'Service created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/service', methods=['PUT'])
def admin_update_service():
    data = request.get_json()
    required_fields = ['service_id', 'new_name', 'new_cost']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f"Missing {field}"}), 400
    try:
        __import__('models.service', fromlist=['update_service']).update_service(data['service_id'], data['new_name'], data['new_cost'])
        return jsonify({'message': 'Service updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/service', methods=['DELETE'])
def admin_delete_service():
    data = request.get_json()
    if 'service_id' not in data or not data['service_id']:
        return jsonify({'error': 'Missing service_id'}), 400
    try:
        __import__('models.service', fromlist=['delete_service']).delete_service(data['service_id'])
        return jsonify({'message': 'Service deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

##############################################
# Các endpoint cho Người dùng
##############################################
@app.route('/admin/user', methods=['GET'])
def admin_get_users():
    try:
        users_list = user.read_users()
        return jsonify({'users': users_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/user', methods=['POST'])
def admin_create_user():
    data = request.get_json()
    required_fields = ['username', 'password_hash', 'role']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f"Missing {field}"}), 400
    try:
        user.create_user(data['username'], data['password_hash'], data['role'])
        return jsonify({'message': 'User created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/user', methods=['PUT'])
def admin_update_user():
    data = request.get_json()
    required_fields = ['user_id', 'new_username', 'new_password_hash', 'new_role']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f"Missing {field}"}), 400
    try:
        user.update_user_full(data['user_id'], data['new_username'], data['new_password_hash'], data['new_role'])
        return jsonify({'message': 'User updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/user', methods=['DELETE'])
def admin_delete_user():
    data = request.get_json()
    if 'user_id' not in data or not data['user_id']:
        return jsonify({'error': 'Missing user_id'}), 400
    try:
        user.delete_user(data['user_id'])
        return jsonify({'message': 'User deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

##############################################
# Các endpoint cho Hồ sơ người dùng
##############################################
@app.route('/admin/user_profile', methods=['GET'])
def admin_get_user_profiles():
    try:
        profiles = user_profile.read_user_profiles()
        return jsonify({'user_profiles': profiles})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/user_profile', methods=['POST'])
def admin_create_user_profile():
    data = request.get_json()
    required_fields = ['user_id']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f"Missing {field}"}), 400
    # doctor_id và patient_id là tùy chọn
    doctor_id = data.get('doctor_id', None)
    patient_id = data.get('patient_id', None)
    try:
        user_profile.create_user_profile(data['user_id'], doctor_id, patient_id)
        return jsonify({'message': 'User profile created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/user_profile', methods=['PUT'])
def admin_update_user_profile():
    data = request.get_json()
    if 'user_profile_id' not in data or not data['user_profile_id']:
        return jsonify({'error': 'Missing user_profile_id'}), 400
    doctor_id = data.get('doctor_id', None)
    patient_id = data.get('patient_id', None)
    try:
        user_profile.update_user_profile(data['user_profile_id'], doctor_id, patient_id)
        return jsonify({'message': 'User profile updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/user_profile', methods=['DELETE'])
def admin_delete_user_profile():
    data = request.get_json()
    if 'user_profile_id' not in data or not data['user_profile_id']:
        return jsonify({'error': 'Missing user_profile_id'}), 400
    try:
        user_profile.delete_user_profile(data['user_profile_id'])
        return jsonify({'message': 'User profile deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

##############################################
# Kiểm tra quyền admin
##############################################
@app.route('/admin/check_admin', methods=['GET'])
def check_admin():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'Missing user_id'}), 400
    try:
        user_id = int(user_id)
        # Sử dụng hàm is_admin trong models/user.py
        result = user.is_admin(user_id)
        return jsonify({'is_admin': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

##############################################
# Chạy server Flask (mặc định debug=True)
##############################################
if __name__ == '__main__':
    app.run(debug=True)