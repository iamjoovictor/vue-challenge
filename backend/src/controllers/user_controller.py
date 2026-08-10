from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from datetime import datetime, timedelta
import uuid
from ..repository import user_repository
from ..schemas import user_schema
from ..middleware.security import hash_password
from ..middleware.utils import SERVER_ERROR


async def register_user(db: AsyncSession, user_create: user_schema.UserCreate) -> user_schema.User:
    try:
        existing = await user_repository.get_user_by_username(db, user_create.username)
    except Exception:
        raise SERVER_ERROR

    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already taken")

    try:
        existing_email = await user_repository.get_user_by_email(db, user_create.email)
    except Exception:
        raise SERVER_ERROR

    if existing_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    hashed = hash_password(user_create.password)

    try:
        return await user_repository.create_user(db, user_create.username, user_create.email, hashed)
    except Exception:
        raise SERVER_ERROR


async def forgot_password(db: AsyncSession, request: user_schema.ForgotPasswordRequest) -> user_schema.ForgotPasswordResponse:
    # Always return success to prevent email enumeration attacks
    generic_response = user_schema.ForgotPasswordResponse(
        message="If that email is registered, a reset link has been sent.",
        reset_token=""
    )

    try:
        user = await user_repository.get_user_by_email(db, request.email)
    except Exception:
        return generic_response

    if not user:
        return generic_response

    token = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(minutes=30)

    try:
        await user_repository.create_reset_token(db, user.id, token, expires_at)
    except Exception:
        raise SERVER_ERROR

    # TODO: send token via email in production instead of returning it in the response
    return user_schema.ForgotPasswordResponse(
        message="If that email is registered, a reset link has been sent.",
        reset_token=token
    )


async def reset_password(db: AsyncSession, request: user_schema.ResetPasswordRequest) -> None:
    try:
        reset_token = await user_repository.get_reset_token(db, request.token)
    except Exception:
        raise SERVER_ERROR

    if not reset_token or reset_token.used or reset_token.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )

    hashed = hash_password(request.new_password)

    try:
        await user_repository.update_user_password(db, reset_token.user_id, hashed)
        await user_repository.mark_reset_token_used(db, reset_token.id)
    except Exception:
        raise SERVER_ERROR
