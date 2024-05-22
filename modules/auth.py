import hashlib
from dotenv import load_dotenv
import os
import jwt
from typing import Annotated, Union
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from models import User

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/sign_in")
jwt_secret = os.getenv('JWT_SECRET')

def hash_password(password: str) -> str:
    return hashlib.sha512(password.encode()).hexdigest()

def generate_token(user_id: int) -> str:
    return jwt.encode({'user_id': user_id}, os.getenv('JWT_SECRET'), algorithm='HS256')


def decode_token(token: str) -> Union[str, dict]:
    try:
        return jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user_id(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = decode_token(token)
        return payload.get('user_id')

    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )