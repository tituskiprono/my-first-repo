import logging
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType

from cassandra.cluster import Cluster

cluster = Cluster(contact_points=['localhost'], protocol_version=5)
session = cluster.connect()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Cassandra keyspace and table creation functions
def create_keyspace(session):
    try:
        session.execute("""
        CREATE KEYSPACE IF NOT EXISTS spark_streams
        WITH replication = {'class':'SimpleStrategy', 'replication_factor':1};
        """)
        logging.info("Keyspace 'spark_streams' created successfully.")
    except Exception as e:
        logging.error(f"Failed to create keyspace: {e}")

def create_table(session):
    try:
        session.execute("""
        CREATE TABLE IF NOT EXISTS spark_streams.created_users(
            user_id UUID PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            gender TEXT,
            address TEXT,
            post_code TEXT,
            email TEXT,
            username TEXT,
            dob TEXT,
            registered_date TEXT,
            phone TEXT,
            picture TEXT
        );
        """)
        logging.info("Table 'created_users' created successfully.")
    except Exception as e:
        logging.error(f"Failed to create table: {e}")

# Cassandra connection setup
def create_cassandra_connection():
    try:
        cluster = Cluster(['localhost'])  # Change to appropriate Cassandra address
        session = cluster.connect()
        logging.info("Connected to Cassandra successfully.")
        return session
    except Exception as e:
        logging.error(f"Failed to connect to Cassandra: {e}")
        return None

# Insert data into Cassandra
def insert_data(session, **kwargs):
    try:
        session.execute("""
        INSERT INTO spark_streams.created_users
        (user_id, first_name, last_name, gender, address, post_code, email, username, dob, registered_date, phone, picture)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            kwargs.get('user_id'), kwargs.get('first_name'), kwargs.get('last_name'), kwargs.get('gender'), 
            kwargs.get('address'), kwargs.get('post_code'), kwargs.get('email'), kwargs.get('username'), 
            kwargs.get('dob'), kwargs.get('registered_date'), kwargs.get('phone'), kwargs.get('picture')
        ))
        logging.info(f"Data inserted for {kwargs.get('first_name')} {kwargs.get('last_name')}.")
    except Exception as e:
        logging.error(f"Failed to insert data: {e}")

# Spark connection setup
def create_spark_connection():
    try:
        spark = SparkSession.builder \
            .appName("SparkDataStreaming") \
            .config("spark.jars.packages", "com.datastax.spark:spark-cassandra-connector_2.13:3.5.1,"
                                            "org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.2") \
            .config("spark.cassandra.connection.host", "localhost") \
            .getOrCreate()
        spark.sparkContext.setLogLevel("DEBUG")
        logging.info("Spark session created successfully.")
        return spark
    except Exception as e:
        logging.error(f"Failed to create Spark session: {e}")
        return None

# Kafka streaming DataFrame setup
def connect_to_kafka(spark):
    try:
        kafka_df = spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "localhost:9092") \
            .option("subscribe", "users_created") \
            .option("startingOffsets", "earliest") \
            .load()
        logging.info("Kafka stream connected successfully.")
        return kafka_df
    except Exception as e:
        logging.error(f"Failed to connect to Kafka stream: {e}")
        return None

# Define schema for Kafka messages
def create_selection_df_from_kafka(kafka_df):
    schema = StructType([
        StructField("id", StringType(), False),
        StructField("first_name", StringType(), False),
        StructField("last_name", StringType(), False),
        StructField("gender", StringType(), False),
        StructField("address", StringType(), False),
        StructField("post_code", StringType(), False),
        StructField("email", StringType(), False),
        StructField("username", StringType(), False),
        StructField("dob", StringType(), False),
        StructField("registered_date", StringType(), False),
        StructField("phone", StringType(), False),
        StructField("picture", StringType(), False)
    ])

    try:
        selection_df = kafka_df.selectExpr("CAST(value AS STRING)") \
            .select(from_json(col("value"), schema).alias("data")) \
            .select("data.*")
        logging.info("Schema applied to Kafka stream.")
        return selection_df
    except Exception as e:
        logging.error(f"Failed to apply schema to Kafka stream: {e}")
        return None

# Main streaming pipeline
if __name__ == "__main__":
    spark_conn = create_spark_connection()

    if spark_conn is not None:
        # connect to kafka with spark connection
        spark_df = connect_to_kafka(spark_conn)
        selection_df = create_selection_df_from_kafka(spark_df)
        session = create_cassandra_connection()

        if session is not None:
            create_keyspace(session)
            create_table(session)

            logging.info("Streaming is being started...")

            streaming_query = (selection_df.writeStream.format("org.apache.spark.sql.cassandra")
                               .option('checkpointLocation', '/tmp/checkpoint')
                               .option('keyspace', 'spark_streams')
                               .option('table', 'created_users')
                               .start())

        streaming_query.awaitTermination()