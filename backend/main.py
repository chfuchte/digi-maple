from fastapi import FastAPI
import uvicorn

import database_layout_tables as db
import example_database_entry as ex

app = FastAPI()

ex.insert_example_map()
ex.insert_example_user()

@app.get("/")
def read_root():
    # Get the contents of the data base as a python dictionary to parse it through FastAPI
    map_dict: dict = db.get_dict()
    return map_dict

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)


