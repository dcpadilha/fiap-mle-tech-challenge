import os
from datetime import datetime, timedelta
from http import HTTPStatus

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from zoneinfo import ZoneInfo

pwd_context = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
    )
    to_encode.update({'exp': expire})
    encoded_jwt = encode(
        to_encode, os.getenv('SECRET_KEY'), algorithm=os.getenv('ALGORITHM')
    )
    return encoded_jwt


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


async def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(
            token, os.getenv('SECRET_KEY'), algorithms=[os.getenv('ALGORITHM')]
        )

        username: str = payload.get('sub')
        if not username:
            raise credentials_exception
        token_data = username
    except DecodeError:
        raise credentials_exception

    query = {'user': token_data}
    user = request.app.database['users'].find_one(query)

    if user is None:
        raise credentials_exception

    user.pop('_id')

    return user
