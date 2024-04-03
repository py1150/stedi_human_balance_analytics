
SELECT 
    step_trainer_landing.* 
FROM step_trainer_landing
INNER JOIN customer_curated
    ON step_trainer_landing.serialNumber = customer_curated.serialNumber
;