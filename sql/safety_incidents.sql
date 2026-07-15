-- CorpRide Command Center: Safety Incidents & Escalations Query
SELECT 
    i.id as incident_id,
    i.incident_type,
    i.severity,
    i.status as incident_status,
    i.description,
    i.created_at,
    i.resolved_at,
    CASE 
        WHEN i.resolved_at IS NOT NULL THEN 
            -- Calculate resolution time in minutes
            -- Works for MySQL and supports general datediff / timestampdiff style
            TIMESTAMPDIFF(MINUTE, i.created_at, i.resolved_at)
        ELSE NULL 
    END as resolution_time_minutes,
    i.resolution_notes,
    rl.id as ride_log_id,
    rl.route_deviation,
    rl.delay_minutes as ride_delay_minutes,
    e.name as employee_name,
    d.name as department_name,
    dr.name as driver_name,
    v.license_plate,
    r.name as route_name
FROM incidents i
JOIN ride_logs rl ON i.ride_log_id = rl.id
JOIN ride_bookings b ON rl.booking_id = b.id
JOIN employees e ON b.employee_id = e.id
JOIN departments d ON e.department_id = d.id
JOIN drivers dr ON rl.driver_id = dr.id
JOIN vehicles v ON rl.vehicle_id = v.id
JOIN routes r ON b.route_id = r.id
WHERE b.scheduled_pickup_time >= :start_date 
  AND b.scheduled_pickup_time <= :end_date
  AND (:department_id IS NULL OR e.department_id = :department_id)
  AND (:office_id IS NULL OR e.office_id = :office_id)
  AND (:route_id IS NULL OR b.route_id = :route_id)
ORDER BY i.created_at DESC;
