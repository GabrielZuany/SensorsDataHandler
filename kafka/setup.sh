GREEN='\033[0;32m'
NC='\033[0m' # No Color
BLUE='\033[0;34m'

echo -e "${GREEN}|=======================|Downloading Kafka|=======================|${NC}"
# wget https://archive.apache.org/dist/kafka/2.8.0/kafka_2.12-2.8.0.tgz

echo -e "${GREEN}|=======================|Extracting Kafka|=======================|${NC}"
# tar -xzf kafka_2.12-2.8.0.tgz
# mv kafka_2.12-2.8.0 kafka
# rm kafka_2.12-2.8.0.tgz

echo -e "${GREEN}|=======================|Starting Zookeeper|=======================|${NC}"
gnome-terminal -- ./kafka/kafka_2.12-2.8.0/bin/zookeeper-server-start.sh ./kafka/kafka_2.12-2.8.0/config/zookeeper.properties
sleep 10

echo -e "${GREEN}|=======================|Starting Server|=======================|${NC}"
gnome-terminal -- ./kafka/kafka_2.12-2.8.0/bin/kafka-server-start.sh ./kafka/kafka_2.12-2.8.0/config/server.properties
sleep 10

echo -e "${GREEN}|=======================|Creating Topic|=======================|${NC}"
python3 kafka/create_topic.py

echo -e "${GREEN}|=======================|Starting Producer|=======================|${NC}"
gnome-terminal -- python3 kafka/write_in_queue.py

echo -e "${GREEN}|=======================|Starting Consumer|=======================|${NC}"
gnome-terminal -- python3 kafka/read_from_queue.py
