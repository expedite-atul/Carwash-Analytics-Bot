from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import NullPool
import os
from dotenv import load_dotenv

load_dotenv()

# Use the read-only user for the bot logic if possible, or admin for now but careful
# The docker-compose maps port 5433 to 5432 in the container
DATABASE_URL = os.getenv("DATABASE_URL")
# Ensure we are using the async driver
if DATABASE_URL and "postgresql://" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# engine = create_async_engine(DATABASE_URL, echo=True, future=True)
# For synchronous operations (LangChain SQLDatabase tool often prefers sync or specifically handled async)
# We will create a sync engine for LangChain and an async one for FastAPI if needed.
# For simplicity in V1 with LangChain, we'll use a standard psycopg2 engine for the Agent tools
# and async for the API if we were doing high concurrency, but let's stick to what works with LangChain SQLToolkit easily first.

SYNC_DATABASE_URL = os.getenv("DATABASE_URL").replace("postgresql+asyncpg://", "postgresql://")
# Fix port for local connection (Docker maps 5433->5432)
# The ENV var likely has "localhost:5432" which needs to be "localhost:5433" for running outside docker
# OR "db:5432" if running inside docker.
# Since we are running `fastapi dev` LOCALLY, we must hit localhost:5433
SYNC_DATABASE_URL = SYNC_DATABASE_URL.replace(":5432", ":5433")

engine = create_engine(SYNC_DATABASE_URL, pool_pre_ping=True)

def get_db_session():
    with Session(engine) as session:
        yield session
