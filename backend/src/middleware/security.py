from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
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
ACCESS_TOKEN_EXPIRE_MINUTES = int(config.get('ACCESS_TOKEN_EXPIRE_MINUTES', 30))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", scheme_name="OAuth2PasswordBearer with JWT")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": username, "exp": expire}
    return jwt.encode(to_encode, ACCESS_TOKEN_SECRET_KEY, algorithm=ACCESS_TOKEN_ALGORITHM)


async def authenticate_user(db: AsyncSession, form_data: OAuth2PasswordRequestForm):
    from ..repository.user_repository import get_user_by_username
    user = await get_user_by_username(db, form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return user.username

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
