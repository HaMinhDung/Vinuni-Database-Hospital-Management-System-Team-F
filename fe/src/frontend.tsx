import React, { useState } from 'react';

interface UserInfo {
    UserID: number;
    Username: string;
    Role: string;
    // Other fields if needed
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
            // If both DoctorID and PatientID are null, consider it admin
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

    // -------------------- Functions for Patient --------------------
    const patientUpdateProfile = async () => {
        if (!patientId) return;
        const newName = prompt('Enter new name:');
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

    // -------------------- Functions for Doctor --------------------
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
            alert("Doctor profile not found.");
            return;
        }
        const info = dataProfile.doctor_profile;
        const newName = prompt(`Enter new name (Press Enter to keep [${info.Name}]): `, info.Name) || info.Name;
        const newSpec = prompt(`Enter new specialization (Press Enter to keep [${info.Specialization}]): `, info.Specialization) || info.Specialization;
        const newDeptInput = prompt(`Enter new department ID (Press Enter to keep [${info.DepartmentID}]): `, info.DepartmentID);
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
        const patientIdInput = prompt("Enter patient ID to schedule appointment: ");
        if (!patientIdInput) return;
        const patient_id = parseInt(patientIdInput);
        const dt = prompt("Enter appointment date and time (YYYY-MM-DD HH:MM:SS): ");
        if (!dt) return;
        const status = prompt("Enter appointment status (default 'Scheduled'):", "Scheduled") || "Scheduled";
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
        const appointmentIdInput = prompt("Enter appointment ID to edit: ");
        if (!appointmentIdInput) return;
        const appointment_id = parseInt(appointmentIdInput);
        const patientIdInput = prompt("Enter new patient ID (or leave blank to keep current): ");
        const new_patient = patientIdInput ? parseInt(patientIdInput) : undefined;
        const newDt = prompt("Enter new date and time (YYYY-MM-DD HH:MM:SS) (leave blank to keep current): ");
        const newStatus = prompt("Enter new status (leave blank to keep current): ");
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
        const appointmentIdInput = prompt("Enter appointment ID to create medical record for: ");
        if (!appointmentIdInput) return;
        const appointment_id = parseInt(appointmentIdInput);
        const diagnosis = prompt("Enter diagnosis: ");
        if (!diagnosis) return;
        const treatment = prompt("Enter treatment plan: ");
        if (!treatment) return;
        const notes = prompt("Enter notes: ") || "";
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

    // -------------------- Functions for Admin --------------------
    const adminManageDoctors = async () => {
        let choice = prompt(
            "--- MANAGE DOCTORS ---\n" +
            "1. View list of doctors\n" +
            "2. Create new doctor\n" +
            "3. Update doctor\n" +
            "4. Delete doctor\n" +
            "0. Exit\n" +
            "Select function:"
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
                    const name = prompt("Enter name of new doctor:");
                    if (!name) break;
                    const specialization = prompt("Enter specialization of new doctor:");
                    if (!specialization) break;
                    const deptInput = prompt("Enter department ID:");
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
                    const docId = prompt("Enter ID of doctor to update:");
                    if (!docId) break;
                    const newName = prompt("Enter new name:");
                    if (!newName) break;
                    const newSpec = prompt("Enter new specialization:");
                    if (!newSpec) break;
                    const newDeptInput = prompt("Enter new department ID:");
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
                    const docId = prompt("Enter ID of doctor to delete:");
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
                    alert("Invalid function!");
                }
            }
            choice = prompt(
                "--- MANAGE DOCTORS ---\n" +
                "1. View list of doctors\n" +
                "2. Create new doctor\n" +
                "3. Update doctor\n" +
                "4. Delete doctor\n" +
                "0. Exit\n" +
                "Select function:"
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

    // Function to display deeper admin menu based on selection
    const adminSubMenu = async () => {
        let choice = prompt(
            "--- ADMIN MENU ---\n" +
            "1. Manage Doctors\n" +
            "2. Manage Patients\n" +
            "3. Manage Appointments\n" +
            "4. Manage Medical Records\n" +
            "5. Manage Departments\n" +
            "6. Manage Services\n" +
            "7. Manage Users\n" +
            "8. Manage User Profiles\n" +
            "9. View data of all tables\n" +
            "0. Exit\n" +
            "Select function:"
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
                    alert("Invalid function!");
            }
            choice = prompt(
                "--- ADMIN MENU ---\n" +
                "1. Manage Doctors\n" +
                "2. Manage Patients\n" +
                "3. Manage Appointments\n" +
                "4. Manage Medical Records\n" +
                "5. Manage Departments\n" +
                "6. Manage Services\n" +
                "7. Manage Users\n" +
                "8. Manage User Profiles\n" +
                "9. View data of all tables\n" +
                "0. Exit\n" +
                "Select function:"
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
                    <h2>Login</h2>
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
                    <button onClick={handleLogin}>Login</button>
                    {message && <p style={{ color: 'red' }}>{message}</p>}
                </div>
            )}

            {view === 'menu' && userInfo && (
                <div>
                    <h2>Welcome, {userInfo.Username} ({userInfo.Role})</h2>
                    
                    {/* Menu for Patient */}
                    {userInfo.Role === 'Patient' && (
                        <div>
                            <h3>--- PATIENT MENU ---</h3>
                            <button onClick={patientUpdateProfile}>1. Edit patient profile</button>
                            <button onClick={fetchAppointments}>2. Display appointment list</button>
                            <button onClick={fetchMedicalRecords}>3. Display medical records</button>
                            <button onClick={fetchPatientProfile}>4. View patient profile</button>
                            <button onClick={fetchPatientDoctors}>5. View list of doctors you have appointments with or have been examined by</button>
                        </div>
                    )}

                    {/* Menu for Doctor */}
                    {userInfo.Role === 'Doctor' && (
                        <div>
                            <h3>--- DOCTOR MENU ---</h3>
                            <button onClick={fetchDoctorProfile}>1. Display doctor profile</button>
                            <button onClick={doctorUpdateProfile}>2. Edit doctor profile</button>
                            <button onClick={fetchDoctorAppointments}>3. Display list of Appointments with patients</button>
                            <button onClick={fetchDoctorMedicalRecords}>4. Display medical records you have provided</button>
                            <button onClick={fetchDoctorPatients}>5. View list of your patients</button>
                            <button onClick={createDoctorAppointment}>6. Schedule appointment with patient</button>
                            <button onClick={updateDoctorAppointment}>7. Edit appointment with patient</button>
                            <button onClick={createMedicalRecord}>8. Create medical record for appointment</button>
                        </div>
                    )}

                    {/* Menu for Admin */}
                    {userInfo.Role === 'Admin' && (
                        <div>
                            <h3>--- ADMIN MENU ---</h3>
                            <button onClick={adminSubMenu}>Open Admin Menu</button>
                        </div>
                    )}

                    <div style={{ marginTop: '20px' }}>
                        <button onClick={logout}>Logout</button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default App;