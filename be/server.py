from flask import Flask, request, jsonify
from flask_cors import CORS
from db.connection import get_connection
from models import user, patient, appointment, medical_record, user_profile, doctor, admin

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
    if not data or 'patient_id' not in data:
        return jsonify({'error': 'Missing patient_id in request data'}), 400

    patient_id = data['patient_id']
    new_name = data.get('new_name')
    new_dob = data.get('new_dob')
    new_gender = data.get('new_gender')
    new_contact = data.get('new_contact')

    # Check if at least one field to update is provided
    if not any([new_name, new_dob, new_gender, new_contact]):
         return jsonify({'message': 'No update data provided.'}), 200 # Or 400 depending on desired behavior

    try:
        patient.update_patient(
            data["patient_id"],
            new_name,
            new_dob,
            new_gender,
            new_contact
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
    if not data or 'doctor_id' not in data:
        return jsonify({'error': 'Missing doctor_id in request data'}), 400

    doctor_id = data['doctor_id']
    new_name = data.get('new_name')
    new_spec = data.get('new_spec')
    new_dept = data.get('new_dept')

    # Check if at least one field to update is provided
    if not any([new_name, new_spec, new_dept]):
         return jsonify({'message': 'No update data provided.'}), 200 # Or 400 depending on desired behavior

    try:
        doctor.update_doctor(
            doctor_id,
            new_name,
            new_spec,
            new_dept # Pass department_id as is, the model function handles int conversion if needed
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

# Xóa lịch hẹn của bệnh nhân (Bác sĩ)
@app.route('/doctor/appointments', methods=['DELETE'])
def delete_appointment_endpoint():
    data = request.get_json()
    if not data or 'appointment_id' not in data:
        return jsonify({'error': 'Missing appointment_id in request data'}), 400

    appointment_id = data['appointment_id']

    try:
        # Assuming appointment.delete_appointment exists
        appointment.delete_appointment(int(appointment_id))
        return jsonify({'message': 'Appointment deleted successfully'})
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

# Cập nhật hồ sơ y tế (Bác sĩ)
@app.route('/doctor/medical_record', methods=['PUT'])
def update_medical_record_endpoint():
    data = request.get_json()
    if not data or 'record_id' not in data:
        return jsonify({'error': 'Missing record_id in request data'}), 400

    record_id = data['record_id']
    diagnosis = data.get('diagnosis')
    treatment = data.get('treatment')
    notes = data.get('notes')

    # Check if at least one field to update is provided
    if not any([diagnosis, treatment, notes]):
         return jsonify({'message': 'No update data provided.'}), 200 # Or 400

    try:
        # Assuming medical_record.update_medical_record exists and handles updates
        medical_record.update_medical_record(
            int(record_id),
            diagnosis,
            treatment,
            notes
        )
        return jsonify({'message': 'Medical record updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Xóa hồ sơ y tế (Bác sĩ)
@app.route('/doctor/medical_record', methods=['DELETE'])
def delete_medical_record_endpoint():
    data = request.get_json()
    if not data or 'record_id' not in data:
        return jsonify({'error': 'Missing record_id in request data'}), 400

    record_id = data['record_id']

    try:
        # Assuming medical_record.delete_medical_record exists
        medical_record.delete_medical_record(int(record_id))
        return jsonify({'message': 'Medical record deleted successfully'})
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
            'doctors': admin.admin_get_all_doctors(),
            'patients': admin.admin_get_all_patients(),
            'appointments': admin.admin_get_all_appointments(),
            'medical_records': admin.admin_get_all_medical_records(),
            'departments': admin.admin_get_all_departments(),
            'services': admin.admin_get_all_services(),
            # 'users': user.read_users(),
            # 'user_profiles': user_profile.read_user_profiles()
        }
        return jsonify(all_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

##############################################
# Các endpoint cho Bác sĩ
##############################################

# Admin get all doctors
@app.route('/admin/doctor', methods=['GET'])
def admin_get_all_doctors():
    try:
        docs = admin.admin_get_all_doctors()
        return jsonify({'doctors': docs})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin create doctor
@app.route('/admin/doctor', methods=['POST'])
def admin_create_doctor():
    data = request.get_json()
    required_fields = ['name', 'specialization', 'department_id']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f"Missing {field}"}), 400
    try:
        admin.admin_create_doctor(data['name'], data['specialization'], int(data['department_id']))
        return jsonify({'message': 'Doctor created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin delete doctor
@app.route('/admin/doctor', methods=['DELETE'])
def admin_delete_doctor():
    data = request.get_json()
    if 'doctor_id' not in data or not data['doctor_id']:
        return jsonify({'error': 'Missing doctor_id'}), 400
    try:
        admin.admin_delete_doctor(int(data['doctor_id']))
        return jsonify({'message': 'Doctor deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin read doctor by ID
@app.route('/admin/doctor/<int:doctor_id>', methods=['GET'])
def admin_get_doctor(doctor_id):
    try:
        doctor_info = admin.admin_get_doctor(doctor_id)
        if not doctor_info:
            return jsonify({'error': 'Doctor not found'}), 404
        return jsonify({'doctor': doctor_info})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin update doctor
@app.route('/admin/doctor', methods=['PUT'])
def admin_update_doctor_endpoint():
    data = request.get_json()
    if not data or 'doctor_id' not in data:
        return jsonify({'error': 'Missing doctor_id in request data'}), 400

    doctor_id = data['doctor_id']
    new_name = data.get('new_name')
    new_spec = data.get('new_specialization') # Assuming specialization is sent explicitly now
    new_dept = data.get('new_department_id')

    # Check if at least one field to update is provided
    if not any([new_name, new_spec, new_dept]):
         return jsonify({'message': 'No update data provided.'}), 200 # Or 400 depending on desired behavior

    try:
        admin.admin_update_doctor(
            int(doctor_id),
            new_name,
            new_spec,
            new_dept # Pass department_id as is, the model function handles int conversion if needed
        )
        return jsonify({'message': 'Doctor profile updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

##############################################
# Các endpoint cho Bệnh nhân
##############################################

# Admin get all patients
@app.route('/admin/patient', methods=['GET'])
def admin_get_all_patients():
    try:
        patients = admin.admin_get_all_patients()
        return jsonify({'patients': patients})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Admin get patient by ID
@app.route('/admin/patient/<int:patient_id>', methods=['GET'])
def admin_get_patient(patient_id):
    try:
        patient_info = admin.admin_get_patient(patient_id)
        if not patient_info:
            return jsonify({'error': 'Patient not found'}), 404
        return jsonify({'patient': patient_info})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin create patient
@app.route('/admin/patient', methods=['POST'])
def admin_create_patient():
    data = request.get_json()
    required_fields = ['name', 'dob', 'gender', 'contact']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f"Missing {field}"}), 400
    try:
        patient_id = admin.admin_create_patient(data['name'], data['dob'], data['gender'], data['contact'])
        return jsonify({'message': 'Patient created successfully', 'patient_id': patient_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin delete patient
@app.route('/admin/patient', methods=['DELETE'])
def admin_delete_patient():
    data = request.get_json()
    if 'patient_id' not in data or not data['patient_id']:
        return jsonify({'error': 'Missing patient_id'}), 400
    try:
        admin.admin_delete_patient(int(data['patient_id']))
        return jsonify({'message': 'Patient deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
##############################################
# Endpoints for Appointments
##############################################

# Admin get all appointments
@app.route('/admin/appointment', methods=['GET'])
def admin_get_all_appointments():
    try:
        appointments = admin.admin_get_all_appointments()
        return jsonify({'appointments': appointments})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Admin get appointment by ID
@app.route('/admin/appointment/<int:appointment_id>', methods=['GET'])
def admin_get_appointment(appointment_id):
    try:
        appointment_info = admin.admin_get_appointment(appointment_id)
        if not appointment_info:
            return jsonify({'error': 'Appointment not found'}), 404
        return jsonify({'appointment': appointment_info})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
##############################################
# Endpoints for Departments
##############################################

# Admin get all departments
@app.route('/admin/department', methods=['GET'])
def admin_get_all_departments():
    try:
        departments = admin.admin_get_all_departments()
        return jsonify({'departments': departments})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Admin create department
@app.route('/admin/department', methods=['POST'])
def admin_create_department():
    data = request.get_json()
    if 'name' not in data or not data['name']:
        return jsonify({'error': 'Missing department name'}), 400
    try:
        department_id = admin.admin_create_department(data['name'])
        return jsonify({'message': 'Department created successfully', 'department_id': department_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Admin delete department
@app.route('/admin/department', methods=['DELETE'])
def admin_delete_department():
    data = request.get_json()
    if 'department_id' not in data or not data['department_id']:
        return jsonify({'error': 'Missing department_id'}), 400
    try:
        admin.admin_delete_department(int(data['department_id']))
        return jsonify({'message': 'Department deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
##############################################
# Enpoints for Medical Records
##############################################

# Admin get all medical records
@app.route('/admin/medical_record', methods=['GET'])
def admin_get_all_medical_records():
    try:
        records = admin.admin_get_all_medical_records()
        return jsonify({'medical_records': records})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
##############################################
# Enpoints for Services
##############################################

# Admin get all services
@app.route('/admin/service', methods=['GET'])
def admin_get_all_services():
    try:
        services = admin.admin_get_all_services()
        return jsonify({'services': services})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Admin get service by ID
@app.route('/admin/service/<int:service_id>', methods=['GET'])
def admin_get_service(service_id):
    try:
        service_info = admin.admin_get_service(service_id)
        if not service_info:
            return jsonify({'error': 'Service not found'}), 404
        return jsonify({'service': service_info})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin create service
@app.route('/admin/service', methods=['POST'])
def admin_create_service():
    data = request.get_json()
    required_fields = ['name', 'cost']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f"Missing {field}"}), 400
    try:
        service_id = admin.admin_create_service(data['name'], float(data['cost']))
        return jsonify({'message': 'Service created successfully', 'service_id': service_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Admin delete service
@app.route('/admin/service', methods=['DELETE'])
def admin_delete_service():
    data = request.get_json()
    if 'service_id' not in data or not data['service_id']:
        return jsonify({'error': 'Missing service_id'}), 400
    try:
        admin.admin_delete_service(int(data['service_id']))
        return jsonify({'message': 'Service deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin update service
@app.route('/admin/service', methods=['PUT'])
def admin_update_service():
    data = request.get_json()
    required_fields = ['service_id', 'name', 'cost']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f"Missing {field}"}), 400
    try:
        admin.admin_update_service(int(data['service_id']), data['name'], float(data['cost']))
        return jsonify({'message': 'Service updated successfully'})
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

@app.route('/user/change_password', methods=['POST'])
def change_password_endpoint():
    data = request.get_json()
    if not data or 'user_id' not in data or 'old_password' not in data or 'new_password' not in data:
        return jsonify({'error': 'Missing user ID, old password, or new password'}), 400

    user_id = data['user_id']
    old_password = data['old_password']
    new_password = data['new_password']

    try:
        success, message = user.change_password(user_id, old_password, new_password)
        if success:
            return jsonify({'message': message}), 200
        else:
            return jsonify({'error': message}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

##############################################
# Chạy server Flask (mặc định debug=True)
##############################################
if __name__ == '__main__':
    app.run(debug=True)