from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import requests
import os

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")
TRACCAR_URL = os.getenv("TRACCAR_URL")

# Adatmodell
class Location(BaseModel):
    device_id: str
    latitude: float
    longitude: float

# POST endpoint (JSON-ból)
@app.post("/locations")
async def receive_location(loc: Location):
    # 1. Mentés Neon DB-be
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

    # 2. Forward a Traccar szerver felé
    try:
        payload = {
            "id": loc.device_id,
            "lat": loc.latitude,
            "lon": loc.longitude
        }
        r = requests.get(f"{TRACCAR_URL}/?{payload}")
    except Exception as e:
        print("Traccar forward error:", e)

    return {"status": "ok", "device_id": loc.device_id}

# GET teszt
@app.get("/")
def read_root():
    return {"status": "ok", "message": "FastAPI is running!"}
