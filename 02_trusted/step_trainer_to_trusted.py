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

# Script generated for node step_trainer_landing
step_trainer_landing_node1711991840954 = glueContext.create_dynamic_frame.from_catalog(
    database="stedi",
    table_name="step_trainer_landing",
    transformation_ctx="step_trainer_landing_node1711991840954",
)

# Script generated for node customer_curated
customer_curated_node1711991778048 = glueContext.create_dynamic_frame.from_catalog(
    database="stedi",
    table_name="customer_curated",
    transformation_ctx="customer_curated_node1711991778048",
)

# Script generated for node step_trainer_landing_to_trusted
SqlQuery0 = """
SELECT 
    step_trainer_landing.* 
FROM step_trainer_landing
INNER JOIN customer_curated
    ON step_trainer_landing.serialNumber = customer_curated.serialNumber
;
"""
step_trainer_landing_to_trusted_node1711991905927 = sparkSqlQuery(
    glueContext,
    query=SqlQuery0,
    mapping={
        "step_trainer_landing": step_trainer_landing_node1711991840954,
        "customer_curated": customer_curated_node1711991778048,
    },
    transformation_ctx="step_trainer_landing_to_trusted_node1711991905927",
)

# Script generated for node step_trainer_trusted
step_trainer_trusted_node1711992013224 = glueContext.getSink(
    path="s3://p3-stedi-lakehouse/step_trainer/trusted/",
    connection_type="s3",
    updateBehavior="LOG",
    partitionKeys=[],
    enableUpdateCatalog=True,
    transformation_ctx="step_trainer_trusted_node1711992013224",
)
step_trainer_trusted_node1711992013224.setCatalogInfo(
    catalogDatabase="stedi", catalogTableName="step_trainer_trusted"
)
step_trainer_trusted_node1711992013224.setFormat("json")
step_trainer_trusted_node1711992013224.writeFrame(
    step_trainer_landing_to_trusted_node1711991905927
)
job.commit()
