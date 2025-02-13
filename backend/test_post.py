# Test the api via http request

"""

class Map(BaseModel):
    name: str
    authorId: int
    imgUrl: str
    imgWidth: int
    imgHeight: int
    markers: list[Marker]


class Marker(BaseModel):
    map_id: int
    x: int
    y: int
    title: str
    description: str
    type: str

"""

import requests


# Adds a new user (possible user_id 2 because the first user is added in main.py)
#url = "http://127.0.0.1:8080/users"
#data = {"username": "new_user", "email": "example_new@email.gmail.com", "password": "password"}

#response = requests.post(url, json=data)
#print(response.text)

# Edits user 1 (From "Olaf" to "edited")
url = "http://127.0.0.1:8080/maps/1"
data = {
            "name": "sigma",
            "author": "olaf",
            "imgUrl": "https://example.com",
            "imgWidth": 1920,
            "imgHeight": 1080,
            "markers": [
                {
                    "x": 100,
                    "y": 200,
                    "title": "Eiffel Tower",
                    "description": "big tower in france",
                    "type": "sight",
                }
            ]
       }

response = requests.post(url, json=data)
print(response.text)
