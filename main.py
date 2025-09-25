from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Location(BaseModel):
    device_id: str
    latitude: float
    longitude: float

@app.post("/locations")
async def receive_location(loc: Location):
    # Ide jön majd az adatbázisba mentés logikája
    return {"status": "ok", "device_id": loc.device_id}
