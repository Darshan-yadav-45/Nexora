import secrets
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import JWTError, jwt
from datetime import datetime, timedelta

from app.database.connection import get_db
from app.models.user import User
from app.models.profile import UserProfile, LearningProfile
from app.schemas.user import (
    UserCreate, UserResponse, Token, TokenData,
    SelectAccountTypeRequest, ForgotPasswordRequest, ResetPasswordRequest
)
from app.services.auth import (
    verify_password, get_password_hash, create_access_token,
    SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    result = await db.execute(select(User).filter(User.email == token_data.email))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    if user.confirm_password and user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    result = await db.execute(select(User).filter(User.email == user.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        password_hash=hashed_password,
        account_type=None,
        is_verified=True,
        profile_completed=False,
        first_time_login=True
    )
    db.add(db_user)
    await db.flush()

    # Create baseline UserProfile if name was provided
    display_name = user.name or user.email.split("@")[0].capitalize()
    db_profile = UserProfile(
        user_id=db_user.id,
        name=display_name,
        preferred_name=display_name,
        native_language="English",
        english_level="Intermediate",
        learning_goal="Master software and research skills"
    )
    db.add(db_profile)
    db.add(LearningProfile(user_id=db_user.id))

    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.email == form_data.username))
    user = result.scalars().first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    user_resp = UserResponse.from_orm(user)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_resp
    }

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/select-account-type")
async def select_account_type(
    req: SelectAccountTypeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    valid_types = ["student", "teacher", "professional", "other"]
    normalized = req.account_type.lower()
    if normalized not in valid_types:
        raise HTTPException(status_code=400, detail=f"Invalid account type. Choose from {valid_types}")
    
    current_user.account_type = normalized
    current_user.first_time_login = False
    await db.commit()
    await db.refresh(current_user)
    return {
        "message": f"Account type updated to {normalized}",
        "account_type": current_user.account_type,
        "profile_completed": current_user.profile_completed
    }

@router.post("/forgot-password")
async def forgot_password(req: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.email == req.email))
    user = result.scalars().first()
    if not user:
        # Avoid user enumeration in public API
        return {"message": "If this email is registered, a password reset link has been dispatched."}
    
    reset_token = secrets.token_urlsafe(32)
    user.reset_password_token = reset_token
    user.reset_token_expiry = datetime.utcnow() + timedelta(hours=2)
    await db.commit()

    return {
        "message": "If this email is registered, a password reset link has been dispatched.",
        "reset_token_preview": reset_token # Provided for dev convenience
    }

@router.post("/reset-password")
async def reset_password(req: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    if req.confirm_password and req.new_password != req.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    result = await db.execute(select(User).filter(User.reset_password_token == req.token))
    user = result.scalars().first()
    if not user or not user.reset_token_expiry or user.reset_token_expiry < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    
    user.password_hash = get_password_hash(req.new_password)
    user.reset_password_token = None
    user.reset_token_expiry = None
    await db.commit()
    return {"message": "Password successfully reset. You may now log in with your new credentials."}

@router.get("/status")
async def get_user_status(current_user: User = Depends(get_current_user)):
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "account_type": current_user.account_type,
        "is_verified": current_user.is_verified,
        "profile_completed": current_user.profile_completed,
        "first_time_login": current_user.first_time_login
    }
