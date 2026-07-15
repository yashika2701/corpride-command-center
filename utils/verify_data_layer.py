import os
import sys
from datetime import datetime, timedelta

# Add workspace directory to python path to import database modules
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.query_runner import execute_query_to_df
from utils.seeder import seed_database

def run_verification():
    print("==================================================")
    print("CorpRide Command Center: Data Layer Verification")
    print("==================================================")
    
    # 1. Run seeder
    print("\n[Step 1] Initializing and Seeding Database...")
    seed_database()
    
    # Setup query parameters (covering the 30-day range of seeded data)
    end_date = datetime.now() + timedelta(days=1)
    start_date = end_date - timedelta(days=32)
    
    params = {
        "start_date": start_date.strftime("%Y-%m-%d %H:%M:%S"),
        "end_date": end_date.strftime("%Y-%m-%d %H:%M:%S"),
        "department_id": None,
        "office_id": None,
        "route_id": None
    }
    
    # 2. Verify Global Summary
    print("\n[Step 2] Executing global_summary.sql...")
    df_summary = execute_query_to_df("global_summary", params)
    print("Global Summary Results:")
    print(df_summary.to_string(index=False))
    
    # 3. Verify Fleet Utilization
    print("\n[Step 3] Executing fleet_utilization.sql...")
    df_util = execute_query_to_df("fleet_utilization", params)
    print(f"Total trip runs retrieved: {len(df_util)}")
    if not df_util.empty:
        print("Average Utilization Rate:", round(df_util["utilization_rate"].mean(), 2), "%")
        print("First 5 Trip Runs:")
        print(df_util.head().to_string(index=False))
        
    # 4. Verify Ghost Billing Leakage
    print("\n[Step 4] Executing billing_leakage.sql...")
    df_billing = execute_query_to_df("billing_leakage", params)
    print(f"Total billing anomalies detected: {len(df_billing)}")
    if not df_billing.empty:
        print("Anomaly type breakdown:")
        print(df_billing["anomaly_type"].value_counts())
        print("\nSample billing leaks:")
        print(df_billing.head(5)[["booking_id", "employee_name", "invoice_number", "invoice_amount", "anomaly_type"]].to_string(index=False))
        
    # 5. Verify Congestion Analytics
    print("\n[Step 5] Executing congestion_analytics.sql...")
    df_congestion = execute_query_to_df("congestion_analytics", params)
    print(f"Congestion rows (by hour): {len(df_congestion)}")
    if not df_congestion.empty:
        print(df_congestion[["hour_of_day", "total_bookings", "avg_pickup_delay_mins", "hourly_sla_breach_rate"]].to_string(index=False))
        
    # 6. Verify Safety Incidents
    print("\n[Step 6] Executing safety_incidents.sql...")
    df_safety = execute_query_to_df("safety_incidents", params)
    print(f"Total safety incidents retrieved: {len(df_safety)}")
    if not df_safety.empty:
        print("Incidents list breakdown:")
        print(df_safety["incident_type"].value_counts())
        print("Average incident resolution time:", round(df_safety["resolution_time_minutes"].dropna().mean(), 2), "mins")
        print("\nSample incidents:")
        print(df_safety.head(5)[["incident_type", "severity", "incident_status", "employee_name", "driver_name", "resolution_time_minutes"]].to_string(index=False))
        
    print("\n==================================================")
    print("Verification Completed Successfully!")
    print("==================================================")

if __name__ == "__main__":
    run_verification()
