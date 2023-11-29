import psycopg2 as pg


class SensorRepository:
    def __init__(self, user, password, host, port, database):
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._database = database
        
        self._connection = None
        self._cursor = None
        
    def connect(self):
        try:
            self._connection = pg.connect(user=self._user,
                                        password=self._password,
                                        host=self._host,
                                        port=self._port,
                                        database=self._database)
            self._cursor = self._connection.cursor()
            self._cursor.execute("SELECT version();")
            record = self._cursor.fetchone()
            print("You are connected to - ", record, "\n")
        except (Exception, pg.Error) as error:
            print("Error while connecting to PostgreSQL", error)
            exit(1)
        
    def create_table(self):
        try:
            self._cursor.execute("CREATE TABLE IF NOT EXISTS sensor_data ("
                                "id SERIAL PRIMARY KEY,"
                                "sensor_id VARCHAR(255) NOT NULL,"
                                "temperature VARCHAR(255) NOT NULL,"
                                "humidity VARCHAR(255) NOT NULL,"
                                "timestamp VARCHAR(255) NOT NULL);")
            self._connection.commit()
        except (Exception, pg.Error) as error:
            print("Error while creating table: ", error)
            exit(1)
        
    def register(self, df):
        try:
            for index, row in df.iterrows():
                self._cursor.execute("INSERT INTO sensor_data (sensor_id, temperature, humidity, timestamp) VALUES (%s, %s, %s, %s);",
                                    (row['sensor_id'], row['temperature'], row['humidity'], row['timestamp']))
            self._connection.commit()
        except (Exception, pg.Error) as error:
            print("Error while inserting data: ", error)
            exit(1)
            
    def end(self):
        try:
            self._cursor.close()
            self._connection.close()
        except (Exception, pg.Error) as error:
            print("Error while closing connection: ", error)
            exit(1)

