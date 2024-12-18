import sqlite3

# Connect to the SQLite database (or create it)
conn = sqlite3.connect('maps_and_markers.db')
cursor = conn.cursor()

# Create the Maps, Markers, and Users tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS maps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    authorId TEXT NOT NULL,
    imgUrl TEXT UNIQUE NOT NULL,
    imgWidth INTEGER NOT NULL,
    imgHeight INTEGER NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS markers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mapId INTEGER NOT NULL,
    x INTEGER NOT NULL,
    y INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    type TEXT NOT NULL,
    FOREIGN KEY (mapId) REFERENCES maps (id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# Function to insert a map into the maps table
def insert_map(name, authorId, imgUrl, imgWidth, imgHeight):
    cursor.execute('''
    INSERT INTO maps (name, authorId, imgUrl, imgWidth, imgHeight)
    VALUES (?, ?, ?, ?, ?)
    ''', (name, authorId, imgUrl, imgWidth, imgHeight))
    conn.commit()
    print(f"Inserted '{name}' into maps")

# Function to insert a marker into the markers table
def insert_marker(mapId, x, y, title, description, marker_type):
    cursor.execute('''
    INSERT INTO markers (mapId, x, y, title, description, type)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (mapId, x, y, title, description, marker_type))
    conn.commit()
    print(f"Inserted marker '{title}' into markers")

# Function to insert a user into the users table
def insert_user(username, email, password):
    cursor.execute('''
    INSERT INTO users (username, email, password)
    VALUES (?, ?, ?)
    ''', (username, email, password))
    conn.commit()
    print(f"Inserted '{username}' into users")

# Function to delete a map by ID
def delete_map(map_id):
    cursor.execute('''
    DELETE FROM maps WHERE id = ?
    ''', (map_id,))
    conn.commit()
    print(f"Deleted map with ID '{map_id}'")

# Function to delete a user by ID
def delete_user(user_id):
    cursor.execute('''
    DELETE FROM users WHERE id = ?
    ''', (user_id,))
    conn.commit()
    print(f"Deleted user with ID '{user_id}'")

# Function to get the database in a dictionary format
def get_dict() -> dict:
    cursor.execute("SELECT * FROM maps")
    maps = cursor.fetchall()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    main_dict = {"maps": {}, "users": {}}

    for map_entry in maps:
        map_id, name, authorId, imgUrl, imgWidth, imgHeight = map_entry
        markers = _get_markers_for_map(map_id)
        main_dict["maps"][map_id] = {
            "name": name,
            "author": authorId,
            "imgUrl": imgUrl,
            "imgWidth": imgWidth,
            "imgHeight": imgHeight,
            "markers": [
                {
                    "id": str(marker[0]),
                    "x": marker[2],
                    "y": marker[3],
                    "display": {
                        "title": marker[1],
                        "description": marker[4],
                        "markerType": marker[5]
                    }
                } for marker in markers
            ]
        }

    for user_entry in users:
        print(user_entry)
        id, username, email, _ = user_entry # don't give out password
        main_dict["users"][username] = {
            "id": id,
            "username": username,
            "email": email,
        }

    return main_dict

# Function to get all markers for a specific map
def _get_markers_for_map(map_id) -> list:
    cursor.execute('''
    SELECT id, title, x, y, description, type
    FROM markers
    WHERE mapId = ?
    ''', (map_id,))
    return cursor.fetchall()

# Main block for testing
if __name__ == "__main__":
    cursor.execute("SELECT id FROM users WHERE username = ?", ("Rafal",))
    user = cursor.fetchone()
    if user:
        delete_user(user[0])
    insert_user("Rafal", "test@gmail.com", "pass1234")

    cursor.execute("SELECT id FROM maps WHERE name = ?", ("Map of the World",))
    map_record = cursor.fetchone()
    if map_record:
        delete_map(map_record[0])
    insert_map("Map of the World", "Rafal", "http://example.com/worldmap.jpg", 1885, 2000)

    # Fetch the map ID for inserting markers
    cursor.execute("SELECT id FROM maps WHERE name = ?", ("Map of the World",))
    map_id = cursor.fetchone()[0]

    insert_marker(map_id, 123, 432, "Eiffel Tower", "A famous landmark in Paris", "default")
    insert_marker(map_id, 420, 69, "Great Wall of China", "A historical wall in China", "info")

    print(get_dict())

    # Close the connection
    conn.close()
