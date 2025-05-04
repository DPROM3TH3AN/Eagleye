# backend/routers/chat.py
from fastapi import APIRouter, HTTPException, Query
from backend.models.schemas import ChatRequest, ChatResponse
from backend.utils.nlp_utils import process_message

router = APIRouter()

# Secured POST endpoint for chatbot
@router.post("/message", response_model=ChatResponse)
async def send_message(chat_request: ChatRequest):
    if not chat_request.message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
    reply = process_message(chat_request.message)
    return ChatResponse(reply=reply)

# Open GET endpoint for chatbot (no API key required)
@router.get("/open/message", response_model=ChatResponse)
async def open_chat_message(message: str = Query(..., description="The message to be processed by the chatbot")):
    if not message:
        raise HTTPException(status_code=400, detail="Message query parameter is required.")
    reply = process_message(message)
    return ChatResponse(reply=reply)
