# Used to setup kafka and start the server, zookeeper, producer and consumer
# Uses gnome-terminal to open multiple terminals and run the commands in parallel
# Check if gnome-terminal is installed and supported by your OS

ORANGE='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${ORANGE}|=======================|Downloading Kafka|=======================|${NC}"
wget https://archive.apache.org/dist/kafka/2.8.0/kafka_2.12-2.8.0.tgz -P kafka/

echo -e "${ORANGE}|=======================|Extracting Kafka|=======================|${NC}"
tar -xzf kafka/kafka_2.12-2.8.0.tgz -C kafka/
rm kafka/kafka_2.12-2.8.0.tgz 

echo -e "${ORANGE}|=======================|Starting Zookeeper|=======================|${NC}"
gnome-terminal -- ./kafka/kafka_2.12-2.8.0/bin/zookeeper-server-start.sh ./kafka/kafka_2.12-2.8.0/config/zookeeper.properties
sleep 10

echo -e "${ORANGE}|=======================|Starting Server|=======================|${NC}"
gnome-terminal -- ./kafka/kafka_2.12-2.8.0/bin/kafka-server-start.sh ./kafka/kafka_2.12-2.8.0/config/server.properties
sleep 10

echo -e "${ORANGE}|=======================|Creating Topic|=======================|${NC}"
python3 kafka/create_topic.py

echo -e "${ORANGE}|=======================|Starting Producer|=======================|${NC}"
gnome-terminal -- python3 kafka/write_in_queue.py

echo -e "${ORANGE}|=======================|Starting Consumer|=======================|${NC}"
gnome-terminal -- python3 kafka/read_from_queue.py
