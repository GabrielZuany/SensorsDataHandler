# Used to write data to the queue in real time from a CSV file 
# In real scenario, this data would come from sensors and would be appended to the CSV file in real time 
# (the logic is the same, but the data source is different and i would read dinamically from the CSV file)

from time import sleep
from kafka import KafkaProducer
import json
import pandas as pd

TOPIC = "SensorsDataStream"
INPUT_FILE = "data/full.csv"

df = pd.read_csv(INPUT_FILE)

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'))

for idx in range(len(df)):
    print(df.iloc[idx].to_dict())
    producer.send(TOPIC, df.iloc[idx].to_dict())
    producer.flush()
    sleep(1)
    
producer.close()