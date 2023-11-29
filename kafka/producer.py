from kafka import KafkaProducer
import json
producer = KafkaProducer(
    bootstrap_servers=['localhost:29092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'))
producer.send("bankbranch", {'atmid':1, 'transid':4545})
producer.send("bankbranch", {'atmid':2, 'transid':2525})

producer.flush()

producer.close()