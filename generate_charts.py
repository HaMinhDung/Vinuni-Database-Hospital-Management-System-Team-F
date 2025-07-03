#!/usr/bin/env python3
import mysql.connector
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import MaxNLocator

def connect_to_db():
    """Connect to the MySQL database"""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='your_username',  # Replace with your actual MySQL username
            password='your_password',  # Replace with your actual MySQL password
            database='HospitalDB'
        )
        print("Successfully connected to database!")
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def generate_doctor_ranking_chart(conn):
    """Generate bar chart for doctor rankings by appointments"""
    query = """
    SELECT 
        d.Name AS DoctorName,
        COUNT(a.AppointmentID) AS TotalAppointments,
        RANK() OVER (ORDER BY COUNT(a.AppointmentID) DESC) AS AppointmentRank
    FROM 
        Doctor d
    LEFT JOIN 
        Appointment a ON d.DoctorID = a.DoctorID
    GROUP BY 
        d.DoctorID, d.Name
    ORDER BY 
        TotalAppointments DESC
    LIMIT 10;
    """
    
    try:
        df = pd.read_sql(query, conn)
        
        # Create the bar chart
        plt.figure(figsize=(12, 8))
        bars = plt.bar(df['DoctorName'], df['TotalAppointments'], color='skyblue')
        
        # Add data labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{height:.0f}', ha='center', va='bottom')
        
        # Customize the chart
        plt.title('Top 10 Doctors by Number of Appointments', fontsize=16)
        plt.xlabel('Doctor Name', fontsize=12)
        plt.ylabel('Number of Appointments', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Add rank annotations
        for i, (name, appointments, rank) in enumerate(zip(df['DoctorName'], df['TotalAppointments'], df['AppointmentRank'])):
            plt.annotate(f'Rank: {rank}', 
                         (i, appointments/2), 
                         ha='center', 
                         va='center',
                         color='white', 
                         fontweight='bold')
        
        # Save the chart
        plt.savefig('doctor_ranking_chart.png')
        plt.close()
        print("Doctor ranking chart generated: doctor_ranking_chart.png")
        
    except Exception as e:
        print(f"Error generating doctor ranking chart: {e}")

def generate_monthly_appointments_chart(conn):
    """Generate line chart for monthly appointments trend"""
    query = """
    SELECT 
        CONCAT(YEAR(a.DateTime), '-', MONTH(a.DateTime)) AS YearMonth,
        COUNT(a.AppointmentID) AS TotalAppointments
    FROM 
        Appointment a
    GROUP BY 
        YEAR(a.DateTime), MONTH(a.DateTime)
    ORDER BY 
        YEAR(a.DateTime), MONTH(a.DateTime);
    """
    
    try:
        df = pd.read_sql(query, conn)
        
        # Create the line chart
        plt.figure(figsize=(12, 8))
        plt.plot(df['YearMonth'], df['TotalAppointments'], marker='o', linestyle='-', linewidth=2, markersize=8)
        
        # Add data points
        for i, txt in enumerate(df['TotalAppointments']):
            plt.annotate(f'{txt:.0f}', 
                         (i, df['TotalAppointments'].iloc[i]),
                         xytext=(0, 10), 
                         textcoords='offset points',
                         ha='center')
        
        # Customize the chart
        plt.title('Monthly Appointment Trends', fontsize=16)
        plt.xlabel('Year-Month', fontsize=12)
        plt.ylabel('Number of Appointments', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        # Force y-axis to be integers
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
        
        # Save the chart
        plt.savefig('monthly_appointments_chart.png')
        plt.close()
        print("Monthly appointments chart generated: monthly_appointments_chart.png")
        
    except Exception as e:
        print(f"Error generating monthly appointments chart: {e}")

def main():
    """Main function to execute the chart generation"""
    conn = connect_to_db()
    if conn:
        generate_doctor_ranking_chart(conn)
        generate_monthly_appointments_chart(conn)
        conn.close()
        print("All charts generated successfully!")
    else:
        print("Failed to connect to database. Charts could not be generated.")

if __name__ == "__main__":
    main() 