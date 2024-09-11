from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from ..middleware.utils_db import get_session
from ..middleware.utils_environment import get_environment_config
from ..schemas.token_schema import TokenData

""""
    @copyright  ALL RIGHTS RESERVED
    @brief      Vue Challenge

    @details     Utility functions to secures the system

    @author     Joao Victor Silva de Sousa <jvsilva.fne@gmail.com>                                                                
    @since      Sep 10, 2024           
"""

config = get_environment_config()

# To get a string like this run on bash prompt:
# openssl rand -hex 32
ACCESS_TOKEN_SECRET_KEY = config.get('ACCESS_TOKEN_SECRET_KEY')
ACCESS_TOKEN_ALGORITHM = config.get('ACCESS_TOKEN_ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = config.get('ACCESS_TOKEN_EXPIRE_MINUTES')
USER_ADMIN = config.get('USER_ADMIN')
PASSWORD_USER_ADMIN = config.get('PASSWORD_USER_ADMIN')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", scheme_name="OAuth2PasswordBearer with JWT")

def create_access_token(username: str):
    # expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # expire = datetime.utcnow() + expires_delta
    # to_encode = {"sub": user.name, "exp": expire}
    
    to_encode = {"sub": username}
        
    encoded_jwt = jwt.encode(to_encode, ACCESS_TOKEN_SECRET_KEY, algorithm=ACCESS_TOKEN_ALGORITHM)
    return encoded_jwt

async def authenticate_user(db: AsyncSession, form_data: OAuth2PasswordRequestForm):
    if(form_data.username == 'admin' and form_data.password == 'admin'):
        return form_data.username
    
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

async def get_current_user(db: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    
    try:
        payload = jwt.decode(token, ACCESS_TOKEN_SECRET_KEY, algorithms=[ACCESS_TOKEN_ALGORITHM])
        username: str = payload.get("sub")
        
        if not username: raise credentials_exception
        token_data = TokenData(username=username)
        
        return True
        
    except JWTError:
        raise credentials_exception
