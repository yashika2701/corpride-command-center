-- CorpRide Command Center: Database Statistics Query
SELECT 
    (SELECT COUNT(*) FROM employees) as employee_count,
    (SELECT COUNT(*) FROM drivers) as driver_count,
    (SELECT COUNT(*) FROM vehicles) as vehicle_count,
    (SELECT COUNT(*) FROM routes) as route_count,
    (SELECT COUNT(*) FROM ride_bookings) as booking_count,
    (SELECT COUNT(*) FROM ride_logs) as ride_count,
    (SELECT COUNT(*) FROM billing) as billing_count,
    (SELECT COUNT(*) FROM incidents) as incident_count;
