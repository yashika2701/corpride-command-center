-- CorpRide Command Center: Billing Leakage & Ghost Billing Query
-- 1. Cancelled or No-Show rides that were invoiced
SELECT 
    b.id as booking_id,
    e.name as employee_name,
    d.name as department_name,
    bil.invoice_number,
    bil.invoice_amount,
    b.status as booking_status,
    COALESCE(rl.status, 'No Log') as ride_log_status,
    'Cancelled/No-Show Ride Invoiced' as anomaly_type,
    b.scheduled_pickup_time as scheduled_time
FROM billing bil
JOIN ride_bookings b ON bil.ride_booking_id = b.id
JOIN employees e ON b.employee_id = e.id
JOIN departments d ON e.department_id = d.id
LEFT JOIN ride_logs rl ON bil.ride_log_id = rl.id
WHERE (b.status IN ('Cancelled', 'No-Show') OR (rl.status = 'Canceled' AND rl.id IS NOT NULL))
  AND bil.billing_status = 'Billed'
  AND b.scheduled_pickup_time >= :start_date 
  AND b.scheduled_pickup_time <= :end_date
  AND (:department_id IS NULL OR e.department_id = :department_id)
  AND (:office_id IS NULL OR e.office_id = :office_id)

UNION ALL

-- 2. Duplicate invoicing (multiple bills for the same booking ID)
SELECT 
    b.id as booking_id,
    e.name as employee_name,
    d.name as department_name,
    bil.invoice_number,
    bil.invoice_amount,
    b.status as booking_status,
    COALESCE(rl.status, 'No Log') as ride_log_status,
    'Duplicate Invoice' as anomaly_type,
    b.scheduled_pickup_time as scheduled_time
FROM billing bil
JOIN (
    -- Subquery to find bookings with more than one billing record
    SELECT ride_booking_id
    FROM billing
    GROUP BY ride_booking_id
    HAVING COUNT(id) > 1
) dup ON bil.ride_booking_id = dup.ride_booking_id
JOIN ride_bookings b ON bil.ride_booking_id = b.id
JOIN employees e ON b.employee_id = e.id
JOIN departments d ON e.department_id = d.id
LEFT JOIN ride_logs rl ON bil.ride_log_id = rl.id
WHERE b.scheduled_pickup_time >= :start_date 
  AND b.scheduled_pickup_time <= :end_date
  AND (:department_id IS NULL OR e.department_id = :department_id)
  AND (:office_id IS NULL OR e.office_id = :office_id)
ORDER BY scheduled_time DESC;
