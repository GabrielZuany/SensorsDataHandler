from time import sleep
from kafka import KafkaConsumer
import json
import pandas as pd
import psycopg2 as pg

TOPIC="SensorsDataStream"
TABLE_NAME=TOPIC

try:
    conn = pg.connect("dbname='postgres' user='postgres' host='localhost' password='example'")
    print("Connected to database")
    cursor = conn.cursor()
except Exception as e:
    print("Exception while connecting to database")
    print(str(e))
    exit(1)
    
try:
    consumer = KafkaConsumer(TOPIC,
                            group_id=None,
                             bootstrap_servers=['localhost:9092'],
                             auto_offset_reset = 'earliest')
except Exception as e:
    print("Exception while connecting Kafka")
    print(str(e))
    exit(1)
    
print("Consumer started")
print(consumer.subscription())
check = True

for msg in consumer:
    dictionary = json.loads(msg.value.decode('utf-8'))
    df = pd.DataFrame(dictionary, index=[0])
    print(df)
    
    columns = ",".join(df.columns)
    
    # create table if not exists
    if check:
        cursor.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)", (TABLE_NAME,))
        exists = cursor.fetchone()[0]
        if exists is None:
            cursor.execute(f"CREATE TABLE {TABLE_NAME} (id SERIAL PRIMARY KEY);")
            for column in df.columns:
                if column == "timestamp":
                    cursor.execute(f"ALTER TABLE {TABLE_NAME} ADD COLUMN {column} TIMESTAMP;")
                elif column == "status":
                    cursor.execute(f"ALTER TABLE {TABLE_NAME} ADD COLUMN {column} VARCHAR;")
                else:
                    cursor.execute(f"ALTER TABLE {TABLE_NAME} ADD COLUMN {column} FLOAT;")
            conn.commit()
        check = False
        
    # insert data
    values = df.values.tolist()[0]
    values_str = ""
    is_timestamp = True
    for value in values:
        if is_timestamp:
            values_str+=f"'{value}',"
            is_timestamp = False
            continue
        if value == "NORMAL" or value == "ANORMAL":
            values_str+=f"'{value}',"
            break
        values_str+=str(value)+","
    values_str = values_str[:-1]
    values_str = values_str.replace("nan", "NULL")
    
    # check if exists
    cursor.execute(f"SELECT EXISTS(SELECT * FROM {TABLE_NAME} WHERE timestamp='{values[0]}')")
    if cursor.fetchone()[0] is not None:
        print("Data already exists")
        continue
    
    cursor.execute(f"INSERT INTO {TABLE_NAME}({columns}) VALUES ({values_str})", values)
    conn.commit()
    sleep(1)
    
cursor.close()
conn.close()