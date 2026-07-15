-- CorpRide Command Center: Department Costs Summary Query
SELECT 
    d.name as department_name,
    COALESCE(SUM(bil.invoice_amount), 0.0) as total_cost,
    SUM(CASE WHEN b.status = 'Completed' THEN 1 ELSE 0 END) as completed_rides,
    CASE 
        WHEN SUM(CASE WHEN b.status = 'Completed' THEN 1 ELSE 0 END) > 0 
        THEN COALESCE(SUM(bil.invoice_amount), 0.0) / SUM(CASE WHEN b.status = 'Completed' THEN 1 ELSE 0 END)
        ELSE 0.0 
    END as avg_ride_cost
FROM departments d
JOIN employees e ON e.department_id = d.id
JOIN ride_bookings b ON b.employee_id = e.id
LEFT JOIN billing bil ON bil.ride_booking_id = b.id
WHERE b.scheduled_pickup_time >= :start_date 
  AND b.scheduled_pickup_time <= :end_date
  AND (:department_id IS NULL OR e.department_id = :department_id)
  AND (:office_id IS NULL OR e.office_id = :office_id)
  AND (:route_id IS NULL OR b.route_id = :route_id)
GROUP BY d.id, d.name
ORDER BY total_cost DESC;
