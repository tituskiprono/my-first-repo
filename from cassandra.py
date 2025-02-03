from cassandra.cluster import Cluster

def test_connection():
    try:
        cluster = Cluster(['localhost'])
        session = cluster.connect()
        print("Connection successful!")
        session.shutdown()
        cluster.shutdown()
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test_connection()
