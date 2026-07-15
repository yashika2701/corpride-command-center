import os
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database.connection import Base, engine, SessionLocal
from database.models import Office, Department, Employee, Driver, Vehicle, Route, RideBooking, RideLog, Billing, Incident

# Ensure database tables exist
Base.metadata.create_all(bind=engine)

def seed_database():
    session = SessionLocal()
    
    # 1. Clean existing data
    session.query(Incident).delete()
    session.query(Billing).delete()
    session.query(RideLog).delete()
    session.query(RideBooking).delete()
    session.query(Route).delete()
    session.query(Employee).delete()
    session.query(Department).delete()
    session.query(Office).delete()
    session.query(Driver).delete()
    session.query(Vehicle).delete()
    session.commit()
    
    print("Cleaned existing database records.")
    
    # Set seed for repeatability
    random.seed(42)
    
    # 2. Seed Offices
    offices = [
        Office(name="Headquarters", city="Bangalore"),
        Office(name="Tech Hub", city="Hyderabad"),
        Office(name="Sales Office", city="Mumbai")
    ]
    session.add_all(offices)
    session.commit()
    
    # 3. Seed Departments
    departments = [
        Department(name="Engineering"),
        Department(name="Operations"),
        Department(name="Finance"),
        Department(name="HR & Safety"),
        Department(name="Sales"),
        Department(name="Customer Support")
    ]
    session.add_all(departments)
    session.commit()
    
    # 4. Seed Employees
    names = [
        "Amit Sharma", "Priyanka Patel", "Rajesh Kumar", "Sunita Rao", "Vijay Singh",
        "Ananya Reddy", "Vikram Aditya", "Neha Gupta", "Sanjay Dutt", "Meera Nair",
        "Rohan Mehta", "Pooja Hegde", "Arjun Kapoor", "Karan Johar", "Aditi Rao",
        "Deepak Verma", "Jyoti Mishra", "Rahul Dravid", "Sachin Tendulkar", "Kunal Bahl"
    ]
    
    employees = []
    for i, name in enumerate(names):
        emp = Employee(
            name=name,
            department_id=random.choice(departments).id,
            office_id=random.choice(offices).id
        )
        employees.append(emp)
    session.add_all(employees)
    session.commit()
    
    # 5. Seed Drivers
    drivers_list = [
        Driver(name="Ramesh Kumar", license_number="DL1420230001", vendor_name="FleetCorp", status="Active"),
        Driver(name="Suresh Singh", license_number="DL1420230002", vendor_name="FleetCorp", status="Active"),
        Driver(name="Madan Lal", license_number="DL1420230003", vendor_name="SafeRide Logistics", status="Active"),
        Driver(name="Jagdish Prasad", license_number="DL1420230004", vendor_name="SafeRide Logistics", status="Active"),
        Driver(name="Harish Chandra", license_number="DL1420230005", vendor_name="FleetCorp", status="Active"),
        Driver(name="Satnam Singh", license_number="DL1420230006", vendor_name="SafeRide Logistics", status="Inactive")
    ]
    session.add_all(drivers_list)
    session.commit()
    
    # 6. Seed Vehicles
    vehicles_list = [
        Vehicle(license_plate="KA03HA1234", model="Toyota Innova", capacity=7, vendor_name="FleetCorp", fuel_type="Diesel"),
        Vehicle(license_plate="KA03HA5678", model="Toyota Camry", capacity=4, vendor_name="FleetCorp", fuel_type="Petrol"),
        Vehicle(license_plate="KA03HB9012", model="Ford Transit (Van)", capacity=12, vendor_name="SafeRide Logistics", fuel_type="CNG"),
        Vehicle(license_plate="KA03HB3456", model="Tata Winger (Van)", capacity=12, vendor_name="SafeRide Logistics", fuel_type="CNG"),
        Vehicle(license_plate="KA03HC7890", model="Mahindra Verito", capacity=4, vendor_name="FleetCorp", fuel_type="Electric"),
        Vehicle(license_plate="KA03HC2345", model="Electric Shuttle", capacity=15, vendor_name="SafeRide Logistics", fuel_type="Electric")
    ]
    session.add_all(vehicles_list)
    session.commit()
    
    # 7. Seed Routes
    routes_list = [
        Route(name="HQ - Whitefield Metro", start_location="Headquarters", end_location="Whitefield Metro Station", scheduled_distance_km=12.5, scheduled_duration_mins=30),
        Route(name="Tech Hub - Hitec City", start_location="Tech Hub", end_location="Hitec City Metro Station", scheduled_distance_km=8.2, scheduled_duration_mins=20),
        Route(name="Sales Office - Airport", start_location="Sales Office", end_location="Airport T2 Terminal", scheduled_distance_km=28.0, scheduled_duration_mins=60),
        Route(name="HQ - Electronic City", start_location="Headquarters", end_location="Electronic City Phase 1", scheduled_distance_km=22.0, scheduled_duration_mins=45)
    ]
    session.add_all(routes_list)
    session.commit()
    
    # 8. Generate bookings, logs, and billing for the last 30 days
    base_date = datetime.now() - timedelta(days=30)
    
    # Trackers for ghost billing & incidents
    all_bookings = []
    
    print("Generating ride bookings, logs, and invoices...")
    
    for day in range(30):
        current_date = base_date + timedelta(days=day)
        if current_date.weekday() >= 5:  # Skip weekends to simulate corporate work week
            continue
            
        # Define time windows: Morning Peak (8-10), Midday Off-Peak (12-14), Evening Peak (17-19)
        time_windows = [
            ("Morning Peak", 8, 10),
            ("Midday Off-Peak", 12, 14),
            ("Evening Peak", 17, 19)
        ]
        
        invoice_counter = day * 100
        
        for window_name, start_hr, end_hr in time_windows:
            # Determine booking density based on window type (Scenario B: Peak hour congestion)
            if "Peak" in window_name:
                num_bookings = random.randint(12, 18)
            else:
                num_bookings = random.randint(3, 6) # Scenario C: Underutilized fleet windows
                
            for b_idx in range(num_bookings):
                invoice_counter += 1
                
                # Pick a random employee and route
                employee = random.choice(employees)
                route = random.choice(routes_list)
                
                # Setup scheduled times
                hr = random.randint(start_hr, end_hr - 1)
                mins = random.randint(0, 59)
                scheduled_time = current_date.replace(hour=hr, minute=mins, second=0, microsecond=0)
                booking_time = scheduled_time - timedelta(hours=random.randint(1, 24))
                
                # Booking status
                # Standard completion rate, lower during peak congestion
                is_peak = "Peak" in window_name
                cancelled_prob = 0.15 if is_peak else 0.05
                no_show_prob = 0.05 if is_peak else 0.02
                
                roll = random.random()
                if roll < cancelled_prob:
                    b_status = "Cancelled"
                elif roll < (cancelled_prob + no_show_prob):
                    b_status = "No-Show"
                else:
                    b_status = "Completed"
                    
                booking = RideBooking(
                    employee_id=employee.id,
                    route_id=route.id,
                    booking_time=booking_time,
                    scheduled_pickup_time=scheduled_time,
                    status=b_status
                )
                session.add(booking)
                session.flush() # Populate ID
                
                all_bookings.append((booking, window_name, is_peak, route, invoice_counter))
                
    # Commit bookings
    session.commit()
    
    # 9. Generate Logs and Billing based on Bookings
    # Map to hold active driver/vehicle runs to simulate grouping passengers
    # Grouping is done by (window_name, day, driver_id, vehicle_id)
    active_runs = {}
    
    # We will pick drivers and vehicles
    active_drivers = [d for d in drivers_list if d.status == "Active"]
    active_vehicles = vehicles_list
    
    # Separate runs for Scenario C (midday underutilization):
    # Midday runs will be assigned 12-seater vans but only 1 passenger.
    
    for booking, window, is_peak, route, inv_idx in all_bookings:
        day_str = booking.scheduled_pickup_time.strftime("%Y-%m-%d")
        
        # Determine driver and vehicle
        # Scenario C: For Midday Off-Peak, use large vans but only put 1 person per vehicle
        if window == "Midday Off-Peak":
            driver = random.choice(active_drivers)
            # Pick a van (capacity = 12) to create underutilization anomaly
            vans = [v for v in active_vehicles if v.capacity == 12]
            vehicle = random.choice(vans) if vans else random.choice(active_vehicles)
        else:
            driver = random.choice(active_drivers)
            vehicle = random.choice(active_vehicles)
            
        # Create or group ride logs
        # Completed rides get logs
        if booking.status == "Completed":
            # Add delay details (Scenario B: Peak hour congestion)
            if is_peak:
                # Delays between 8 to 25 mins
                delay = random.randint(8, 25)
                # Durations are longer than scheduled duration by 10 to 30 mins
                duration = route.scheduled_duration_mins + random.randint(10, 30)
                distance = route.scheduled_distance_km + random.uniform(0.5, 2.5)
            else:
                # Delays between 0 to 5 mins
                delay = random.randint(0, 5)
                duration = route.scheduled_duration_mins + random.randint(-2, 5)
                distance = route.scheduled_distance_km + random.uniform(-0.2, 0.5)
                
            # Randomly trigger Route Deviation (monitored metric)
            deviation = random.random() < 0.08 # 8% chance of route deviation
            
            actual_pickup = booking.scheduled_pickup_time + timedelta(minutes=delay)
            actual_drop = actual_pickup + timedelta(minutes=duration)
            
            ride_log = RideLog(
                booking_id=booking.id,
                driver_id=driver.id,
                vehicle_id=vehicle.id,
                actual_pickup_time=actual_pickup,
                actual_drop_time=actual_drop,
                distance_travelled_km=round(distance, 1),
                duration_mins=duration,
                route_deviation=deviation,
                delay_minutes=delay,
                status="Completed"
            )
            session.add(ride_log)
            session.flush()
            
            # Standard billing for completed rides
            invoice_amount = round(50.0 + (distance * 12.0) + (delay * 2.0), 2)
            billing = Billing(
                invoice_number=f"INV-{(booking.scheduled_pickup_time.year % 100):02d}{inv_idx:05d}",
                ride_booking_id=booking.id,
                ride_log_id=ride_log.id,
                invoice_amount=invoice_amount,
                billing_status="Billed"
            )
            session.add(billing)
            
            # Scenario D: Safety Incident Escalation
            # If delay is severe (>20m) or deviation occurs during peak, trigger safety SOS/Incident
            if (deviation or delay > 22) and random.random() < 0.4:
                incident_type = "SOS" if deviation else "Delay"
                severity = "High" if incident_type == "SOS" else "Medium"
                
                # SOS details
                desc = "SOS panic button pressed" if incident_type == "SOS" else "Severe commute delay reported"
                if incident_type == "SOS":
                    desc += " due to unauthorized route deviation"
                    
                # Some are resolved, some are open (active escalation)
                # Let's keep 2 SOS incidents open (unresolved)
                is_resolved = random.random() < 0.7
                resolved_time = None
                status = "Open"
                notes = None
                
                if is_resolved:
                    res_delay = random.randint(10, 45) # 10 to 45 mins resolution
                    resolved_time = actual_pickup + timedelta(minutes=res_delay)
                    status = "Resolved"
                    notes = "Checked by control room. Passenger confirmed safe."
                    
                incident = Incident(
                    ride_log_id=ride_log.id,
                    incident_type=incident_type,
                    description=desc,
                    severity=severity,
                    status=status,
                    created_at=actual_pickup,
                    resolved_at=resolved_time,
                    resolution_notes=notes
                )
                session.add(incident)
                
        else:
            # For Cancelled / No-show bookings, normally there is NO ride log
            # Scenario A: Ghost Billing
            # Let's deliberately charge invoice records for 10% of Cancelled/No-Show rides!
            if random.random() < 0.25: # 25% of cancelled/no-show rides get billed!
                ghost_amount = round(random.uniform(150.0, 300.0), 2)
                billing = Billing(
                    invoice_number=f"INV-{(booking.scheduled_pickup_time.year % 100):02d}{inv_idx:05d}",
                    ride_booking_id=booking.id,
                    ride_log_id=None,  # Crucial: No ride log associated (Ghost)
                    invoice_amount=ghost_amount,
                    billing_status="Billed"  # Marked billed
                )
                session.add(billing)
                
                # Duplicate Billing: For some of these ghost bills, write a duplicate entry
                if random.random() < 0.3:
                    session.add(Billing(
                        invoice_number=f"INV-{(booking.scheduled_pickup_time.year % 100):02d}{inv_idx:05d}-DUP",
                        ride_booking_id=booking.id,
                        ride_log_id=None,
                        invoice_amount=ghost_amount, # Double charge
                        billing_status="Billed"
                    ))
                    
    session.commit()
    print("Database seeding completed successfully.")
    
    # Print out summary counts
    print(f"Total bookings seeded: {session.query(RideBooking).count()}")
    print(f"Total completed ride logs: {session.query(RideLog).count()}")
    print(f"Total billing records: {session.query(Billing).count()}")
    print(f"Total safety incidents: {session.query(Incident).count()}")
    
    session.close()

if __name__ == "__main__":
    seed_database()
