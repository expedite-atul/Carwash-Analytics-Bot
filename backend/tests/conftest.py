import pytest
from httpx import AsyncClient
from backend.app.main import app, lifespan
from backend.app.db import get_session
from backend.app.security import create_access_token, get_password_hash
from backend.app.models import User, UserRole
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

# In-memory DB for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL, 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client")
async def client_fixture(session: Session):
    # Override Dependency
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    
    app.dependency_overrides.clear()

@pytest.fixture(name="admin_token")
def admin_token_fixture():
    return create_access_token(
        data={"sub": "admin@test.com", "role": "admin"}
    )

@pytest.fixture(name="employee_token")
def employee_token_fixture():
    return create_access_token(
        data={"sub": "employee@test.com", "role": "employee"}
    )
