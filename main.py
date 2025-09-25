from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

@app.get("/locations")
def receive_location(device_id: str, lat: float, lon: float):
    # Ide jön az adatbázisba mentés logikája
    print(f"Device {device_id} -> {lat},{lon}")  # ideiglenes debug
    return {"status": "ok", "device_id": device_id}

@app.post("/locations")
async def receive_location_post(loc: dict):
    # POST verzió JSON-ból
    return {"status": "ok", "device_id": loc.get("device_id")}

@app.get("/")
def read_root():
    return {"status": "ok", "message": "FastAPI is running!"}