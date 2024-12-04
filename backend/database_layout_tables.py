import sqlite3

# Connect to the SQLite database (or create it)
conn = sqlite3.connect('maps_and_markers.db')
cursor = conn.cursor()

# Create the Maps and Markers tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS Maps_Table (
    map_name TEXT PRIMARY KEY,
    map_link TEXT,
    width REAL,
    heigth REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Markers_Table (
    marker_variety TEXT,
    marker_name TEXT,
    longitude REAL,
    latitude REAL,
    map_name TEXT,
    FOREIGN KEY (map_name) REFERENCES Maps_Table(map_name)
)
''')

# Function to insert a map into the Maps table
def insert_map(map_name, map_link, width, heigth):
    cursor.execute('''
    INSERT INTO Maps_Table (map_name, map_link, width, heigth)
    VALUES (?, ?, ?, ?)
    ''', (map_name, map_link, width, heigth))
    conn.commit()

# Function to insert a marker into the Markers table
def insert_marker(marker_variety, marker_name, longitude, latitude, map_name):
    cursor.execute('''
    INSERT INTO Markers_Table (marker_variety, marker_name, longitude, latitude, map_name)
    VALUES (?, ?, ?, ?, ?)
    ''', (marker_variety, marker_name, longitude, latitude, map_name))
    conn.commit()

# Function to get all markers for a specific map
def get_markers_for_map(map_name):
    cursor.execute('''
    SELECT marker_variety, marker_name, longitude, latitude
    FROM Markers_Table
    WHERE map_name = ?
    ''', (map_name,))
    markers = cursor.fetchall()
    return markers

# Example usage
insert_map( "Map of the World", "http://example.com/worldmap.jpg", 1885, 2000)
insert_marker("POI-tower", "Eiffel Tower", 2.2943506, 48.8588443, "Map of the World")
insert_marker("bold line", "Great Wall of China", 116.5703749, 40.4319077, "Map of the World")

markers = get_markers_for_map("Map of the World")
for marker in markers:
    print(f"Marker-ID: {marker[0]}, Marker-Name: {marker[1]}, Location: ({marker[2]}, {marker[3]})")

# Close the connection
conn.close()