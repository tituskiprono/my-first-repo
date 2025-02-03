from kafka import KafkaProducer
import json
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime
import pandas as pd
import time


client = CryptoHistoricalDataClient()

def fetch_and_send_data(producer):
    request = CryptoBarsRequest(
        symbol_or_symbols=["ETH/BTC"],
        timeframe=TimeFrame.Day,
        start_date=datetime(2024, 1, 1),
        end_date=datetime(2024, 1, 29)
    )

    bars = client.get_crypto_bars(request)

    df = bars.df.reset_index()

    print("DataFrame columns:", df.columns)
    print(df.head())

    if 'symbol' in df.columns and 'ETH/BTC' in df['symbol'].values:
        eth_btc_data = df[df['symbol'] == 'ETH/BTC']
        print("ETH/BTC Data:\n", eth_btc_data)

        eth_btc_data['timestamp'] = eth_btc_data['timestamp'].astype(str)

        message = {'data': eth_btc_data.to_dict(orient='records')} 
        

        producer.send('my_topic', value=message)
        producer.flush()
        
        print("Message sent successfully")
    else:
        print("No data available for 'ETH/BTC'.")


def get_producer() -> KafkaProducer:
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    return producer


producer = get_producer()

try:
    while True:
        fetch_and_send_data(producer)
        time.sleep(1) 
except KeyboardInterrupt:
    print("Producer stopped")
finally:
    producer.close()
