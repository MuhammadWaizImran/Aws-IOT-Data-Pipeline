import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.types import StructType, StructField, FloatType, StringType, LongType

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# DMS exports CSV with NO headers — define schema manually
schema = StructType([
    StructField("id",          LongType(),   True),
    StructField("device_id",   StringType(), True),
    StructField("temperature", FloatType(),  True),
    StructField("humidity",    FloatType(),  True),
    StructField("recorded_at", StringType(), True)
])

# Read all CSV files from S3 Raw Bucket
df = spark.read \
    .option("header", "false") \
    .option("recursiveFileLookup", "true") \
    .schema(schema) \
    .csv("s3://iot-raw-bucket-waiz/")

# Drop null rows
df_enriched = df.dropna()

print(f"Total rows after cleaning: {df_enriched.count()}")

# Write Parquet to S3 Enriched Bucket
df_enriched.write.mode("overwrite").parquet(
    "s3://iot-enriched-bucket-waiz/enriched-data/"
)

job.commit()
