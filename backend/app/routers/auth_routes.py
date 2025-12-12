from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from datetime import timedelta

from ..db import get_session
from ..models import User, UserRole
from ..security import verify_password, get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from ..auth import get_current_active_user, oauth2_scheme

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    # Check User
    statement = select(User).where(User.email == form_data.username)
    user = session.exec(statement).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
         raise HTTPException(status_code=400, detail="Inactive user")

    # Generate Token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer", "role": user.role}

@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.post("/logout")
async def logout(
    token: str = Depends(oauth2_scheme), 
    user: User = Depends(get_current_active_user)
):
    """Server-side logout: Blocklist the token."""
    from ..cache import cache
    # Block for 24 hours (default token expiry)
    await cache.block_token(token, ttl=86400)
    return {"message": "Successfully logged out (Token Invalidated)"}

@router.post("/register", status_code=201)
async def register_user(
    new_user: User, # In real app, use a separate UserCreate schema
    session: Session = Depends(get_session)
):
    # Only allow registration if no users exist OR if called by Admin (logic simplified for MVP)
    # Check valid email
    statement = select(User).where(User.email == new_user.email)
    if session.exec(statement).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password
    new_user.hashed_password = get_password_hash(new_user.hashed_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"message": "User created successfully", "id": new_user.id}
