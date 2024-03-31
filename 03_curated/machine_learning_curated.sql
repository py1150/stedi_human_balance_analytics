

CREATE TABLE machine_learning_curated AS
SELECT 
    trainer.*
    ,acc.*
FROM step_trainer_trusted as trainer
INNER JOIN accelerometer_trusted as acc
    ON trainer.sensorReadingTime=acc.timestamp    
;