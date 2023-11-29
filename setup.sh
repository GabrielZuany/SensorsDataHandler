NC='\033[0m' # No Color
GREEN='\033[0;32m'
BLUE='\033[0;34m'

sudo rm -rf /tmp/kafka-logs /tmp/zookeeper

echo -e "${GREEN}|=======================|Setting up Database in Docker|=======================|${NC}"
docker-compose -f database/docker-compose.yml up -d

echo -e "${GREEN}|=======================|Setting up Kafka|=======================|${NC}"
dos2unix kafka/setup.sh
./kafka/setup.sh

echo -e "${GREEN}|=======================|Running Machine Learning Model|=======================|${NC}"
python3 src/model.py