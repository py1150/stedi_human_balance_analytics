
CREATE TABLE step_trainer_trusted AS
SELECT 
    acc.* 
FROM step_trainer_landing AS st
INNER JOIN customer_curated AS cust
    ON acc.serialNumber = cust.serialNumber
;