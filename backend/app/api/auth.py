from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
import uuid
import secrets

from app.database.database import get_db
from app.models.user import User, UserProfile
from app.schemas.user import UserCreate, UserResponse, Token, EmailRequest, PasswordResetRequest
from app.services.auth import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.api.dependencies import get_current_user

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create profile
    profile = UserProfile(user_id=new_user.id, first_name=user.first_name, last_name=user.last_name)
    db.add(profile)
    db.commit()

    # In a real app, generate verification token and send email here
    print(f"Mock Email: Verification link sent to {user.email}")

    return new_user

@router.post("/login", response_model=UserResponse)
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    # Set HttpOnly Cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=False, # Set to True in production with HTTPS
    )

    # Update last login
    user.last_login_at = datetime.utcnow()
    db.commit()
    db.refresh(user)

    return user

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    # Mock implementation
    # In real app, look up user by verification token, set email_verified=True
    return {"message": "Email verified successfully"}

@router.post("/forgot-password")
def forgot_password(request: EmailRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if user:
        # Generate token, save to db, send email
        reset_token = secrets.token_urlsafe(32)
        print(f"Mock Email: Password reset token for {request.email} is {reset_token}")
    
    # Always return success to prevent email enumeration
    return {"message": "If an account exists for this email, you will receive a password reset link."}

@router.post("/reset-password")
def reset_password(request: PasswordResetRequest, db: Session = Depends(get_db)):
    # Mock implementation: Accept any token and just reset for the email provided implicitly?
    # No, we'd normally look up by token. Let's just mock a success message for MVP.
    return {"message": "Password reset successfully"}
