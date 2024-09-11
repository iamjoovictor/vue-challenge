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
    Grants application access to a user if the credentials are correct
    
    Returns:
    -------
    A access token to the frontEnd. The Token hasn't a time to expire.
    """
    username = await authenticate_user(db, form_data)
    access_token = create_access_token(username)

    return Token(access_token=access_token, token_type="bearer")
