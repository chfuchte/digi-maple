from sqlite3 import IntegrityError
import database_layout_tables as db
from env import is_docker

def insert_example_map():
    demo_map_url = "http://localhost/dev/Lageplan_Campus_Bockenheim.svg" if is_docker() else "http://localhost:3000/dev/Lageplan_Campus_Bockenheim.svg"

    try:
        # Check if the map already exists
        cursor = db.conn.cursor()
        cursor.execute("SELECT id FROM maps WHERE name = ?", ("Uni Campus Bockenheim",))
        existing_map = cursor.fetchone()

        if existing_map:
            db.delete_map(existing_map[0])  # Delete the map by ID if it exists

        # Insert the new map
        db.insert_map("Uni Campus Bockenheim", "Olaf", demo_map_url, 1885, 2000)

        # Fetch the new map ID
        cursor.execute("SELECT id FROM maps WHERE name = ?", ("Uni Campus Bockenheim",))
        map_id = cursor.fetchone()[0]

        # Insert markers for the map
        db.insert_marker(map_id, 942, 1000, "Wuhu!", "Ich bin ein Marker", "warning")
        db.insert_marker(map_id, 942, 800, "Sekretariat", "Get some help here", "info")
        db.insert_marker(map_id, 942, 600, "Achtung", "Viele Besucher hier", "warning")
        db.insert_marker(map_id, 942, 400, "Eingang zum Gebäude", "Barrierefreier Eingang zum Gebäude", "weelchair")

    except IntegrityError as e:
        print(f"Warning: IntegrityError occurred: {e}")

def insert_example_user():
    try:
        # Check if the user already exists
        cursor = db.conn.cursor()
        cursor.execute("SELECT id FROM users WHERE name = ?", ("test",))
        existing_user = cursor.fetchone()

        if existing_user:
            db.delete_user(existing_user[0])  # Delete the user by ID if it exists

        # Insert the new user
        db.insert_user("test", "test@mail.com", "12345678")

    except IntegrityError as e:
        print(f"Warning: IntegrityError occurred: {e}")
