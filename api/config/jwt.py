import jwt
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from zoneinfo import ZoneInfo
from http import HTTPStatus
from pwdlib import PasswordHash

# Dados utilizados na geração do token de acesso
# Em um ambiente produtivo, estes dados devem estar protegidos
SECRET_KEY = "Y-3WUtZYme8PR8Q-yrHZKr_FPMR7CBzPhXoLsG2q1Ww"  # Substitua isso por uma chave secreta segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/v1/token')

pwd_context = PasswordHash.recommended()

class UserData(BaseModel):
    user: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
    role: str

# Criação do Token do usuário após a validação da autenticação
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(tz=ZoneInfo('UTC')) + expires_delta
    else:
        expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Validação do Token e retorno do objeto TokenData que será utilizado na validação das autorizações
def verify_token(token: str) -> Optional[TokenData]:
    
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if not username:
            raise credentials_exception
        return TokenData(username=username, role=role)
    except jwt.PyJWTError:
        raise credentials_exception
    
# Função que retorna os dados do usuário baseados no token enviado pela chamada da API    
def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    token_data = verify_token(token)
    if token_data is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return token_data

# Função responsável pela geração do Hash da senha, em ambientes produtivos é recomendável
# a utilização de um algoritmo de criptografia mais robusto
def get_password_hash(password: str):
    return pwd_context.hash(password)

# Função que valida se a senha fornecida corresponde à senha codificada
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)