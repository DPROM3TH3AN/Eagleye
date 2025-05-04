# backend/models/schemas.py
from pydantic import BaseModel
from typing import Dict, Any

# Chatbot models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

# Tracking models (tomtom)
class TrackingData(BaseModel):
    device_id: str
    imei: str = None

class TrackingResponse(BaseModel):
    location: Dict[str, float]
    nextbillion_data: Dict[str, Any] = None

# Phone number analysis models
class NumberAnalysisRequest(BaseModel):
    number: str

class NumberAnalysisResponse(BaseModel):
    analysis: Dict[str, Any]
