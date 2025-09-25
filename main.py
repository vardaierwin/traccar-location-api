from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
DATABASE_URL = os.getenv("DATABASE_URL")

class Location(BaseModel):
    device_id: str
    latitude: float
    longitude: float

@app.post("/locations")
async def receive_location(loc: Location):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO locations (device_id, latitude, longitude) VALUES (%s, %s, %s)",
            (loc.device_id, loc.latitude, loc.longitude)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        return {"status": "error", "message": str(e)}

    return {"status": "ok", "device_id": loc.device_id}

@app.get("/")
def read_root():
    return {"status": "ok", "message": "FastAPI is running!"}
