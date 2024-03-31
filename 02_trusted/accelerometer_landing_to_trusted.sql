/*
Sanitize the Accelerometer data from the Mobile App (Landing Zone) - and only store Accelerometer Readings from customers who agreed to share their data for research purposes (Trusted Zone) - creating a Glue Table called accelerometer_trusted.
*/

/*
Hint: Use Transform - SQL Query nodes whenever you can. Other node types may give you unexpected results.

For example, rather than a Join node, you may use a SQL node that has two parents, then join them through a SQL query.
*/

/*
Landing
Customer: 956
Accelerometer: 81273
Step Trainer: 28680
Trusted
Customer: 482
Accelerometer: 40981
Step Trainer: 14460
Curated
Customer: 482
Machine Learning: 43681

source:
s3://p3-stedi-lakehouse/accelerometer/landing/
target:
s3://p3-stedi-lakehouse/accelerometer/trusted/
*/


CREATE TABLE acceleromter_trusted AS
SELECT 
    acc.* 
FROM accelerometer_landing AS acc
INNER JOIN (
    SELECT 
        * 
    FROM customers_landing where shareWithResearchAsOfDate IS NOT NULL;      
) AS cust
/*alternative*/
INNER JOIN customers_trusted cust
ON acc.user = cust.email
;