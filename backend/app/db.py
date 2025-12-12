from sqlmodel import create_engine, SQLModel, Session, select
import os
from dotenv import load_dotenv
from .models import User, ChatSession, ChatMessage # Importing registers them in metadata

load_dotenv()

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL")

# --- URL ADJUSTMENT LOGIC ---
# Local Docker Compose maps 5433->5432.
# If running locally (localhost) and port is 5432, we likely need 5433.
# In Production (Render), we use the URL as-is (internal ntwk or pooler).
if DATABASE_URL:
    if "localhost" in DATABASE_URL and ":5432" in DATABASE_URL:
        # Check if we are actually inside docker (usually host is not localhost then)
        # But to be safe, we assume if localhost is used, we are on host machine.
        DATABASE_URL = DATABASE_URL.replace(":5432", ":5433")

# Ensure Sync Driver for SQLModel
if DATABASE_URL and "+asyncpg" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("+asyncpg", "")
if DATABASE_URL and "postgresql://" not in DATABASE_URL:
     # Generic fallback if protocol missing? Unlikely but good safety.
    pass

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
