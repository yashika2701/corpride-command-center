-- CorpRide Command Center: Fleet Utilization (Trip-Level) Query
WITH trip_runs AS (
    SELECT 
        DATE(rl.actual_pickup_time) as trip_date,
        HOUR(rl.actual_pickup_time) as trip_hour,
        rl.driver_id,
        rl.vehicle_id,
        rl.booking_id,
        r.id as route_id,
        r.name as route_name,
        v.model as vehicle_model,
        v.capacity as vehicle_capacity,
        e.department_id,
        e.office_id
    FROM ride_logs rl
    JOIN vehicles v ON rl.vehicle_id = v.id
    JOIN ride_bookings b ON rl.booking_id = b.id
    JOIN routes r ON b.route_id = r.id
    JOIN employees e ON b.employee_id = e.id
    WHERE rl.status = 'Completed'
      AND b.scheduled_pickup_time >= :start_date 
      AND b.scheduled_pickup_time <= :end_date
      AND (:department_id IS NULL OR e.department_id = :department_id)
      AND (:office_id IS NULL OR e.office_id = :office_id)
      AND (:route_id IS NULL OR b.route_id = :route_id)
),
grouped_trips AS (
    -- Group by same vehicle, driver, date, and hour to represent a single consolidated shuttle trip
    -- In SQLite, DATE and HOUR can be done via strftime, but we write MySQL compatible syntax
    -- To ensure portability across both, we group by vehicle, driver, date, and hour
    SELECT 
        trip_date,
        trip_hour,
        route_name,
        vehicle_model,
        vehicle_capacity,
        COUNT(DISTINCT booking_id) as passenger_count
    FROM trip_runs
    GROUP BY trip_date, trip_hour, route_name, vehicle_model, vehicle_capacity, driver_id, vehicle_id
)
SELECT 
    trip_date,
    trip_hour,
    route_name,
    vehicle_model,
    vehicle_capacity,
    passenger_count,
    (passenger_count * 100.0 / vehicle_capacity) as utilization_rate
FROM grouped_trips;
