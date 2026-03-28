from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone
from emergentintegrations.llm.chat import LlmChat, UserMessage

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Models
class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class ChatRequest(BaseModel):
    session_id: str
    message: str
    agent_type: str

class ChatResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    session_id: str
    response: str
    timestamp: str

class ChatHistory(BaseModel):
    model_config = ConfigDict(extra="ignore")
    session_id: str
    messages: List[ChatMessage]

class JobApplication(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    full_name: str
    email: str
    phone: str
    address: str
    position_applied: str
    education: str
    experience: str
    skills: str
    reference_name: str
    reference_contact: str
    reference_relationship: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class Feedback(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    rating: int
    category: str
    feedback_text: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class Appointment(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    patient_name: str
    email: str
    phone: str
    address: str
    date_of_birth: str
    appointment_date: str
    appointment_time: str
    reason: str
    medical_history: Optional[str] = ""
    status: str = "pending"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

# Helper function to get chat history
async def get_chat_messages(session_id: str, agent_type: str):
    collection_map = {
        "healthcare": "healthcare_chats",
        "support": "support_chats",
        "customer_service": "customer_service_chats"
    }
    collection = db[collection_map.get(agent_type, "healthcare_chats")]
    chat = await collection.find_one({"session_id": session_id}, {"_id": 0})
    if chat:
        return chat.get("messages", [])
    return []

# Helper function to save chat message
async def save_chat_message(session_id: str, agent_type: str, role: str, content: str):
    collection_map = {
        "healthcare": "healthcare_chats",
        "support": "support_chats",
        "customer_service": "customer_service_chats"
    }
    collection = db[collection_map.get(agent_type, "healthcare_chats")]
    
    message = ChatMessage(role=role, content=content)
    
    await collection.update_one(
        {"session_id": session_id},
        {
            "$push": {"messages": message.model_dump()},
            "$setOnInsert": {"created_at": datetime.now(timezone.utc).isoformat()}
        },
        upsert=True
    )

# Routes
@api_router.get("/")
async def root():
    return {"message": "Multi Task Chatbox API"}

@api_router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    try:
        # Save user message
        await save_chat_message(request.session_id, request.agent_type, "user", request.message)
        
        # Get chat history for context
        history = await get_chat_messages(request.session_id, request.agent_type)
        
        # System messages for different agents
        system_messages = {
            "healthcare": "You are a knowledgeable healthcare AI assistant specializing in weight management, home remedies, exercise recommendations, and general health advice. Provide helpful, empathetic, and scientifically-backed guidance. Always remind users to consult healthcare professionals for serious concerns.",
            "support": "You are a helpful customer support agent. Answer questions clearly, resolve issues efficiently, and provide solutions promptly. Be friendly, professional, and patient.",
            "customer_service": "You are a customer service representative. Help with product inquiries, service information, returns, and troubleshooting. Proactively address common questions and ensure customer satisfaction."
        }
        
        system_message = system_messages.get(request.agent_type, system_messages["healthcare"])
        
        # Initialize LLM chat
        llm_key = os.environ.get('EMERGENT_LLM_KEY')
        chat = LlmChat(
            api_key=llm_key,
            session_id=request.session_id,
            system_message=system_message
        ).with_model("openai", "gpt-5.2")
        
        # Create user message
        user_message = UserMessage(text=request.message)
        
        # Get AI response
        ai_response = await chat.send_message(user_message)
        
        # Save AI response
        await save_chat_message(request.session_id, request.agent_type, "assistant", ai_response)
        
        return ChatResponse(
            session_id=request.session_id,
            response=ai_response,
            timestamp=datetime.now(timezone.utc).isoformat()
        )
    except Exception as e:
        logging.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/chat/history/{session_id}/{agent_type}")
async def get_chat_history(session_id: str, agent_type: str):
    messages = await get_chat_messages(session_id, agent_type)
    return {"session_id": session_id, "messages": messages}

@api_router.post("/job-application")
async def submit_job_application(application: JobApplication):
    try:
        app_dict = application.model_dump()
        await db.job_applications.insert_one(app_dict)
        return {"success": True, "message": "Application submitted successfully", "id": application.id}
    except Exception as e:
        logging.error(f"Job application error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/job-applications")
async def get_job_applications():
    applications = await db.job_applications.find({}, {"_id": 0}).to_list(1000)
    return {"applications": applications}

@api_router.post("/feedback")
async def submit_feedback(feedback: Feedback):
    try:
        feedback_dict = feedback.model_dump()
        await db.feedback.insert_one(feedback_dict)
        return {"success": True, "message": "Feedback submitted successfully", "id": feedback.id}
    except Exception as e:
        logging.error(f"Feedback error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/feedback")
async def get_feedback():
    feedback_list = await db.feedback.find({}, {"_id": 0}).to_list(1000)
    return {"feedback": feedback_list}

@api_router.post("/appointments")
async def book_appointment(appointment: Appointment):
    try:
        appointment_dict = appointment.model_dump()
        await db.appointments.insert_one(appointment_dict)
        return {"success": True, "message": "Appointment booked successfully", "id": appointment.id}
    except Exception as e:
        logging.error(f"Appointment error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/appointments")
async def get_appointments():
    appointments = await db.appointments.find({}, {"_id": 0}).to_list(1000)
    return {"appointments": appointments}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()