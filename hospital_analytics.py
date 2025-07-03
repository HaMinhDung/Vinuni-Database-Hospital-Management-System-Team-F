#!/usr/bin/env python3
import mysql.connector
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import MaxNLocator
import seaborn as sns
import os
from datetime import datetime

# Create a directory for saving analytics results
output_dir = 'analytics_results'
os.makedirs(output_dir, exist_ok=True)

def connect_to_db():
    """Connect to the MySQL database"""
    try:
        # Update these with your actual database credentials
        conn = mysql.connector.connect(
            host='localhost',
            user='root',  # Replace with your MySQL username
            password='',  # Replace with your MySQL password
            database='HospitalDB'
        )
        print("Successfully connected to database!")
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def doctor_appointment_ranking(conn):
    """Generate analytics for doctor appointment rankings"""
    print("Generating doctor appointment ranking analytics...")
    
    # SQL Query using RANK() window function
    query = """
    SELECT 
        d.DoctorID,
        d.Name AS DoctorName,
        d.Specialization,
        dept.Name AS DepartmentName,
        COUNT(a.AppointmentID) AS TotalAppointments,
        RANK() OVER (ORDER BY COUNT(a.AppointmentID) DESC) AS AppointmentRank
    FROM 
        Doctor d
    LEFT JOIN 
        Department dept ON d.DepartmentID = dept.DepartmentID
    LEFT JOIN 
        Appointment a ON d.DoctorID = a.DoctorID
    GROUP BY 
        d.DoctorID, d.Name, d.Specialization, dept.Name
    ORDER BY 
        TotalAppointments DESC
    LIMIT 15;
    """
    
    try:
        # Read data into pandas DataFrame
        df = pd.read_sql(query, conn)
        
        if df.empty:
            print("No doctor appointment data available.")
            return
        
        # Save raw data to CSV
        df.to_csv(f"{output_dir}/doctor_rankings.csv", index=False)
        
        # Generate bar chart for all doctors
        plt.figure(figsize=(14, 10))
        bars = plt.bar(df['DoctorName'], df['TotalAppointments'], color=plt.cm.viridis(np.linspace(0, 0.8, len(df))))
        
        # Add data labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            if pd.isna(height) or height == 0:
                height = 0
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{height:.0f}', ha='center', va='bottom', fontsize=9)
        
        # Customize the chart
        plt.title('Doctor Rankings by Number of Appointments', fontsize=16)
        plt.xlabel('Doctor Name', fontsize=12)
        plt.ylabel('Number of Appointments', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Add rank annotations
        for i, (doctor, appointments, rank) in enumerate(zip(df['DoctorName'], df['TotalAppointments'], df['AppointmentRank'])):
            if pd.isna(appointments) or appointments == 0:
                continue
            plt.annotate(f'#{rank}', 
                        (i, appointments/2), 
                        ha='center', 
                        va='center',
                        color='white', 
                        fontweight='bold',
                        fontsize=10)
        
        # Save chart
        plt.savefig(f"{output_dir}/doctor_appointment_ranking.png", dpi=300)
        plt.close()
        
        # Generate specialized chart for top 5 doctors
        top_doctors = df.head(5)
        
        plt.figure(figsize=(12, 8))
        sns.barplot(x='DoctorName', y='TotalAppointments', data=top_doctors, palette='viridis')
        
        for i, row in enumerate(top_doctors.itertuples()):
            plt.text(i, row.TotalAppointments + 1, f"Rank #{row.AppointmentRank}", 
                    ha='center', fontweight='bold')
            plt.text(i, row.TotalAppointments/2, f"{row.Specialization}", 
                    ha='center', va='center', color='white', fontweight='bold')
            
        plt.title('Top 5 Doctors by Number of Appointments', fontsize=16)
        plt.xlabel('Doctor Name', fontsize=12)
        plt.ylabel('Number of Appointments', fontsize=12)
        plt.xticks(rotation=30, ha='right')
        plt.tight_layout()
        
        plt.savefig(f"{output_dir}/top_doctors_ranking.png", dpi=300)
        plt.close()
        
        print("Doctor appointment ranking analytics completed.")
        
        # Return dataframe for potential further analysis
        return df
    
    except Exception as e:
        print(f"Error in doctor_appointment_ranking: {e}")
        return None

def monthly_appointment_trends(conn):
    """Generate analytics for monthly appointment trends"""
    print("Generating monthly appointment trends analytics...")
    
    # SQL Query using GROUP BY MONTH()
    query = """
    SELECT 
        YEAR(a.DateTime) AS Year,
        MONTH(a.DateTime) AS Month,
        MONTHNAME(a.DateTime) AS MonthName,
        COUNT(a.AppointmentID) AS TotalAppointments,
        COUNT(DISTINCT a.PatientID) AS UniquePatients,
        AVG(CASE WHEN mr.RecordID IS NOT NULL THEN 1 ELSE 0 END) * 100 AS CompletionRate
    FROM 
        Appointment a
    LEFT JOIN 
        MedicalRecord mr ON a.AppointmentID = mr.AppointmentID
    GROUP BY 
        YEAR(a.DateTime), MONTH(a.DateTime), MONTHNAME(a.DateTime)
    ORDER BY 
        Year, Month;
    """
    
    try:
        # Read data into pandas DataFrame
        df = pd.read_sql(query, conn)
        
        if df.empty:
            print("No monthly appointment data available.")
            return
        
        # Save raw data to CSV
        df.to_csv(f"{output_dir}/monthly_appointment_trends.csv", index=False)
        
        # Create a combined Year-Month field for plotting
        df['YearMonth'] = df['Year'].astype(str) + '-' + df['Month'].astype(str)
        
        # Generate line chart for monthly appointments
        plt.figure(figsize=(14, 8))
        
        # Plot total appointments
        plt.plot(df['YearMonth'], df['TotalAppointments'], marker='o', 
                 linestyle='-', linewidth=2, markersize=8, label='Total Appointments')
        
        # Plot unique patients
        plt.plot(df['YearMonth'], df['UniquePatients'], marker='s', 
                 linestyle='--', linewidth=2, markersize=6, label='Unique Patients')
        
        # Add data labels for total appointments
        for i, txt in enumerate(df['TotalAppointments']):
            plt.annotate(f'{txt:.0f}', 
                        (i, df['TotalAppointments'].iloc[i]),
                        xytext=(0, 10), 
                        textcoords='offset points',
                        ha='center', fontsize=9)
        
        # Customize chart
        plt.title('Monthly Appointment Trends', fontsize=16)
        plt.xlabel('Year-Month', fontsize=12)
        plt.ylabel('Number of Appointments', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        plt.tight_layout()
        
        # Force y-axis to be integers
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
        
        # Save chart
        plt.savefig(f"{output_dir}/monthly_appointment_trends.png", dpi=300)
        plt.close()
        
        # Generate completion rate chart
        plt.figure(figsize=(14, 8))
        bars = plt.bar(df['YearMonth'], df['CompletionRate'], color=plt.cm.cool(np.linspace(0.2, 0.8, len(df))))
        
        # Add data labels
        for bar in bars:
            height = bar.get_height()
            if pd.isna(height):
                height = 0
            plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{height:.1f}%', ha='center', va='bottom', fontsize=9)
        
        # Customize chart
        plt.title('Monthly Appointment Completion Rate', fontsize=16)
        plt.xlabel('Year-Month', fontsize=12)
        plt.ylabel('Completion Rate (%)', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(True, linestyle='--', alpha=0.7, axis='y')
        plt.tight_layout()
        
        # Save chart
        plt.savefig(f"{output_dir}/appointment_completion_rate.png", dpi=300)
        plt.close()
        
        print("Monthly appointment trends analytics completed.")
        
        # Return dataframe for potential further analysis
        return df
    
    except Exception as e:
        print(f"Error in monthly_appointment_trends: {e}")
        return None

def department_performance(conn):
    """Generate analytics for department performance"""
    print("Generating department performance analytics...")
    
    # SQL Query for department performance
    query = """
    SELECT 
        d.Name AS DepartmentName,
        COUNT(DISTINCT doc.DoctorID) AS DoctorCount,
        COUNT(a.AppointmentID) AS TotalAppointments,
        COUNT(DISTINCT a.PatientID) AS UniquePatients,
        AVG(CASE WHEN mr.RecordID IS NOT NULL THEN 1 ELSE 0 END) * 100 AS CompletionRate
    FROM 
        Department d
    LEFT JOIN 
        Doctor doc ON d.DepartmentID = doc.DepartmentID
    LEFT JOIN 
        Appointment a ON doc.DoctorID = a.DoctorID
    LEFT JOIN 
        MedicalRecord mr ON a.AppointmentID = mr.AppointmentID
    GROUP BY 
        d.DepartmentID, d.Name
    ORDER BY 
        TotalAppointments DESC;
    """
    
    try:
        # Read data into pandas DataFrame
        df = pd.read_sql(query, conn)
        
        if df.empty:
            print("No department performance data available.")
            return
        
        # Save raw data to CSV
        df.to_csv(f"{output_dir}/department_performance.csv", index=False)
        
        # Generate stacked bar chart for department metrics
        plt.figure(figsize=(14, 10))
        
        # Create stacked bars
        bottom_bars = np.zeros(len(df))
        
        # Plot doctor count
        p1 = plt.bar(df['DepartmentName'], df['DoctorCount'], label='Doctors')
        
        # Plot unique patients
        p2 = plt.bar(df['DepartmentName'], df['UniquePatients'], 
                     bottom=df['DoctorCount'], label='Unique Patients')
        
        # Customize chart
        plt.title('Department Performance Overview', fontsize=16)
        plt.xlabel('Department Name', fontsize=12)
        plt.ylabel('Count', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.legend()
        plt.tight_layout()
        
        # Save chart
        plt.savefig(f"{output_dir}/department_performance.png", dpi=300)
        plt.close()
        
        # Generate bubble chart for department performance
        plt.figure(figsize=(14, 10))
        
        # Create bubble chart
        # Size bubbles by appointment count
        sizes = df['TotalAppointments'] * 20
        # Minimum size for visibility
        sizes = sizes.apply(lambda x: max(100, x) if not pd.isna(x) else 100)
        
        # Color bubbles by completion rate
        colors = df['CompletionRate']
        colors = colors.fillna(0)
        
        # Create scatter plot with varying bubble sizes
        scatter = plt.scatter(df.index, df['UniquePatients'], 
                             s=sizes, c=colors, cmap='viridis', 
                             alpha=0.7, edgecolors='black')
        
        # Add department name labels
        for i, dept in enumerate(df['DepartmentName']):
            plt.annotate(dept, (i, df['UniquePatients'].iloc[i]),
                        xytext=(0, 10), textcoords='offset points',
                        ha='center', fontsize=9)
        
        # Add a color bar to show completion rate scale
        cbar = plt.colorbar(scatter)
        cbar.set_label('Appointment Completion Rate (%)')
        
        # Customize chart
        plt.title('Department Performance: Patients, Appointments and Completion Rate', fontsize=16)
        plt.xlabel('Department Index', fontsize=12)
        plt.ylabel('Number of Unique Patients', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        # Save chart
        plt.savefig(f"{output_dir}/department_bubble_chart.png", dpi=300)
        plt.close()
        
        print("Department performance analytics completed.")
        
        # Return dataframe for potential further analysis
        return df
    
    except Exception as e:
        print(f"Error in department_performance: {e}")
        return None

def patient_demographics(conn):
    """Generate analytics for patient demographics"""
    print("Generating patient demographics analytics...")
    
    # SQL Query for patient demographics
    query = """
    SELECT 
        Gender,
        COUNT(*) AS PatientCount,
        AVG(TIMESTAMPDIFF(YEAR, DOB, CURDATE())) AS AvgAge,
        MIN(TIMESTAMPDIFF(YEAR, DOB, CURDATE())) AS MinAge,
        MAX(TIMESTAMPDIFF(YEAR, DOB, CURDATE())) AS MaxAge
    FROM 
        Patient
    WHERE
        DOB IS NOT NULL
    GROUP BY 
        Gender;
    """
    
    try:
        # Read data into pandas DataFrame
        df = pd.read_sql(query, conn)
        
        if df.empty:
            print("No patient demographics data available.")
            return
        
        # Save raw data to CSV
        df.to_csv(f"{output_dir}/patient_demographics.csv", index=False)
        
        # Generate pie chart for gender distribution
        plt.figure(figsize=(10, 8))
        
        # Create pie chart
        plt.pie(df['PatientCount'], labels=df['Gender'], autopct='%1.1f%%',
                startangle=90, shadow=True, explode=[0.05] * len(df),
                colors=plt.cm.Set3.colors[:len(df)])
        
        # Add title
        plt.title('Patient Gender Distribution', fontsize=16)
        plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular
        
        # Save chart
        plt.savefig(f"{output_dir}/patient_gender_distribution.png", dpi=300)
        plt.close()
        
        # Generate bar chart for age statistics by gender
        plt.figure(figsize=(12, 8))
        
        # Set width of bars
        barWidth = 0.25
        
        # Set position of bar on X axis
        r1 = np.arange(len(df))
        r2 = [x + barWidth for x in r1]
        r3 = [x + barWidth for x in r2]
        
        # Create bars
        plt.bar(r1, df['AvgAge'], width=barWidth, label='Average Age', color='skyblue')
        plt.bar(r2, df['MinAge'], width=barWidth, label='Minimum Age', color='lightgreen')
        plt.bar(r3, df['MaxAge'], width=barWidth, label='Maximum Age', color='salmon')
        
        # Add labels and title
        plt.xlabel('Gender', fontsize=12)
        plt.ylabel('Age (years)', fontsize=12)
        plt.title('Patient Age Statistics by Gender', fontsize=16)
        plt.xticks([r + barWidth for r in range(len(df))], df['Gender'])
        plt.legend()
        
        # Add value labels on bars
        for i in range(len(df)):
            plt.text(r1[i], df['AvgAge'].iloc[i] + 0.5, f"{df['AvgAge'].iloc[i]:.1f}", ha='center', va='bottom')
            plt.text(r2[i], df['MinAge'].iloc[i] + 0.5, f"{df['MinAge'].iloc[i]:.0f}", ha='center', va='bottom')
            plt.text(r3[i], df['MaxAge'].iloc[i] + 0.5, f"{df['MaxAge'].iloc[i]:.0f}", ha='center', va='bottom')
        
        plt.tight_layout()
        
        # Save chart
        plt.savefig(f"{output_dir}/patient_age_statistics.png", dpi=300)
        plt.close()
        
        print("Patient demographics analytics completed.")
        
        # Return dataframe for potential further analysis
        return df
    
    except Exception as e:
        print(f"Error in patient_demographics: {e}")
        return None

def medical_record_analysis(conn):
    """Generate analytics for medical records"""
    print("Generating medical record analytics...")
    
    # SQL Query for common diagnoses
    diagnosis_query = """
    SELECT 
        Diagnosis,
        COUNT(*) AS RecordCount
    FROM 
        MedicalRecord
    GROUP BY 
        Diagnosis
    ORDER BY 
        RecordCount DESC
    LIMIT 10;
    """
    
    # Query for treatments
    treatment_query = """
    SELECT 
        Treatment,
        COUNT(*) AS RecordCount
    FROM 
        MedicalRecord
    GROUP BY 
        Treatment
    ORDER BY 
        RecordCount DESC
    LIMIT 10;
    """
    
    try:
        # Read data into pandas DataFrames
        diagnosis_df = pd.read_sql(diagnosis_query, conn)
        treatment_df = pd.read_sql(treatment_query, conn)
        
        if diagnosis_df.empty and treatment_df.empty:
            print("No medical record data available.")
            return
        
        # Save raw data to CSV
        if not diagnosis_df.empty:
            diagnosis_df.to_csv(f"{output_dir}/common_diagnoses.csv", index=False)
            
            # Generate horizontal bar chart for common diagnoses
            plt.figure(figsize=(12, 8))
            
            # Plot horizontal bars in descending order
            bars = plt.barh(diagnosis_df['Diagnosis'], diagnosis_df['RecordCount'], color='skyblue')
            
            # Add data labels
            for bar in bars:
                width = bar.get_width()
                plt.text(width + 0.3, bar.get_y() + bar.get_height()/2, 
                        f'{width:.0f}', ha='left', va='center')
            
            # Customize chart
            plt.title('Top 10 Common Diagnoses', fontsize=16)
            plt.xlabel('Number of Records', fontsize=12)
            plt.ylabel('Diagnosis', fontsize=12)
            plt.tight_layout()
            
            # Save chart
            plt.savefig(f"{output_dir}/common_diagnoses.png", dpi=300)
            plt.close()
        
        if not treatment_df.empty:
            treatment_df.to_csv(f"{output_dir}/common_treatments.csv", index=False)
            
            # Generate horizontal bar chart for common treatments
            plt.figure(figsize=(12, 8))
            
            # Plot horizontal bars in descending order
            bars = plt.barh(treatment_df['Treatment'], treatment_df['RecordCount'], color='lightgreen')
            
            # Add data labels
            for bar in bars:
                width = bar.get_width()
                plt.text(width + 0.3, bar.get_y() + bar.get_height()/2, 
                        f'{width:.0f}', ha='left', va='center')
            
            # Customize chart
            plt.title('Top 10 Common Treatments', fontsize=16)
            plt.xlabel('Number of Records', fontsize=12)
            plt.ylabel('Treatment', fontsize=12)
            plt.tight_layout()
            
            # Save chart
            plt.savefig(f"{output_dir}/common_treatments.png", dpi=300)
            plt.close()
        
        print("Medical record analytics completed.")
        
    except Exception as e:
        print(f"Error in medical_record_analysis: {e}")

def service_analytics(conn):
    """Generate analytics for hospital services"""
    print("Generating service analytics...")
    
    # SQL Query for services by cost
    query = """
    SELECT 
        Name AS ServiceName,
        Cost
    FROM 
        Service
    ORDER BY 
        Cost DESC;
    """
    
    try:
        # Read data into pandas DataFrame
        df = pd.read_sql(query, conn)
        
        if df.empty:
            print("No service data available.")
            return
        
        # Save raw data to CSV
        df.to_csv(f"{output_dir}/services_by_cost.csv", index=False)
        
        # Generate horizontal bar chart for services by cost
        plt.figure(figsize=(12, 10))
        
        # Plot horizontal bars in descending order
        bars = plt.barh(df['ServiceName'], df['Cost'], color=plt.cm.Greens(np.linspace(0.4, 0.8, len(df))))
        
        # Add data labels
        for bar in bars:
            width = bar.get_width()
            plt.text(width + 0.5, bar.get_y() + bar.get_height()/2, 
                    f'${width:.2f}', ha='left', va='center')
        
        # Customize chart
        plt.title('Hospital Services by Cost', fontsize=16)
        plt.xlabel('Cost ($)', fontsize=12)
        plt.ylabel('Service Name', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7, axis='x')
        plt.tight_layout()
        
        # Save chart
        plt.savefig(f"{output_dir}/services_by_cost.png", dpi=300)
        plt.close()
        
        # Create a summary statistics table
        stats = df['Cost'].describe()
        
        # Generate text file with summary statistics
        with open(f"{output_dir}/service_cost_statistics.txt", 'w') as f:
            f.write("Hospital Service Cost Statistics\n")
            f.write("===============================\n\n")
            f.write(f"Count: {stats['count']:.0f}\n")
            f.write(f"Mean Cost: ${stats['mean']:.2f}\n")
            f.write(f"Std Dev: ${stats['std']:.2f}\n")
            f.write(f"Min Cost: ${stats['min']:.2f}\n")
            f.write(f"25% Quartile: ${stats['25%']:.2f}\n")
            f.write(f"Median Cost: ${stats['50%']:.2f}\n")
            f.write(f"75% Quartile: ${stats['75%']:.2f}\n")
            f.write(f"Max Cost: ${stats['max']:.2f}\n")
        
        print("Service analytics completed.")
        
        # Return dataframe for potential further analysis
        return df
    
    except Exception as e:
        print(f"Error in service_analytics: {e}")
        return None

def query_optimization_analysis(conn):
    """Demonstrate query optimization with and without indexes"""
    print("Performing query optimization analysis...")
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # First, ensure we have the necessary indexes
        print("Creating test environment...")
        
        # Record start time for non-indexed query
        print("Testing query without indexes...")
        cursor.execute("SET profiling = 1")
        
        # Execute the non-indexed query and capture EXPLAIN plan
        cursor.execute("""
        EXPLAIN
        SELECT 
            a.AppointmentID,
            a.DateTime,
            a.Status,
            p.PatientID,
            p.Name AS PatientName,
            d.DoctorID,
            d.Name AS DoctorName
        FROM 
            Appointment a
        JOIN 
            Patient p ON a.PatientID = p.PatientID
        JOIN 
            Doctor d ON a.DoctorID = d.DoctorID
        WHERE 
            a.Status = 'Scheduled'
            AND a.DateTime BETWEEN '2023-01-01' AND '2023-12-31'
        ORDER BY 
            a.DateTime
        """)
        
        explain_results_before = cursor.fetchall()
        
        # Execute the actual query to measure performance
        cursor.execute("""
        SELECT 
            COUNT(*) 
        FROM 
            Appointment a
        JOIN 
            Patient p ON a.PatientID = p.PatientID
        JOIN 
            Doctor d ON a.DoctorID = d.DoctorID
        WHERE 
            a.Status = 'Scheduled'
            AND a.DateTime BETWEEN '2023-01-01' AND '2023-12-31'
        """)
        
        cursor.fetchall()  # Fetch results to complete the query
        
        # Get timing information
        cursor.execute("SHOW PROFILES")
        timing_before = cursor.fetchall()
        
        # Now add indexes
        print("Adding indexes...")
        try:
            cursor.execute("CREATE INDEX idx_appointment_status ON Appointment(Status)")
            cursor.execute("CREATE INDEX idx_appointment_datetime ON Appointment(DateTime)")
            cursor.execute("CREATE INDEX idx_appointment_patient_doctor ON Appointment(PatientID, DoctorID)")
        except mysql.connector.Error:
            print("Indexes may already exist - continuing with analysis")
        
        # Record start time for indexed query
        print("Testing query with indexes...")
        cursor.execute("SET profiling = 1")
        
        # Execute the indexed query and capture EXPLAIN plan
        cursor.execute("""
        EXPLAIN
        SELECT 
            a.AppointmentID,
            a.DateTime,
            a.Status,
            p.PatientID,
            p.Name AS PatientName,
            d.DoctorID,
            d.Name AS DoctorName
        FROM 
            Appointment a
        JOIN 
            Patient p ON a.PatientID = p.PatientID
        JOIN 
            Doctor d ON a.DoctorID = d.DoctorID
        WHERE 
            a.Status = 'Scheduled'
            AND a.DateTime BETWEEN '2023-01-01' AND '2023-12-31'
        ORDER BY 
            a.DateTime
        """)
        
        explain_results_after = cursor.fetchall()
        
        # Execute the actual query to measure performance
        cursor.execute("""
        SELECT 
            COUNT(*) 
        FROM 
            Appointment a
        JOIN 
            Patient p ON a.PatientID = p.PatientID
        JOIN 
            Doctor d ON a.DoctorID = d.DoctorID
        WHERE 
            a.Status = 'Scheduled'
            AND a.DateTime BETWEEN '2023-01-01' AND '2023-12-31'
        """)
        
        cursor.fetchall()  # Fetch results to complete the query
        
        # Get timing information
        cursor.execute("SHOW PROFILES")
        timing_after = cursor.fetchall()
        
        # Save the EXPLAIN results
        with open(f"{output_dir}/query_optimization_explain.txt", 'w') as f:
            f.write("Query Optimization Analysis - EXPLAIN Results\n")
            f.write("===========================================\n\n")
            
            f.write("EXPLAIN Results Before Indexing:\n")
            f.write("------------------------------\n")
            for row in explain_results_before:
                f.write(str(row) + "\n")
            
            f.write("\nEXPLAIN Results After Indexing:\n")
            f.write("-----------------------------\n")
            for row in explain_results_after:
                f.write(str(row) + "\n")
        
        # Extract timing information
        before_time = timing_before[-1]['Duration'] if timing_before else 0
        after_time = timing_after[-1]['Duration'] if timing_after else 0
        
        # Save timing results
        with open(f"{output_dir}/query_optimization_timing.txt", 'w') as f:
            f.write("Query Optimization Analysis - Timing Results\n")
            f.write("=========================================\n\n")
            f.write(f"Query execution time before indexing: {before_time:.6f} seconds\n")
            f.write(f"Query execution time after indexing: {after_time:.6f} seconds\n")
            
            if before_time > 0:
                improvement = ((before_time - after_time) / before_time) * 100
                f.write(f"Performance improvement: {improvement:.2f}%\n")
        
        # Create a visualization of the timing differences
        plt.figure(figsize=(10, 6))
        
        # Create the bar chart
        labels = ['Before Indexing', 'After Indexing']
        times = [before_time, after_time]
        bars = plt.bar(labels, times, color=['indianred', 'seagreen'])
        
        # Add data labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.0005,
                    f'{height:.6f}s', ha='center', va='bottom')
        
        # Customize chart
        plt.title('Query Execution Time: Before vs After Indexing', fontsize=16)
        plt.ylabel('Execution Time (seconds)', fontsize=12)
        plt.ylim(0, max(times) * 1.2)  # Add some space above bars
        
        # Add percentage improvement
        if before_time > 0:
            improvement = ((before_time - after_time) / before_time) * 100
            plt.figtext(0.5, 0.01, f"Performance Improvement: {improvement:.2f}%", 
                        ha="center", fontsize=12, bbox={"facecolor":"lightgray", "alpha":0.5, "pad":5})
        
        # Save chart
        plt.savefig(f"{output_dir}/query_optimization_comparison.png", dpi=300)
        plt.close()
        
        print("Query optimization analysis completed.")
        
    except Exception as e:
        print(f"Error in query_optimization_analysis: {e}")
    finally:
        if cursor:
            cursor.close()

def run_all_analytics():
    """Run all analytics functions"""
    conn = connect_to_db()
    if conn:
        try:
            # Create a report header
            with open(f"{output_dir}/analytics_report.txt", 'w') as f:
                f.write("Hospital Management System Analytics Report\n")
                f.write("========================================\n\n")
                f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("This report contains analytics on various aspects of the hospital management system.\n")
                f.write("Please refer to the individual CSV files and charts in this directory for detailed data.\n\n")
            
            # Run all analytics functions
            doctor_df = doctor_appointment_ranking(conn)
            monthly_df = monthly_appointment_trends(conn)
            dept_df = department_performance(conn)
            patient_df = patient_demographics(conn)
            medical_record_analysis(conn)
            service_df = service_analytics(conn)
            query_optimization_analysis(conn)
            
            # Append summary to report
            with open(f"{output_dir}/analytics_report.txt", 'a') as f:
                f.write("\nSummary of Findings\n")
                f.write("==================\n\n")
                
                if doctor_df is not None and not doctor_df.empty:
                    top_doctor = doctor_df.iloc[0]
                    f.write(f"Top Doctor by Appointments: {top_doctor['DoctorName']} ")
                    f.write(f"with {top_doctor['TotalAppointments']} appointments\n")
                
                if monthly_df is not None and not monthly_df.empty:
                    max_month = monthly_df.loc[monthly_df['TotalAppointments'].idxmax()]
                    f.write(f"Busiest Month: {max_month['MonthName']} {max_month['Year']} ")
                    f.write(f"with {max_month['TotalAppointments']} appointments\n")
                
                if dept_df is not None and not dept_df.empty:
                    top_dept = dept_df.iloc[0]
                    f.write(f"Busiest Department: {top_dept['DepartmentName']} ")
                    f.write(f"with {top_dept['TotalAppointments']} appointments\n")
                
                if service_df is not None and not service_df.empty:
                    top_service = service_df.iloc[0]
                    f.write(f"Most Expensive Service: {top_service['ServiceName']} ")
                    f.write(f"at ${top_service['Cost']:.2f}\n")
            
            print(f"All analytics completed. Results saved to {output_dir}/")
            
        except Exception as e:
            print(f"Error in analytics: {e}")
        finally:
            conn.close()
    else:
        print("Failed to connect to database. Cannot run analytics.")

if __name__ == "__main__":
    run_all_analytics() 