from fastapi import APIRouter, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
import os
import sqlite3
from PIL import Image
from io import BytesIO
from env import DB_PATH as DATABASE_PATH
from env import IMAGES_DIR as ABSOLUTE_IMAGES_DIR

router = APIRouter()

conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()


def save_image(file, map_id: int):
    if not os.path.exists(ABSOLUTE_IMAGES_DIR):
        os.makedirs(ABSOLUTE_IMAGES_DIR)

    image_path = os.path.join(ABSOLUTE_IMAGES_DIR, f"{map_id}_original.jpg")
    with open(image_path, "wb") as f:
        f.write(file)

    # Convert image to WebP
    img = Image.open(BytesIO(file))
    img.save(f"{ABSOLUTE_IMAGES_DIR}/{map_id}.webp", "WEBP", quality=90)

    # Get image dimensions
    width, height = img.size

    return width, height, image_path


# Endpoint to upload a map image
@router.post("/api/maps/upload/{map_id}")
async def upload_map_image(map_id: int, file: UploadFile = File(...)):
    print(f"POST /api/maps/upload/{map_id} called")

    # Save the image and convert to webp
    content = await file.read()
    width, height, original_image_path = save_image(content, map_id)

    # Update map with image dimensions
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE maps SET imgWidth = ?, imgHeight = ? WHERE id = ?", (width, height, map_id))
    conn.commit()

    # Return image URL
    image_url = f"http://localhost:8000/api/maps/images/{map_id}.webp"
    print(f"Map {map_id} updated with new image: {image_url}")
    
    # Remove the original image
    os.remove(original_image_path)

    return JSONResponse(content={"imageUrl": image_url, "imgWidth": width, "imgHeight": height}, status_code=200)


# Endpoint to create a new map
@router.post("/api/maps")
async def create_map(name: str, user_id: int):
    print(f"POST /api/maps called")

    if not name:
        raise HTTPException(status_code=400, detail="Name is required")

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO maps (name, userId) VALUES (?, ?)", (name, user_id))
    conn.commit()
    map_id = cursor.lastrowid

    print(f"Map created with ID: {map_id}")
    return {"id": map_id}


# Endpoint to get the user's maps
@router.get("/api/maps/my")
async def get_user_maps(user_id: int):
    print(f"GET /api/maps/my called")

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, imgWidth, imgHeight FROM maps WHERE userId = ?", (user_id,))
    maps = cursor.fetchall()

    if not maps:
        raise HTTPException(status_code=404, detail="No maps found")

    result = []
    for map in maps:
        map_id, name, img_width, img_height = map
        img_url = f"http://localhost:8000/api/maps/images/{map_id}.webp"
        result.append({"id": map_id, "name": name, "imgUrl": img_url, "imgWidth": img_width, "imgHeight": img_height})

    return result


# Endpoint to search maps by name
@router.get("/api/maps/search")
async def search_maps(s: str):
    print(f"GET /api/maps/search called with search term: {s}")

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    if not s:
        cursor.execute("SELECT id, name, imgWidth, imgHeight FROM maps LIMIT 10")
    else:
        cursor.execute("SELECT id, name, imgWidth, imgHeight FROM maps WHERE name LIKE ?", ('%' + s + '%',))
    maps = cursor.fetchall()

    if not maps:
        raise HTTPException(status_code=404, detail="No maps found")

    result = []
    for map in maps:
        map_id, name, img_width, img_height = map
        img_url = f"http://localhost:8000/api/maps/images/{map_id}.webp"
        result.append({"id": map_id, "name": name, "imgUrl": img_url, "imgWidth": img_width, "imgHeight": img_height})

    return result


# Endpoint to get details of a specific map
@router.get("/api/maps/{map_id}")
async def get_map(map_id: int):
    print(f"GET /api/maps/{map_id} called")

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, imgWidth, imgHeight FROM maps WHERE id = ?", (map_id,))
    map_details = cursor.fetchone()

    if not map_details:
        raise HTTPException(status_code=404, detail="Map not found")

    map_id, name, img_width, img_height = map_details
    img_url = f"http://localhost:8000/api/maps/images/{map_id}.webp"

    cursor.execute("SELECT id, x, y, title, description, color, icon FROM markers WHERE mapId = ?", (map_id,))
    markers = cursor.fetchall()

    marker_data = [{"id": marker[0], "x": marker[1], "y": marker[2], "title": marker[3], "description": marker[4], "color": marker[5], "icon": marker[6]} for marker in markers]

    return {
        "id": map_id,
        "name": name,
        "imgWidth": img_width,
        "imgHeight": img_height,
        "imgUrl": img_url,
        "markers": marker_data
    }


# Endpoint to delete a map
@router.delete("/api/maps/{map_id}")
async def delete_map(map_id: int):
    print(f"DELETE /api/maps/{map_id} called")

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM maps WHERE id = ?", (map_id,))
    conn.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Map not found")

    print(f"Map deleted with ID: {map_id}")
    return {"message": "Map deleted successfully"}


# Endpoint to update a map's name
@router.patch("/api/maps/{map_id}")
async def update_map(map_id: int, name: str):
    print(f"PATCH /api/maps/{map_id} called")

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE maps SET name = ? WHERE id = ?", (name, map_id))
    conn.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Map not found")

    print(f"Map updated with ID: {map_id}")
    return {"message": "Map updated successfully"}


# Endpoint to add a marker to a map
@router.post("/api/maps/{map_id}/markers")
async def add_marker(map_id: int, x: int, y: int, title: str, description: str, color: str, icon: str):
    print(f"POST /api/maps/{map_id}/markers called")

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO markers (mapId, x, y, title, description, color, icon) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (map_id, x, y, title, description, color, icon))
    conn.commit()

    marker_id = cursor.lastrowid
    print(f"Marker added to map with ID: {map_id}")
    return {"id": marker_id}


# Endpoint to update a marker on a map
@router.patch("/api/maps/{map_id}/markers/{marker_id}")
async def update_marker(map_id: int, marker_id: int, x: int = None, y: int = None, title: str = None, description: str = None, color: str = None, icon: str = None):
    print(f"PATCH /api/maps/{map_id}/markers/{marker_id} called")

    update_data = {"x": x, "y": y, "title": title, "description": description, "color": color, "icon": icon}
    update_data = {key: value for key, value in update_data.items() if value is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields to update")

    set_clause = ", ".join([f"{key} = ?" for key in update_data.keys()])
    values = list(update_data.values()) + [marker_id]

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE markers SET {set_clause} WHERE id = ?", values)
    conn.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Marker not found")

    print(f"Marker updated with ID: {marker_id}")
    return {"message": "Marker updated successfully"}


# Endpoint to delete a marker from a map
@router.delete("/api/maps/{map_id}/markers/{marker_id}")
async def delete_marker(map_id: int, marker_id: int):
    print(f"DELETE /api/maps/{map_id}/markers/{marker_id} called")

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM markers WHERE id = ?", (marker_id,))
    conn.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Marker not found")

    print(f"Marker deleted from map with ID: {map_id}")
    return {"message": "Marker deleted successfully"}
