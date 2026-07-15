-- CorpRide Command Center: Safety Metrics Summary Query
SELECT 
    COUNT(rl.id) as total_completed_rides,
    SUM(CASE WHEN rl.route_deviation = 1 THEN 1 ELSE 0 END) as deviation_rides_count,
    CASE 
        WHEN COUNT(rl.id) > 0 THEN (SUM(CASE WHEN rl.route_deviation = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(rl.id))
        ELSE 0.0 
    END as route_deviation_rate,
    (SELECT COUNT(*) FROM incidents i 
     JOIN ride_logs rl2 ON i.ride_log_id = rl2.id
     JOIN ride_bookings b2 ON rl2.booking_id = b2.id
     JOIN employees e2 ON b2.employee_id = e2.id
     WHERE b2.scheduled_pickup_time >= :start_date 
       AND b2.scheduled_pickup_time <= :end_date
       AND (:department_id IS NULL OR e2.department_id = :department_id)
       AND (:office_id IS NULL OR e2.office_id = :office_id)
       AND (:route_id IS NULL OR b2.route_id = :route_id)
    ) as total_incidents,
    (SELECT COUNT(*) FROM incidents i 
     JOIN ride_logs rl2 ON i.ride_log_id = rl2.id
     JOIN ride_bookings b2 ON rl2.booking_id = b2.id
     JOIN employees e2 ON b2.employee_id = e2.id
     WHERE i.incident_type = 'SOS'
       AND b2.scheduled_pickup_time >= :start_date 
       AND b2.scheduled_pickup_time <= :end_date
       AND (:department_id IS NULL OR e2.department_id = :department_id)
       AND (:office_id IS NULL OR e2.office_id = :office_id)
       AND (:route_id IS NULL OR b2.route_id = :route_id)
    ) as total_sos,
    (SELECT COUNT(*) FROM incidents i 
     JOIN ride_logs rl2 ON i.ride_log_id = rl2.id
     JOIN ride_bookings b2 ON rl2.booking_id = b2.id
     JOIN employees e2 ON b2.employee_id = e2.id
     WHERE i.incident_type = 'SOS' AND i.status != 'Resolved'
       AND b2.scheduled_pickup_time >= :start_date 
       AND b2.scheduled_pickup_time <= :end_date
       AND (:department_id IS NULL OR e2.department_id = :department_id)
       AND (:office_id IS NULL OR e2.office_id = :office_id)
       AND (:route_id IS NULL OR b2.route_id = :route_id)
    ) as active_sos
FROM ride_logs rl
JOIN ride_bookings b ON rl.booking_id = b.id
JOIN employees e ON b.employee_id = e.id
WHERE rl.status = 'Completed'
  AND b.scheduled_pickup_time >= :start_date 
  AND b.scheduled_pickup_time <= :end_date
  AND (:department_id IS NULL OR e.department_id = :department_id)
  AND (:office_id IS NULL OR e.office_id = :office_id)
  AND (:route_id IS NULL OR b.route_id = :route_id);
