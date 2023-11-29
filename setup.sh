# ISSO TUDO VAI PRO AIRFLOW

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# setting up database in docker container
docker-compose -f database/docker-compose.yml up -d

# run kafka 
# blablabla

# run ML model