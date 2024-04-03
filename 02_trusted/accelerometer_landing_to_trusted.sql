
SELECT 
    accelerometer_landing.* 
FROM accelerometer_landing
INNER JOIN customer_trusted
ON accelerometer_landing.user = customer_trusted.email
limit 10
;

/* we can check the number of resulting rows */
SELECT count(*) FROM
(
SELECT 
    accelerometer_landing.* 
FROM accelerometer_landing
INNER JOIN customer_trusted
ON accelerometer_landing.user = customer_trusted.email
)
;
