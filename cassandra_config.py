from cassandra.cluster import Cluster, NoHostAvailable
import uuid
import os
import time

class CassandraConnector:
    def __init__(self):
        self.session = None
        self.cassandra_host = os.environ.get('CASSANDRA_HOST')  # Use get to avoid KeyError
        self.connect()

    def connect(self):
        try:
            if self.cassandra_host:
                print("Cassandra HOST::::::::::::::::::::::::::::", self.cassandra_host)
                cluster = Cluster([self.cassandra_host], port=9042)

                self.session = cluster.connect()

                # Create a keyspace and table (if they don't exist)
                self.session.execute("""
                    CREATE KEYSPACE IF NOT EXISTS final_app
                    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
                """)

                self.session.set_keyspace('final_app')

                self.session.execute("""
                    CREATE TABLE IF NOT EXISTS final_app.student_data (
                        id UUID PRIMARY KEY,
                        name TEXT,
                        andrewid TEXT,
                        course TEXT,
                        grade TEXT
                    )
                """)
        except NoHostAvailable as e:
            print(f"Failed to connect to Cassandra. Reason: {str(e)}")

    def save_data(self, name, andrewid, course, grade):
        print("Session before create new session: GET ALL", self.session)
        if not self.session:
            self.connect()  # Reconnect if not connected

        new_id = uuid.uuid4()

        self.session.execute("""
            INSERT INTO final_app.student_data (id, name, andrewid, course, grade)
            VALUES (%s, %s, %s, %s, %s)
        """, (new_id, name, andrewid, course, grade))

    def get_all_data(self):
        try:
            print("Session before create new session: GET ALL", self.session)
            if not self.session:
                self.connect()  # Reconnect if not connected
                if not self.session:
                    print("Cassandra not connected. Cannot fetch data.")
                    return []

            rows = self.session.execute('SELECT * FROM final_app.student_data')
            return [{'id': row.id, 'name': row.name, 'andrewid': row.andrewid, 'course': row.course, 'grade': row.grade} for row in rows]
        except Exception as e:
            print(f"Failed to fetch data from Cassandra. Reason: {str(e)}")
            return []
