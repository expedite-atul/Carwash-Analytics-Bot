from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from .agent import process_user_question, execute_approved_sql

app = FastAPI()

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

@app.post("/chat/plan")
async def create_plan(request: ChatRequest):
    """Generate SQL but wait for approval"""
    result = process_user_question(request.message)
    return result

@app.post("/chat/execute")
async def execute_plan(request: ExecuteRequest):
    """Execute approved SQL"""
    result = execute_approved_sql(request.sql)
    return result

@app.get("/")
async def root():
    return {"message": "Carwash Bot API is running"}

