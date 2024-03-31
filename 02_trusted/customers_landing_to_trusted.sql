/*
Sanitize the Customer data from the Website (Landing Zone) and only store the Customer Records who agreed to share their data for research purposes (Trusted Zone) - creating a Glue Table called customer_trusted.

source
s3://p3-stedi-lakehouse/customer/landing/
target
s3://p3-stedi-lakehouse/customer/trusted/
*/

CREATE TABLE customers_trusted AS
SELECT * FROM customers_landing WHERE shareWithResearchAsOfDate IS NOT NULL;