from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

import database_layout_tables as db
import example_database_entry as ex

app = FastAPI()


origins = [
    "*", # Allow all origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ex.insert_example_map()
ex.insert_example_user()

map_dict: dict = db.get_dict()

@app.get("/")
def read_root():
    # Get the contents of the data base as a python dictionary to parse it through FastAPI
    return map_dict

@app.get("/auth/whoami")
def whoami():
    cursor = db.conn.cursor()
    cursor.execute("SELECT name FROM user")
    name = cursor.fetchone()
    if name:
        return {"status": "success", "name": name[0]}
    return {"status": "failure"}

@app.post("/auth/login")
def login(email: str, password: str):
    cursor = db.conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ? AND password = ?", (email, password))
    user_id = cursor.fetchone()
    if user_id:
        return {"status": "success", "id": user_id[0]}
    return {"status": "failure"}

@app.post("/auth/register")
def register(name: str, email: str, password: str):
    cursor = db.conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    existing_user = cursor.fetchone()
    if existing_user:
        return {"status": "failure", "reason": "email already exists"}
    db.insert_user(name, email, password)
    return {"status": "success"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
