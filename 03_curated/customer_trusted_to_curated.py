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


args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node customer_trusted
customer_trusted_node1711991840954 = glueContext.create_dynamic_frame.from_catalog(
    database="stedi",
    table_name="customer_trusted",
    transformation_ctx="customer_trusted_node1711991840954",
)

# Script generated for node accelerometer_trusted
accelerometer_trusted_node1711991778048 = glueContext.create_dynamic_frame.from_catalog(
    database="stedi",
    table_name="accelerometer_trusted",
    transformation_ctx="accelerometer_trusted_node1711991778048",
)

# Script generated for node customer_trusted_to_curated
SqlQuery0 = """
SELECT DISTINCT
    customer_trusted.*
FROM customer_trusted
INNER JOIN accelerometer_trusted
    ON customer_trusted.email=accelerometer_trusted.user
;
"""
customer_trusted_to_curated_node1711991905927 = sparkSqlQuery(
    glueContext,
    query=SqlQuery0,
    mapping={
        "customer_trusted": customer_trusted_node1711991840954,
        "accelerometer_trusted": accelerometer_trusted_node1711991778048,
    },
    transformation_ctx="customer_trusted_to_curated_node1711991905927",
)

# Script generated for node customer_curated
customer_curated_node1711992013224 = glueContext.getSink(
    path="s3://p3-stedi-lakehouse/customer/curated/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    enableUpdateCatalog=True,
    transformation_ctx="customer_curated_node1711992013224",
)
customer_curated_node1711992013224.setCatalogInfo(
    catalogDatabase="stedi", catalogTableName="customer_curated"
)
customer_curated_node1711992013224.setFormat("json")
customer_curated_node1711992013224.writeFrame(
    customer_trusted_to_curated_node1711991905927
)
job.commit()
