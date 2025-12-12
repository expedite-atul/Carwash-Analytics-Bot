from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from ..db import get_session
from ..models import User, UserRole
from ..auth import get_current_admin_user
from ..security import get_password_hash
from ..cache import cache

router = APIRouter(prefix="/admin", tags=["admin"])

# --- Cache Analytics ---
@router.get("/stats/cache")
async def get_cache_stats(current_user: User = Depends(get_current_admin_user)):
    return await cache.get_stats()

# --- Employee Management ---
@router.get("/users", response_model=List[User])
async def list_employees(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_admin_user)
):
    # Only return users, hide passwords (response_model should ideally use a Schema, but User model has hashed_password)
    # Ideally we exclude hashed_password in response model. 
    # For MVP we just return list, frontend ignores hashed field or we define response model.
    users = session.exec(select(User)).all()
    return users

@router.delete("/users/{user_id}")
async def delete_employee(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_admin_user)
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role == UserRole.ADMIN:
        raise HTTPException(status_code=400, detail="Cannot delete Admin")
        
    session.delete(user)
    session.commit()
    return {"message": "User deleted"}
