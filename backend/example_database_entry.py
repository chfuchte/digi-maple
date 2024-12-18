from sqlite3 import IntegrityError
import database_layout_tables as db 

def insert_example_map():
    try:
        # Check if the map already exists
        cursor = db.conn.cursor()
        cursor.execute("SELECT id FROM maps WHERE name = ?", ("Cool Map",))
        existing_map = cursor.fetchone()

        if existing_map:
            db.delete_map(existing_map[0])  # Delete the map by ID if it exists

        # Insert the new map
        db.insert_map("Cool Map", "Olaf", "https://example.com/map.jpg", 100, 200)

        # Fetch the new map ID
        cursor.execute("SELECT id FROM maps WHERE name = ?", ("Cool Map",))
        map_id = cursor.fetchone()[0]

        # Insert markers for the map
        db.insert_marker(map_id, 123, 321, "Eiffel Tower", "A famous landmark in Paris", "default")
        db.insert_marker(map_id, 436, 342, "Cool spot", "A nice place to visit", "info")

    except IntegrityError as e:
        print(f"Warning: IntegrityError occurred: {e}")

def insert_example_user():
    try:
        # Check if the user already exists
        cursor = db.conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", ("Olaf",))
        existing_user = cursor.fetchone()

        if existing_user:
            db.delete_user(existing_user[0])  # Delete the user by ID if it exists

        # Insert the new user
        db.insert_user("Olaf", "Olaf@gmail.com", "pass1234")

    except IntegrityError as e:
        print(f"Warning: IntegrityError occurred: {e}")
