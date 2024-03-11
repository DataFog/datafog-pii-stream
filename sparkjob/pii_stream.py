from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

from datafog import PresidioEngine as presidio


def redact(input):
    return presidio.scan(str(input))


spark = SparkSession.builder.appName("Tickets Streamer").getOrCreate()

redact_udf = udf(redact, StringType())

df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "redpanda-1:9092")
    .option("subscribe", "tickets")
    .load()
)

jsonschema = StructType(
    [
        StructField("name", StringType()),
        StructField("request", StringType()),
        StructField("priority", IntegerType()),
        StructField("comment", StringType()),
        StructField("request_id", StringType()),
    ]
)


df = (
    df.select(from_json(col("value").cast(StringType()), jsonschema).alias("value"))
    .select("value.*")
    .withColumn("request_id", col("request_id"))
    .withColumn("PII_found", redact_udf(col("comment")))
    .withColumn("value", to_json(struct(col("request_id"), col("PII_found"))))
)


query = (
    df.writeStream.format("kafka")
    .option("kafka.bootstrap.servers", "redpanda-1:9092")
    .option("topic", "pii-detection")
    .option("checkpointLocation", "/home/muser/chkpoint")
    .start()
)

query.awaitTermination()
