from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    EMPLOYEE = "employee"
    OWNER = "owner"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    full_name: Optional[str] = None
    role: UserRole = Field(default=UserRole.EMPLOYEE)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    sessions: List["ChatSession"] = Relationship(back_populates="user")

class ChatSession(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    title: str = Field(default="New Chat")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    user: Optional[User] = Relationship(back_populates="sessions")
    messages: List["ChatMessage"] = Relationship(back_populates="session")

class ChatMessage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: int = Field(foreign_key="chatsession.id")
    role: str # "user" or "bot"
    content: str
    meta_info: Optional[str] = None # JSON string for extra data (SQL queries, etc.)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    session: ChatSession = Relationship(back_populates="messages")
