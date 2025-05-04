# backend/routers/tracking.py
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, Query
from backend.models.schemas import TrackingData, TrackingResponse
from backend.utils.traccar import simulate_gps_data
from backend.utils.supabase_client import insert_tracking_data
from backend.utils.tomtom import get_tracking_info  # Using TomTom integration
import folium

router = APIRouter()

# Basic Tracking Endpoint (simulation only)
@router.post("/", response_model=TrackingResponse)
async def track_device(data: TrackingData):
    if not data.device_id:
        raise HTTPException(status_code=400, detail="Device ID is required.")
    identifier = data.imei if data.imei else data.device_id
    location = simulate_gps_data(identifier)
    insert_tracking_data(location)
    return TrackingResponse(location=location)

# Tracking endpoint with TomTom enrichment
@router.get("/tomtom", response_model=TrackingResponse)
async def tomtom_tracking(
    device_id: str = Query(None, description="Device identifier"),
    imei: str = Query(None, description="IMEI number")
):
    identifier = imei if imei else device_id
    if not identifier:
        raise HTTPException(status_code=400, detail="Device ID or IMEI is required.")
    
    location = simulate_gps_data(identifier)
    try:
        enriched_info = get_tracking_info(identifier, location["lat"], location["lon"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling TomTom API: {e}")
    
    # Combine basic and enriched information
    combined_data = {"location": location, "enriched_data": enriched_info}
    insert_tracking_data(combined_data)
    return TrackingResponse(location=location, enriched_data=enriched_info)

# Realtime tracking via WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections = []
    async def connect(self, websocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    def disconnect(self, websocket):
        self.active_connections.remove(websocket)
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@router.websocket("/ws/tracking")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            identifier = data.get("device_id") or data.get("imei")
            if not identifier:
                await websocket.send_json({"error": "No identifier provided."})
                continue
            location = simulate_gps_data(identifier)
            insert_tracking_data(location)
            await manager.broadcast({"location": location})
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Map endpoint using Folium
@router.get("/map")
async def get_tracking_map(device_id: str = None, imei: str = None):
    identifier = imei if imei else device_id
    if not identifier:
        raise HTTPException(status_code=400, detail="Device ID or IMEI is required.")
    location = simulate_gps_data(identifier)
    m = folium.Map(location=[location["lat"], location["lon"]], zoom_start=13)
    folium.Marker([location["lat"], location["lon"]], popup=f"{identifier} Location").add_to(m)
    map_html = m._repr_html_()
    return {"map": map_html}
