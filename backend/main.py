from typing import Union
import subprocess
import sys

#import FaskAPI and pydantic
#Install the packages if needed

try:
    from fastapi import FastAPI
    from pydantic import BaseModel
    import uvicorn

except:
    print("Warning: FastAPI and it's dependencies are not installed", file=sys.stderr)
    print("Installing requirements...")

    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])


#Import project modules
import simple_module



app = FastAPI()


#Communication with the server (Simple example)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, x: Union[str, None] = None):
    return {"item_id": item_id, "x": x}



# Main (create local server)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


