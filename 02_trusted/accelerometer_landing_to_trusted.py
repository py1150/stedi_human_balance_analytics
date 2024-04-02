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
accelerometer_landing_node1711991778048 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="accelerometer_landing", transformation_ctx="accelerometer_landing_node1711991778048")

# Script generated for node customer_trusted
customer_trusted_node1712035179261 = glueContext.create_dynamic_frame.from_options(format_options={"multiline": False}, connection_type="s3", format="json", connection_options={"paths": ["s3://p3-stedi-lakehouse/customer/trusted/"], "recurse": True}, transformation_ctx="customer_trusted_node1712035179261")

# Script generated for node accelerometer_landing_to_trusted
SqlQuery0 = '''
SELECT 
    accelerometer_landing.* 
FROM accelerometer_landing
INNER JOIN customer_trusted
ON accelerometer_landing.user = customer_trusted.email
;
'''
accelerometer_landing_to_trusted_node1711991905927 = sparkSqlQuery(glueContext, query = SqlQuery0, mapping = {"accelerometer_landing":accelerometer_landing_node1711991778048, "":customer_trusted_node1712035179261}, transformation_ctx = "accelerometer_landing_to_trusted_node1711991905927")

# Script generated for node accelerometer_trusted
accelerometer_trusted_node1711992013224 = glueContext.getSink(path="s3://p3-stedi-lakehouse/accelerometer/trusted/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="accelerometer_trusted_node1711992013224")
accelerometer_trusted_node1711992013224.setCatalogInfo(catalogDatabase="stedi",catalogTableName="accelerometer_trusted")
accelerometer_trusted_node1711992013224.setFormat("json")
accelerometer_trusted_node1711992013224.writeFrame(accelerometer_landing_to_trusted_node1711991905927)
job.commit()