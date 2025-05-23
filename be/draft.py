from models import doctor, patient, appointment, medical_record, department, service, user, user_profile
from db.connection import get_connection

print(appointment.get_doctor_ids_by_patient(1))