import subprocess
import sys

#import FaskAPI and pydantic
#Install the packages if needed

try:
    from fastapi import FastAPI
    import uvicorn

except:
    print("Warning: FastAPI and it's dependencies are not installed", file=sys.stderr)
    print("Installing requirements...")

    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

    from fastapi import FastAPI
    import uvicorn


#Import project modules
import database_layout_tables as db
import example_database_entry as ex

app = FastAPI()

#Load example entry to the database (Uncomment the lines below)

ex.new_user()
ex.new_map()

# Get the contents of the data base as a python dictionary to parse it through FastAPI
map_dict: dict = db.get_dict()

#Upload the database contents to the server
@app.get("/")
def read_root():
    return map_dict

# Main (run local server)
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


