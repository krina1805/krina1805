from fastapi import FastAPI, APIRouter, HTTPException, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
import sqlite3
import hashlib
import hmac
import secrets
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone
from emergentintegrations.llm.chat import LlmChat, UserMessage

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')
templates = Jinja2Templates(directory=str(ROOT_DIR / "templates"))
SQLITE_DB_PATH = ROOT_DIR / "chatbot_history.db"

# MongoDB connection (optional for local chatbot-only mode)
mongo_url = os.environ.get("MONGO_URL")
db_name = os.environ.get("DB_NAME", "app_db")
client = AsyncIOMotorClient(mongo_url) if mongo_url else None
db = client[db_name] if client else None

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
    if db is None:
        return []

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
    if db is None:
        return

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
    if db is None:
        raise HTTPException(status_code=503, detail="MongoDB is not configured. Set MONGO_URL and DB_NAME.")

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
    if db is None:
        raise HTTPException(status_code=503, detail="MongoDB is not configured. Set MONGO_URL and DB_NAME.")
    try:
        app_dict = application.model_dump()
        await db.job_applications.insert_one(app_dict)
        return {"success": True, "message": "Application submitted successfully", "id": application.id}
    except Exception as e:
        logging.error(f"Job application error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/job-applications")
async def get_job_applications():
    if db is None:
        raise HTTPException(status_code=503, detail="MongoDB is not configured. Set MONGO_URL and DB_NAME.")
    applications = await db.job_applications.find({}, {"_id": 0}).to_list(1000)
    return {"applications": applications}

@api_router.post("/feedback")
async def submit_feedback(feedback: Feedback):
    if db is None:
        raise HTTPException(status_code=503, detail="MongoDB is not configured. Set MONGO_URL and DB_NAME.")
    try:
        feedback_dict = feedback.model_dump()
        await db.feedback.insert_one(feedback_dict)
        return {"success": True, "message": "Feedback submitted successfully", "id": feedback.id}
    except Exception as e:
        logging.error(f"Feedback error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/feedback")
async def get_feedback():
    if db is None:
        raise HTTPException(status_code=503, detail="MongoDB is not configured. Set MONGO_URL and DB_NAME.")
    feedback_list = await db.feedback.find({}, {"_id": 0}).to_list(1000)
    return {"feedback": feedback_list}

@api_router.post("/appointments")
async def book_appointment(appointment: Appointment):
    if db is None:
        raise HTTPException(status_code=503, detail="MongoDB is not configured. Set MONGO_URL and DB_NAME.")
    try:
        appointment_dict = appointment.model_dump()
        await db.appointments.insert_one(appointment_dict)
        return {"success": True, "message": "Appointment booked successfully", "id": appointment.id}
    except Exception as e:
        logging.error(f"Appointment error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/appointments")
async def get_appointments():
    if db is None:
        raise HTTPException(status_code=503, detail="MongoDB is not configured. Set MONGO_URL and DB_NAME.")
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
app.add_middleware(SessionMiddleware, secret_key=os.environ.get("SESSION_SECRET", "dev-session-secret"))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
if db is None:
    logger.warning("MONGO_URL not set. Mongo-backed endpoints will return 503; /chatbot remains available.")

def init_sqlite_db():
    with sqlite3.connect(SQLITE_DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS chatbot_conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_input TEXT NOT NULL,
                chatbot_response TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS chatbot_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()

def hash_password(password: str, salt: Optional[str] = None) -> str:
    salt = salt or secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 200000).hex()
    return f"{salt}${hashed}"

def verify_password(password: str, password_hash: str) -> bool:
    try:
        salt, stored_hash = password_hash.split("$", 1)
    except ValueError:
        return False
    recalculated = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 200000).hex()
    return hmac.compare_digest(stored_hash, recalculated)

