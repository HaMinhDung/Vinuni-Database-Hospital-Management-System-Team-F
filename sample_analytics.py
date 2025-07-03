#!/usr/bin/env python3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import MaxNLocator
import os
from datetime import datetime

# Create directory for saving analytics results
output_dir = 'analytics_results'
os.makedirs(output_dir, exist_ok=True)

def doctor_ranking_analysis():
    """Generate sample doctor ranking analysis with RANK() window function visualization"""
    print("Generating doctor ranking analysis...")
    
    # Sample data - simulating data that would come from SQL RANK() function
    data = {
        'DoctorID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'DoctorName': ['Dr. Smith', 'Dr. Johnson', 'Dr. Williams', 'Dr. Jones', 'Dr. Brown', 
                     'Dr. Davis', 'Dr. Miller', 'Dr. Wilson', 'Dr. Moore', 'Dr. Taylor'],
        'Specialization': ['Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics', 'Dermatology',
                         'Ophthalmology', 'Internal Medicine', 'Surgery', 'Psychiatry', 'Oncology'],
        'DepartmentName': ['Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics', 'Dermatology',
                         'Ophthalmology', 'Internal Medicine', 'Surgery', 'Psychiatry', 'Oncology'],
        'TotalAppointments': [143, 128, 112, 95, 81, 74, 67, 59, 45, 38],
        'AppointmentRank': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV for reference
    df.to_csv(f"{output_dir}/sample_doctor_rankings.csv", index=False)
    
    # Create visualization
    plt.figure(figsize=(14, 10))
    bars = plt.bar(df['DoctorName'], df['TotalAppointments'], color='skyblue')
    
    # Add data labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.0f}', ha='center', va='bottom')
    
    # Add rank annotations
    for i, (doctor, appointments, rank) in enumerate(zip(df['DoctorName'], df['TotalAppointments'], df['AppointmentRank'])):
        plt.annotate(f'Rank: {rank}', 
                     (i, appointments/2), 
                     ha='center', 
                     va='center',
                     color='white', 
                     fontweight='bold')
    
    # Customize chart
    plt.title('Doctor Rankings by Number of Appointments (RANK() Function)', fontsize=16)
    plt.xlabel('Doctor Name', fontsize=12)
    plt.ylabel('Number of Appointments', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Save chart
    plt.savefig(f"{output_dir}/doctor_ranking_chart.png", dpi=300)
    plt.close()
    
    print(f"Doctor ranking chart saved to {output_dir}/doctor_ranking_chart.png")
    return df

def monthly_appointment_trends():
    """Generate sample monthly appointment trends with GROUP BY MONTH() visualization"""
    print("Generating monthly appointment trends analysis...")
    
    # Sample data - simulating data that would come from GROUP BY MONTH()
    data = {
        'Year': [2023] * 12,
        'Month': list(range(1, 13)),
        'MonthName': ['January', 'February', 'March', 'April', 'May', 'June', 
                    'July', 'August', 'September', 'October', 'November', 'December'],
        'TotalAppointments': [45, 52, 61, 67, 75, 80, 85, 91, 87, 76, 65, 72],
        'UniquePatients': [38, 43, 50, 57, 62, 65, 70, 76, 72, 65, 54, 60],
        'CompletionRate': [85.5, 86.2, 84.9, 88.1, 90.3, 91.5, 92.0, 93.7, 90.8, 89.2, 87.6, 88.9]
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Create a combined Year-Month field for plotting
    df['YearMonth'] = df['Year'].astype(str) + '-' + df['Month'].astype(str)
    
    # Save to CSV for reference
    df.to_csv(f"{output_dir}/sample_monthly_trends.csv", index=False)
    
    # Create visualization
    plt.figure(figsize=(14, 8))
    plt.plot(df['MonthName'], df['TotalAppointments'], marker='o', 
             linestyle='-', linewidth=2, markersize=8, color='#3498db')
    
    # Add data labels
    for i, txt in enumerate(df['TotalAppointments']):
        plt.annotate(f'{txt:.0f}', 
                    (i, df['TotalAppointments'].iloc[i]),
                    xytext=(0, 10), 
                    textcoords='offset points',
                    ha='center')
    
    # Customize chart
    plt.title('Monthly Appointment Trends (GROUP BY MONTH Analysis)', fontsize=16)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Number of Appointments', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Force y-axis to be integers
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    
    # Save chart
    plt.savefig(f"{output_dir}/monthly_trends_chart.png", dpi=300)
    plt.close()
    
    print(f"Monthly trends chart saved to {output_dir}/monthly_trends_chart.png")
    return df

def query_optimization_visualization():
    """Generate sample query optimization visualization comparing performance before and after indexing"""
    print("Generating query optimization visualization...")
    
    # Sample data - simulating query performance metrics
    execution_times = {
        'scenario': ['Before Indexing', 'After Indexing'],
        'time': [1.85, 0.23]  # seconds
    }
    
    # Calculate improvement
    improvement = ((execution_times['time'][0] - execution_times['time'][1]) / execution_times['time'][0]) * 100
    
    # Save to text file
    with open(f"{output_dir}/query_optimization_results.txt", 'w') as f:
        f.write("Query Optimization Analysis\n")
        f.write("========================\n\n")
        f.write(f"Execution time before indexing: {execution_times['time'][0]:.2f} seconds\n")
        f.write(f"Execution time after indexing: {execution_times['time'][1]:.2f} seconds\n")
        f.write(f"Performance improvement: {improvement:.1f}%\n\n")
        f.write("EXPLAIN Analysis:\n")
        f.write("--------------\n")
        f.write("Before indexing: Full table scan on Appointment table, followed by nested loop joins.\n")
        f.write("After indexing: Index scan on Status and DateTime, followed by index lookups for joins.\n")
    
    # Create visualization
    plt.figure(figsize=(10, 6))
    bars = plt.bar(execution_times['scenario'], execution_times['time'], 
                  color=['indianred', 'seagreen'])
    
    # Add data labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f'{height:.2f}s', ha='center', va='bottom')
    
    # Customize chart
    plt.title('Query Execution Time: Before vs After Indexing', fontsize=16)
    plt.ylabel('Execution Time (seconds)', fontsize=12)
    plt.ylim(0, max(execution_times['time']) * 1.2)  # Add some space above bars
    
    # Add improvement text
    plt.figtext(0.5, 0.01, f"Performance Improvement: {improvement:.1f}%", 
                ha="center", fontsize=12, bbox={"facecolor":"lightgray", "alpha":0.5, "pad":5})
    
    # Save chart
    plt.savefig(f"{output_dir}/query_optimization_chart.png", dpi=300)
    plt.close()
    
    print(f"Query optimization chart saved to {output_dir}/query_optimization_chart.png")

def run_sample_analytics():
    """Run all sample analytics functions"""
    print(f"Running sample analytics (results will be saved to {output_dir}/)")
    
    # Create summary report
    with open(f"{output_dir}/sample_analytics_report.txt", 'w') as f:
        f.write("Hospital Management System - Sample Analytics Report\n")
        f.write("==============================================\n\n")
        f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("This report contains sample analytics visualizations for the hospital management system.\n")
        f.write("These are based on simulated data to demonstrate SQL analytical functions like RANK() and GROUP BY MONTH().\n\n")
        f.write("Files included in this report:\n")
        f.write("- doctor_ranking_chart.png: Visualization of doctor rankings using RANK() function\n")
        f.write("- monthly_trends_chart.png: Visualization of monthly appointment trends using GROUP BY MONTH()\n")
        f.write("- query_optimization_chart.png: Comparison of query performance before and after indexing\n")
    
    # Run all analyses
    doctor_ranking_analysis()
    monthly_appointment_trends()
    query_optimization_visualization()
    
    print("All sample analytics completed!")

if __name__ == "__main__":
    run_sample_analytics() 