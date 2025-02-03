from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("SimpleTest").getOrCreate()
data = [("Alice", 1), ("Bob", 2), ("Charlie", 3)]
df = spark.createDataFrame(data, ["Name", "Value"])
df.show()
spark.stop()
