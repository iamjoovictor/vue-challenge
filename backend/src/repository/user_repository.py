from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime
from ..models.user_model import User
from ..models.password_reset_token_model import PasswordResetToken


async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()


async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()


async def create_user(db: AsyncSession, username: str, email: str, hashed_password: str) -> User:
    user = User(username=username, email=email, hashed_password=hashed_password, is_active=True)
    db.add(user)
    await db.flush()
    await db.refresh(user)
    await db.commit()
    return user


async def update_user_password(db: AsyncSession, user_id: int, hashed_password: str) -> None:
    await db.execute(
        update(User).where(User.id == user_id).values(hashed_password=hashed_password)
    )
    await db.commit()


async def create_reset_token(db: AsyncSession, user_id: int, token: str, expires_at: datetime) -> PasswordResetToken:
    reset_token = PasswordResetToken(user_id=user_id, token=token, expires_at=expires_at, used=False)
    db.add(reset_token)
    await db.flush()
    await db.refresh(reset_token)
    await db.commit()
    return reset_token


async def get_reset_token(db: AsyncSession, token: str):
    result = await db.execute(
        select(PasswordResetToken).where(PasswordResetToken.token == token)
    )
    return result.scalars().first()


async def mark_reset_token_used(db: AsyncSession, token_id: int) -> None:
    await db.execute(
        update(PasswordResetToken).where(PasswordResetToken.id == token_id).values(used=True)
    )
    await db.commit()
