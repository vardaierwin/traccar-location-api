from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")
TRACCAR_URL = os.getenv("TRACCAR_URL")

class Location(BaseModel):
    device_id: str
    latitude: float
    longitude: float

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

    # 2. Forward az ngrok URL-re
    try:
        payload = {"id": loc.device_id, "lat": loc.latitude, "lon": loc.longitude}
        r = requests.get(f"{TRACCAR_URL}/?id={payload['id']}&lat={payload['lat']}&lon={payload['lon']}")
    except Exception as e:
        print("Traccar forward error:", e)

    return {"status": "ok", "device_id": loc.device_id}

@app.get("/")
def read_root():
    return {"status": "ok", "message": "FastAPI is running!"}
