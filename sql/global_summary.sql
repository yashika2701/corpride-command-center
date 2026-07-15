-- CorpRide Command Center: Global Summary Metrics Query
SELECT 
    COUNT(b.id) as total_bookings,
    SUM(CASE WHEN b.status = 'Completed' THEN 1 ELSE 0 END) as completed_bookings,
    CASE 
        WHEN COUNT(b.id) > 0 THEN (SUM(CASE WHEN b.status = 'Completed' THEN 1 ELSE 0 END) * 100.0 / COUNT(b.id))
        ELSE 0.0 
    END as completion_rate,
    COALESCE(SUM(bil.invoice_amount), 0.0) as total_cost,
    CASE 
        WHEN SUM(CASE WHEN b.status = 'Completed' THEN 1 ELSE 0 END) > 0 
        THEN COALESCE(SUM(bil.invoice_amount), 0.0) / SUM(CASE WHEN b.status = 'Completed' THEN 1 ELSE 0 END)
        ELSE 0.0 
    END as cost_per_ride,
    COALESCE(AVG(rl.delay_minutes), 0.0) as avg_pickup_delay,
    CASE 
        WHEN SUM(CASE WHEN rl.id IS NOT NULL AND rl.status = 'Completed' THEN 1 ELSE 0 END) > 0 
        THEN (SUM(CASE WHEN rl.status = 'Completed' AND (rl.delay_minutes > 10 OR rl.duration_mins > r.scheduled_duration_mins + 15) THEN 1 ELSE 0 END) * 100.0 / SUM(CASE WHEN rl.id IS NOT NULL AND rl.status = 'Completed' THEN 1 ELSE 0 END))
        ELSE 0.0 
    END as sla_breach_rate
FROM ride_bookings b
LEFT JOIN ride_logs rl ON rl.booking_id = b.id AND rl.status = 'Completed'
LEFT JOIN routes r ON b.route_id = r.id
LEFT JOIN employees e ON b.employee_id = e.id
LEFT JOIN billing bil ON bil.ride_booking_id = b.id
WHERE b.scheduled_pickup_time >= :start_date 
  AND b.scheduled_pickup_time <= :end_date
  AND (:department_id IS NULL OR e.department_id = :department_id)
  AND (:office_id IS NULL OR e.office_id = :office_id)
  AND (:route_id IS NULL OR b.route_id = :route_id);
