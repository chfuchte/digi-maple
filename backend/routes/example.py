from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from db.models.map import Map
from db.models.markers import Marker
from db.models.user import User
from db.database import get_session
from env import is_docker

router = APIRouter()

@router.get("/maps")
def get_maps(session: Session = Depends(get_session)):
    maps = session.query(Map).all()
    response = []
    for map_instance in maps:
        markers = session.query(Marker).filter_by(map_id=map_instance.id).all()
        markers_data = [
            {
                "id": marker.id,
                "x": marker.x,
                "y": marker.y,
                "display": {
                    "title": marker.title,
                    "description": marker.description,
                    "markerType": marker.type,
                },
            }
            for marker in markers
        ]
        map_data = {
            "id": map_instance.id,
            "name": map_instance.title,
            "author": session.query(User).filter_by(id=map_instance.author_id).first().full_name,
            "imgUrl": map_instance.img_url,
            "imgWidth": map_instance.imgWidth,
            "imgHeight": map_instance.imgHeight,
            "markers": markers_data,
        }
        response.append(map_data)
    return response

@router.get("/insert-example-user")
def insert_example_user(session: Session = Depends(get_session)):
    if session.query(User).filter_by(email="test@test.com").first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Example user already exists")
    user = User(email="test@test.com", full_name="Test User", password="test")
    session.add(user)
    session.commit()
    return user

@router.get("/insert-example-map")
def insert_example_map(session: Session = Depends(get_session)):
    demo_map_url = "http://localhost/dev/Lageplan_Campus_Bockenheim.svg" if is_docker() else "http://localhost:3000/dev/Lageplan_Campus_Bockenheim.svg"
    if session.query(Map).filter_by(img_url=demo_map_url).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Example map already exists")
    author_id = session.query(User).filter_by(email="test@test.com").first().id
    if not author_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Example user does not exist")
    map = Map(title="Uni Campus Bockenheim", img_url=demo_map_url, imgWidth=1885, imgHeight=2000, author_id=author_id)
    session.add(map)
    session.commit()
    map = session.query(Map).filter_by(img_url=demo_map_url).first()
    marker1 = Marker(x=942, y=1000, map_id=map.id, title="Wuhu", description="Ich bin ein marker", type="default")
    marker2 = Marker(x=942, y=800, map_id=map.id, title="Sekretariat", description="Get some help here", type="info")
    marker3 = Marker(x=942, y=600, map_id=map.id, title="Achtung", description="Viele Besucher hier", type="warning")
    marker4 = Marker(x=942, y=400, map_id=map.id, title="Eingang zum Gebäude", description="Barrierefreier Eingang zum Gebäude", type="weelchair")
    session.add(marker1)
    session.add(marker2)
    session.add(marker3)
    session.add(marker4)
    session.commit()
    return map
