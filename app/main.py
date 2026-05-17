from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uuid
from app.chatbot import CustomerSupportBot

app = FastAPI(title="Customer Support Bot")

# CORS enable করো (frontend এর জন্য)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chatbot initialize
bot = CustomerSupportBot()

# Request/Response Models
class ChatRequest(BaseModel):
    user_id: str = ""
    message: str

class ChatResponse(BaseModel):
    user_id: str
    reply: str

# API Endpoints
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat endpoint"""
    # New user হলে ID দাও
    user_id = request.user_id or str(uuid.uuid4())
    
    # Response নাও
    reply = bot.get_response(user_id, request.message)
    
    return ChatResponse(user_id=user_id, reply=reply)

@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "🟢 Running",
        "model": "Gemini 2.5 Flash"
    }

@app.get("/")
async def home():
    """Serve frontend"""
    return FileResponse("frontend/index.html")

# Static files serve করো
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Server run করার জন্য
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)