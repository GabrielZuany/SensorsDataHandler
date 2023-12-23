# Used to create a topic in Kafka to be used by the producer and consumer

from kafka.admin import KafkaAdminClient,NewTopic

TOPIC="SensorsDataStream"

try:
    admin_client = KafkaAdminClient(bootstrap_servers="localhost:9092", client_id='GabrielZuany')
except Exception as e:
    print("Exception while connecting Kafka")
    print(str(e))
    exit(1)


if TOPIC in admin_client.list_topics():
    print("Topic already exists")
    exit(0)

try:
    topic_list = []
    new_topic = NewTopic(name=TOPIC, num_partitions= 2, replication_factor=1)
    topic_list.append(new_topic)
    admin_client.create_topics(new_topics=topic_list)
    print("Topic created successfully")
except Exception as e:
    print("Exception while creating topic")
    print(str(e))
    exit(1)