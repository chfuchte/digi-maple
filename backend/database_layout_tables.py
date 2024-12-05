import sqlite3

# Connect to the SQLite database (or create it)
conn = sqlite3.connect('maps_and_markers.db')
cursor = conn.cursor()

# Create the Maps, Markers and Users tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS Maps_Table (
    id INT PRIMARY KEY,
    map_name TEXT,
    map_link TEXT,
    width REAL,
    heigth REAL,
    map_author TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Markers_Table (
    marker_variety TEXT,
    marker_name TEXT,
    x_position REAL,
    y_position REAL,
    map_name TEXT,
    FOREIGN KEY (map_name) REFERENCES Maps_Table(map_name)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    username TEXT PRIMARY KEY,
    email TEXT,
    password TEXT
)
''')

# Function to insert a map into the Maps table
def insert_map(map_id, map_name, map_link, width, heigth, map_author):
    cursor.execute('''
    INSERT INTO Maps_Table (id, map_name, map_link, width, heigth, map_author)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (map_id, map_name, map_link, width, heigth, map_author))
    conn.commit()
    print(f"Inserted '{map_name}' into Maps_Table")

# Function to insert a marker into the Markers table
def insert_marker(marker_variety, marker_name, x, y, map_name):
    cursor.execute('''
    INSERT INTO Markers_Table (marker_variety, marker_name, x_position, y_position, map_name)
    VALUES (?, ?, ?, ?, ?)
    ''', (marker_variety, marker_name, x, y, map_name))
    conn.commit()
    print(f"Inserted '{marker_name}' into Markers_Table")

# Function to insert a marker into the Markers table
def insert_user(username, email, password):
    cursor.execute('''
    INSERT INTO Users (username, email, password)
    VALUES (?, ?, ?)
    ''', (username, email, password))
    conn.commit()
    print(f"Inserted '{username}' into Users")

def delete_map(map_name):
    cursor.execute(f"DELETE FROM Maps_Table WHERE map_name='{map_name}'")
    conn.commit()
    print(f"Deleted '{map_name}' from Maps_Table")


def delete_user(username):
    cursor.execute(f"DELETE FROM Users WHERE username='{username}'")
    conn.commit()
    print(f"Deleted '{username}' from Users")

# Function to get the database in a dictionary format
# The dict will then be parsed throught FastAPI
def get_dict() -> dict:
    cursor.execute("SELECT * FROM Maps_Table")
    maps = cursor.fetchall()
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()

    main_dict = {"maps": {}, "users": {}}
    
    
    for (map_id, name, link, width, height, author), (username, email, password) in zip(maps, users):
        main_dict["maps"][map_id] = {}
        main_dict["maps"][map_id]["name"] = name
        main_dict["maps"][map_id]["link"] = link
        main_dict["maps"][map_id]["height"] = height
        main_dict["maps"][map_id]["width"] = width
        main_dict["maps"][map_id]["author"] = author

        markers = _get_markers_for_map(name)
        markers_dict = _markers_to_dict(markers)

        main_dict["maps"][map_id]["markers"] = markers_dict

        main_dict["users"][username] = {}
        main_dict["users"][username]["email"] = email
        main_dict["users"][username]["password"] = password

        

    return main_dict

# Function to get all markers for a specific map
def _get_markers_for_map(map_name) -> list:
    cursor.execute('''
    SELECT marker_variety, marker_name, x_position, y_position
    FROM Markers_Table
    WHERE map_name = ?
    ''', (map_name,))
    markers = cursor.fetchall()
    return markers


# Function to turn a list of markers to a dictionary
def _markers_to_dict(markers) -> dict:
    markers_dict: dict = {}
    for m_id, name, x, y in markers:
        markers_dict[name] = {}
        markers_dict[name]["type"] = m_id
        markers_dict[name]["position"] = {}
        markers_dict[name]["position"]["x"] = x
        markers_dict[name]["position"]["y"] = y

    return markers_dict



# Main block for testing. Creates a 'Map of the World' entry and 'Rafal' user when ran.
if __name__ == "__main__":
    # Example usage
    delete_user("Rafal")
    insert_user("Rafal", "test@gmail.com", "pass1234")
    
    delete_map ("Map of the World")
    insert_map(0, "Map of the World" , "http://example.com/worldmap.jpg", 1885, 2000, "Rafal")
    insert_marker("POI-tower", "Eiffel Tower", 123, 432, "Map of the World")
    insert_marker("bold line", "Great Wall of China", 420, 69, "Map of the World")

    markers = _get_markers_for_map("Map of the World")

    print(get_dict())

    for marker in markers:
        print(f"Marker-ID: {marker[0]}, Marker-Name: {marker[1]}, Location: ({marker[2]}, {marker[3]})")

    # Close the connection
    conn.close()
