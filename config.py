from kafka import KafkaConsumer
import json

consumer1 = KafkaConsumer(
    'my_topic', 
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,  # Enables automatic offset commits
    group_id='my_group',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))

)
consumerf2 = KafkaConsumer(
    bootstrap_servers = ['localhost:9092'],
    auto_offset_reset = 'earliest',
    enable_auto_commit = True,
    group_id = 'my_group',
    value_deserializer = lambda v: json.loads(v.decode('utf_8'))
   
)