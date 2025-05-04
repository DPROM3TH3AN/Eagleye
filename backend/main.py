# backend/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from backend.routers import chat, tracking, numbers

app = FastAPI(
    title="Tracking System API",
    description="API for chat, device tracking (including IMEI), phone analysis, realtime updates, and NextBillion AI integration.",
    version="1.0.0"
)

# Include routers for different services
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(tracking.router, prefix="/tracking", tags=["Tracking"])
app.include_router(numbers.router, prefix="/numbers", tags=["Numbers"])

# Mount static files and templates
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

@app.get("/")
async def root():
    return {"message": "Welcome to the Tracking System API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
