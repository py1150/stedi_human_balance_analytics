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

# Script generated for node step_trainer_landing
step_trainer_landing_node1711875249347 = glueContext.create_dynamic_frame.from_options(format_options={"multiline": False}, connection_type="s3", format="json", connection_options={"paths": ["s3://p3-stedi-lakehouse/step_trainer/landing/"], "recurse": True}, transformation_ctx="step_trainer_landing_node1711875249347")

# Script generated for node customer_curated
customer_curated_node1711875859119 = glueContext.create_dynamic_frame.from_options(format_options={"multiline": False}, connection_type="s3", format="json", connection_options={"paths": ["s3://p3-stedi-lakehouse/customer/curated/"], "recurse": True}, transformation_ctx="customer_curated_node1711875859119")

# Script generated for node step_trainer_landing_to_trusted
SqlQuery0 = '''
CREATE TABLE step_trainer_trusted AS
SELECT 
    acc.* 
FROM step_trainer_landing AS st
INNER JOIN customer_curated AS cust
    ON acc.serialNumber = cust.serialNumber
;
'''
step_trainer_landing_to_trusted_node1711875317614 = sparkSqlQuery(glueContext, query = SqlQuery0, mapping = {"st":step_trainer_landing_node1711875249347, "cust":customer_curated_node1711875859119}, transformation_ctx = "step_trainer_landing_to_trusted_node1711875317614")

# Script generated for node step_trainer_trusted
step_trainer_trusted_node1711875384742 = glueContext.write_dynamic_frame.from_options(frame=step_trainer_landing_to_trusted_node1711875317614, connection_type="s3", format="json", connection_options={"path": "s3://p3-stedi-lakehouse/step_trainer/trusted/", "compression": "snappy", "partitionKeys": []}, transformation_ctx="step_trainer_trusted_node1711875384742")

job.commit()