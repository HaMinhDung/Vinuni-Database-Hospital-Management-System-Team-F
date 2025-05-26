# 1. Hospital Management System Project

## 1.1. Project Overview

**Title:** Hospital Management System
![Nothing Burger logo](skibidi.png)
## 1.2. Brief Description

This project involves the design, development, and implementation of a comprehensive Hospital Management System. It is built as a MySQL-based information system with a web interface, focusing on managing core healthcare entities and operations. The system will provide functionalities for data management, analytics, reporting, and secure access, aiming to streamline workflows within a healthcare facility through a user-friendly platform.

## 1.3. Functional & Non-functional Requirements

### 1.3.1. Functional Requirements

* **Entities Management:** Implement full CRUD (Create, Read, Update, Delete) operations for core entities such as Patients, Doctors, Appointments, Medical Records, Departments, and Services.
* **Appointment Scheduling:** Allow users to schedule, view, modify, and manage patient appointments with doctors.
* **Medical Records Management:** Enable structured storage, retrieval, and update of patient medical history, including diagnoses, treatments, prescriptions, and test results.
* **Reporting and Analytics:** Provide capabilities to generate statistical reports and visualize key performance indicators (e.g., appointment statistics by doctor or department, common diagnoses, service usage) utilizing SQL aggregations, grouping, and database views.
* **User Authentication and Authorization:** Implement a secure system for user login across different roles (e.g., Admin, Doctor, Patient, Staff) with role-based access control to restrict access to specific functionalities and data.
* **Search and Filtering:** Offer robust search and filtering capabilities across various entities and data fields to quickly locate information.
![Doctor logo](skibidi_doctor.png)
### 1.3.2. Non-functional Requirements

* **Security:** Ensure data security and privacy through appropriate database-level security configurations, user privilege management, encryption for sensitive data fields, and prevention of common web vulnerabilities like SQL injection.
* **Performance:** Optimize database queries and structure (e.g., using indexing, appropriate data types) to ensure efficient data retrieval and transaction processing, maintaining system responsiveness.
* **Usability:** Develop an intuitive, consistent, and user-friendly web interface that is accessible and easy to navigate for all intended user roles.
* **Reliability:** Design the database schema with appropriate constraints (Primary Keys, Foreign Keys, Check Constraints) to maintain data integrity and consistency across the system.
![Patient logo](skibidi_patient.png)
## 1.4. Planned Core Entities (brief outline)

* `Patients`: Stores demographic and contact information for patients.
* `Doctors`: Stores professional and contact details for doctors, including specialization and department.
* `Appointments`: Records details of scheduled visits, linking patients, doctors, dates, times, and status.
* `MedicalRecords`: Contains patient medical history, linking to specific encounters, diagnoses, treatments, and notes.
* `Users`: Manages user accounts for system access, including roles and credentials.
* `Departments`: Lists the various departments within the hospital.
* `Services`: Defines the medical services provided, potentially including costs.

## 1.5. Tech Stack

* **Database:** MySQL
* **Backend:** Python
* **Frontend:** Typescript (with HTML, CSS, and JavaScript)

## 1.6. Team Members and Roles

* **Ha Minh Dung:** Backend Developer
* **Nguyen Duc Trung:** Database Developer
* **Tran Hung Dat:** Frontend Developer


## 1.7. Timeline

* **By Tuesday, May 6:** Start initial requirements analysis.
* **By Tuesday, May 13:** Continue requirements analysis and begin Conceptual & Logical Design (ERD draft, initial entity definition). 
* **By Tuesday, May 20:** Complete Conceptual & Logical Design (Finalized ERD, Normalized Schema). Prepare SQL DDL scripts. Define detailed task division.
* **By Tuesday, May 27:** Physical Implementation (Create DB, Load sample data, Develop stored procedures, triggers, views, indexing). Develop Backend and Frontend, integrate layers. Implement security. Conduct End-to-End Testing and Performance Testing. Prepare final presentation slides and report.

---
