# Hospital Management System Project

---

**Project**

**Title:** Hospital Management System

---

**Brief Description**

This project is a comprehensive Hospital Management System designed to streamline the operations of a healthcare facility. Developed as a MySQL-based information system with a web interface, it focuses on managing key entities such as patients, doctors, and appointments, providing functionalities for data management, analytics, reporting, and secure user access. The system aims to offer a user-friendly platform for interacting with healthcare data.

---

**Functional & Non-functional Requirements**

**Functional Requirements:**

* **Entities Management:** Implement full CRUD (Create, Read, Update, Delete) operations for core entities like Patients, Doctors, Appointments, Medical Records, Departments, etc.
* **Appointment Scheduling:** Allow scheduling, viewing, and managing patient appointments with doctors.
* **Medical Records:** Store and retrieve patient medical history, diagnoses, treatments, and prescriptions.
* **Reporting and Analytics:** Generate statistical reports and visualize key metrics (e.g., number of appointments per doctor/day, common diagnoses) using SQL aggregations and views.
* **User Authentication and Authorization:** Secure login for different user roles (Admin, Doctor, Patient, Staff) with role-based access control to system functionalities and data.
* **Search and Filtering:** Enable searching and filtering of records based on some criteria.

**Non-functional Requirements:**

* **Security:** Enforce security at the database level (user roles, privileges, data encryption for sensitive fields) and prevent common web vulnerabilities (like SQL injection).
* **Performance:** Ensure efficient data retrieval and transaction processing through database indexing and query optimization.
* **Usability:** Provide a user-friendly and intuitive web interface for all user roles.
* **Reliability:** Maintain data integrity and consistency through proper database design and constraints.

---

**Planned Core Entities** (brief outline)

* `Patients`: Information about patients (ID, Name, DOB, Contact, Medical History link).
* `Doctors`: Information about doctors (ID, Name, Specialization, Department, Contact).
* `Appointments`: Details of scheduled appointments (ID, Patient ID, Doctor ID, Date, Time, Status).
* `MedicalRecords`: Patient's medical history, linking to diagnoses, treatments, prescriptions (ID, Patient ID, Date, Doctor ID, Summary/Notes).
* `Users`: System users for web login (ID, Username, Password Hash, Role, linked to Patient/Doctor/Staff).
* `Departments`: Hospital departments (ID, Name).
* `Services`: Medical services provided (ID, Name, Cost).

---

**Tech Stack**

* **Database:** MySQL
* **Backend:** Python
* **Frontend:** Typescript (along with CSS and JavaScript)

---

**Team Members and Roles**

* **Ha Minh Dung:** Backend Developer, Database Developer 
* **Tran Hung Dat:** Frontend Developer

---

**Timeline**

Based on the provided assignment deadlines:

* **By Tuesday, May 6:** Start initial requirements analysis.
* **By Tuesday, May 13:** Continue requirements analysis and begin Conceptual & Logical Design (ERD draft, initial entity definition). 
* **By Tuesday, May 20:** Complete Conceptual & Logical Design (Finalized ERD, Normalized Schema). Prepare SQL DDL scripts. Define detailed task division. *
* **Between May 20 and May 27:** Physical Implementation (Create DB, Load sample data, Develop stored procedures, triggers, views, indexing). Develop Backend and Frontend, integrate layers. Implement security. Conduct End-to-End Testing and Performance Testing. Prepare final presentation slides and report.
* **By Tuesday, May 27:**  Final Presentation demonstration.

