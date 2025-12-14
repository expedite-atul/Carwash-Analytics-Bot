from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from .agent import process_user_question, execute_approved_sql, add_golden_query
from .db import create_db_and_tables, engine, get_session
from .routers import auth_routes, admin_routes
from .auth import get_current_active_user
from .cache import cache
from .models import User, UserRole, ChatSession, ChatMessage
from sqlmodel import Session, select
from .security import get_password_hash
import json
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    
    # Seed Admin User if not exists
    with Session(engine) as session:
        statement = select(User).where(User.role == UserRole.ADMIN)
        admin = session.exec(statement).first()
        if not admin:
            print("Seeding Default Admin User...")
            admin_user = User(
                email="admin@carwash.com",
                hashed_password=get_password_hash("password123"),
                full_name="System Admin",
                role=UserRole.ADMIN
            )
            session.add(admin_user)
            session.commit()
            print("Admin created: admin@carwash.com / password123")
            
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth_routes.router)
app.include_router(admin_routes.router)

# Allow frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ExecuteRequest(BaseModel):
    sql: str

class FeedbackRequest(BaseModel):
    question: str
    sql: str

@app.post("/chat/feedback")
async def feedback_endpoint(request: FeedbackRequest, user: User = Depends(get_current_active_user)):
    """User likes a query -> Add to Golden Queries (RBAC: Employees can do this too)."""
    success = add_golden_query(request.question, request.sql)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to save feedback")
    return {"status": "success", "message": "Feedback received! I got smarter."}

@app.get("/chat/history")
async def get_chat_history(user: User = Depends(get_current_active_user), session: Session = Depends(get_session)):
    """Fetch recent chat history for the user."""
    # MVP: Get or Create a default session
    chat_session = session.exec(select(ChatSession).where(ChatSession.user_id == user.id).order_by(ChatSession.id.desc())).first()
    
    if not chat_session:
        return []
    
    messages = session.exec(select(ChatMessage).where(ChatMessage.session_id == chat_session.id).order_by(ChatMessage.created_at)).all()
    
    # Format for frontend
    history = []
    for m in messages:
        try:
            # Parse meta_info if it exists
            meta = json.loads(m.meta_info) if m.meta_info else {}
            
            msg_obj = {
                "role": m.role, # 'user' or 'model' (stored as 'bot' in db maybe? let's standardise to 'model' for frontend)
                "content": m.content,
                **meta
            }
            # Unify role names
            if m.role == "bot": msg_obj["role"] = "model"
            
            history.append(msg_obj)
        except:
            history.append({"role": m.role, "content": m.content})
            
    return history

@app.post("/chat/plan")
async def create_plan(
    request: ChatRequest, 
    user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    # 1. Get/Create Session
    chat_session = session.exec(select(ChatSession).where(ChatSession.user_id == user.id).order_by(ChatSession.id.desc())).first()
    if not chat_session:
        chat_session = ChatSession(user_id=user.id, title="New Chat")
        session.add(chat_session)
        session.commit()
        session.refresh(chat_session)

    # 2. Save User Message
    user_msg = ChatMessage(
        session_id=chat_session.id,
        role="user",
        content=request.message
    )
    session.add(user_msg)
    
    # 3. Generate Plan
    plan_response = await process_user_question(request.message)
    
    # 4. Save Bot Response
    meta = {}
    if plan_response["status"] == "success":
        meta = {
            "type": "plan",
            "sql": plan_response["sql"]
        }
        content = plan_response["explanation"]
    else:
        content = f"Error: {plan_response['message']}"

    bot_msg = ChatMessage(
        session_id=chat_session.id,
        role="model",
        content=content,
        meta_info=json.dumps(meta)
    )
    session.add(bot_msg)
    session.commit()
    
    return plan_response

@app.post("/chat/execute")
async def execute_query(
    request: ExecuteRequest, 
    user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    # 1. Execute
    result_response = execute_approved_sql(request.sql)
    
    # 2. Save Result (to the latest session)
    chat_session = session.exec(select(ChatSession).where(ChatSession.user_id == user.id).order_by(ChatSession.id.desc())).first()
    if chat_session:
        content = "Here is the result."
        meta = {}
        
        if result_response["status"] == "success":
             meta = {
                 "type": result_response["type"],
                 "data": result_response["data"],
                 "sql": request.sql
             }
        else:
            content = f"Execution Error: {result_response['message']}"

        bot_msg = ChatMessage(
            session_id=chat_session.id,
            role="model",
            content=content,
            meta_info=json.dumps(meta)
        )
        session.add(bot_msg)
        session.commit()

    # 3. Auto-Learn (Feedback Loop)
    if result_response["status"] == "success":
        # Get the executed SQL 
        # Get the original question (Last user message in this session)
        last_user_msg = session.exec(
            select(ChatMessage)
            .where(ChatMessage.session_id == chat_session.id)
            .where(ChatMessage.role == "user")
            .order_by(ChatMessage.created_at.desc())
        ).first()

        if last_user_msg:
            print(f"Auto-Learning: Saving '{last_user_msg.content}' -> SQL")
            add_golden_query(last_user_msg.content, request.sql)

    return result_response

@app.get("/")
async def root():
    return {"message": "Query Sense Bot API v2 (Auth + Redis)"}
