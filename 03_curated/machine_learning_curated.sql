

SELECT 
    step_trainer_trusted.*
    ,accelerometer_trusted.*
FROM step_trainer_trusted
INNER JOIN accelerometer_trusted
    ON step_trainer_trusted.sensorReadingTime=accelerometer_trusted.timestamp  
;    