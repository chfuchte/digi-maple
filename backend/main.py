from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlite3 import IntegrityError

from database import database_layout_tables as db
from database import example_database_entry as ex


class User(BaseModel):
    username: str
    email: str
    password: str


class Marker(BaseModel):
    id: int
    map_id: int
    x: int
    y: int
    title: str
    description: str
    type: str


class Map(BaseModel):
    name: str
    authorId: int
    imgUrl: str
    imgWidth: int
    imgHeight: int
    markers: list[Marker]


def search_by_id(list_dicts: list[dict], id: int):
    for i in range(len(list_dicts)):
        if list_dicts[i]["id"] == id:
            return list_dicts[i]
    return None


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
async def read_root():
    # Get the contents of the data base as a python dictionary to pass it through FastAPI
    return {"root": map_dict}

@app.get("/maps")
async def read_maps():
    return {"message": "success","value": map_dict["maps"]}

@app.get("/maps/{map_id}")
async def read_map(map_id: str):
    try:
        return {"message": "success", "value": map_dict["maps"][int(map_id)]}
    except KeyError:
        return {"message": "map not found", "value": ""}
    except ValueError:
        return {"message": "invalid request", "value": "Non integer map_id specified"}

@app.get("/users")
async def read_users():
    map_dict = db.get_dict()
    return {"users": map_dict["users"]}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    try:
        map_dict = db.get_dict()
        return map_dict["users"][int(user_id)]
    except KeyError:
        return {"message": "user not found", "value": ""}
    except ValueError:
        return {"message": "invalid request", "value": "Non integer user_id specified"}


@app.post("/")
async def post_root(_item: User):
    return {"message": "invalid request", "value": "Can't post to root"}

@app.post("/users")
async def post_user(user: User):
    try:
        db.insert_user(
            user.username,
            user.email,
            user.password
        )

        return {"message": "success", "value": ""}
    except IntegrityError:
        return {"message": "user exists", "value": ""}

@app.post("/users/{user_id}")
async def edit_user(user_id: str, user: User):
    try:

        db.edit_user(user_id, user.username, user.email, user.password)


        return {"message": "success", "value": ""}
    except KeyError as e:
        return {"message": "user not found", "value": ""}
    except ValueError:
        return {"message": "invalid request", "value": "Non integer user_id specified"}


@app.post("/maps")
async def post_map(map: Map):
    try:
        db.insert_user(
            user.username,
            user.email,
            user.password
        )

        return {"message": "success", "value": ""}
    except IntegrityError:
        return {"message": "user exists", "value": ""}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080)

