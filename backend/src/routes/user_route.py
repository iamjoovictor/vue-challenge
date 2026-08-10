from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..middleware.utils_db import get_session
from ..controllers import user_controller
from ..schemas import user_schema

""""
    @copyright  ALL RIGHTS RESERVED
    @brief      Vue Challenge

    @details    Responsible for managing User routes

    @author     Joao Victor Silva de Sousa <jvsilva.fne@gmail.com>
    @since      Aug 10, 2026
"""

router = APIRouter(tags=["users"], prefix="/users")


@router.post("/register", response_model=user_schema.User, status_code=status.HTTP_201_CREATED)
async def register(user_create: user_schema.UserCreate, db: AsyncSession = Depends(get_session)):
    """
    Register a new user account.

    **Request body:** `UserCreate` — username, email, password (min 8 chars, 1 uppercase, 1 digit).

    **Returns:** The created `User` object.

    **Errors:**
    - `409 Conflict` — username or email already registered.
    - `422 Unprocessable Entity` — password does not meet strength requirements.
    """
    return await user_controller.register_user(db=db, user_create=user_create)


@router.post("/forgot-password", response_model=user_schema.ForgotPasswordResponse)
async def forgot_password(request: user_schema.ForgotPasswordRequest, db: AsyncSession = Depends(get_session)):
    """
    Request a password reset token for the given email.

    Always returns a success message to prevent email enumeration.
    In production the `reset_token` should be sent via email rather than returned here.

    **Errors:**
    - `500 Internal Server Error` — unexpected database error.
    """
    return await user_controller.forgot_password(db=db, request=request)


@router.post("/reset-password", status_code=status.HTTP_204_NO_CONTENT)
async def reset_password(request: user_schema.ResetPasswordRequest, db: AsyncSession = Depends(get_session)):
    """
    Reset a user's password using a valid reset token.

    **Request body:** `ResetPasswordRequest` — token, new_password.

    **Errors:**
    - `400 Bad Request` — token is invalid, expired, or already used.
    - `422 Unprocessable Entity` — password does not meet strength requirements.
    """
    await user_controller.reset_password(db=db, request=request)
