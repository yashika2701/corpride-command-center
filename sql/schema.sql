-- CorpRide Command Center: Database Schema (MySQL DDL)

CREATE DATABASE IF NOT EXISTS corpride_db;
USE corpride_db;

-- 1. Offices
CREATE TABLE IF NOT EXISTS offices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL
);

-- 2. Departments
CREATE TABLE IF NOT EXISTS departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- 3. Employees
CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department_id INT NOT NULL,
    office_id INT NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (office_id) REFERENCES offices(id)
);

-- 4. Drivers
CREATE TABLE IF NOT EXISTS drivers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    license_number VARCHAR(50) NOT NULL UNIQUE,
    vendor_name VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'Active'
);

-- 5. Vehicles
CREATE TABLE IF NOT EXISTS vehicles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    license_plate VARCHAR(20) NOT NULL UNIQUE,
    model VARCHAR(50) NOT NULL,
    capacity INT NOT NULL,
    vendor_name VARCHAR(100) NOT NULL,
    fuel_type VARCHAR(20) NOT NULL
);

-- 6. Routes
CREATE TABLE IF NOT EXISTS routes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    start_location VARCHAR(100) NOT NULL,
    end_location VARCHAR(100) NOT NULL,
    scheduled_distance_km FLOAT NOT NULL,
    scheduled_duration_mins INT NOT NULL
);

-- 7. Ride Bookings
CREATE TABLE IF NOT EXISTS ride_bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    route_id INT NOT NULL,
    booking_time DATETIME NOT NULL,
    scheduled_pickup_time DATETIME NOT NULL,
    status VARCHAR(20) DEFAULT 'Completed',
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (route_id) REFERENCES routes(id)
);

-- 8. Ride Logs
CREATE TABLE IF NOT EXISTS ride_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NULL,
    driver_id INT NOT NULL,
    vehicle_id INT NOT NULL,
    actual_pickup_time DATETIME NULL,
    actual_drop_time DATETIME NULL,
    distance_travelled_km FLOAT NULL,
    duration_mins INT NULL,
    route_deviation BOOLEAN DEFAULT FALSE,
    delay_minutes INT DEFAULT 0,
    status VARCHAR(20) DEFAULT 'Completed',
    FOREIGN KEY (booking_id) REFERENCES ride_bookings(id),
    FOREIGN KEY (driver_id) REFERENCES drivers(id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
);

-- 9. Billing Table
CREATE TABLE IF NOT EXISTS billing (
    id INT AUTO_INCREMENT PRIMARY KEY,
    invoice_number VARCHAR(50) NOT NULL,
    ride_booking_id INT NOT NULL,
    ride_log_id INT NULL,
    invoice_amount FLOAT NOT NULL,
    billing_status VARCHAR(20) DEFAULT 'Billed',
    FOREIGN KEY (ride_booking_id) REFERENCES ride_bookings(id),
    FOREIGN KEY (ride_log_id) REFERENCES ride_logs(id)
);

-- 10. Incidents Table
CREATE TABLE IF NOT EXISTS incidents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ride_log_id INT NOT NULL,
    incident_type VARCHAR(50) NOT NULL,
    description VARCHAR(255) NULL,
    severity VARCHAR(20) DEFAULT 'Medium',
    status VARCHAR(20) DEFAULT 'Open',
    created_at DATETIME NOT NULL,
    resolved_at DATETIME NULL,
    resolution_notes VARCHAR(255) NULL,
    FOREIGN KEY (ride_log_id) REFERENCES ride_logs(id)
);
