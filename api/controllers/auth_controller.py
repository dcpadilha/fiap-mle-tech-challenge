from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import timedelta
from config.jwt import create_access_token, Token, UserData
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from repositories.auth_repository import get_usuario
from config.database import SessionLocal
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from models.vitbrasil import Usuario

router = APIRouter(prefix="/api/v1")

pwd_context = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

class UserLogin(BaseModel):
    usuario: str
    senha: str
    role: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/token", response_model=Token)
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    if not form_data.username:
        raise HTTPException(status_code=422, detail="Username is required")
    
    user = get_usuario(db,form_data.username)

    if not user:
        raise HTTPException(
            status_code=422, 
            detail="Erro ao acessar usuário ao banco de dados"
        )    


    if not verify_password(form_data.password, user['senha']):
        raise HTTPException(
            status_code=401,
            detail='Incorrect email or password',
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user["usuario"], "role": user["role"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def get_password_hash(password: str):
    return pwd_context.hash(password)

@router.post("/user", response_model=UserData)
def add_user(user_info: UserLogin,db: Session = Depends(get_db)):
    user_info.senha = get_password_hash(user_info.senha)

    try:
        new_user = Usuario(usuario=user_info.usuario, senha=user_info.senha, role=user_info.role)
        db.add(new_user)
        db.commit()
        return {'message': 'Usuário adicionado.'}
    except Exception as e:
        raise HTTPException(status_code=422, detail="Erro ao adicionar usuário ao banco de dados")