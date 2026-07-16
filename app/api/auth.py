from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.services.user_service import register_user, login_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await register_user(db=db, data=data)


@router.post("/login")
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    return await login_user(db=db, email=data.email, password=data.password)
