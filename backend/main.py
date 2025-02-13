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
    x: int
    y: int
    title: str
    description: str
    type: str



class Map(BaseModel):
    name: str
    author: str
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
    map_dict = db.get_dict()
    return {"root": map_dict}

@app.get("/maps")
async def read_maps():
    map_dict = db.get_dict()
    return {"message": "success","value": map_dict["maps"]}

@app.get("/maps/{map_id}")
async def read_map(map_id: str):
    map_dict = db.get_dict()
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
        return {"message": "success", "value": map_dict["users"][int(user_id)]}
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
async def post_map(map_obj: Map):
    try:

        db.insert_map(
            map_obj.name,
            map_obj.author,
            map_obj.imgUrl,
            map_obj.imgWidth,
            map_obj.imgHeight,
        )

        # Fetch the map ID
        map_id = db.get_map_id_by_name(map_obj.name)
        print(map_id)

        # Insert markers for the map

        for marker in map_obj.markers:
            db.insert_marker(
                map_id,
                marker.x,
                marker.y,
                marker.title,
                marker.description,
                marker.type,
            )


        return {"message": "success", "value": ""}
    except IntegrityError:
        return {"message": "map exists", "value": str(map_obj)}



@app.post("/maps/{map_id}")
async def edit_map(map_id: str, map_obj: Map):
    try:

        db.edit_map(
            map_id,
            map_obj.name,
            map_obj.author,
            map_obj.imgUrl,
            map_obj.imgWidth,
            map_obj.imgHeight,
            map_obj.markers,
        )


        return {"message": "success", "value": ""}
    except KeyError as e:
        return {"message": "user not found", "value": ""}
    except ValueError:
        return {"message": "invalid request", "value": "Non integer user_id specified"}
    except IntegrityError as e:
        return {"message": "unique constraint failed", "value": str(e)}




if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080)




"""
Endpoint documentation:
[HTTP request; path; data]


POST; 127.0.0.1:8080/users; {"username": "edited", "email": "exampl_editede@email.gmail.com", "password": "pass123456789"}
    -> Uploads a new user with the specified properties (name, email, password)


POST; 127.0.0.1:8080/users/{user_id}; {"username": "edited", "email": "exampl_editede@email.gmail.com", "password": "pass123456789"}
    -> Edits the user going by {user_id} to satisfy the specified properties


POST

"""
