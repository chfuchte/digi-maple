from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

import database_layout_tables as db
import example_database_entry as ex

app = FastAPI()


origins = [
    "http://localhost:3000",
    "http://localhost:8080",
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

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)


