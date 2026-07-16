from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password
from app.schemas.user import UserCreate, UserResponse


async def register_user(db: AsyncSession, data: UserCreate) -> UserResponse:
    repo = UserRepository(db)

    existing = await repo.get_by_email(data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(data.password)
    user = await repo.create(
        name=data.name,
        email=data.email,
        hashed_password=hashed,
    )
    return UserResponse.model_validate(user)
