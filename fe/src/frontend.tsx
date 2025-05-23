import React, { useState } from 'react';

interface UserInfo {
    UserID: number;
    Username: string;
    Role: string;
    // Các trường khác nếu cần
}

const App: React.FC = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [userInfo, setUserInfo] = useState<UserInfo | null>(null);
    const [doctorId, setDoctorId] = useState<number | null>(null);
    const [patientId, setPatientId] = useState<number | null>(null);
    const [message, setMessage] = useState('');
    const [view, setView] = useState<'login' | 'menu'>('login');

    const handleLogin = async () => {
        const response = await fetch('http://localhost:5000/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        const data = await response.json();
        if (response.ok) {
            // Nếu cả DoctorID và PatientID đều null thì coi là admin
            if (data.doctor_id === null && data.patient_id === null) {
                data.user_info.Role = "Admin";
            }
            setUserInfo(data.user_info);
            setDoctorId(data.doctor_id);
            setPatientId(data.patient_id);
            setView('menu');
            setMessage('');
        } else {
            setMessage(data.error || 'Login failed');
        }
    };

    // -------------------- Các hàm cho Patient --------------------
    const patientUpdateProfile = async () => {
        if (!patientId) return;
        const newName = prompt('Nhập tên mới:');
        if (!newName) return;
        const response = await fetch('http://localhost:5000/patient/update_profile', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                patient_id: patientId,
                new_name: newName,
                new_dob: "1990-01-01",
                new_gender: "Other",
                new_contact: "0000000000"
            })
        });
        const data = await response.json();
        alert(data.message || data.error);
    };

    const fetchAppointments = async () => {
        if (!patientId) return;
        const response = await fetch(`http://localhost:5000/patient/appointments?patient_id=${patientId}`);
        const data = await response.json();
        alert(JSON.stringify(data.appointments, null, 2));
    };

    const fetchMedicalRecords = async () => {
        if (!patientId) return;
        const response = await fetch(`http://localhost:5000/patient/medical_records?patient_id=${patientId}`);
        const data = await response.json();
        alert(JSON.stringify(data.medical_records, null, 2));
    };

    const fetchPatientProfile = async () => {
        if (!patientId) return;
        const response = await fetch(`http://localhost:5000/patient/profile?patient_id=${patientId}`);
        const data = await response.json();
        alert(JSON.stringify(data.patient_profile, null, 2));
    };

    const fetchPatientDoctors = async () => {
        if (!patientId) return;
        const response = await fetch(`http://localhost:5000/patient/doctors?patient_id=${patientId}`);
        const data = await response.json();
        alert(JSON.stringify(data.doctors || data.message, null, 2));
    };

    // -------------------- Các hàm cho Doctor --------------------
    const fetchDoctorProfile = async () => {
        if (!doctorId) return;
        const response = await fetch(`http://localhost:5000/doctor/profile?doctor_id=${doctorId}`);
        const data = await response.json();
        alert(JSON.stringify(data.doctor_profile, null, 2));
    };

    const doctorUpdateProfile = async () => {
        if (!doctorId) return;
        const responseProfile = await fetch(`http://localhost:5000/doctor/profile?doctor_id=${doctorId}`);
        const dataProfile = await responseProfile.json();
        if (!dataProfile.doctor_profile) {
            alert("Không tìm thấy hồ sơ bác sĩ.");
            return;
        }
        const info = dataProfile.doctor_profile;
        const newName = prompt(`Nhập tên mới (Enter để giữ nguyên [${info.Name}]): `, info.Name) || info.Name;
        const newSpec = prompt(`Nhập chuyên khoa mới (Enter để giữ nguyên [${info.Specialization}]): `, info.Specialization) || info.Specialization;
        const newDeptInput = prompt(`Nhập ID khoa mới (Enter để giữ nguyên [${info.DepartmentID}]): `, info.DepartmentID);
        const newDept = newDeptInput ? parseInt(newDeptInput) : info.DepartmentID;
        const response = await fetch('http://localhost:5000/doctor/update_profile', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                doctor_id: doctorId,
                new_name: newName,
                new_spec: newSpec,
                new_dept: newDept
            })
        });
        const data = await response.json();
        alert(data.message || data.error);
    };

    const fetchDoctorAppointments = async () => {
        if (!doctorId) return;
        const response = await fetch(`http://localhost:5000/doctor/appointments?doctor_id=${doctorId}`);
        const data = await response.json();
        alert(JSON.stringify(data.appointments, null, 2));
    };

    const fetchDoctorMedicalRecords = async () => {
        if (!doctorId) return;
        const response = await fetch(`http://localhost:5000/doctor/medical_records?doctor_id=${doctorId}`);
        const data = await response.json();
        alert(JSON.stringify(data.medical_records, null, 2));
    };

    const fetchDoctorPatients = async () => {
        if (!doctorId) return;
        const response = await fetch(`http://localhost:5000/doctor/patients?doctor_id=${doctorId}`);
        const data = await response.json();
        alert(JSON.stringify(data.patients || data.message, null, 2));
    };

    const createDoctorAppointment = async () => {
        if (!doctorId) return;
        const patientIdInput = prompt("Nhập ID bệnh nhân cần đặt lịch: ");
        if (!patientIdInput) return;
        const patient_id = parseInt(patientIdInput);
        const dt = prompt("Nhập ngày giờ cuộc hẹn (YYYY-MM-DD HH:MM:SS): ");
        if (!dt) return;
        const status = prompt("Nhập trạng thái cuộc hẹn (mặc định 'Scheduled'):", "Scheduled") || "Scheduled";
        const response = await fetch('http://localhost:5000/doctor/appointments', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                patient_id,
                doctor_id: doctorId,
                datetime_str: dt,
                status
            })
        });
        const data = await response.json();
        alert(data.message || data.error);
    };

    const updateDoctorAppointment = async () => {
        if (!doctorId) return;
        const appointmentIdInput = prompt("Nhập ID cuộc hẹn cần chỉnh sửa: ");
        if (!appointmentIdInput) return;
        const appointment_id = parseInt(appointmentIdInput);
        const patientIdInput = prompt("Nhập ID bệnh nhân mới (hoặc để trống giữ nguyên): ");
        const new_patient = patientIdInput ? parseInt(patientIdInput) : undefined;
        const newDt = prompt("Nhập ngày giờ mới (YYYY-MM-DD HH:MM:SS) (để trống giữ nguyên): ");
        const newStatus = prompt("Nhập trạng thái mới (để trống giữ nguyên): ");
        const response = await fetch('http://localhost:5000/doctor/appointments', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                appointment_id,
                patient_id: new_patient || 0,
                doctor_id: doctorId,
                datetime_str: newDt || "",
                status: newStatus || ""
            })
        });
        const data = await response.json();
        alert(data.message || data.error);
    };

    const createMedicalRecord = async () => {
        if (!doctorId) return;
        const appointmentIdInput = prompt("Nhập ID cuộc hẹn cần tạo hồ sơ y tế: ");
        if (!appointmentIdInput) return;
        const appointment_id = parseInt(appointmentIdInput);
        const diagnosis = prompt("Nhập chẩn đoán: ");
        if (!diagnosis) return;
        const treatment = prompt("Nhập phác đồ điều trị: ");
        if (!treatment) return;
        const notes = prompt("Nhập ghi chú: ") || "";
        const response = await fetch('http://localhost:5000/doctor/medical_record', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                appointment_id,
                diagnosis,
                treatment,
                notes
            })
        });
        const data = await response.json();
        alert(data.message || data.error);
    };

    // -------------------- Các hàm cho Admin --------------------
    const adminManageDoctors = async () => {
        let choice = prompt(
            "--- QUẢN LÝ BÁC SĨ ---\n" +
            "1. Xem danh sách bác sĩ\n" +
            "2. Tạo bác sĩ mới\n" +
            "3. Cập nhật bác sĩ\n" +
            "4. Xóa bác sĩ\n" +
            "0. Thoát\n" +
            "Chọn chức năng:"
        );
        while (choice !== "0") {
            switch (choice) {
                case "1": {
                    const response = await fetch('http://localhost:5000/admin/doctor');
                    const data = await response.json();
                    alert(JSON.stringify(data.doctors, null, 2));
                    break;
                }
                case "2": {
                    const name = prompt("Nhập tên bác sĩ mới:");
                    if (!name) break;
                    const specialization = prompt("Nhập chuyên môn của bác sĩ:");
                    if (!specialization) break;
                    const deptInput = prompt("Nhập ID khoa:");
                    if (!deptInput) break;
                    const department_id = parseInt(deptInput);
                    const response = await fetch('http://localhost:5000/admin/doctor', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ name, specialization, department_id })
                    });
                    const data = await response.json();
                    alert(data.message || data.error);
                    break;
                }
                case "3": {
                    const docId = prompt("Nhập ID bác sĩ cần cập nhật:");
                    if (!docId) break;
                    const newName = prompt("Nhập tên mới:");
                    if (!newName) break;
                    const newSpec = prompt("Nhập chuyên môn mới:");
                    if (!newSpec) break;
                    const newDeptInput = prompt("Nhập ID khoa mới:");
                    if (!newDeptInput) break;
                    const newDept = parseInt(newDeptInput);
                    const response = await fetch('http://localhost:5000/admin/doctor', {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            doctor_id: parseInt(docId),
                            new_name: newName,
                            new_spec: newSpec,
                            new_dept: newDept
                        })
                    });
                    const data = await response.json();
                    alert(data.message || data.error);
                    break;
                }
                case "4": {
                    const docId = prompt("Nhập ID bác sĩ cần xóa:");
                    if (!docId) break;
                    const response = await fetch('http://localhost:5000/admin/doctor', {
                        method: 'DELETE',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ doctor_id: parseInt(docId) })
                    });
                    const data = await response.json();
                    alert(data.message || data.error);
                    break;
                }
                default: {
                    alert("Chức năng không hợp lệ!");
                }
            }
            choice = prompt(
                "--- QUẢN LÝ BÁC SĨ ---\n" +
                "1. Xem danh sách bác sĩ\n" +
                "2. Tạo bác sĩ mới\n" +
                "3. Cập nhật bác sĩ\n" +
                "4. Xóa bác sĩ\n" +
                "0. Thoát\n" +
                "Chọn chức năng:"
            );
        }
    };

    const adminManagePatients = async () => {
        const response = await fetch('http://localhost:5000/admin/patient');
        const data = await response.json();
        alert(JSON.stringify(data.patients, null, 2));
    };

    const adminManageAppointments = async () => {
        const response = await fetch('http://localhost:5000/admin/appointment');
        const data = await response.json();
        alert(JSON.stringify(data.appointments, null, 2));
    };

    const adminManageMedicalRecords = async () => {
        const response = await fetch('http://localhost:5000/admin/medical_record');
        const data = await response.json();
        alert(JSON.stringify(data.medical_records, null, 2));
    };

    const adminManageDepartments = async () => {
        const response = await fetch('http://localhost:5000/admin/department');
        const data = await response.json();
        alert(JSON.stringify(data.departments, null, 2));
    };

    const adminManageServices = async () => {
        const response = await fetch('http://localhost:5000/admin/service');
        const data = await response.json();
        alert(JSON.stringify(data.services, null, 2));
    };

    const adminManageUsers = async () => {
        const response = await fetch('http://localhost:5000/admin/user');
        const data = await response.json();
        alert(JSON.stringify(data.users, null, 2));
    };

    const adminManageUserProfiles = async () => {
        const response = await fetch('http://localhost:5000/admin/user_profile');
        const data = await response.json();
        alert(JSON.stringify(data.user_profiles, null, 2));
    };

    // Hàm hiển thị menu admin sâu hơn theo lựa chọn
    const adminSubMenu = async () => {
        let choice = prompt(
            "--- MENU ADMIN ---\n" +
            "1. Quản lý Bác sĩ\n" +
            "2. Quản lý Bệnh nhân\n" +
            "3. Quản lý Cuộc hẹn\n" +
            "4. Quản lý Hồ sơ y tế\n" +
            "5. Quản lý Khoa\n" +
            "6. Quản lý Dịch vụ\n" +
            "7. Quản lý Người dùng\n" +
            "8. Quản lý Hồ sơ người dùng\n" +
            "9. Xem dữ liệu tất cả các bảng\n" +
            "0. Thoát\n" +
            "Chọn chức năng:"
        );
        while (choice !== "0") {
            switch (choice) {
                case "1":
                    adminManageDoctors();
                    break;
                case "2":
                    adminManagePatients();
                    break;
                case "3":
                    adminManageAppointments();
                    break;
                case "4":
                    adminManageMedicalRecords();
                    break;
                case "5":
                    adminManageDepartments();
                    break;
                case "6":
                    adminManageServices();
                    break;
                case "7":
                    adminManageUsers();
                    break;
                case "8":
                    adminManageUserProfiles();
                    break;
                case "9":
                    const response = await fetch('http://localhost:5000/admin/all_data');
                    const data = await response.json();
                    alert(JSON.stringify(data, null, 2));
                    break;
                default:
                    alert("Chức năng không hợp lệ!");
            }
            choice = prompt(
                "--- MENU ADMIN ---\n" +
                "1. Quản lý Bác sĩ\n" +
                "2. Quản lý Bệnh nhân\n" +
                "3. Quản lý Cuộc hẹn\n" +
                "4. Quản lý Hồ sơ y tế\n" +
                "5. Quản lý Khoa\n" +
                "6. Quản lý Dịch vụ\n" +
                "7. Quản lý Người dùng\n" +
                "8. Quản lý Hồ sơ người dùng\n" +
                "9. Xem dữ liệu tất cả các bảng\n" +
                "0. Thoát\n" +
                "Chọn chức năng:"
            );
        }
    };

    const logout = () => {
        setUserInfo(null);
        setDoctorId(null);
        setPatientId(null);
        setView('login');
        setUsername('');
        setPassword('');
    };

    return (
        <div style={{ padding: '20px' }}>
            {view === 'login' && (
                <div>
                    <h2>Đăng nhập</h2>
                    <div style={{ marginBottom: '10px' }}>
                        <input
                            type="text"
                            placeholder="Username"
                            value={username}
                            onChange={e => setUsername(e.target.value)}
                        />
                    </div>
                    <div style={{ marginBottom: '10px' }}>
                        <input
                            type="password"
                            placeholder="Password"
                            value={password}
                            onChange={e => setPassword(e.target.value)}
                        />
                    </div>
                    <button onClick={handleLogin}>Đăng nhập</button>
                    {message && <p style={{ color: 'red' }}>{message}</p>}
                </div>
            )}

            {view === 'menu' && userInfo && (
                <div>
                    <h2>Chào, {userInfo.Username} ({userInfo.Role})</h2>
                    
                    {/* Menu cho Patient */}
                    {userInfo.Role === 'Patient' && (
                        <div>
                            <h3>--- MENU BỆNH NHÂN ---</h3>
                            <button onClick={patientUpdateProfile}>1. Chỉnh sửa hồ sơ bệnh nhân</button>
                            <button onClick={fetchAppointments}>2. Hiển thị danh sách appointment</button>
                            <button onClick={fetchMedicalRecords}>3. Hiển thị hồ sơ y tế</button>
                            <button onClick={fetchPatientProfile}>4. Xem hồ sơ bệnh nhân</button>
                            <button onClick={fetchPatientDoctors}>5. Xem danh sách bác sĩ đã hẹn hoặc từng khám cho bạn</button>
                        </div>
                    )}

                    {/* Menu cho Doctor */}
                    {userInfo.Role === 'Doctor' && (
                        <div>
                            <h3>--- MENU BÁC SĨ ---</h3>
                            <button onClick={fetchDoctorProfile}>1. Hiển thị hồ sơ bác sĩ</button>
                            <button onClick={doctorUpdateProfile}>2. Chỉnh sửa hồ sơ bác sĩ</button>
                            <button onClick={fetchDoctorAppointments}>3. Hiển thị danh sách Appointment với bệnh nhân</button>
                            <button onClick={fetchDoctorMedicalRecords}>4. Hiển thị hồ sơ y tế bạn đã cung cấp</button>
                            <button onClick={fetchDoctorPatients}>5. Xem danh sách bệnh nhân của bạn</button>
                            <button onClick={createDoctorAppointment}>6. Đặt lịch hẹn với bệnh nhân</button>
                            <button onClick={updateDoctorAppointment}>7. Chỉnh sửa lịch hẹn với bệnh nhân</button>
                            <button onClick={createMedicalRecord}>8. Tạo hồ sơ y tế cho cuộc hẹn</button>
                        </div>
                    )}

                    {/* Menu cho Admin */}
                    {userInfo.Role === 'Admin' && (
                        <div>
                            <h3>--- MENU ADMIN ---</h3>
                            <button onClick={adminSubMenu}>Mở Menu Admin</button>
                        </div>
                    )}

                    <div style={{ marginTop: '20px' }}>
                        <button onClick={logout}>Đăng xuất</button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default App;