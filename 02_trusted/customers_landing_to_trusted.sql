/*
Sanitize the Customer data from the Website (Landing Zone) and only store the Customer Records who agreed to share their data for research purposes (Trusted Zone) - creating a Glue Table called customer_trusted.

source
s3://p3-stedi-lakehouse/customer/landing/
target
s3://p3-stedi-lakehouse/customer/trusted/
*/

/*
Input sources: customer_landing
SQL aliases customer_landing
*/
SELECT * FROM customer_landing WHERE shareWithResearchAsOfDate IS NOT NULL;