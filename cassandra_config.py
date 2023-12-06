from cassandra.cluster import Cluster, NoHostAvailable
import uuid

class CassandraConnector:
    def __init__(self):
        try:
            self.cluster = Cluster(['127.0.0.1'])  # Use your Cassandra cluster IP addresses
            self.session = self.cluster.connect('final_app')  # Replace 'final_app' with your actual keyspace

            # Create a keyspace and table (if they don't exist)
            self.session.execute("""
                CREATE KEYSPACE IF NOT EXISTS final_app
                WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
            """)

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
            return None

    def save_data(self, name, andrewid, course, grade):
        new_id = uuid.uuid4()

        self.session.execute("""
            INSERT INTO final_app.student_data (id, name, andrewid, course, grade)
            VALUES (%s, %s, %s, %s, %s)
        """, (new_id, name, andrewid, course, grade))
    def get_all_data(self):
        try:
            if not self.session:
                print("Cassandra not connected. Cannot fetch data.")
                return []
            rows = self.session.execute('SELECT * FROM final_app.student_data')
            return [{'id': row.id, 'name': row.name, 'andrewid': row.andrewid, 'course': row.course, 'grade': row.grade} for row in rows]
        except Exception as e:
            print(f"Failed to fetch data from Cassandra. Reason: {str(e)}")
            return []
