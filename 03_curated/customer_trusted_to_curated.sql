CREATE TABLE customer_curated as
SELECT
    cust.*
FROM customer_trusted AS cust
INNER JOIN accelerometer_trusted AS acc
    ON cust.email=acc.email
;
