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

# Script generated for node customer_landing
customer_landing_node1711959758722 = glueContext.create_dynamic_frame.from_catalog(
    database="stedi",
    table_name="customer_landing",
    transformation_ctx="customer_landing_node1711959758722",
)

# Script generated for node customer_landing_to_trusted
SqlQuery0 = """
SELECT * FROM customer_landing WHERE shareWithResearchAsOfDate IS NOT NULL;
"""
customer_landing_to_trusted_node1711961375644 = sparkSqlQuery(
    glueContext,
    query=SqlQuery0,
    mapping={"customer_landing": customer_landing_node1711959758722},
    transformation_ctx="customer_landing_to_trusted_node1711961375644",
)

# Script generated for node customer_trusted
customer_trusted_node1711959887476 = glueContext.getSink(
    path="s3://p3-stedi-lakehouse/customer/trusted/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    enableUpdateCatalog=True,
    transformation_ctx="customer_trusted_node1711959887476",
)
customer_trusted_node1711959887476.setCatalogInfo(
    catalogDatabase="stedi", catalogTableName="customer_trusted"
)
customer_trusted_node1711959887476.setFormat("json")
customer_trusted_node1711959887476.writeFrame(
    customer_landing_to_trusted_node1711961375644
)
job.commit()

