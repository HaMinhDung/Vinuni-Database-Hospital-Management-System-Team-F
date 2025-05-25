# db/connection.py

import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="020412",
        database="HospitalDB"
    )

