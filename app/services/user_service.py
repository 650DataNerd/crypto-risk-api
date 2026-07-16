from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password, create_access_token
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


async def login_user(db: AsyncSession, email: str, password: str) -> dict:
    repo = UserRepository(db)

    user = await repo.get_by_email(email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user_id=user.id)
    return {"access_token": token, "token_type": "bearer"}
