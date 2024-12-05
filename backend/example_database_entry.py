import database_layout_tables as db
from sqlite3 import IntegrityError

# Intended to show how to add an entry to the database
def new_map():
    try:
        db.delete_map("Cool Map")
        db.insert_map(1, "Cool Map", "https://example.com/map.jpg", 100, 200, "Olaf")
        db.insert_marker("POI-tower", "Eiffel Tower", 123, 321, "Cool Map")
        db.insert_marker("Circle", "Cool spot", 436, 342, "Cool Map")
    except IntegrityError:
        print("Warning: Map by the name 'Cool Map' is already in the database")

def new_user():
    try:
        db.delete_user("Olaf")
        db.insert_user("Olaf", "Olaf@gmail.com", "pass1234")
    except IntegrityError:
        print("Warning: User by the name 'Olaf' is already in the database")
