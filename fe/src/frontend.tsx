import React, { useState } from 'react';

interface UserInfo {
    UserID: number;
    Username: string;
    Role: string;
    // Other fields if needed, such as FullName if provided by backend
}

interface DoctorProfile {
    DoctorID: number;
    Name: string;
    Specialization: string;
    DepartmentID: number;
}

interface Appointment {
    AppointmentID: number;
    PatientID: number;
    PatientName?: string;
    DoctorID: number;
    DateTime: string; // Or Date type if preferred
    Status: string;
    // Add other relevant appointment fields
}

interface MedicalRecord {
    RecordID: number;
    AppointmentID: number;
    Diagnosis: string;
    Treatment: string;
    Notes: string;
    RecordDate: string; // Or Date type
    // Add other relevant medical record fields
}

interface Patient {
    PatientID: number;
    Name: string;
    DOB: string; // Or Date type
    Gender: string;
    Contact: string;
    // Add other relevant patient fields
}

interface PatientProfile {
    PatientID: number;
    Name: string;
    DOB: string; // Or Date type
    Gender: string;
    Contact: string;
    // Add other relevant patient profile fields
}

interface Department {
    DepartmentID: number;
    Name: string;
}

const App: React.FC = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [userInfo, setUserInfo] = useState<UserInfo | null>(null);
    const [doctorId, setDoctorId] = useState<number | null>(null);
    const [patientId, setPatientId] = useState<number | null>(null);
    const [message, setMessage] = useState('');
    const [view, setView] = useState<'login' | 'menu'>('login');
    const [doctorActiveMenuItem, setDoctorActiveMenuItem] = useState<'profile' | 'appointments' | 'medical_records' | 'patients' | 'schedule_appointment' | 'edit_appointment' | 'create_medical_record' | 'edit_doctor_profile' | null>('profile');
    const [patientActiveMenuItem, setPatientActiveMenuItem] = useState<'profile' | 'appointments' | 'medical_records' | 'doctors' | 'edit_patient_profile' | null>('profile');
    const [doctorProfile, setDoctorProfile] = useState<DoctorProfile | null>(null);
    const [doctorAppointments, setDoctorAppointments] = useState<Appointment[]>([]);
    const [doctorMedicalRecords, setDoctorMedicalRecords] = useState<MedicalRecord[]>([]);
    const [doctorPatients, setDoctorPatients] = useState<Patient[]>([]);
    const [loadingDoctorData, setLoadingDoctorData] = useState<boolean>(false);
    const [doctorError, setDoctorError] = useState<string | null>(null);
    const [editProfileFormData, setEditProfileFormData] = useState<Partial<DoctorProfile>>({});
    const [editProfileMessage, setEditProfileMessage] = useState<string | null>(null);
    const [newAppointmentFormData, setNewAppointmentFormData] = useState({ patient_id: '', datetime_str: '', status: 'Scheduled' });
    const [newAppointmentMessage, setNewAppointmentMessage] = useState<string | null>(null);
    const [editAppointmentFormData, setEditAppointmentFormData] = useState({ appointment_id: '', patient_id: '', datetime_str: '', status: '' });
    const [editAppointmentMessage, setEditAppointmentMessage] = useState<string | null>(null);
    const [newMedicalRecordFormData, setNewMedicalRecordFormData] = useState({ appointment_id: '', diagnosis: '', treatment: '', notes: '' });
    const [newMedicalRecordMessage, setNewMedicalRecordMessage] = useState<string | null>(null);
    const [patientProfile, setPatientProfile] = useState<PatientProfile | null>(null);
    const [patientAppointments, setPatientAppointments] = useState<Appointment[]>([]);
    const [patientMedicalRecords, setPatientMedicalRecords] = useState<MedicalRecord[]>([]);
    const [patientDoctors, setPatientDoctors] = useState<DoctorProfile[]>([]);
    const [loadingPatientData, setLoadingPatientData] = useState<boolean>(false);
    const [patientError, setPatientError] = useState<string | null>(null);
    const [editPatientProfileFormData, setEditPatientProfileFormData] = useState<Partial<Patient>>({});
    const [editPatientProfileMessage, setEditPatientProfileMessage] = useState<string | null>(null);
    const [departments, setDepartments] = useState<Department[]>([]);
    const [showNewAppointmentRow, setShowNewAppointmentRow] = useState(false);
    const [showNewMedicalRecordRow, setShowNewMedicalRecordRow] = useState(false);
    const [newAppointmentPatientName, setNewAppointmentPatientName] = useState<string | null>(null);
    const [editingAppointmentId, setEditingAppointmentId] = useState<number | null>(null);
    const [editingMedicalRecordId, setEditingMedicalRecordId] = useState<number | null>(null);
    const [editMedicalRecordFormData, setEditMedicalRecordFormData] = useState<Partial<MedicalRecord>>({});
    const [editMedicalRecordMessage, setEditMedicalRecordMessage] = useState<string | null>(null);
    const [showChangePasswordForm, setShowChangePasswordForm] = useState(false);
    const [oldPassword, setOldPassword] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [confirmNewPassword, setConfirmNewPassword] = useState('');
    const [changePasswordMessage, setChangePasswordMessage] = useState<string | null>(null);

    // Function to calculate the next rounded hour 24 hours from now
    const calculateDefaultAppointmentTime = () => {
        const now = new Date();
        const twentyFourHoursLater = new Date(now.getTime() + 24 * 60 * 60 * 1000);

        const year = twentyFourHoursLater.getFullYear();
        const month = (twentyFourHoursLater.getMonth() + 1).toString().padStart(2, '0'); // Months are 0-indexed
        const day = twentyFourHoursLater.getDate().toString().padStart(2, '0');
        let hours = twentyFourHoursLater.getHours();
        const minutes = twentyFourHoursLater.getMinutes();
        const seconds = twentyFourHoursLater.getSeconds();

        // Round up to the next hour if there are minutes or seconds
        if (minutes > 0 || seconds > 0) {
            hours++;
        }

        // Handle hour overflow (e.g., 24 becomes 00 of the next day)
        let nextHourDate = new Date(twentyFourHoursLater.getTime());
        nextHourDate.setHours(hours, 0, 0, 0); // Set minutes, seconds, milliseconds to 0

        const finalYear = nextHourDate.getFullYear();
        const finalMonth = (nextHourDate.getMonth() + 1).toString().padStart(2, '0');
        const finalDay = nextHourDate.getDate().toString().padStart(2, '0');
        const finalHours = nextHourDate.getHours().toString().padStart(2, '0');

        return `${finalYear}-${finalMonth}-${finalDay} ${finalHours}:00:00`;
    };

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
            if (data.user_info.Role === 'Doctor') {
                setDoctorActiveMenuItem('profile'); // Set default view to profile for doctor
                // Automatically fetch profile on login for doctor
                if (data.doctor_id) {
                    fetchDoctorProfile(data.doctor_id);
                }
                // Fetch departments on login for doctors (or other roles that might need it)
                fetchDepartments();
            } else if (data.user_info.Role === 'Patient') {
                 setPatientActiveMenuItem('profile'); // Set default view to profile for patient
                 // Automatically fetch profile on login for patient
                 if (data.patient_id) {
                     fetchPatientProfile(data.patient_id);
                 }
            }
        } else {
            setMessage(data.error || 'Login failed');
        }
    };

    const fetchPatientName = async (patientId: number) => {
        if (!patientId) {
            setNewAppointmentPatientName(null);
            return;
        }
        try {
            const response = await fetch(`http://localhost:5000/patient/profile?patient_id=${patientId}`);
            const data = await response.json();
            if (response.ok && data.patient_profile) {
                setNewAppointmentPatientName(data.patient_profile.Name);
            } else {
                setNewAppointmentPatientName('Not Found');
            }
        } catch (error) {
            console.error('Error fetching patient name:', error);
            setNewAppointmentPatientName('Error');
        }
    };

    // -------------------- Functions for Patient --------------------
    const patientUpdateProfile = async () => {
        if (!patientId || !editPatientProfileFormData) return;

        setLoadingPatientData(true);
        setPatientError(null);
        setEditPatientProfileMessage(null);

        // Prepare update data, only include fields that have changed or are required
        const updateData: any = { patient_id: patientId };
        // Add checks for each field to see if it has changed before adding to updateData
        if (editPatientProfileFormData.Name !== patientProfile?.Name && editPatientProfileFormData.Name !== '') updateData.new_name = editPatientProfileFormData.Name;
        if (editPatientProfileFormData.DOB !== patientProfile?.DOB && editPatientProfileFormData.DOB !== '') updateData.new_dob = editPatientProfileFormData.DOB;
        if (editPatientProfileFormData.Gender !== patientProfile?.Gender && editPatientProfileFormData.Gender !== '') updateData.new_gender = editPatientProfileFormData.Gender;
        if (editPatientProfileFormData.Contact !== patientProfile?.Contact && editPatientProfileFormData.Contact !== '') updateData.new_contact = editPatientProfileFormData.Contact;

        // Only proceed if there are changes other than the patient_id
        if (Object.keys(updateData).length <= 1) {
            setEditPatientProfileMessage('No changes to save.');
            setLoadingPatientData(false);
            return;
        }

        try {
            const response = await fetch('http://localhost:5000/patient/update_profile', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(updateData)
            });
            const data = await response.json();
            if (response.ok) {
                setEditPatientProfileMessage(data.message || 'Profile updated successfully!');
                fetchPatientProfile(patientId); // Refresh profile after update
            } else {
                setEditPatientProfileMessage(data.error || 'Failed to update profile');
                setPatientError(data.error || 'Failed to update profile'); // Also set main error state
            }
        } catch (error: any) {
            setEditPatientProfileMessage(error.message || 'An error occurred while updating profile');
            setPatientError(error.message || 'An error occurred while updating profile'); // Also set main error state
        } finally {
            setLoadingPatientData(false);
        }
    };

    const fetchAppointments = async (id: number | null) => {
        if (!id) return;
        setLoadingPatientData(true);
        setPatientError(null);
        try {
            const response = await fetch(`http://localhost:5000/patient/appointments?patient_id=${id}`);
            const data = await response.json();
            if (response.ok) {
                setPatientAppointments(data.appointments || []);
            } else {
                setPatientError(data.error || 'Failed to fetch appointments');
                setPatientAppointments([]);
            }
        } catch (error: any) {
             setPatientError(error.message || 'An error occurred while fetching appointments');
             setPatientAppointments([]);
        } finally {
            setLoadingPatientData(false);
        }
    };

    const fetchMedicalRecords = async (id: number | null) => {
        if (!id) return;
        setLoadingPatientData(true);
        setPatientError(null);
        try {
            const response = await fetch(`http://localhost:5000/patient/medical_records?patient_id=${id}`);
            const data = await response.json();
            if (response.ok) {
                setPatientMedicalRecords(data.medical_records || []);
            } else {
                setPatientError(data.error || 'Failed to fetch medical records');
                setPatientMedicalRecords([]);
            }
        } catch (error: any) {
             setPatientError(error.message || 'An error occurred while fetching medical records');
             setPatientMedicalRecords([]);
        } finally {
            setLoadingPatientData(false);
        }
    };

    const fetchPatientProfile = async (id: number | null) => {
         if (!id) return;
         setLoadingPatientData(true);
         setPatientError(null);
         try {
            const response = await fetch(`http://localhost:5000/patient/profile?patient_id=${id}`);
            const data = await response.json();
            if (response.ok) {
                 setPatientProfile(data.patient_profile);
                  setEditPatientProfileFormData(data.patient_profile);
            } else {
                 setPatientError(data.error || 'Failed to fetch patient profile');
                 setPatientProfile(null);
                 setEditPatientProfileFormData({});
            }
         } catch (error: any) {
              setPatientError(error.message || 'An error occurred while fetching patient profile');
              setPatientProfile(null);
              setEditPatientProfileFormData({});
         } finally {
             setLoadingPatientData(false);
         }
    };

    const fetchPatientDoctors = async (id: number | null) => {
        if (!id) return;
        setLoadingPatientData(true);
        setPatientError(null);
        try {
            const response = await fetch(`http://localhost:5000/patient/doctors?patient_id=${id}`);
            const data = await response.json();
            if (response.ok) {
                setPatientDoctors(data.doctors || []);
            } else {
                 setPatientError(data.error || 'Failed to fetch doctors');
                 setPatientDoctors([]);
            }
        } catch (error: any) {
             setPatientError(error.message || 'An error occurred while fetching doctors');
             setPatientDoctors([]);
        } finally {
            setLoadingPatientData(false);
        }
    };

    // -------------------- Functions for Doctor --------------------
    const fetchDoctorProfile = async (id: number | null) => {
        if (!id) return;
        setLoadingDoctorData(true);
        setDoctorError(null);
        try {
            const response = await fetch(`http://localhost:5000/doctor/profile?doctor_id=${id}`);
            const data = await response.json();
            if (response.ok) {
                setDoctorProfile(data.doctor_profile);
                // Initialize edit form data with fetched profile data
                setEditProfileFormData(data.doctor_profile);
            } else {
                setDoctorError(data.error || 'Failed to fetch profile');
                setDoctorProfile(null);
                setEditProfileFormData({});
            }
        } catch (error: any) {
             setDoctorError(error.message || 'An error occurred while fetching profile');
             setDoctorProfile(null);
             setEditProfileFormData({});
        } finally {
            setLoadingDoctorData(false);
        }
    };

    const handleEditProfileFormChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        setEditProfileFormData({
            ...editProfileFormData,
            [e.target.name]: e.target.value
        });
    };

    const doctorUpdateProfile = async () => {
        if (!doctorId || !editProfileFormData) return;

        setLoadingDoctorData(true);
        setDoctorError(null);
        setEditProfileMessage(null);

        // Prepare update data, only include fields that have changed or are required
        const updateData: any = { doctor_id: doctorId };
        if (editProfileFormData.Name !== doctorProfile?.Name) updateData.new_name = editProfileFormData.Name;

        // Find the selected department name based on the selected DepartmentID
        const selectedDepartment = departments.find(dept => dept.DepartmentID === editProfileFormData.DepartmentID);
        const newSpecialization = selectedDepartment ? selectedDepartment.Name : ''; // Use department name as specialization

        // Add specialization and department ID to updateData if they have changed
        if (newSpecialization !== doctorProfile?.Specialization) updateData.new_spec = newSpecialization;
        if (editProfileFormData.DepartmentID !== doctorProfile?.DepartmentID) updateData.new_dept = editProfileFormData.DepartmentID;

        // Only proceed if there are changes other than the doctor_id
        if (Object.keys(updateData).length <= 1) {
            setEditProfileMessage('No changes to save.');
            setLoadingDoctorData(false);
            return;
        }

        try {
            const response = await fetch('http://localhost:5000/doctor/update_profile', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(updateData)
            });
            const data = await response.json();
            if (response.ok) {
                setEditProfileMessage(data.message || 'Profile updated successfully!');
                fetchDoctorProfile(doctorId); // Refresh profile after update
                console.log('Doctor profile fetched after update:', doctorProfile);
            } else {
                setEditProfileMessage(data.error || 'Failed to update profile');
                setDoctorError(data.error || 'Failed to update profile'); // Also set main error state
            }
        } catch (error: any) {
            setEditProfileMessage(error.message || 'An error occurred while updating profile');
            setDoctorError(error.message || 'An error occurred while updating profile'); // Also set main error state
        } finally {
            setLoadingDoctorData(false);
        }
    };

    const fetchDoctorAppointments = async () => {
        if (!doctorId) return;
        setLoadingDoctorData(true);
        setDoctorError(null);
        try {
            const response = await fetch(`http://localhost:5000/doctor/appointments?doctor_id=${doctorId}`);
            const data = await response.json();
            if (response.ok) {
                setDoctorAppointments(data.appointments || []);
            } else {
                setDoctorError(data.error || 'Failed to fetch appointments');
                setDoctorAppointments([]);
            }
        } catch (error: any) {
            setDoctorError(error.message || 'An error occurred while fetching appointments');
            setDoctorAppointments([]);
        } finally {
            setLoadingDoctorData(false);
        }
    };

    const fetchDoctorMedicalRecords = async () => {
        if (!doctorId) return;
        setLoadingDoctorData(true);
        setDoctorError(null);
        try {
            const response = await fetch(`http://localhost:5000/doctor/medical_records?doctor_id=${doctorId}`);
            const data = await response.json();
            if (response.ok) {
                setDoctorMedicalRecords(data.medical_records || []);
            } else {
                setDoctorError(data.error || 'Failed to fetch medical records');
                setDoctorMedicalRecords([]);
            }
        } catch (error: any) {
             setDoctorError(error.message || 'An error occurred while fetching medical records');
             setDoctorMedicalRecords([]);
        } finally {
            setLoadingDoctorData(false);
        }
    };

    const fetchDoctorPatients = async () => {
        if (!doctorId) return;
        setLoadingDoctorData(true);
        setDoctorError(null);
        try {
            const response = await fetch(`http://localhost:5000/doctor/patients?doctor_id=${doctorId}`);
            const data = await response.json();
            if (response.ok) {
                setDoctorPatients(data.patients || []);
            } else {
                 setDoctorError(data.error || 'Failed to fetch patients');
                 setDoctorPatients([]);
            }
        } catch (error: any) {
             setDoctorError(error.message || 'An error occurred while fetching patients');
             setDoctorPatients([]);
        } finally {
            setLoadingDoctorData(false);
        }
    };

    const createDoctorAppointment = async () => {
        if (!doctorId) return;
        // Using form state instead of prompt
        const { patient_id, datetime_str, status } = newAppointmentFormData;

        if (!patient_id || !datetime_str) {
            setNewAppointmentMessage('Patient ID and Date/Time are required.');
            return;
        }

        setLoadingDoctorData(true);
        setDoctorError(null);
        setNewAppointmentMessage(null);

        try {
             const response = await fetch('http://localhost:5000/doctor/appointments', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    patient_id: parseInt(patient_id),
                    doctor_id: doctorId,
                    datetime_str: datetime_str,
                    status: status || 'Scheduled'
                })
            });
            const data = await response.json();
            if (response.ok) {
                 setNewAppointmentMessage(data.message || 'Appointment created successfully!');
                 // Clear form
                 setNewAppointmentFormData({ patient_id: '', datetime_str: '', status: 'Scheduled' });
                 fetchDoctorAppointments(); // Refresh appointments list
                 setShowNewAppointmentRow(false); // Hide the new appointment row
                 setNewAppointmentPatientName(null); // Clear the fetched patient name
            } else {
                 setNewAppointmentMessage(data.error || 'Failed to create appointment');
                 setDoctorError(data.error || 'Failed to create appointment');
            }
        } catch (error: any) {
            setNewAppointmentMessage(error.message || 'An error occurred while creating appointment');
            setDoctorError(error.message || 'An error occurred while creating appointment');
        } finally {
             setLoadingDoctorData(false);
        }
    };

    const updateDoctorAppointment = async () => {
        if (!doctorId || !editAppointmentFormData.appointment_id) return;

        // Using form state instead of prompt
        const { appointment_id, patient_id, datetime_str, status } = editAppointmentFormData;

        setLoadingDoctorData(true);
        setDoctorError(null);
        setEditAppointmentMessage(null);

         // Prepare update data, only include fields that are provided
        const updateData: any = { appointment_id: parseInt(appointment_id), doctor_id: doctorId };
        if (patient_id) updateData.patient_id = parseInt(patient_id);
        if (datetime_str) updateData.datetime_str = datetime_str;
        if (status) updateData.status = status;

         // Only proceed if there are changes other than the appointment_id and doctor_id
        if (Object.keys(updateData).length <= 2) {
             setEditAppointmentMessage('No changes to save.');
             setLoadingDoctorData(false);
             return;
        }

        try {
            const response = await fetch('http://localhost:5000/doctor/appointments', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(updateData)
            });
            const data = await response.json();
             if (response.ok) {
                 setEditAppointmentMessage(data.message || 'Appointment updated successfully!');
                 // Clear form
                 setEditAppointmentFormData({ appointment_id: '', patient_id: '', datetime_str: '', status: '' });
                 fetchDoctorAppointments(); // Refresh appointments list
                 setDoctorActiveMenuItem('appointments'); // Go back to appointments list
            } else {
                 setEditAppointmentMessage(data.error || 'Failed to update appointment');
                 setDoctorError(data.error || 'Failed to update appointment');
            }
        } catch (error: any) {
             setEditAppointmentMessage(error.message || 'An error occurred while updating appointment');
             setDoctorError(error.message || 'An error occurred while updating appointment');
        } finally {
             setLoadingDoctorData(false);
        }
    };

    const createMedicalRecord = async () => {
        if (!doctorId) return;
        // Using form state instead of prompt
        const { appointment_id, diagnosis, treatment, notes } = newMedicalRecordFormData;

        if (!appointment_id || !diagnosis || !treatment) {
             setNewMedicalRecordMessage('Appointment ID, Diagnosis, and Treatment are required.');
             return;
        }

        setLoadingDoctorData(true);
        setDoctorError(null);
        setNewMedicalRecordMessage(null);

        try {
            const response = await fetch('http://localhost:5000/doctor/medical_record', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    appointment_id: parseInt(appointment_id),
                    diagnosis,
                    treatment,
                    notes: notes || ""
                })
            });
            const data = await response.json();
            if (response.ok) {
                 setNewMedicalRecordMessage(data.message || 'Medical record created successfully!');
                 // Clear form
                 setNewMedicalRecordFormData({ appointment_id: '', diagnosis: '', treatment: '', notes: '' });
                 fetchDoctorMedicalRecords(); // Refresh medical records list
                 setShowNewMedicalRecordRow(false); // Hide the new medical record row
            } else {
                 setNewMedicalRecordMessage(data.error || 'Failed to create medical record');
                 setDoctorError(data.error || 'Failed to create medical record');
            }
        } catch (error: any) {
             setNewMedicalRecordMessage(error.message || 'An error occurred while creating medical record');
             setDoctorError(error.message || 'An error occurred while creating medical record');
        } finally {
             setLoadingDoctorData(false);
        }
    };

    const updateMedicalRecord = async () => {
        if (!doctorId || !editingMedicalRecordId || !editMedicalRecordFormData) return;

        setLoadingDoctorData(true);
        setDoctorError(null);
        setEditMedicalRecordMessage(null);

        // Prepare update data, only include fields that have changed or are required
        const updateData: any = { record_id: editingMedicalRecordId };
        // Note: AppointmentID, RecordDate are generally not editable.
        // We will only include Diagnosis, Treatment, and Notes if they are present in the form data.
        if (editMedicalRecordFormData.Diagnosis !== undefined) updateData.diagnosis = editMedicalRecordFormData.Diagnosis;
        if (editMedicalRecordFormData.Treatment !== undefined) updateData.treatment = editMedicalRecordFormData.Treatment;
        if (editMedicalRecordFormData.Notes !== undefined) updateData.notes = editMedicalRecordFormData.Notes;

        // Only proceed if there are changes other than the record_id
        if (Object.keys(updateData).length <= 1) {
            setEditMedicalRecordMessage('No changes to save.');
            setLoadingDoctorData(false);
            return;
        }

        try {
            const response = await fetch('http://localhost:5000/doctor/medical_record', { // Assuming a PUT endpoint for doctor to update medical record
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(updateData)
            });
            const data = await response.json();
            if (response.ok) {
                setEditMedicalRecordMessage(data.message || 'Medical record updated successfully!');
                setEditingMedicalRecordId(null); // Exit editing mode
                setEditMedicalRecordFormData({}); // Clear edit form data
                fetchDoctorMedicalRecords(); // Refresh the list
            } else {
                setEditMedicalRecordMessage(data.error || 'Failed to update medical record');
                setDoctorError(data.error || 'Failed to update medical record');
            }
        } catch (error: any) {
            setEditMedicalRecordMessage(error.message || 'An error occurred while updating medical record');
            setDoctorError(error.message || 'An error occurred while updating medical record');
        } finally {
            setLoadingDoctorData(false);
        }
    };

    const fetchDepartments = async () => {
        setLoadingDoctorData(true); // Using doctor loading state for now, could add separate state if needed
        setDoctorError(null);
        try {
            const response = await fetch('http://localhost:5000/admin/department'); // Assuming this endpoint exists and returns a list of departments
            const data = await response.json();
            if (response.ok && data.departments) {
                setDepartments(data.departments);
            } else {
                setDoctorError(data.error || 'Failed to fetch departments');
                setDepartments([]);
            }
        } catch (error: any) {
            setDoctorError(error.message || 'An error occurred while fetching departments');
            setDepartments([]);
        } finally {
            setLoadingDoctorData(false);
        }
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
        setDoctorActiveMenuItem(null);
        setPatientActiveMenuItem(null);
        setDoctorProfile(null);
        setDoctorAppointments([]);
        setDoctorMedicalRecords([]);
        setDoctorPatients([]);
        setEditProfileFormData({});
        setEditProfileMessage(null);
        setNewAppointmentFormData({ patient_id: '', datetime_str: '', status: 'Scheduled' });
        setNewAppointmentMessage(null);
        setEditAppointmentFormData({ appointment_id: '', patient_id: '', datetime_str: '', status: '' });
        setEditAppointmentMessage(null);
        setNewMedicalRecordFormData({ appointment_id: '', diagnosis: '', treatment: '', notes: '' });
        setNewMedicalRecordMessage(null);
        setPatientProfile(null);
        setPatientAppointments([]);
        setPatientMedicalRecords([]);
        setPatientDoctors([]);
         setEditPatientProfileFormData({});
         setEditPatientProfileMessage(null);
        setDepartments([]); // Clear departments on logout
    };

    const handleNewAppointmentFormChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
         setNewAppointmentFormData({
             ...newAppointmentFormData,
             [e.target.name]: e.target.value
         });
         // If the patient_id is changed, fetch the patient name
         if (e.target.name === 'patient_id') {
             const patientId = parseInt(e.target.value);
             if (!isNaN(patientId)) {
                 fetchPatientName(patientId);
             } else {
                 setNewAppointmentPatientName(null);
             }
         }
    };

    const handleEditAppointmentFormChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
         setEditAppointmentFormData({
             ...editAppointmentFormData,
             [e.target.name]: e.target.value
         });
    };

     const handleNewMedicalRecordFormChange = (e: React.ChangeEvent<HTMLInputElement>) => {
         setNewMedicalRecordFormData({
             ...newMedicalRecordFormData,
             [e.target.name]: e.target.value
         });
     };

    const handleEditPatientProfileFormChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
         setEditPatientProfileFormData({
             ...editPatientProfileFormData,
             [e.target.name]: e.target.value
         });
    };

    const handleEditMedicalRecordFormChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
        setEditMedicalRecordFormData({
            ...editMedicalRecordFormData,
            [e.target.name]: e.target.value
        });
    };

    const handleChangePassword = async () => {
        if (!oldPassword || !newPassword || !confirmNewPassword) {
            setChangePasswordMessage('All fields are required.');
            return;
        }
        if (newPassword !== confirmNewPassword) {
            setChangePasswordMessage('New password and confirm password do not match.');
            return;
        }

        const response = await fetch('http://localhost:5000/change_password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ old_password: oldPassword, new_password: newPassword })
        });
        const data = await response.json();
        if (response.ok) {
            setChangePasswordMessage('Password changed successfully!');
            setOldPassword('');
            setNewPassword('');
            setConfirmNewPassword('');
        } else {
            setChangePasswordMessage(data.error || 'Failed to change password');
        }
    };

    const renderDoctorContent = () => {
        if (loadingDoctorData) return <p>Loading...</p>;
        if (doctorError) return <p style={{ color: 'red' }}>Error: {doctorError}</p>;

        switch (doctorActiveMenuItem) {
            case 'profile':
                return (
                    <div>
                        <h3>Doctor Profile</h3>
                        {doctorProfile ? (
                            <div>
                                <p><strong>Name:</strong> {doctorProfile.Name}</p>
                                <p><strong>Specialization:</strong> {doctorProfile.Specialization}</p>
                                <p><strong>Department ID:</strong> {doctorProfile.DepartmentID}</p>
                            </div>
                        ) : (
                            <p>No profile data available.</p>
                        )}
                    </div>
                );
            case 'edit_doctor_profile':
                return (
                    <div>
                        <h3>Edit Doctor Profile</h3>
                        {doctorProfile ? (
                            <div>
                                <div style={{ marginBottom: '10px' }}>
                                    <label>Name:</label>
                                    <input
                                        type="text"
                                        name="Name"
                                        value={editProfileFormData.Name || ''}
                                        onChange={handleEditProfileFormChange}
                                        style={{ marginLeft: '10px' }}
                                    />
                                </div>
                                <div style={{ marginBottom: '10px' }}>
                                    <label>Department:</label>
                                    <select
                                        name="DepartmentID"
                                        value={editProfileFormData.DepartmentID || ''}
                                        onChange={handleEditProfileFormChange}
                                        style={{ marginLeft: '10px' }}
                                    >
                                        <option value="">Select Department</option>
                                        {departments.map(dept => (
                                            <option key={dept.DepartmentID} value={dept.DepartmentID}>
                                                {dept.Name}
                                            </option>
                                        ))}
                                    </select>
                                </div>
                                <button onClick={doctorUpdateProfile}>Save Changes</button>
                                {editProfileMessage && <p style={{ color: editProfileMessage.includes('Failed') ? 'red' : 'green' }}>{editProfileMessage}</p>}
                            </div>
                        ) : (
                            <p>Loading profile for editing...</p>
                        )}
                    </div>
                );
            case 'appointments':
                return (
                    <div>
                        <div style={{ marginBottom: '10px' }}>
                            <button onClick={fetchDoctorAppointments} style={{ padding: '8px', border: '1px solid #ccc', borderRadius: '5px', backgroundColor: '#f9f9f9', transition: 'background-color 0.3s ease', cursor: 'pointer', fontSize: '0.9em', marginRight: '10px' }}>Refresh Appointments</button>
                             <button onClick={() => { setShowNewAppointmentRow(true); setNewAppointmentFormData({...newAppointmentFormData, datetime_str: calculateDefaultAppointmentTime()}); }} style={{ padding: '8px', border: '1px solid #ccc', borderRadius: '5px', backgroundColor: '#f9f9f9', transition: 'background-color 0.3s ease', cursor: 'pointer', fontSize: '0.9em', marginRight: '10px' }}>Schedule New Appointment</button>
                        </div>
                        {doctorAppointments.length > 0 ? (
                            <table style={{ borderCollapse: 'collapse', width: '100%', backgroundColor: '#fff' }}>
                                <thead>
                                    <tr>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Appointment ID</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Patient ID</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Patient Name</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Date/Time</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Status</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {showNewAppointmentRow && (
                                        <tr style={{ backgroundColor: '#e9e9e9' }}>
                                            <td>New</td>
                                            <td>
                                                <input
                                                    type="number"
                                                    name="patient_id"
                                                    value={newAppointmentFormData.patient_id || ''}
                                                    onChange={handleNewAppointmentFormChange}
                                                    style={{ width: '100%', padding: '5px' }}
                                                />
                                            </td>
                                            <td>
                                                {newAppointmentPatientName || 'Enter Patient ID'}
                                            </td>
                                            <td>
                                                <input
                                                    type="text"
                                                    name="datetime_str"
                                                    placeholder="YYYY-MM-DD HH:MM:SS"
                                                    value={newAppointmentFormData.datetime_str || ''}
                                                    onChange={handleNewAppointmentFormChange}
                                                    style={{ width: '100%', padding: '5px' }}
                                                />
                                            </td>
                                            <td>
                                                 <select
                                                     name="status"
                                                     value={newAppointmentFormData.status}
                                                     onChange={handleNewAppointmentFormChange}
                                                      style={{ width: '100%', padding: '5px' }}
                                                 >
                                                     <option value="Scheduled">Scheduled</option>
                                                     <option value="Completed">Completed</option>
                                                     <option value="Cancelled">Cancelled</option>
                                                 </select>
                                            </td>
                                        </tr>
                                    )}
                                    {doctorAppointments.map(appointment => (
                                        <tr key={appointment.AppointmentID}>
                                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{appointment.AppointmentID}</td>
                                            {editingAppointmentId === appointment.AppointmentID ? (
                                                <>
                                                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                                                         <input
                                                            type="number"
                                                            name="patient_id"
                                                            value={editAppointmentFormData.patient_id || ''}
                                                            onChange={handleEditAppointmentFormChange}
                                                            style={{ width: '100%', padding: '5px' }}
                                                        />
                                                    </td>
                                                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>{/* Patient Name placeholder */}
                                                         {/* We don't dynamically fetch name here for simplicity */}
                                                         {appointment.PatientName || 'N/A'}
                                                     </td>
                                                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                                                        <input
                                                            type="text"
                                                            name="datetime_str"
                                                            placeholder="YYYY-MM-DD HH:MM:SS"
                                                            value={editAppointmentFormData.datetime_str || ''}
                                                            onChange={handleEditAppointmentFormChange}
                                                            style={{ width: '100%', padding: '5px' }}
                                                        />
                                                    </td>
                                                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                                                        <select
                                                             name="status"
                                                             value={editAppointmentFormData.status || ''}
                                                             onChange={handleEditAppointmentFormChange}
                                                             style={{ width: '100%', padding: '5px' }}
                                                        >
                                                             <option value="Scheduled">Scheduled</option>
                                                             <option value="Completed">Completed</option>
                                                             <option value="Cancelled">Cancelled</option>
                                                        </select>
                                                    </td>
                                                     <td style={{ border: '1px solid #ddd', padding: '8px' }}> {/* Action buttons */}
                                                         <button onClick={() => updateDoctorAppointment()} style={{ padding: '8px', border: '1px solid #ccc', borderRadius: '5px', backgroundColor: '#f9f9f9', transition: 'background-color 0.3s ease', cursor: 'pointer', fontSize: '0.9em', marginRight: '5px' }}>Confirm</button>
                                                         <button onClick={() => setEditingAppointmentId(null)} style={{ padding: '8px', border: '1px solid #ccc', borderRadius: '5px', backgroundColor: '#f9f9f9', transition: 'background-color 0.3s ease', cursor: 'pointer', fontSize: '0.9em' }}>Cancel</button>
                                                     </td>
                                                </>
                                            ) : (
                                                <>
                                                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>{appointment.PatientID}</td>
                                                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>{appointment.PatientName || 'N/A'}</td> {/* Display patient name */}
                                                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>{appointment.DateTime}</td>
                                                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>{appointment.Status}</td>
                                                    <td style={{ border: '1px solid #ddd', padding: '8px' }}> {/* Action button */}
                                                        <button onClick={() => { setEditingAppointmentId(appointment.AppointmentID); setEditAppointmentFormData({ appointment_id: String(appointment.AppointmentID), patient_id: String(appointment.PatientID), datetime_str: appointment.DateTime, status: appointment.Status }); }} style={{ padding: '8px', border: '1px solid #ccc', borderRadius: '5px', backgroundColor: '#f9f9f9', transition: 'background-color 0.3s ease', cursor: 'pointer', fontSize: '0.9em' }}>Edit</button>
                                                    </td>
                                                </>
                                            )}
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        ) : (
                            <p>No appointments found.</p>
                        )}
                        {showNewAppointmentRow && (
                            <div style={{ marginBottom: '10px', textAlign: 'center' }}>
                                <button onClick={createDoctorAppointment} style={{ padding: '8px', border: '1px solid #ccc', borderRadius: '5px', backgroundColor: '#f9f9f9', transition: 'background-color 0.3s ease', cursor: 'pointer', fontSize: '0.9em', marginRight: '10px' }}>Confirm</button>
                                <button onClick={() => setShowNewAppointmentRow(false)} style={{ padding: '8px', border: '1px solid #ccc', borderRadius: '5px', backgroundColor: '#f9f9f9', transition: 'background-color 0.3s ease', cursor: 'pointer', fontSize: '0.9em' }}>Cancel</button>
                            </div>
                        )}
                    </div>
                );
             case 'schedule_appointment':
                 return (
                     <div>
                         <h3>Schedule New Appointment</h3>
                          <div style={{ marginBottom: '10px' }}>
                              <label>Patient ID:</label>
                              <input
                                   type="number"
                                   name="patient_id"
                                   value={newAppointmentFormData.patient_id}
                                   onChange={handleNewAppointmentFormChange}
                                   style={{ marginLeft: '10px' }}
                              />
                          </div>
                          <div style={{ marginBottom: '10px' }}>
                              <label>Date and Time:</label>
                              <input
                                   type="text"
                                   name="datetime_str"
                                   placeholder="YYYY-MM-DD HH:MM:SS"
                                   value={newAppointmentFormData.datetime_str}
                                   onChange={handleNewAppointmentFormChange}
                                   style={{ marginLeft: '10px' }}
                              />
                          </div>
                           <div style={{ marginBottom: '10px' }}>
                              <label>Status:</label>
                              <input
                                   type="text"
                                   name="status"
                                   value={newAppointmentFormData.status}
                                   onChange={handleNewAppointmentFormChange}
                                   style={{ marginLeft: '10px' }}
                              />
                          </div>
                          <button onClick={createDoctorAppointment}>Create Appointment</button>
                           {newAppointmentMessage && <p style={{ color: newAppointmentMessage.includes('Failed') ? 'red' : 'green' }}>{newAppointmentMessage}</p>}
                     </div>
                 );
             case 'edit_appointment':
                  return (
                      <div>
                          <h3>Edit Existing Appointment</h3>
                           <div style={{ marginBottom: '10px' }}>
                               <label>Appointment ID:</label>
                               <input
                                   type="number"
                                   name="appointment_id"
                                   value={editAppointmentFormData.appointment_id}
                                   onChange={handleEditAppointmentFormChange}
                                   style={{ marginLeft: '10px' }}
                               />
                           </div>
                           <div style={{ marginBottom: '10px' }}>
                               <label>New Patient ID (Optional):</label>
                               <input
                                   type="number"
                                   name="patient_id"
                                   value={editAppointmentFormData.patient_id}
                                   onChange={handleEditAppointmentFormChange}
                                   style={{ marginLeft: '10px' }}
                               />
                           </div>
                           <div style={{ marginBottom: '10px' }}>
                               <label>New Date and Time (Optional):</label>
                               <input
                                   type="text"
                                   name="datetime_str"
                                   placeholder="YYYY-MM-DD HH:MM:SS"
                                   value={editAppointmentFormData.datetime_str}
                                   onChange={handleEditAppointmentFormChange}
                                   style={{ marginLeft: '10px' }}
                               />
                           </div>
                           <div style={{ marginBottom: '10px' }}>
                               <label>New Status (Optional):</label>
                               <input
                                   type="text"
                                   name="status"
                                   value={editAppointmentFormData.status}
                                   onChange={handleEditAppointmentFormChange}
                                   style={{ marginLeft: '10px' }}
                               />
                           </div>
                           <button onClick={updateDoctorAppointment}>Update Appointment</button>
                           {editAppointmentMessage && <p style={{ color: editAppointmentMessage.includes('Failed') ? 'red' : 'green' }}>{editAppointmentMessage}</p>}
                      </div>
                  );
            case 'medical_records':
                return (
                    <div>
                        <h3>Medical Records</h3>
                        <div style={{ marginBottom: '10px' }}>
                            <button onClick={fetchDoctorMedicalRecords} style={{ padding: '8px', border: '1px solid #ccc', borderRadius: '5px', backgroundColor: '#f9f9f9', transition: 'background-color 0.3s ease', cursor: 'pointer', fontSize: '0.9em', marginRight: '10px' }}>Refresh Medical Records</button>
                             <button onClick={() => setShowNewMedicalRecordRow(true)} style={{ padding: '8px', border: '1px solid #ccc', borderRadius: '5px', backgroundColor: '#f9f9f9', transition: 'background-color 0.3s ease', cursor: 'pointer', fontSize: '0.9em' }}>Create New Medical Record</button>
                        </div>
                        {doctorMedicalRecords.length > 0 ? (
                            <table style={{ borderCollapse: 'collapse', width: '100%', backgroundColor: '#fff' }}>
                                <thead>
                                    <tr>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Record ID</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Appointment ID</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Diagnosis</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Treatment</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Notes</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Date</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {showNewMedicalRecordRow && (
                                        <tr style={{ backgroundColor: '#e9e9e9' }}>
                                            <td>New</td>
                                            <td>
                                                 <input
                                                    type="number"
                                                    name="appointment_id"
                                                    value={newMedicalRecordFormData.appointment_id}
                                                    onChange={handleNewMedicalRecordFormChange}
                                                    style={{ width: '100%', padding: '5px' }}
                                                 />
                                            </td>
                                            <td>
                                                <input
                                                    type="text"
                                                    name="diagnosis"
                                                    value={newMedicalRecordFormData.diagnosis}
                                                    onChange={handleNewMedicalRecordFormChange}
                                                    style={{ width: '100%', padding: '5px' }}
                                                />
                                            </td>
                                            <td>
                                                <input
                                                    type="text"
                                                    name="treatment"
                                                    value={newMedicalRecordFormData.treatment}
                                                    onChange={handleNewMedicalRecordFormChange}
                                                    style={{ width: '100%', padding: '5px' }}
                                                />
                                            </td>
                                             <td>
                                                <input
                                                    type="text"
                                                    name="notes"
                                                    value={newMedicalRecordFormData.notes}
                                                    onChange={handleNewMedicalRecordFormChange}
                                                    style={{ width: '100%', padding: '5px' }}
                                                 />
                                            </td>
                                            <td></td>
                                        </tr>
                                    )}
                                    {doctorMedicalRecords.map(record => (
                                        <tr key={record.RecordID}>
                                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{record.RecordID}</td>
                                            {editingMedicalRecordId === record.RecordID ? (
                                                <>
                                                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>{record.AppointmentID}</td> {/* Keep AppointmentID as is */}
                                                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                                                        <input
                                                            type="text"
                                                            name="diagnosis"
                                                            value={editMedicalRecordFormData.Diagnosis || ''}
                                                            onChange={handleEditMedicalRecordFormChange}
                                                            style={{ width: '100%', padding: '5px' }}
                                                        />
                                                    </td>
                                                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                                                        <input
                                                            type="text"
                                                            name="treatment"
                                                            value={editMedicalRecordFormData.Treatment || ''}
                                                            onChange={handleEditMedicalRecordFormChange}
                                                            style={{ width: '100%', padding: '5px' }}
                                                        />
                                                    </td>
                                                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                                                         <textarea
                                                            name="notes"
                                                            value={editMedicalRecordFormData.Notes || ''}
                                                            onChange={handleEditMedicalRecordFormChange as any}
                                                            style={{ width: '100%', padding: '5px' }}
                                                            rows={3}
                                                         />
                                                    </td>
                                                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>{record.RecordDate}</td> {/* Keep RecordDate as is */}
                                                     <td style={{ border: '1px solid #ddd', padding: '8px' }}> {/* Action buttons */}
                                                         <button onClick={() => updateMedicalRecord()} style={{ padding: '8px', border: '1px solid #ccc', borderRadius: '5px', backgroundColor: '#f9f9f9', transition: 'background-color 0.3s ease', cursor: 'pointer', fontSize: '0.9em', marginRight: '5px' }}>Confirm</button>
                                                         <button onClick={() => setEditingMedicalRecordId(null)} style={{ padding: '8px', border: '1px solid #ccc', borderRadius: '5px', backgroundColor: '#f9f9f9', transition: 'background-color 0.3s ease', cursor: 'pointer', fontSize: '0.9em' }}>Cancel</button>
                                                     </td>
                                                </>
                                            ) : (
                                                <>
                                                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>{record.RecordID}</td>
                                                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>{record.AppointmentID}</td>
                                                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>{record.Diagnosis}</td>
                                                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>{record.Treatment}</td>
                                                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>{record.Notes}</td>
                                                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>{record.RecordDate}</td>
                                                    <td style={{ border: '1px solid #ddd', padding: '8px' }}> {/* Action button */}
                                                        <button onClick={() => { setEditingMedicalRecordId(record.RecordID); setEditMedicalRecordFormData(record); }} style={{ padding: '8px', border: '1px solid #ccc', borderRadius: '5px', backgroundColor: '#f9f9f9', transition: 'background-color 0.3s ease', cursor: 'pointer', fontSize: '0.9em' }}>Edit</button>
                                                    </td>
                                                </>
                                            )}
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        ) : (
                            <p>No medical records found.</p>
                        )}
                        {showNewMedicalRecordRow && (
                            <div style={{ marginBottom: '10px', textAlign: 'center' }}>
                                <button onClick={createMedicalRecord} style={{ padding: '8px', border: '1px solid #ccc', borderRadius: '5px', backgroundColor: '#f9f9f9', transition: 'background-color 0.3s ease', cursor: 'pointer', fontSize: '0.9em', marginRight: '10px' }}>Confirm</button>
                                <button onClick={() => setShowNewMedicalRecordRow(false)} style={{ padding: '8px', border: '1px solid #ccc', borderRadius: '5px', backgroundColor: '#f9f9f9', transition: 'background-color 0.3s ease', cursor: 'pointer', fontSize: '0.9em' }}>Cancel</button>
                            </div>
                        )}
                    </div>
                );
            case 'create_medical_record':
                 return (
                     <div>
                         <h3>Create Medical Record</h3>
                          <div style={{ marginBottom: '10px' }}>
                               <label>Appointment ID:</label>
                               <input
                                   type="number"
                                   name="appointment_id"
                                   value={newMedicalRecordFormData.appointment_id}
                                   onChange={handleNewMedicalRecordFormChange}
                                   style={{ marginLeft: '10px' }}
                               />
                           </div>
                           <div style={{ marginBottom: '10px' }}>
                               <label>Diagnosis:</label>
                               <input
                                   type="text"
                                   name="diagnosis"
                                   value={newMedicalRecordFormData.diagnosis}
                                   onChange={handleNewMedicalRecordFormChange}
                                   style={{ marginLeft: '10px' }}
                               />
                           </div>
                           <div style={{ marginBottom: '10px' }}>
                               <label>Treatment Plan:</label>
                               <input
                                   type="text"
                                   name="treatment"
                                   value={newMedicalRecordFormData.treatment}
                                   onChange={handleNewMedicalRecordFormChange}
                                   style={{ marginLeft: '10px' }}
                               />
                           </div>
                            <div style={{ marginBottom: '10px' }}>
                               <label>Notes (Optional):</label>
                               <input
                                   type="text"
                                   name="notes"
                                   value={newMedicalRecordFormData.notes}
                                   onChange={handleNewMedicalRecordFormChange}
                                   style={{ marginLeft: '10px' }}
                               />
                           </div>
                          <button onClick={createMedicalRecord}>Create Medical Record</button>
                           {newMedicalRecordMessage && <p style={{ color: newMedicalRecordMessage.includes('Failed') ? 'red' : 'green' }}>{newMedicalRecordMessage}</p>}
                     </div>
                 );
            case 'patients':
                return (
                    <div>
                        <h3>My Patients</h3>
                         {doctorPatients.length > 0 ? (
                            <table style={{ borderCollapse: 'collapse', width: '100%', backgroundColor: '#fff' }}>
                                <thead>
                                    <tr>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Patient ID</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Name</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>DOB</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Gender</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px' }}>Contact</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {doctorPatients.map(patient => (
                                        <tr key={patient.PatientID}>
                                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{patient.PatientID}</td>
                                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{patient.Name}</td>
                                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{patient.DOB ? new Date(patient.DOB).toLocaleDateString('en-GB') : 'N/A'}</td>
                                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{patient.Gender}</td>
                                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{patient.Contact}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        ) : (
                            <p>No patients found.</p>
                        )}
                         <button onClick={fetchDoctorPatients} style={{ padding: '8px', border: '1px solid #ccc', borderRadius: '5px', backgroundColor: '#f9f9f9', transition: 'background-color 0.3s ease', cursor: 'pointer', fontSize: '0.9em' }}>Refresh Patients</button>
                    </div>
                );
             default:
                 return <div>Select a menu item</div>;
         }
    };

    const renderPatientContent = () => {
        if (loadingPatientData) return <p>Loading...</p>;
        if (patientError) return <p style={{ color: 'red' }}>Error: {patientError}</p>;

        switch (patientActiveMenuItem) {
             case 'profile':
                 return (
                     <div>
                         <h3>Patient Profile</h3>
                         {patientProfile ? (
                             <div>
                                 <p><strong>Name:</strong> {patientProfile.Name}</p>
                                 <p><strong>Date of Birth:</strong> {
                                     patientProfile.DOB ? new Date(patientProfile.DOB).toLocaleDateString('en-GB') : 'N/A'
                                 }</p>
                                 <p><strong>Gender:</strong> {patientProfile.Gender}</p>
                                 <p><strong>Contact:</strong> {patientProfile.Contact}</p>
                             </div>
                         ) : (
                             <p>No profile data available.</p>
                         )}
                     </div>
                 );
            case 'edit_patient_profile':
                 return (
                     <div>
                         <h3>Edit Patient Profile</h3>
                          {patientProfile ? (
                              <div>
                                  <div style={{ marginBottom: '10px' }}>
                                      <label htmlFor="patientName">Name:</label>
                                      <input
                                          id="patientName"
                                          type="text"
                                          name="Name"
                                          value={editPatientProfileFormData.Name || ''}
                                          onChange={handleEditPatientProfileFormChange}
                                          style={{ marginLeft: '10px' }}
                                      />
                                  </div>
                                   <div style={{ marginBottom: '10px' }}>
                                      <label htmlFor="patientDOB">Date of Birth:</label>
                                      <input
                                          id="patientDOB"
                                          type="text"
                                          name="DOB"
                                          placeholder="DD/MM/YYYY"
                                          value={editPatientProfileFormData.DOB || ''}
                                          onChange={handleEditPatientProfileFormChange}
                                          style={{ marginLeft: '10px' }}
                                       />
                                  </div>
                                   <div style={{ marginBottom: '10px' }}>
                                      <label htmlFor="patientGender">Gender:</label>
                                       <select
                                           id="patientGender"
                                           name="Gender"
                                           value={editPatientProfileFormData.Gender || ''}
                                           onChange={handleEditPatientProfileFormChange}
                                            style={{ marginLeft: '10px' }}
                                       >
                                           <option value="">Select Gender</option>
                                           <option value="Male">Male</option>
                                           <option value="Female">Female</option>
                                           <option value="Other">Other</option>
                                       </select>
                                  </div>
                                   <div style={{ marginBottom: '10px' }}>
                                      <label htmlFor="patientContact">Contact:</label>
                                      <input
                                          id="patientContact"
                                          type="text"
                                          name="Contact"
                                          value={editPatientProfileFormData.Contact || ''}
                                          onChange={handleEditPatientProfileFormChange}
                                          style={{ marginLeft: '10px' }}
                                      />
                                   </div>
                                   <button onClick={patientUpdateProfile}>Save Changes</button>
                                    {editPatientProfileMessage && <p style={{ color: editPatientProfileMessage.includes('Failed') ? 'red' : 'green' }}>{editPatientProfileMessage}</p>}
                               </div>
                            ) : (
                                <p>Loading profile for editing...</p>
                            )}
                     </div>
                 );
             case 'appointments':
                 return (
                     <div>
                         <h3>Appointments</h3>
                         {patientAppointments.length > 0 ? (
                             <table style={{ borderCollapse: 'collapse', width: '100%' }}>
                                 <thead>
                                     <tr>
                                         <th style={{ border: '1px solid #ddd', padding: '8px' }}>Appointment ID</th>
                                         <th style={{ border: '1px solid #ddd', padding: '8px' }}>Doctor ID</th>
                                         <th style={{ border: '1px solid #ddd', padding: '8px' }}>Date/Time</th>
                                         <th style={{ border: '1px solid #ddd', padding: '8px' }}>Status</th>
                                     </tr>
                                 </thead>
                                 <tbody>
                                     {patientAppointments.map(appointment => (
                                         <tr key={appointment.AppointmentID}>
                                             <td style={{ border: '1px solid #ddd', padding: '8px' }}>{appointment.AppointmentID}</td>
                                             <td style={{ border: '1px solid #ddd', padding: '8px' }}>{appointment.DoctorID}</td>
                                             <td style={{ border: '1px solid #ddd', padding: '8px' }}>{appointment.DateTime}</td>
                                             <td style={{ border: '1px solid #ddd', padding: '8px' }}>{appointment.Status}</td>
                                         </tr>
                                     ))}
                                 </tbody>
                             </table>
                         ) : (
                             <p>No appointments found.</p>
                         )}
                          <button onClick={() => { if (patientId) fetchAppointments(patientId); }} style={{ padding: '8px', border: '1px solid #ccc', borderRadius: '5px', backgroundColor: '#f9f9f9', transition: 'background-color 0.3s ease', cursor: 'pointer', fontSize: '0.9em' }}>Refresh Appointments</button>
                     </div>
                 );
             case 'medical_records':
                 return (
                     <div>
                         <h3>Medical Records</h3>
                         {patientMedicalRecords.length > 0 ? (
                             <table style={{ borderCollapse: 'collapse', width: '100%' }}>
                                 <thead>
                                     <tr>
                                         <th style={{ border: '1px solid #ddd', padding: '8px' }}>Record ID</th>
                                         <th style={{ border: '1px solid #ddd', padding: '8px' }}>Appointment ID</th>
                                         <th style={{ border: '1px solid #ddd', padding: '8px' }}>Diagnosis</th>
                                         <th style={{ border: '1px solid #ddd', padding: '8px' }}>Treatment</th>
                                         <th style={{ border: '1px solid #ddd', padding: '8px' }}>Notes</th>
                                         <th style={{ border: '1px solid #ddd', padding: '8px' }}>Date</th>
                                     </tr>
                                 </thead>
                                 <tbody>
                                     {patientMedicalRecords.map(record => (
                                         <tr key={record.RecordID}>
                                             <td style={{ border: '1px solid #ddd', padding: '8px' }}>{record.RecordID}</td>
                                             <td style={{ border: '1px solid #ddd', padding: '8px' }}>{record.AppointmentID}</td>
                                             <td style={{ border: '1px solid #ddd', padding: '8px' }}>{record.Diagnosis}</td>
                                             <td style={{ border: '1px solid #ddd', padding: '8px' }}>{record.Treatment}</td>
                                             <td style={{ border: '1px solid #ddd', padding: '8px' }}>{record.Notes}</td>
                                             <td style={{ border: '1px solid #ddd', padding: '8px' }}>{record.RecordDate}</td>
                                         </tr>
                                     ))}
                                 </tbody>
                             </table>
                         ) : (
                             <p>No medical records found.</p>
                         )}
                          <button onClick={() => { if (patientId) fetchMedicalRecords(patientId); }} style={{ padding: '8px', border: '1px solid #ccc', borderRadius: '5px', backgroundColor: '#f9f9f9', transition: 'background-color 0.3s ease', cursor: 'pointer', fontSize: '0.9em' }}>Refresh Medical Records</button>
                     </div>
                 );
             case 'doctors':
                 return (
                     <div>
                         <h3>My Doctors</h3>
                          {patientDoctors.length > 0 ? (
                             <table style={{ borderCollapse: 'collapse', width: '100%' }}>
                                 <thead>
                                     <tr>
                                         <th style={{ border: '1px solid #ddd', padding: '8px' }}>Doctor ID</th>
                                         <th style={{ border: '1px solid #ddd', padding: '8px' }}>Name</th>
                                         <th style={{ border: '1px solid #ddd', padding: '8px' }}>Specialization</th>
                                     </tr>
                                 </thead>
                                 <tbody>
                                     {patientDoctors.map(doctor => (
                                         <tr key={doctor.DoctorID}>
                                             <td style={{ border: '1px solid #ddd', padding: '8px' }}>{doctor.DoctorID}</td>
                                             <td style={{ border: '1px solid #ddd', padding: '8px' }}>{doctor.Name}</td>
                                             <td style={{ border: '1px solid #ddd', padding: '8px' }}>{doctor.Specialization}</td>
                                         </tr>
                                     ))}
                                 </tbody>
                             </table>
                         ) : (
                             <p>No doctors found.</p>
                         )}
                          <button onClick={() => { if (patientId) fetchPatientDoctors(patientId); }} style={{ padding: '8px', border: '1px solid #ccc', borderRadius: '5px', backgroundColor: '#f9f9f9', transition: 'background-color 0.3s ease', cursor: 'pointer', fontSize: '0.9em' }}>Refresh Doctors</button>
                     </div>
                 );
             default:
                 return <div>Select a menu item</div>;
        }
    };

    const displayFullName = userInfo?.Role === 'Doctor' && doctorProfile?.Name ? doctorProfile.Name : userInfo?.Username;
    const displayPatientFullName = userInfo?.Role === 'Patient' && patientProfile?.Name ? patientProfile.Name : userInfo?.Username;

    return (
        <div style={{
            padding: '20px',
            backgroundColor: '#f0f0f0',
            minHeight: '100vh'
        }}>
            {view === 'login' && (
                <div style={{
                    backgroundColor: 'rgba(255, 255, 255, 0.8)',
                    padding: '50px',
                    borderRadius: '10px',
                    textAlign: 'center',
                    width: '400px',
                    margin: 'auto',
                    backgroundImage: `url('background_loginpage.jpg')`,
                    backgroundSize: 'cover'
                }}>
                    <h2>Login</h2>
                    <div style={{ marginBottom: '20px' }}>
                        <input
                            type="text"
                            placeholder="Username"
                            value={username}
                            onChange={e => setUsername(e.target.value)}
                            style={{ padding: '10px', width: 'calc(100% - 22px)' }}
                        />
                    </div>
                    <div style={{ marginBottom: '20px' }}>
                        <input
                            type="password"
                            placeholder="Password"
                            value={password}
                            onChange={e => setPassword(e.target.value)}
                            style={{ padding: '10px', width: 'calc(100% - 22px)' }}
                        />
                    </div>
                    <button onClick={handleLogin} style={{ padding: '10px 40px' }}>Login</button>
                    {message && <p style={{ color: 'red' }}>{message}</p>}
                </div>
            )}

            {view === 'menu' && userInfo && (
                <div style={{
                    display: 'flex',
                    backgroundColor: '#f0f0f0',
                    borderRadius: '10px',
                    boxShadow: '7px 7px 15px #bebebe, -7px -7px 15px #ffffff',
                    minHeight: 'calc(100vh - 40px)',
                    fontFamily: 'Arial, sans-serif',
                    padding: '20px'
                }}>
                    {/* Sidebar */}
                    {userInfo.Role === 'Doctor' && (
                         <div style={{
                            width: '225px',
                            borderRight: '1px solid #ccc',
                            paddingRight: '20px',
                            flexShrink: 0,
                            display: 'flex',
                            flexDirection: 'column',
                            justifyContent: 'flex-start',
                            overflowY: 'auto',
                            paddingTop: '20px'
                        }}>
                             {/* Doctor Logo and Menu */}
                              <div style={{flexGrow: 1}}> {/* Wrap logo and menu in a div to push logout down */}
                                  <img src="doctor_logo.png" alt="Doctor Menu" style={{ maxWidth: '100%', height: 'auto', marginBottom: '20px' }} />
                                   <ul style={{
                                      listStyle: 'none',
                                      padding: 0,
                                       marginBottom: '20px' // Add margin below the list
                                  }}>
                                     <li style={{
                                         marginBottom: '10px',
                                         cursor: 'pointer',
                                         fontWeight: doctorActiveMenuItem === 'profile' ? 'bold' : 'normal',
                                         padding: '8px',
                                         border: '1px solid #ccc',
                                         borderRadius: '5px',
                                         backgroundColor: doctorActiveMenuItem === 'profile' ? '#e0e0e0' : '#f9f9f9',
                                         transition: 'background-color 0.3s ease'
                                     }} onClick={() => { setDoctorActiveMenuItem('profile'); if (doctorId) fetchDoctorProfile(doctorId); }}>Profile</li>
                                      <li style={{
                                          marginBottom: '10px',
                                          cursor: 'pointer',
                                          fontWeight: doctorActiveMenuItem === 'edit_doctor_profile' ? 'bold' : 'normal',
                                          padding: '8px',
                                          border: '1px solid #ccc',
                                          borderRadius: '5px',
                                          backgroundColor: doctorActiveMenuItem === 'edit_doctor_profile' ? '#e0e0e0' : '#f9f9f9',
                                          transition: 'background-color 0.3s ease'
                                      }} onClick={() => setDoctorActiveMenuItem('edit_doctor_profile')}>Edit Profile</li>
                                     <li style={{
                                          marginBottom: '10px',
                                          cursor: 'pointer',
                                          fontWeight: doctorActiveMenuItem === 'appointments' ? 'bold' : 'normal',
                                          padding: '8px',
                                          border: '1px solid #ccc',
                                          borderRadius: '5px',
                                          backgroundColor: doctorActiveMenuItem === 'appointments' ? '#e0e0e0' : '#f9f9f9',
                                          transition: 'background-color 0.3s ease'
                                      }} onClick={() => { setDoctorActiveMenuItem('appointments'); fetchDoctorAppointments(); }}>Appointments</li>
                                    <li style={{
                                         marginBottom: '10px',
                                         cursor: 'pointer',
                                         fontWeight: doctorActiveMenuItem === 'medical_records' ? 'bold' : 'normal',
                                         padding: '8px',
                                         border: '1px solid #ccc',
                                         borderRadius: '5px',
                                         backgroundColor: doctorActiveMenuItem === 'medical_records' ? '#e0e0e0' : '#f9f9f9',
                                         transition: 'background-color 0.3s ease'
                                      }} onClick={() => { setDoctorActiveMenuItem('medical_records'); fetchDoctorMedicalRecords(); }}>Medical Records</li>
                                 </ul>
                              </div>

                             {/* Logout Button and Username */}
                             <div style={{
                                  display: 'flex',
                                  alignItems: 'center',
                                  marginTop: '20px', // Add space above logout section
                                  paddingTop: '20px', // Add space above the top border
                                  borderTop: '1px solid #eee', // Add a border at the top
                                  justifyContent: 'flex-start' // Align to the start
                              }}>
                                   <span style={{ marginRight: '10px' }}>Logged in as: <strong>{userInfo.Username}</strong></span>
                                  <button onClick={logout} style={{
                                       padding: '8px', // Match menu item padding
                                       border: '1px solid #ccc', // Match menu item border
                                       borderRadius: '5px', // Match menu item border radius
                                       backgroundColor: '#f9f9f9', // Match menu item background
                                       transition: 'background-color 0.3s ease', // Match menu item transition
                                       cursor: 'pointer', // Add pointer cursor
                                       fontSize: '0.9em' // Match menu item font size
                                   }}>Logout</button>
                               </div>
                          </div>
                      )}

                    {/* Sidebar for Patient */}
                     {userInfo.Role === 'Patient' && (
                         <div style={{
                             width: '225px',
                             borderRight: '1px solid #ccc',
                             paddingRight: '20px',
                             flexShrink: 0,
                             display: 'flex',
                             flexDirection: 'column',
                             justifyContent: 'flex-start',
                             overflowY: 'auto',
                             paddingTop: '20px'
                         }}>
                             {/* Patient Logo and Menu */}
                              <div style={{flexGrow: 1}}> {/* Wrap logo and menu in a div to push logout down */}
                                  <img src="patient_logo.png" alt="Patient Menu" style={{ maxWidth: '100%', height: 'auto', marginBottom: '20px' }} />
                                   <ul style={{
                                       listStyle: 'none',
                                       padding: 0,
                                        marginBottom: '20px' // Add margin below the list
                                   }}>
                                      <li style={{
                                          marginBottom: '10px',
                                          cursor: 'pointer',
                                          fontWeight: patientActiveMenuItem === 'profile' ? 'bold' : 'normal',
                                          padding: '8px',
                                          border: '1px solid #ccc',
                                          borderRadius: '5px',
                                          backgroundColor: patientActiveMenuItem === 'profile' ? '#e0e0e0' : '#f9f9f9',
                                          transition: 'background-color 0.3s ease'
                                      }} onClick={() => { setPatientActiveMenuItem('profile'); if (patientId) fetchPatientProfile(patientId); }}>Profile</li>
                                       <li style={{
                                           marginBottom: '10px',
                                           cursor: 'pointer',
                                           fontWeight: patientActiveMenuItem === 'edit_patient_profile' ? 'bold' : 'normal',
                                           padding: '8px',
                                           border: '1px solid #ccc',
                                           borderRadius: '5px',
                                           backgroundColor: patientActiveMenuItem === 'edit_patient_profile' ? '#e0e0e0' : '#f9f9f9',
                                           transition: 'background-color 0.3s ease'
                                       }} onClick={() => setPatientActiveMenuItem('edit_patient_profile')}>Edit Profile</li>
                                      <li style={{
                                           marginBottom: '10px',
                                           cursor: 'pointer',
                                           fontWeight: patientActiveMenuItem === 'appointments' ? 'bold' : 'normal',
                                           padding: '8px',
                                           border: '1px solid #ccc',
                                           borderRadius: '5px',
                                           backgroundColor: patientActiveMenuItem === 'appointments' ? '#e0e0e0' : '#f9f9f9',
                                           transition: 'background-color 0.3s ease'
                                      }} onClick={() => { setPatientActiveMenuItem('appointments'); if (patientId) fetchAppointments(patientId); }}>Appointments</li>
                                      <li style={{
                                           marginBottom: '10px',
                                           cursor: 'pointer',
                                           fontWeight: patientActiveMenuItem === 'medical_records' ? 'bold' : 'normal',
                                           padding: '8px',
                                           border: '1px solid #ccc',
                                           borderRadius: '5px',
                                           backgroundColor: patientActiveMenuItem === 'medical_records' ? '#e0e0e0' : '#f9f9f9',
                                           transition: 'background-color 0.3s ease'
                                      }} onClick={() => { setPatientActiveMenuItem('medical_records'); if (patientId) fetchMedicalRecords(patientId); }}>Medical Records</li>
                                      <li style={{
                                           marginBottom: '10px',
                                           cursor: 'pointer',
                                           fontWeight: patientActiveMenuItem === 'doctors' ? 'bold' : 'normal',
                                           padding: '8px',
                                           border: '1px solid #ccc',
                                           borderRadius: '5px',
                                           backgroundColor: patientActiveMenuItem === 'doctors' ? '#e0e0e0' : '#f9f9f9',
                                           transition: 'background-color 0.3s ease'
                                      }} onClick={() => { setPatientActiveMenuItem('doctors'); if (patientId) fetchPatientDoctors(patientId); }}>My Doctors</li>
                                  </ul>
                               </div>

                             {/* Logout Button and Username (Patient) */}
                             <div style={{
                                  display: 'flex',
                                  alignItems: 'center',
                                  marginTop: '20px',
                                  paddingTop: '20px',
                                  borderTop: '1px solid #eee',
                                  justifyContent: 'flex-start'
                              }}>
                                   <span style={{ marginRight: '10px' }}>Logged in as: <strong>{userInfo.Username}</strong></span>
                                  <button onClick={logout} style={{
                                       padding: '8px',
                                       border: '1px solid #ccc',
                                       borderRadius: '5px',
                                       backgroundColor: '#f9f9f9',
                                       transition: 'background-color 0.3s ease',
                                       cursor: 'pointer',
                                       fontSize: '0.9em'
                                   }}>Logout</button>
                               </div>
                          </div>
                      )}

                    {/* Main Content */}
                    <div style={{
                        flexGrow: 1,
                        padding: '20px',
                        backgroundColor: '#f0f0f0',
                        borderRadius: '10px',
                        boxShadow: 'inset 5px 5px 10px #bebebe, inset -5px -5px 10px #ffffff',
                        marginLeft: userInfo?.Role === 'Doctor' || userInfo?.Role === 'Patient' ? '20px' : '0' // Add a gap if sidebar is present
                    }}>
                         <h2>Welcome, {userInfo?.Role === 'Patient' ? displayPatientFullName : displayFullName} ({userInfo?.Role})</h2>
                        {userInfo?.Role === 'Doctor' && renderDoctorContent()}
                         {userInfo?.Role === 'Patient' && renderPatientContent()}
                         {showChangePasswordForm && (
                              <div style={{ marginTop: '20px' }}>
                                   <h3>Change Password</h3>
                                   {changePasswordMessage && <p style={{ color: changePasswordMessage.includes('Failed') ? 'red' : 'green' }}>{changePasswordMessage}</p>}
                                   <div style={{ marginBottom: '10px' }}>
                                       <label>Old Password:</label>
                                       <input type="password" value={oldPassword} onChange={e => setOldPassword(e.target.value)} style={{ marginLeft: '10px' }} />
                                   </div>
                                   <div style={{ marginBottom: '10px' }}>
                                       <label>New Password:</label>
                                       <input type="password" value={newPassword} onChange={e => setNewPassword(e.target.value)} style={{ marginLeft: '10px' }} />
                                   </div>
                                   <div style={{ marginBottom: '10px' }}>
                                       <label>Confirm New Password:</label>
                                       <input type="password" value={confirmNewPassword} onChange={e => setConfirmNewPassword(e.target.value)} style={{ marginLeft: '10px' }} />
                                   </div>
                                   <button onClick={handleChangePassword} style={{ padding: '8px 15px', marginRight: '10px' }}>Confirm Change</button>
                                   <button onClick={() => setShowChangePasswordForm(false)} style={{ padding: '8px 15px' }}>Cancel</button>
                              </div>
                         )}
                         {/* Other roles' content would go here */}

                    </div>
                </div>
            )}
        </div>
    );
};

export default App;