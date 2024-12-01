import json
from neo4j import GraphDatabase
from tqdm import tqdm

class Neo4jConnection:
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)

    def close(self):
        if self.__driver is not None:
            self.__driver.close()

    def query(self, query, parameters=None, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.__driver.session(database=db) if db is not None else self.__driver.session()
            response = list(session.run(query, parameters))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response

def populate_neo4j(conn, data):
    """Populate the Neo4j database with wall data."""
    # Updated constraint syntax
    conn.query("CREATE CONSTRAINT IF NOT EXISTS FOR (w:Wall) REQUIRE w.id IS UNIQUE;")
    conn.query("CREATE CONSTRAINT IF NOT EXISTS FOR (m:Material) REQUIRE m.name IS UNIQUE;")

    for wall in tqdm(data, desc="Processing walls"):
        wall_id = wall['wall_id']
        total_thickness = wall['total_thickness']
        total_r_value = wall['total_r_value']
        total_u_value = wall['total_u_value']
        total_embodied_carbon = wall['total_embodied_carbon']
        heat_transfer = wall['heat_transfer']
        total_cost = wall['total_cost']
        materials = wall['materials']

        # Create Wall node
        conn.query("""
            MERGE (w:Wall {id: $id, total_thickness: $thickness, total_r_value: $r_value, 
                           total_u_value: $u_value, total_embodied_carbon: $embodied_carbon, 
                           heat_transfer: $heat_transfer, total_cost: $cost})
        """, parameters={
            'id': wall_id,
            'thickness': total_thickness,
            'r_value': total_r_value,
            'u_value': total_u_value,
            'embodied_carbon': total_embodied_carbon,
            'heat_transfer': heat_transfer,
            'cost': total_cost
        })

        # Create Material nodes and relationships
        for material in materials:
            conn.query("""
                MERGE (m:Material {name: $name})
                MERGE (w:Wall {id: $wall_id})
                MERGE (m)-[:USED_IN {thickness: $thickness}]->(w)
            """, parameters={
                'name': material['material'],
                'wall_id': wall_id,
                'thickness': material['thickness']
            })


if __name__ == "__main__":
    # Path to your JSON file
    file_path = r'datasets/outputted.json'

    # Load JSON data
    print("Loading data...")
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Neo4j connection details
    uri = "neo4j+s://cb8d7141.databases.neo4j.io"  # Replace with your Neo4j URI
    user = "neo4j"                 # Replace with your Neo4j username
    password = "ZfHZvwNG6JMJqIvBDqzOzmFNdHf2n9gzP6gz_frXnmI"          # Replace with your Neo4j password

    # Establish connection
    print("Connecting to Neo4j...")
    conn = Neo4jConnection(uri, user, password)

    # Populate Neo4j database
    print("Populating the Neo4j database...")
    populate_neo4j(conn, data)

    # Close connection
    conn.close()
    print("Neo4j database population complete.")
