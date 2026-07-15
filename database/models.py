from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .connection import Base

class Office(Base):
    __tablename__ = "offices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)

    employees = relationship("Employee", back_populates="office")


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    employees = relationship("Employee", back_populates="department")


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    office_id = Column(Integer, ForeignKey("offices.id"), nullable=False)

    department = relationship("Department", back_populates="employees")
    office = relationship("Office", back_populates="employees")
    bookings = relationship("RideBooking", back_populates="employee")


class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    license_number = Column(String(50), nullable=False, unique=True)
    vendor_name = Column(String(100), nullable=False)
    status = Column(String(20), default="Active")  # Active, Inactive

    ride_logs = relationship("RideLog", back_populates="driver")


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    license_plate = Column(String(20), nullable=False, unique=True)
    model = Column(String(50), nullable=False)
    capacity = Column(Integer, nullable=False)
    vendor_name = Column(String(100), nullable=False)
    fuel_type = Column(String(20), nullable=False)  # Electric, Diesel, Petrol, CNG

    ride_logs = relationship("RideLog", back_populates="vehicle")


class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    start_location = Column(String(100), nullable=False)
    end_location = Column(String(100), nullable=False)
    scheduled_distance_km = Column(Float, nullable=False)
    scheduled_duration_mins = Column(Integer, nullable=False)

    bookings = relationship("RideBooking", back_populates="route")


class RideBooking(Base):
    __tablename__ = "ride_bookings"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)
    booking_time = Column(DateTime, nullable=False)
    scheduled_pickup_time = Column(DateTime, nullable=False)
    status = Column(String(20), default="Completed")  # Completed, Cancelled, No-Show

    employee = relationship("Employee", back_populates="bookings")
    route = relationship("Route", back_populates="bookings")
    ride_logs = relationship("RideLog", back_populates="booking")
    billing_records = relationship("Billing", back_populates="booking")


class RideLog(Base):
    __tablename__ = "ride_logs"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("ride_bookings.id"), nullable=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    actual_pickup_time = Column(DateTime, nullable=True)
    actual_drop_time = Column(DateTime, nullable=True)
    distance_travelled_km = Column(Float, nullable=True)
    duration_mins = Column(Integer, nullable=True)
    route_deviation = Column(Boolean, default=False)
    delay_minutes = Column(Integer, default=0)
    status = Column(String(20), default="Completed")  # Completed, Canceled

    booking = relationship("RideBooking", back_populates="ride_logs")
    driver = relationship("Driver", back_populates="ride_logs")
    vehicle = relationship("Vehicle", back_populates="ride_logs")
    billing_records = relationship("Billing", back_populates="ride_log")
    incidents = relationship("Incident", back_populates="ride_log")


class Billing(Base):
    __tablename__ = "billing"

    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String(50), nullable=False)
    ride_booking_id = Column(Integer, ForeignKey("ride_bookings.id"), nullable=False)
    ride_log_id = Column(Integer, ForeignKey("ride_logs.id"), nullable=True)
    invoice_amount = Column(Float, nullable=False)
    billing_status = Column(String(20), default="Billed")  # Billed, Disputed, Paid

    booking = relationship("RideBooking", back_populates="billing_records")
    ride_log = relationship("RideLog", back_populates="billing_records")


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    ride_log_id = Column(Integer, ForeignKey("ride_logs.id"), nullable=False)
    incident_type = Column(String(50), nullable=False)  # SOS, Delay, Deviation, Accident
    description = Column(String(255), nullable=True)
    severity = Column(String(20), default="Medium")  # Low, Medium, High
    status = Column(String(20), default="Open")  # Open, Investigating, Resolved
    created_at = Column(DateTime, nullable=False)
    resolved_at = Column(DateTime, nullable=True)
    resolution_notes = Column(String(255), nullable=True)

    ride_log = relationship("RideLog", back_populates="incidents")
