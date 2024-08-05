from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Optional

# Modelo de usuário e senha
class User(BaseModel):
    username: str
    password: str

class UserInDB(User):
    hashed_password: str

# Contexto para criptografia de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para verificar se a senha em texto claro corresponde à senha criptografada
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Função para criar o hash de uma senha
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
