from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json,col
from pyspark.sql.types import StructType,StringType,DoubleType,TimestampType

spark = SparkSession.builder \
       .appName("KafkaSparkIntergration") \
       .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.1") \
       .getOrCreate()

kafka_brokers = "localhost:9092"

schema = StructType() \
       .add("symbol", StringType())\
       .add("price",DoubleType()) \
       .add("Timestamp",TimestampType())

df = spark\
     .readStream\
     .format('kafka')\
     .option('kafka.bootstrap.servers',kafka_brokers)\
     .option('subscribe','stock_prices')\
     .load()

df = df.selectExpr("CAST(value AS STRING) as json")\
     .select(from_json(col("json"),schema).alias("data"))\
     .select('data.*')

query = df \
   .writestream \
   .outputMode('append') \
   .format('console') \
   .option('truncate','false') \
   .start()

query.awaitTermination()
