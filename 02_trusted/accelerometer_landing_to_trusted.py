import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue import DynamicFrame

def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node accelerometer_landing
accelerometer_landing_node1711875249347 = glueContext.create_dynamic_frame.from_options(format_options={"multiline": False}, connection_type="s3", format="json", connection_options={"paths": ["s3://p3-stedi-lakehouse/accelerometer/landing/"], "recurse": True}, transformation_ctx="accelerometer_landing_node1711875249347")

# Script generated for node customer_landing
customer_landing_node1711875859119 = glueContext.create_dynamic_frame.from_options(format_options={"multiline": False}, connection_type="s3", format="json", connection_options={"paths": ["s3://p3-stedi-lakehouse/customer/landing/"], "recurse": True}, transformation_ctx="customer_landing_node1711875859119")

# Script generated for node accelerometer_landing_to_trusted
SqlQuery0 = '''
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
'''
accelerometer_landing_to_trusted_node1711875317614 = sparkSqlQuery(glueContext, query = SqlQuery0, mapping = {"acc":accelerometer_landing_node1711875249347, "cust":customer_landing_node1711875859119}, transformation_ctx = "accelerometer_landing_to_trusted_node1711875317614")

# Script generated for node accelerometer_trusted
accelerometer_trusted_node1711875384742 = glueContext.write_dynamic_frame.from_options(frame=accelerometer_landing_to_trusted_node1711875317614, connection_type="s3", format="json", connection_options={"path": "s3://p3-stedi-lakehouse/accelerometer/trusted/", "compression": "snappy", "partitionKeys": []}, transformation_ctx="accelerometer_trusted_node1711875384742")

job.commit()