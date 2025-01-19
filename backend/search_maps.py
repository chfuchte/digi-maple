from difflib import get_close_matches
import database_layout_tables as db
map_dict: dict = db.get_dict()
cursor = db.conn.cursor()

# Create a list only of the maps' names
map_list = map_dict['maps']
name_list = []
for i in range(0, len(map_list)):
    current_name = map_list[i]['name']
    name_list.append(current_name)

# Find and print close matches to user's input
while True:
    # Take the user's search input
    query = input("Nach Karten suchen: ")

    # Find the n closest matches (n = 5)
    def search_matching_maps(query, name_list):
        matches = get_close_matches(query, name_list, n = 5, cutoff = 0.3)
        return matches
    
    matches_list = search_matching_maps(query, name_list)
    
    # Output of matching maps incl. their id, author and image url or restart search if no matches found
    if len(matches_list) >= 1:
        if len(matches_list) >= 2:
            print("Ihre Kartensuche ergab folgende Treffer: ")
        else:
            print("Ihre Kartensuche ergab folgenden Treffer: ")
        for j in range(0, len(matches_list)):
            current_map = matches_list[j]
            cursor.execute("SELECT id, authorId, imgUrl FROM maps WHERE name = ?", (current_map,))
            map_data = cursor.fetchall()
            current_id = str(map_data[0][0])
            current_author = map_data[0][1]
            current_url = map_data[0][2]
            print("Kartenname:", current_map+", ID:", current_id+", Autor:", current_author+", URL:", current_url)
        break
    else:
        print("Ihre Suche ergab leider keinen Treffer. Bitte versuchen Sie es mit einer veränderten Eingabe erneut: ")
