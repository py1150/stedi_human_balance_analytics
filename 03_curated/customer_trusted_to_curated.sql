SELECT DISTINCT
    customer_trusted.*
FROM customer_trusted
INNER JOIN acelerometer_trusted
    ON customer_trusted.email=acelerometer_trusted.user
;
