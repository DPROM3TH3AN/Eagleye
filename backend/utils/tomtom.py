# backend/utils/tomtom.py
import requests
import os

TOMTOM_API_KEY = os.getenv('YOUR_TOMTOM_API_KEY')  # update with your TomTom key
TOMTOM_BASE_URL = "https://api.tomtom.com/search/2/reverseGeocode/{lat},{lon}.json"

def get_tracking_info(identifier: str, lat: float, lon: float):
    url = TOMTOM_BASE_URL.format(lat=lat, lon=lon)
    params = {
        "key": TOMTOM_API_KEY
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()
