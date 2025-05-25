Step 0: cd be

Step 1: Install requirements:
pip install -r requirements.txt
If you get an error about a missing library, install it (pip install ) and add it to requirements.txt.

Step 2: Run the database script in MySQL.

Step 3: Open ./db/Connection.py and enter your MySQL username and password.
After connecting:
-Run main.py to test admin functions
-Run login.py to log in (checks credentials against the User table); try Doctor and Patient roles to test features
-Run p_sign_up.py to test creating a new user and patient profile (doctors must be added by the admin)

Step 4: python server.py  (start the backend and connect to the frontend)

Note: In frontend.tsx, the app checks your row in userProfile:
• If DoctorID is set, you’re a Doctor
• If PatientID is set, you’re a Patient
• If both are null, you’re the Admin