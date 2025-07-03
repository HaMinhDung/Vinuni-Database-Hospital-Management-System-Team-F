#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import MaxNLocator

def generate_doctor_ranking_chart():
    """Generate a sample bar chart for doctor rankings by appointments"""
    # Sample data for doctor rankings
    doctors = ['Dr. Smith', 'Dr. Johnson', 'Dr. Williams', 'Dr. Jones', 'Dr. Brown', 
               'Dr. Davis', 'Dr. Miller', 'Dr. Wilson', 'Dr. Moore', 'Dr. Taylor']
    appointments = [145, 132, 120, 98, 87, 75, 68, 55, 42, 31]
    ranks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # Create a DataFrame
    df = pd.DataFrame({
        'DoctorName': doctors,
        'TotalAppointments': appointments,
        'AppointmentRank': ranks
    })
    
    # Create the bar chart
    plt.figure(figsize=(12, 8))
    bars = plt.bar(df['DoctorName'], df['TotalAppointments'], color='skyblue')
    
    # Add data labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
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

def generate_monthly_appointments_chart():
    """Generate a sample line chart for monthly appointments trend"""
    # Sample data for monthly appointments
    months = ['2023-1', '2023-2', '2023-3', '2023-4', '2023-5', '2023-6', 
              '2023-7', '2023-8', '2023-9', '2023-10', '2023-11', '2023-12']
    appointments = [45, 52, 61, 67, 75, 80, 85, 91, 87, 76, 65, 72]
    
    # Create a DataFrame
    df = pd.DataFrame({
        'YearMonth': months,
        'TotalAppointments': appointments
    })
    
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
    plt.title('Monthly Appointment Trends in 2023', fontsize=16)
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

def generate_query_optimization_chart():
    """Generate a sample bar chart comparing query performance before and after indexing"""
    # Sample data for query performance
    scenarios = ['Before Indexing', 'After Indexing']
    execution_times = [1.85, 0.23]  # seconds
    
    # Create the bar chart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(scenarios, execution_times, color=['indianred', 'seagreen'])
    
    # Add data labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f'{height:.2f}s', ha='center', va='bottom')
    
    # Customize the chart
    plt.title('Query Execution Time: Before vs After Indexing', fontsize=16)
    plt.xlabel('Scenario', fontsize=12)
    plt.ylabel('Execution Time (seconds)', fontsize=12)
    plt.ylim(0, max(execution_times) * 1.2)  # Add some space above bars
    
    # Add percentage improvement
    improvement = ((execution_times[0] - execution_times[1]) / execution_times[0]) * 100
    plt.figtext(0.5, 0.01, f"Performance Improvement: {improvement:.1f}%", 
                ha="center", fontsize=12, bbox={"facecolor":"lightgray", "alpha":0.5, "pad":5})
    
    # Save the chart
    plt.savefig('query_optimization_chart.png')
    plt.close()
    print("Query optimization chart generated: query_optimization_chart.png")

def main():
    """Main function to execute sample chart generation"""
    try:
        generate_doctor_ranking_chart()
        generate_monthly_appointments_chart()
        generate_query_optimization_chart()
        print("All sample charts generated successfully!")
    except Exception as e:
        print(f"Error generating sample charts: {e}")

if __name__ == "__main__":
    main() 