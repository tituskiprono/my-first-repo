import mysql.connector
import json
from kafka import KafkaConsumer
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# MySQL database connection setup
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Tituskiprono123*",
    database="Crypto_db"
)

cursor = connection.cursor()

# Kafka consumer setup
consumer = KafkaConsumer(
    'my_topic', 
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    group_id='my_group',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

insert_query = """INSERT INTO crypto(symbol, timestamp, open, high, low, close, volume, trade_count, vwap)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

batch_size = 100  # Set batch size to commit after processing 100 rows

try:
    logging.info("Starting Kafka consumer...")
    for message in consumer:
        logging.info("Received message from Kafka")

        try:
            data = message.value

            if 'data' in data and isinstance(data['data'], list):
                # Convert the data to a DataFrame
                df = pd.DataFrame(data['data'])
                logging.info("Received data:\n%s", df.head())

                # Insert data into MySQL database
                for index, row in df.iterrows():
                    try:
                        cursor.execute(insert_query, (
                            row['symbol'],
                            row['timestamp'],
                            row['open'],
                            row['high'],
                            row['low'],
                            row['close'],
                            row['volume'],
                            row['trade_count'],
                            row['vwap']
                        ))
                    except Exception as db_err:
                        logging.error("Error inserting data into MySQL: %s", db_err)
                        # You can choose to skip or break, depending on your requirements

                # Commit changes after processing a batch of rows
                connection.commit()

            else:
                logging.warning("Unexpected data format: %s", data)

        except Exception as e:
            logging.error("Error processing message: %s", e)

except KeyboardInterrupt:
    logging.info("Consumer stopped by user")
except Exception as kafka_err:
    logging.error("Error with Kafka consumer: %s", kafka_err)
finally:
    # Clean up: close cursor and connection
    if cursor:
        logging.info("Closing MySQL cursor")
        cursor.close()
    if connection:
        logging.info("Closing MySQL connection")
        connection.close()
