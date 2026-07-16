from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.database import get_db
from app.core.config import settings
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.services.user_service import register_user, login_user

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await register_user(db=db, data=data)


@router.post("/login")
@limiter.limit("5/minute", exempt_when=lambda request: settings.testing)
async def login(request: Request, data: UserLogin, db: AsyncSession = Depends(get_db)):
    return await login_user(db=db, email=data.email, password=data.password)
