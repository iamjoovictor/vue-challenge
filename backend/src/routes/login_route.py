from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from ..middleware.utils_db import get_session
from ..middleware.security import create_access_token,authenticate_user
from ..schemas.token_schema import Token

""""
    @copyright  ALL RIGHTS RESERVED
    @brief      Vue Challenge

    @details    Responsible for managing Login routes

    @author     Joao Victor Silva de Sousa <jvsilva.fne@gmail.com>                                                                
    @since      Sep 10, 2024           
"""

router = APIRouter(tags=["login"], prefix="/login")

@router.post("/", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    """
    Authenticate a user and return a JWT Bearer token.

    **Request body (form-encoded):** `username` and `password`.

    **Returns:** `Token` — `{ access_token: string, token_type: "bearer" }`.

    The token does not expire and must be sent as a `Bearer` header on all
    protected endpoints: `Authorization: Bearer <token>`.

    **Errors:**
    - `401 Unauthorized` — invalid username or password.
    """
    username = await authenticate_user(db, form_data)
    access_token = create_access_token(username)

    return Token(access_token=access_token, token_type="bearer")
