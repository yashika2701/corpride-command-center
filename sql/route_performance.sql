-- CorpRide Command Center: Route Performance Summary Query
SELECT 
    r.id as route_id,
    r.name as route_name,
    COUNT(b.id) as total_bookings,
    SUM(CASE WHEN b.status = 'Completed' THEN 1 ELSE 0 END) as completed_rides,
    CASE 
        WHEN COUNT(b.id) > 0 THEN (SUM(CASE WHEN b.status = 'Completed' THEN 1 ELSE 0 END) * 100.0 / COUNT(b.id))
        ELSE 0.0 
    END as completion_rate,
    COALESCE(AVG(rl.delay_minutes), 0.0) as avg_pickup_delay_mins,
    CASE 
        WHEN SUM(CASE WHEN rl.id IS NOT NULL AND rl.status = 'Completed' THEN 1 ELSE 0 END) > 0 
        THEN (SUM(CASE WHEN rl.status = 'Completed' AND (rl.delay_minutes > 10 OR rl.duration_mins > r.scheduled_duration_mins + 15) THEN 1 ELSE 0 END) * 100.0 / SUM(CASE WHEN rl.id IS NOT NULL AND rl.status = 'Completed' THEN 1 ELSE 0 END))
        ELSE 0.0 
    END as route_sla_breach_rate
FROM routes r
JOIN ride_bookings b ON b.route_id = r.id
LEFT JOIN ride_logs rl ON rl.booking_id = b.id AND rl.status = 'Completed'
LEFT JOIN employees e ON b.employee_id = e.id
WHERE b.scheduled_pickup_time >= :start_date 
  AND b.scheduled_pickup_time <= :end_date
  AND (:department_id IS NULL OR e.department_id = :department_id)
  AND (:office_id IS NULL OR e.office_id = :office_id)
  AND (:route_id IS NULL OR b.route_id = :route_id)
GROUP BY r.id, r.name
ORDER BY route_sla_breach_rate DESC;
