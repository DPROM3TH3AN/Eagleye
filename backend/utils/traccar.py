# backend/utils/traccar.py
import random

def simulate_gps_data(identifier: str):
    lat = round(random.uniform(-90, 90), 6)
    lon = round(random.uniform(-180, 180), 6)
    return {"identifier": identifier, "lat": lat, "lon": lon}