def get_user_by_email(email: str):
    with sqlite3.connect(SQLITE_DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        user = conn.execute(
            "SELECT id, name, email, password_hash, created_at FROM chatbot_users WHERE email = ?",
            (email.lower().strip(),),
        ).fetchone()
    return dict(user) if user else None

def create_user(name: str, email: str, password: str):
    with sqlite3.connect(SQLITE_DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO chatbot_users (name, email, password_hash, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (name.strip(), email.lower().strip(), hash_password(password), datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()

def generate_chatbot_response(user_input: str, recent_messages: Optional[List[dict]] = None) -> str:
    text = user_input.lower().strip()
    recent_messages = recent_messages or []

    greeting_keywords = ("hello", "hi", "hey", "good morning", "good afternoon", "good evening")
    pricing_keywords = ("price", "pricing", "cost", "plan", "subscription")
    support_keywords = ("help", "support", "issue", "problem", "error", "trouble")
    escalation_keywords = ("human", "agent", "representative", "person")
    billing_keywords = ("invoice", "billing", "refund", "charged", "payment")
    integration_keywords = ("api", "integration", "webhook", "sdk")
    hours_keywords = ("hours", "open", "availability", "available", "time")
    contact_keywords = ("contact", "email", "phone", "call")
    features_keywords = ("feature", "features", "what can you do", "capabilities")
    thanks_keywords = ("thanks", "thank you", "appreciate")
    goodbye_keywords = ("bye", "goodbye", "see you")

    def contains_any(keywords):
        return any(keyword in text for keyword in keywords)

    if contains_any(greeting_keywords):
        return (
            "Hi, thanks for reaching out. I can help with pricing, feature details, support options, "
            "business hours, and contact information. What are you looking for today?"
        )

    if contains_any(features_keywords):
        return (
            "I can help with a few practical areas right now:\n"
            "• Compare available plans and expected usage fit\n"
            "• Share support channels and office hours\n"
            "• Walk through basic troubleshooting steps\n"
            "• Keep a server-side history of this conversation"
        )

    if contains_any(integration_keywords):
        return (
            "For integrations, start with these basics:\n"
            "• API docs and endpoint references under /api/\n"
            "• Use test credentials in a non-production environment first\n"
            "• Log request IDs so support can trace issues faster"
        )

    if contains_any(pricing_keywords):
        return (
            "Most teams choose between three options:\n"
            "• Starter: for individual or light usage\n"
            "• Growth: for regular team workflows and higher limits\n"
            "• Scale: for advanced security and dedicated support\n"
            "If you share your expected users or volume, I can suggest the best fit."
        )

    if contains_any(billing_keywords):
        return (
            "I can help with billing questions. Please include:\n"
            "• Invoice ID or billing email\n"
            "• Charge date and amount\n"
            "• Whether you need clarification, correction, or refund review"
        )

    if contains_any(hours_keywords):
        return "Support is available Monday to Friday, 9:00 AM–6:00 PM (UTC). For urgent issues, email support and include a short impact summary."

    if contains_any(contact_keywords):
        return (
            "You can contact the team through:\n"
            "• Email: support@example.com\n"
            "• Phone: +1 (800) 555-0100\n"
            "• API endpoint reference: /api/"
        )

    if contains_any(support_keywords):
        return (
            "Sorry you’re running into this. Let’s troubleshoot step by step:\n"
            "1) Tell me what action you were taking\n"
            "2) Share the exact error message if there is one\n"
            "3) Confirm whether it happens every time or intermittently"
        )

    if contains_any(escalation_keywords):
        return (
            "Absolutely — I can hand this off to a human support specialist. "
            "Please share your preferred contact method and a short summary of the issue."
        )

    if "more" in text and recent_messages:
        last_assistant = next(
            (message for message in reversed(recent_messages) if message.get("chatbot_response")),
            None
        )
        if last_assistant:
            return (
                "Sure — here are additional details based on the last topic:\n"
                f"{last_assistant.get('chatbot_response')}\n\n"
                "If you want, I can narrow this down for your specific situation."
            )

    if contains_any(thanks_keywords):
        return "You’re welcome. If you want, I can also help compare plans or continue troubleshooting."

    if contains_any(goodbye_keywords):
        return "Glad I could help. Reach out anytime."

    return (
        "I can help best with pricing, feature details, support troubleshooting, office hours, and contact options. "
        "Try asking: 'Which plan fits a small team?' or 'How do I report an urgent issue?'"
    )

def get_conversation_history(limit: int = 20):
    with sqlite3.connect(SQLITE_DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT user_input, chatbot_response, created_at
            FROM chatbot_conversations
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [dict(row) for row in reversed(rows)]

def get_conversation_history_for_display(limit: int = 20):
    history = get_conversation_history(limit=limit)
    formatted_history = []

    for item in history:
        timestamp = item.get("created_at", "")
        display_time = timestamp
        try:
            parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            display_time = parsed.astimezone(timezone.utc).strftime("%b %d, %Y %H:%M UTC")
        except Exception:
            pass

        formatted_history.append(
            {
                "user_input": item.get("user_input", ""),
                "chatbot_response": item.get("chatbot_response", ""),
                "created_at_display": display_time,
            }
        )

    return formatted_history

def save_conversation(user_input: str, chatbot_response: str):
    with sqlite3.connect(SQLITE_DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO chatbot_conversations (user_input, chatbot_response, created_at)
            VALUES (?, ?, ?)
            """,
            (user_input, chatbot_response, datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()

@app.on_event("startup")
async def startup_event():
    init_sqlite_db()

@app.get("/chatbot", response_class=HTMLResponse)
async def chatbot_page(request: Request):
    current_user = request.session.get("user")
    if not current_user:
        return RedirectResponse(url="/login?next=/chatbot", status_code=303)
    return templates.TemplateResponse(
        "chatbot.html",
        {
            "request": request,
            "chatbot_reply": None,
            "conversation_history": get_conversation_history_for_display(),
            "last_user_input": "",
            "current_user": current_user,
        },
    )

@app.post("/chatbot", response_class=HTMLResponse)
async def chatbot_submit(request: Request, user_input: str = Form(...)):
    current_user = request.session.get("user")
    if not current_user:
        return RedirectResponse(url="/login?next=/chatbot", status_code=303)
    recent_messages = get_conversation_history(limit=5)
    chatbot_reply = generate_chatbot_response(user_input, recent_messages=recent_messages)
    save_conversation(user_input, chatbot_reply)

    return templates.TemplateResponse(
        "chatbot.html",
        {
            "request": request,
            "chatbot_reply": chatbot_reply,
            "conversation_history": get_conversation_history_for_display(),
            "last_user_input": user_input,
            "current_user": current_user,
        },
    )

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse(
        "auth.html",
        {"request": request, "mode": "signup", "error": None, "success": None},
    )

@app.post("/signup", response_class=HTMLResponse)
async def signup_submit(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
):
    if password != confirm_password:
        return templates.TemplateResponse(
            "auth.html",
            {"request": request, "mode": "signup", "error": "Passwords do not match.", "success": None},
            status_code=400,
        )
    if len(password) < 8:
        return templates.TemplateResponse(
            "auth.html",
            {"request": request, "mode": "signup", "error": "Password must be at least 8 characters.", "success": None},
            status_code=400,
        )
    if get_user_by_email(email):
        return templates.TemplateResponse(
            "auth.html",
            {"request": request, "mode": "signup", "error": "An account with this email already exists.", "success": None},
            status_code=400,
        )

    create_user(name=name, email=email, password=password)
    return templates.TemplateResponse(
        "auth.html",
        {
            "request": request,
            "mode": "login",
            "error": None,
            "success": "Account created successfully. Please log in.",
        },
    )

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    if request.session.get("user"):
        return RedirectResponse(url="/chatbot", status_code=303)
    next_url = request.query_params.get("next", "/chatbot")
    return templates.TemplateResponse(
        "auth.html",
        {"request": request, "mode": "login", "error": None, "success": None, "next_url": next_url},
    )

@app.post("/login", response_class=HTMLResponse)
async def login_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    next_url: str = Form("/chatbot"),
):
    user = get_user_by_email(email)
    if not user or not verify_password(password, user["password_hash"]):
        return templates.TemplateResponse(
            "auth.html",
            {"request": request, "mode": "login", "error": "Invalid email or password.", "success": None},
            status_code=401,
        )

    request.session["user"] = {"id": user["id"], "name": user["name"], "email": user["email"]}
    safe_next = next_url if next_url.startswith("/") else "/chatbot"
    return RedirectResponse(url=safe_next, status_code=303)

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)

@app.on_event("shutdown")
async def shutdown_db_client():
    if client is not None:
        client.close()
