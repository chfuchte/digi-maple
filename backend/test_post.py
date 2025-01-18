# Test the api via http request

import requests

# Adds a new user (possible user_id 2 because the first user is added in main.py)
url = "http://127.0.0.1:8080/users"
data = {"username": "new_user", "email": "example_new@email.gmail.com", "password": "password"}

response = requests.post(url, json=data)
print(response.text)

# Edits user 1 (From "Olaf" to "edited")
url = "http://127.0.0.1:8080/users/1"
data = {"username": "edited", "email": "exampl_editede@email.gmail.com", "password": "pass123456789"}

response = requests.post(url, json=data)
print(response.text)
